"""使用 OpenAI 验证图片内容理解。"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from fastapi import UploadFile


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.backend.config import AppSettings
from src.backend.services import OpenAIImageUnderstandingService


ROOT_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = ROOT_DIR / 'tests' / 'TODO.png'


async def extract_text_from_todo_image() -> str:
    settings = AppSettings.from_env()
    service = OpenAIImageUnderstandingService(settings)

    with IMAGE_PATH.open('rb') as image_file:
        upload_file = UploadFile(
            filename='TODO.png',
            file=image_file,
            headers={'content-type': 'image/png'},
        )
        result = await service.extract_question(upload_file)

    return result.text


def _extract_with_retries(max_attempts: int = 3) -> str:
    last_result = ""
    for _ in range(max_attempts):
        last_result = asyncio.run(extract_text_from_todo_image())
        if '帆船比赛中' in last_result and ('A．' in last_result or 'A.' in last_result):
            return last_result
    return last_result


def test_todo_png_openai_understanding():
    if not os.getenv('OPENAI_API_KEY'):
        raise AssertionError('缺少 OPENAI_API_KEY，无法执行 OpenAI 图片理解测试')

    extracted = _extract_with_retries()

    assert extracted
    assert '帆船比赛中' in extracted
    assert '视风风速' in extracted or '视风风速对应的向量' in extracted
    assert 'A.' in extracted and 'B.' in extracted and 'C.' in extracted and 'D.' in extracted


if __name__ == '__main__':
    text = asyncio.run(extract_text_from_todo_image())
    print(text)
