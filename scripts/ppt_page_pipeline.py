from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from llm_client import AliyunGLM5Client, ensure_host_llm_client_ready
from pipeline_types import StageTimeouts
from prompt_loader import load_prompt
from task_parser import parse_markdown_task, write_task_json
from validators import (
    ensure_parent,
    extract_html_document,
    parse_review_verdict,
    validate_blueprint,
    validate_html_output,
    validate_task_basic,
)

MAX_REVIEW_LOOPS = 3
MAX_REQUEST_RETRIES = 3
REQUEST_RETRYABLE_ERRORS = {'TimeoutError', 'URLError', 'RemoteDisconnected', 'ConnectionResetError'}


def now() -> str:
    return datetime.now().isoformat(timespec='seconds')


def append_log(path: Path, event: dict) -> None:
    ensure_parent(path)
    with path.open('a') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def summarize_task_for_review(task: dict) -> str:
    lines = [
        f"- 页码：{task.get('page_number', '')}",
        f"- 页面标题：{task.get('page_title', '')}",
        f"- 页面目标：{task.get('page_goal', '')}",
        f"- 风格要求：{task.get('style_requirements', '')}",
        f"- 禁用项：{task.get('forbidden_items', '')}",
        f"- 特殊硬规则：{task.get('special_rules', '')}",
    ]
    return '\n'.join(lines)


def summarize_blueprint_for_review(text: str, max_chars: int = 2200) -> str:
    keep_sections = []
    markers = [
        '1. 页面定位',
        '2. 页面核心结论',
        '3. 版面骨架',
        '8. 视觉重心',
        '9. 阅读路径',
        '11. 禁止做法',
    ]
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            keep_sections.append((idx, marker))
    if not keep_sections:
        return text[:max_chars]
    keep_sections.sort()
    chunks: list[str] = []
    for i, (idx, marker) in enumerate(keep_sections):
        end = keep_sections[i + 1][0] if i + 1 < len(keep_sections) else len(text)
        chunks.append(text[idx:end].strip())
    summary = '\n\n'.join(chunks)
    return summary[:max_chars]


def chat_logged(
    *,
    client: AliyunGLM5Client,
    log_path: Path,
    stage: str,
    loop_idx: int,
    system_prompt: str,
    user_prompt: str,
    timeout: int,
    max_tokens: int | None = None,
) -> tuple[str, dict]:
    request_meta = {
        'time': now(),
        'stage': stage,
        'loop': loop_idx,
        'status': 'request_start',
        'provider': client.provider_name,
        'model': client.model,
        'base_url': client.base_url,
        'timeout': timeout,
        'max_tokens': max_tokens,
        'system_prompt_chars': len(system_prompt),
        'user_prompt_chars': len(user_prompt),
    }
    append_log(log_path, request_meta)

    last_error: Exception | None = None
    for attempt in range(1, MAX_REQUEST_RETRIES + 1):
        started = time.perf_counter()
        try:
            append_log(
                log_path,
                {
                    'time': now(),
                    'stage': stage,
                    'loop': loop_idx,
                    'status': 'request_attempt_start',
                    'attempt': attempt,
                },
            )
            resp = client.chat(system_prompt, user_prompt, timeout=timeout, max_tokens=max_tokens)
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            append_log(
                log_path,
                {
                    'time': now(),
                    'stage': stage,
                    'loop': loop_idx,
                    'status': 'request_success',
                    'attempt': attempt,
                    'elapsed_ms': elapsed_ms,
                    'response_chars': len(resp.text),
                    'response_tokens_hint': len(resp.text),
                },
            )
            return resp.text, resp.raw
        except Exception as e:  # noqa: BLE001
            last_error = e
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            error_type = type(e).__name__
            append_log(
                log_path,
                {
                    'time': now(),
                    'stage': stage,
                    'loop': loop_idx,
                    'status': 'request_failed',
                    'attempt': attempt,
                    'elapsed_ms': elapsed_ms,
                    'error_type': error_type,
                    'error': str(e),
                    'retryable': error_type in REQUEST_RETRYABLE_ERRORS,
                },
            )
            if error_type not in REQUEST_RETRYABLE_ERRORS or attempt >= MAX_REQUEST_RETRIES:
                raise
            time.sleep(attempt * 2)

    raise RuntimeError(f'{stage} 请求失败：{last_error}')


