"""
Math Tutor 核心模块
"""

from .solver import (
    MathSolver,
    MathProblem,
    SolutionResponse,
    SolverMode,
    solve_math_problem
)

from .llm_client import (
    BaseLLMClient,
    OpenAIClient,
    AnthropicClient,
    MockLLMClient,
    create_llm_client
)

from .visualization import (
    VisualizationJudge,
    VisualizationType,
    VisualizationHint,
    VisualizationPlaceholder,
    check_visualization_need
)

__all__ = [
    'MathSolver',
    'MathProblem',
    'SolutionResponse',
    'SolverMode',
    'solve_math_problem',
    'BaseLLMClient',
    'OpenAIClient',
    'AnthropicClient',
    'MockLLMClient',
    'create_llm_client',
    'VisualizationJudge',
    'VisualizationType',
    'VisualizationHint',
    'VisualizationPlaceholder',
    'check_visualization_need',
]
