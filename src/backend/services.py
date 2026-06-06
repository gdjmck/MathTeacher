"""后端业务服务。"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Optional
import base64
import os

from fastapi import UploadFile
from openai import OpenAI

from src.backend.config import AppSettings
from src.core import MathProblem, MathSolver, SolverMode, VisualizationJudge
from src.core.llm_client import BaseLLMClient, create_llm_client
from src.core.plot_generator import PlotGenerator  # Milestone 5

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

try:
    import pytesseract
except ImportError:  # pragma: no cover
    pytesseract = None


@dataclass
class OCRResult:
    text: str
    provider: str


class SolverService:
    """封装解题流程和返回结构。"""

    def __init__(self, settings: AppSettings, llm_client: Optional[BaseLLMClient] = None):
        self.settings = settings
        self.llm_client = llm_client or self._create_llm_client()
        self.solver = MathSolver(llm_client=self.llm_client)
        self.viz_judge = VisualizationJudge()

        # Milestone 5: 初始化绘图生成器
        self.plot_generator = None
        if settings.enable_plot_generation:
            try:
                self.plot_generator = PlotGenerator(
                    llm_client=self.llm_client,
                    openai_api_key=os.getenv("OPENAI_API_KEY"),
                    openai_base_url=os.getenv("OPENAI_BASE_URL"),
                )
            except Exception:
                pass  # 绘图功能可选，失败不影响核心功能

    def _create_llm_client(self) -> Optional[BaseLLMClient]:
        provider = self.settings.llm_provider.lower()

        if provider == "anthropic":
            raise ValueError("Anthropic 客户端尚未完成，Milestone 4 当前仅支持 openai 或 mock")

        return create_llm_client(
            provider,
            model=self.settings.llm_model,
            temperature=self.settings.llm_temperature,
            max_tokens=self.settings.llm_max_tokens,
        )

    def solve(
        self,
        question: str,
        mode: str,
        subject: Optional[str] = None,
        grade_level: Optional[str] = None,
        context: Optional[str] = None,
        source: str = "text",
        extracted_text: Optional[str] = None,
        generate_plot: bool = False,  # Milestone 5: 是否生成绘图
    ) -> dict:
        problem = MathProblem(
            question=question,
            subject=subject,
            grade_level=grade_level,
            context=context,
        )
        response = self.solver.solve(problem, SolverMode(mode))
        hint = self.viz_judge.judge(question, response.content)

        result = {
            "mode": response.mode.value,
            "content": response.content,
            "question": response.problem.question,
            "needs_visualization": hint.needed,
            "visualization_hint": {
                "needed": hint.needed,
                "type": hint.viz_type.value,
                "description": hint.description,
                "keywords": hint.keywords,
            },
            "source": source,
            "extracted_text": extracted_text,
        }

        # Milestone 5: 如果需要可视化且启用了绘图生成
        if generate_plot and hint.needed and self.plot_generator:
            try:
                plot_result = self.plot_generator.generate_plot(
                    question=question,
                    answer_content=response.content,
                    visualization_type=hint.viz_type.value
                )
                result["plot"] = {
                    "success": plot_result.success,
                    "method": plot_result.method.value,
                    "image_data": plot_result.image_data,
                    "image_url": plot_result.image_url,
                    "code": plot_result.code,
                    "error": plot_result.error,
                }
            except Exception as e:
                result["plot"] = {
                    "success": False,
                    "error": str(e)
                }
        else:
            result["plot"] = None

        return result


class OCRService:
    """负责从上传文件中抽取题目文本。"""

    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def extract_question(self, upload_file: UploadFile) -> OCRResult:
        content = await upload_file.read()
        if not content:
            raise ValueError("上传文件为空")

        content_type = upload_file.content_type or "application/octet-stream"

        if content_type.startswith("text/"):
            text = content.decode("utf-8").strip()
            if not text:
                raise ValueError("上传的文本文件中没有可用内容")
            return OCRResult(text=text, provider="text")

        if not content_type.startswith("image/"):
            raise ValueError("目前只支持文本文件或图片文件上传")

        providers = self._resolve_providers()
        for provider in providers:
            if provider == "tesseract":
                text = self._extract_with_tesseract(content)
            elif provider == "openai":
                text = self._extract_with_openai(content, content_type)
            else:
                text = None

            if text:
                return OCRResult(text=text, provider=provider)

        raise ValueError(
            "未能从图片中提取题目文本。请安装 pytesseract 并配置 OCR，或设置 OPENAI_API_KEY 以启用 OpenAI OCR。"
        )

    def _resolve_providers(self) -> list[str]:
        provider = self.settings.ocr_provider.lower()
        if provider == "auto":
            providers: list[str] = []
            if os.getenv("OPENAI_API_KEY"):
                providers.append("openai")
            if pytesseract is not None and Image is not None:
                providers.append("tesseract")
            return providers

        return [provider]

    def _extract_with_tesseract(self, content: bytes) -> Optional[str]:
        if pytesseract is None or Image is None:
            return None

        try:
            image = Image.open(BytesIO(content))
            text = pytesseract.image_to_string(image, lang=self.settings.ocr_languages).strip()
        except Exception:
            return None

        return text or None

    def _extract_with_openai(self, content: bytes, content_type: str) -> Optional[str]:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        client_kwargs = {"api_key": api_key}
        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url:
            client_kwargs["base_url"] = base_url

        client = OpenAI(**client_kwargs)
        encoded = base64.b64encode(content).decode("utf-8")
        image_url = f"data:{content_type};base64,{encoded}"

        try:
            response = client.chat.completions.create(
                model=self.settings.openai_ocr_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "请阅读这张图片中的数学题目，并做内容理解后输出适合后续解题的完整题干。"
                                    "要求：1. 尽量忠实于原题；2. 保留题号、条件、选项；"
                                    "3. 修正常见 OCR 识别错误；4. 只返回题目文本，不要分析，不要作答。"
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                        ],
                    }
                ],
                temperature=0,
            )
        except Exception:
            return None

        content_text = response.choices[0].message.content
        if isinstance(content_text, str):
            return content_text.strip() or None

        return None


class StaticOCRService(OCRService):
    """测试用 OCR 服务。"""

    def __init__(self, text: str):
        self.text = text
        super().__init__(AppSettings.from_env())

    async def extract_question(self, upload_file: UploadFile) -> OCRResult:
        return OCRResult(text=self.text, provider="static")


class OpenAIImageUnderstandingService(OCRService):
    """测试时显式走 OpenAI 图片理解。"""

    def __init__(self, settings: AppSettings):
        super().__init__(settings)

    def _resolve_providers(self) -> list[str]:
        return ["openai"]


def build_default_solver_service() -> SolverService:
    settings = AppSettings.from_env()
    return SolverService(settings=settings)


def build_default_ocr_service() -> OCRService:
    settings = AppSettings.from_env()
    return OCRService(settings=settings)
