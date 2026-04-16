from __future__ import annotations

import re
from pathlib import Path


class ValidationError(Exception):
    pass


def validate_task_basic(task: dict) -> None:
    required = ['page_number', 'page_title', 'page_goal', 'output_html']
    missing = [k for k in required if not task.get(k)]
    if missing:
        raise ValidationError(f'任务缺少必要字段: {missing}')


def validate_blueprint(text: str) -> None:
    required_sections = [
        '1. 页面定位',
        '2. 页面核心结论',
        '3. 版面骨架',
        '11. 禁止做法',
    ]
    for sec in required_sections:
        if sec not in text:
            raise ValidationError(f'施工图缺少章节: {sec}')
    banned = ['<!DOCTYPE html>', '<html', '<body']
    for bad in banned:
        if bad.lower() in text.lower():
            raise ValidationError('施工图输出误混入 HTML')


def parse_review_verdict(text: str) -> str:
    match = re.search(r'审核结论\s*[:：]?\s*(?:\n+\s*)?(带小问题通过|不通过|通过)', text)
    if match:
        return match.group(1)
    raise ValidationError('无法解析审核结论')


def extract_html_document(text: str) -> tuple[str, str]:
    text = text.replace('\r\n', '\n').strip()
    start = text.lower().find('<!doctype html>')
    if start == -1:
        start = text.lower().find('<html')
    if start == -1:
        raise ValidationError('输出中未找到 HTML 文档起点')

    end_marker = '</html>'
    end = text.lower().rfind(end_marker)
    if end == -1:
        raise ValidationError('输出中未找到 HTML 文档结束标记 </html>')
    end += len(end_marker)

    html = text[start:end].strip()
    note = text[end:].strip()
    return html, note


def validate_html_output(text: str, task: dict) -> None:
    lower = text.lower()
    for token in ['<!doctype html>', '<html', '<body', '</html>']:
        if token not in lower:
            raise ValidationError(f'HTML 缺少必要结构: {token}')
    if lower.lstrip().startswith('```'):
        raise ValidationError('HTML 仍包含 Markdown 代码围栏')
    page_no = str(task.get('page_number', '')).strip()
    if page_no and re.search(r'第\s*0?2\s*页', text) and page_no not in {'02', '2'}:
        raise ValidationError('HTML 疑似写错页码（出现第02页）')


def ensure_parent(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
