"""FastAPI 请求与响应模型。"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


SolverModeValue = Literal["hint", "brief", "detailed"]


class SolveRequest(BaseModel):
    question: str = Field(..., min_length=1, description="题目文本")
    mode: SolverModeValue = Field(default="brief")
    subject: Optional[str] = None
    grade_level: Optional[str] = None
    context: Optional[str] = None
    generate_plot: bool = Field(default=False, description="是否生成绘图（Milestone 5）")


class VisualizationHintResponse(BaseModel):
    needed: bool
    type: str
    description: str
    keywords: list[str]


class PlotResponse(BaseModel):
    """Milestone 5: 绘图响应"""
    success: bool
    method: str = Field(default="none")
    image_data: Optional[str] = None
    image_url: Optional[str] = None
    code: Optional[str] = None
    error: Optional[str] = None


class SolveResponse(BaseModel):
    mode: SolverModeValue
    content: str
    question: str
    needs_visualization: bool
    visualization_hint: VisualizationHintResponse
    source: Literal["text", "image"] = "text"
    extracted_text: Optional[str] = None
    plot: Optional[PlotResponse] = None  # Milestone 5


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    llm_provider: str
    ocr_provider: str
    plot_enabled: bool = False  # Milestone 5