def build_blueprint(
    client: AliyunGLM5Client,
    task_file: str,
    work_dir: Path,
    timeouts: StageTimeouts,
    log_path: Path,
    loop_idx: int,
    feedback: str = '',
) -> str:
    system_prompt = load_prompt('/root/.openclaw/workspace/prompts/ppt_pipeline/blueprint_maker.system.md')
    user_prompt = Path(task_file).read_text()
    if feedback:
        user_prompt += f"\n\n# 上一轮施工图审核未通过，必须逐条修正\n\n{feedback}\n"
    text, raw = chat_logged(
        client=client,
        log_path=log_path,
        stage='blueprint_generate',
        loop_idx=loop_idx,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        timeout=timeouts.blueprint_generate,
    )
    (work_dir / '01-blueprint.raw.json').write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    (work_dir / '01-blueprint.md').write_text(text)
    validate_blueprint(text)
    return text


def review_blueprint(
    client: AliyunGLM5Client,
    task_file: str,
    blueprint: str,
    work_dir: Path,
    timeouts: StageTimeouts,
    log_path: Path,
    loop_idx: int,
) -> tuple[str, str]:
    system_prompt = load_prompt('/root/.openclaw/workspace/prompts/ppt_pipeline/blueprint_reviewer.system.md')
    user_prompt = f"# 任务包\n\n{Path(task_file).read_text()}\n\n# 待审核施工图\n\n{blueprint}"
    text, raw = chat_logged(
        client=client,
        log_path=log_path,
        stage='blueprint_review',
        loop_idx=loop_idx,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        timeout=timeouts.blueprint_review,
        max_tokens=1400,
    )
    (work_dir / '02-blueprint-review.raw.json').write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    (work_dir / '02-blueprint-review.md').write_text(text)
    verdict = parse_review_verdict(text)
    (work_dir / '02-blueprint-review.parsed.json').write_text(json.dumps({'verdict': verdict}, ensure_ascii=False, indent=2))
    return text, verdict


def build_html(
    client: AliyunGLM5Client,
    task_file: str,
    blueprint: str,
    blueprint_review: str,
    work_dir: Path,
    timeouts: StageTimeouts,
    log_path: Path,
    loop_idx: int,
    feedback: str = '',
) -> str:
    system_prompt = load_prompt('/root/.openclaw/workspace/prompts/ppt_pipeline/html_builder.system.md')
    user_prompt = (
        f"# 任务包\n\n{Path(task_file).read_text()}\n\n"
        f"# 已通过施工图\n\n{blueprint}\n\n"
        f"# 施工图审核结论\n\n{blueprint_review}"
    )
    if feedback:
        user_prompt += f"\n\n# 上一轮HTML审核未通过，必须逐条修正\n\n{feedback}\n"
    text, raw = chat_logged(
        client=client,
        log_path=log_path,
        stage='html_build',
        loop_idx=loop_idx,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        timeout=timeouts.html_build,
        max_tokens=5200,
    )
    (work_dir / '03-builder.raw.json').write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    html_part, trailing_part = extract_html_document(text)
    note_part = trailing_part
    if not note_part and '2）简短实现说明' in text:
        note_part = '2）简短实现说明' + text.split('2）简短实现说明', 1)[1]
    (work_dir / '03-page.html').write_text(html_part)
    (work_dir / '03-builder-note.md').write_text(note_part)
    validate_html_output(html_part, parse_markdown_task(task_file).to_dict())
    return html_part


