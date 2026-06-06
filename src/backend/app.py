"""FastAPI 应用入口。"""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.backend.config import AppSettings
from src.backend.schemas import HealthResponse, SolveRequest, SolveResponse
from src.backend.services import OCRService, SolverService, build_default_ocr_service, build_default_solver_service


def create_app(
    solver_service: Optional[SolverService] = None,
    ocr_service: Optional[OCRService] = None,
    settings: Optional[AppSettings] = None,
) -> FastAPI:
    app_settings = settings or AppSettings.from_env()

    app = FastAPI(
        title="Math Tutor API",
        version="0.1.0",
        description="Milestone 4: Python 后端接口，支持文字与图片输入。",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.settings = app_settings
    app.state.solver_service = solver_service or build_default_solver_service()
    app.state.ocr_service = ocr_service or build_default_ocr_service()

    @app.get("/api/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            llm_provider=app.state.settings.llm_provider,
            ocr_provider=app.state.settings.ocr_provider,
            plot_enabled=app.state.settings.enable_plot_generation,  # Milestone 5
        )

    @app.post("/api/solve", response_model=SolveResponse)
    def solve_text(payload: SolveRequest) -> SolveResponse:
        try:
            result = app.state.solver_service.solve(
                question=payload.question,
                mode=payload.mode,
                subject=payload.subject,
                grade_level=payload.grade_level,
                context=payload.context,
                source="text",
                generate_plot=payload.generate_plot,  # Milestone 5
            )
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        return SolveResponse(**result)

    @app.post("/api/solve/image", response_model=SolveResponse)
    async def solve_image(
        file: UploadFile = File(...),
        mode: str = Form("brief"),
        subject: Optional[str] = Form(None),
        grade_level: Optional[str] = Form(None),
        context: Optional[str] = Form(None),
        generate_plot: bool = Form(False),  # Milestone 5
    ) -> SolveResponse:
        try:
            ocr_result = await app.state.ocr_service.extract_question(file)
            result = app.state.solver_service.solve(
                question=ocr_result.text,
                mode=mode,
                subject=subject,
                grade_level=grade_level,
                context=context,
                source="image",
                extracted_text=ocr_result.text,
                generate_plot=generate_plot,  # Milestone 5
            )
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        return SolveResponse(**result)

    return app


app = create_app()
