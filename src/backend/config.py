"""后端配置与环境变量加载。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import os


def load_env_file(env_path: Path) -> None:
    """加载简单的 .env 配置文件。"""
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue

        if "#" in value:
            value = value.split("#", 1)[0].strip()

        if key not in os.environ:
            os.environ[key] = value


ROOT_DIR = Path(__file__).resolve().parents[2]
load_env_file(ROOT_DIR / ".env")


@dataclass
class AppSettings:
    llm_provider: str = "mock"
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    cors_origins: List[str] | None = None
    ocr_provider: str = "auto"
    ocr_languages: str = "eng"
    openai_ocr_model: str = "gpt-4o-mini"
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    enable_plot_generation: bool = True  # Milestone 5: 启用绘图生成

    @classmethod
    def from_env(cls) -> "AppSettings":
        origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")

        return cls(
            llm_provider=os.getenv("LLM_PROVIDER", "mock"),
            llm_model=os.getenv("LLM_MODEL", "gpt-4"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
            cors_origins=[item.strip() for item in origins.split(",") if item.strip()],
            ocr_provider=os.getenv("OCR_PROVIDER", "auto"),
            ocr_languages=os.getenv("OCR_LANGUAGES", "eng"),
            openai_ocr_model=os.getenv("OPENAI_OCR_MODEL", "gpt-4o-mini"),
            backend_host=os.getenv("BACKEND_HOST", "127.0.0.1"),
            backend_port=int(os.getenv("BACKEND_PORT", "8000")),
            enable_plot_generation=os.getenv("ENABLE_PLOT_GENERATION", "true").lower() == "true",
        )