def review_html(
    client: AliyunGLM5Client,
    task: dict,
    blueprint: str,
    html: str,
    work_dir: Path,
    timeouts: StageTimeouts,
    log_path: Path,
    loop_idx: int,
) -> tuple[str, str]:
    system_prompt = load_prompt('/root/.openclaw/workspace/prompts/ppt_pipeline/html_reviewer.system.md')
    task_summary = summarize_task_for_review(task)
    blueprint_summary = summarize_blueprint_for_review(blueprint)
    user_prompt = (
        f"# 任务包摘要\n\n{task_summary}\n\n"
        f"# 施工图摘要\n\n{blueprint_summary}\n\n"
        f"# 待审核HTML\n\n{html}"
    )
    text, raw = chat_logged(
        client=client,
        log_path=log_path,
        stage='html_review',
        loop_idx=loop_idx,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        timeout=timeouts.html_review,
        max_tokens=1200,
    )
    (work_dir / '04-html-review.raw.json').write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    (work_dir / '04-html-review.md').write_text(text)
    verdict = parse_review_verdict(text)
    (work_dir / '04-html-review.parsed.json').write_text(json.dumps({'verdict': verdict}, ensure_ascii=False, indent=2))
    return text, verdict


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-file', required=True)
    parser.add_argument('--output-html', required=True)
    parser.add_argument('--work-dir', required=True)
    args = parser.parse_args()

    work_dir = Path(args.work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    log_path = work_dir / 'run-log.jsonl'
    timeouts = StageTimeouts()

    task_obj = parse_markdown_task(args.task_file)
    task_obj.output_html = args.output_html
    task = task_obj.to_dict()
    validate_task_basic(task)
    write_task_json(task_obj, work_dir / 'task.json')
    append_log(log_path, {'time': now(), 'stage': 'task_parse', 'status': 'success', 'task': task})

    ready = ensure_host_llm_client_ready(smoke_test=True, timeout=20)
    append_log(
        log_path,
        {
            'time': now(),
            'stage': 'llm_client_preflight',
            'status': ready.get('status', 'ready'),
            'provider': ready.get('provider_name'),
            'model': ready.get('model'),
            'base_url': ready.get('base_url'),
            'config_path': ready.get('config_path'),
        },
    )

    client = AliyunGLM5Client()
    append_log(
        log_path,
        {
            'time': now(),
            'stage': 'client_init',
            'status': 'success',
            'provider': client.provider_name,
            'model': client.model,
            'base_url': client.base_url,
        },
    )

    blueprint_feedback = ''
    blueprint = ''
    blueprint_review_text = ''
    for loop_idx in range(1, MAX_REVIEW_LOOPS + 1):
        append_log(log_path, {'time': now(), 'stage': 'blueprint_generate', 'loop': loop_idx, 'status': 'running'})
        blueprint = build_blueprint(client, args.task_file, work_dir, timeouts, log_path, loop_idx, blueprint_feedback)
        append_log(log_path, {'time': now(), 'stage': 'blueprint_generate', 'loop': loop_idx, 'status': 'success'})

        append_log(log_path, {'time': now(), 'stage': 'blueprint_review', 'loop': loop_idx, 'status': 'running'})
        blueprint_review_text, verdict = review_blueprint(client, args.task_file, blueprint, work_dir, timeouts, log_path, loop_idx)
        append_log(log_path, {'time': now(), 'stage': 'blueprint_review', 'loop': loop_idx, 'status': verdict})
        if verdict == '通过' or verdict == '带小问题通过':
            break
        blueprint_feedback = blueprint_review_text
    else:
        raise RuntimeError('blueprint_review 闭环返工 3 次后仍不通过，需回到主控处理')

    html_feedback = ''
    html = ''
    html_review_text = ''
    for loop_idx in range(1, MAX_REVIEW_LOOPS + 1):
        append_log(log_path, {'time': now(), 'stage': 'html_build', 'loop': loop_idx, 'status': 'running'})
        html = build_html(client, args.task_file, blueprint, blueprint_review_text, work_dir, timeouts, log_path, loop_idx, html_feedback)
        append_log(log_path, {'time': now(), 'stage': 'html_build', 'loop': loop_idx, 'status': 'success'})

        append_log(log_path, {'time': now(), 'stage': 'html_review', 'loop': loop_idx, 'status': 'running'})
        html_review_text, verdict = review_html(client, task, blueprint, html, work_dir, timeouts, log_path, loop_idx)
        append_log(log_path, {'time': now(), 'stage': 'html_review', 'loop': loop_idx, 'status': verdict})
        if verdict == '通过' or verdict == '带小问题通过':
            break
        html_feedback = html_review_text
    else:
        raise RuntimeError('html_review 闭环返工 3 次后仍不通过，需回到主控处理')

    output_path = Path(args.output_html)
    ensure_parent(output_path)
    output_path.write_text(html)
    final_report = {
        'time': now(),
        'output_html': str(output_path),
        'html_review': html_review_text,
        'status': 'done',
    }
    (work_dir / 'final-report.md').write_text(json.dumps(final_report, ensure_ascii=False, indent=2))
    append_log(log_path, {'time': now(), 'stage': 'final_output', 'status': 'success', 'output_html': str(output_path)})
    print(str(output_path))


if __name__ == '__main__':
    main()
