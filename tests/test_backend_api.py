"""Milestone 4 后端接口测试。"""

import io
import os
import sys
from unittest.mock import patch

from fastapi.testclient import TestClient


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.backend.app import create_app
from src.backend.config import AppSettings
from src.backend.services import OCRService, SolverService, StaticOCRService
from src.core.llm_client import MockLLMClient


def build_test_client() -> TestClient:
    settings = AppSettings(
        llm_provider="mock",
        llm_model="gpt-4",
        llm_temperature=0.7,
        llm_max_tokens=2000,
        cors_origins=["http://localhost:5173"],
        ocr_provider="auto",
        ocr_languages="eng",
        openai_ocr_model="gpt-4o-mini",
        backend_host="127.0.0.1",
        backend_port=8000,
    )
    solver_service = SolverService(settings=settings, llm_client=MockLLMClient())
    ocr_service = StaticOCRService("求解方程：2x + 5 = 15")
    app = create_app(solver_service=solver_service, ocr_service=ocr_service, settings=settings)
    return TestClient(app)


def test_health_endpoint():
    client = build_test_client()

    response = client.get('/api/health')

    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
    assert response.json()['llm_provider'] == 'mock'


def test_text_solve_endpoint():
    client = build_test_client()

    response = client.post(
        '/api/solve',
        json={
            'question': '求解方程：2x + 5 = 15',
            'mode': 'brief',
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload['mode'] == 'brief'
    assert payload['source'] == 'text'
    assert payload['question'] == '求解方程：2x + 5 = 15'
    assert '答案' in payload['content']
    assert 'visualization_hint' in payload


def test_image_solve_endpoint_uses_ocr_result():
    client = build_test_client()

    response = client.post(
        '/api/solve/image',
        files={
            'file': ('problem.png', io.BytesIO(b'fake-image-content'), 'image/png'),
        },
        data={
            'mode': 'hint',
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload['mode'] == 'hint'
    assert payload['source'] == 'image'
    assert payload['extracted_text'] == '求解方程：2x + 5 = 15'
    assert payload['question'] == '求解方程：2x + 5 = 15'


def test_image_endpoint_rejects_empty_upload():
    client = build_test_client()
    app = client.app

    class EmptyOCRService(StaticOCRService):
        async def extract_question(self, upload_file):
            raise ValueError('上传文件为空')

    app.state.ocr_service = EmptyOCRService('')

    response = client.post(
        '/api/solve/image',
        files={
            'file': ('problem.png', io.BytesIO(b''), 'image/png'),
        },
        data={
            'mode': 'hint',
        },
    )

    assert response.status_code == 400
    assert response.json()['detail'] == '上传文件为空'


def test_ocr_auto_mode_prefers_openai_when_available():
    settings = AppSettings(
        llm_provider="mock",
        llm_model="gpt-4",
        llm_temperature=0.7,
        llm_max_tokens=2000,
        cors_origins=["http://localhost:5173"],
        ocr_provider="auto",
        ocr_languages="eng",
        openai_ocr_model="gpt-4o-mini",
        backend_host="127.0.0.1",
        backend_port=8000,
    )
    service = OCRService(settings)

    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}, clear=False):
        providers = service._resolve_providers()

    assert providers[0] == 'openai'
