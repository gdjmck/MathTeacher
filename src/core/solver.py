"""
Math Tutor 核心解题逻辑模块

提供三种解题模式：
1. 思路提示（hint）
2. 简略思路（brief）
3. 详细详解（detailed）
"""

from enum import Enum
from typing import Optional
from dataclasses import dataclass

# 导入可视化模块（Milestone 2）
try:
    from .visualization import VisualizationJudge
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


class SolverMode(Enum):
    """解题模式枚举"""
    HINT = "hint"           # 思路提示
    BRIEF = "brief"         # 简略思路
    DETAILED = "detailed"   # 详细详解


@dataclass
class MathProblem:
    """数学问题数据结构"""
    question: str                    # 题目内容
    subject: Optional[str] = None    # 学科分类（代数、几何等）
    grade_level: Optional[str] = None # 年级水平
    context: Optional[str] = None    # 额外上下文


@dataclass
class SolutionResponse:
    """解题响应数据结构"""
    mode: SolverMode           # 使用的模式
    content: str               # 回答内容
    problem: MathProblem       # 原问题
    needs_visualization: bool = False  # 是否需要可视化（Milestone 2预留）


class PromptTemplate:
    """Prompt 模板管理"""

    @staticmethod
    def get_system_prompt() -> str:
        """获取系统提示词"""
        return """你是一位经验丰富的数学教师，擅长用清晰易懂的方式讲解数学问题。
你的目标是帮助学生理解数学概念和解题方法，而不仅仅是给出答案。

在回答时请注意：
- 使用准确的数学术语
- 步骤清晰，逻辑严密
- 根据学生水平调整讲解深度
- 鼓励学生思考"""

    @staticmethod
    def get_hint_prompt(problem: MathProblem) -> str:
        """获取思路提示模式的prompt"""
        return f"""请为以下数学问题提供解题思路提示。

【要求】
- 不要直接给出完整解答
- 提供关键的思考方向和切入点
- 点出需要使用的重要概念或公式
- 引导学生自主思考
- 控制在2-3个提示点

【题目】
{problem.question}

请给出思路提示："""

    @staticmethod
    def get_brief_prompt(problem: MathProblem) -> str:
        """获取简略思路模式的prompt"""
        return f"""请为以下数学问题提供简洁完整的解题思路。

【要求】
- 给出完整的解题步骤
- 每个步骤简明扼要
- 突出关键推理过程
- 避免冗长的解释
- 控制在300字以内

【题目】
{problem.question}

请给出解题思路："""

    @staticmethod
    def get_detailed_prompt(problem: MathProblem) -> str:
        """获取详细详解模式的prompt"""
        return f"""请为以下数学问题提供详细的解题讲解。

【要求】
- 给出完整详细的解题过程
- 每个步骤都要解释为什么这样做
- 总结涉及的知识点
- 指出易错点和注意事项
- 如果有多种解法，可以提及并比较
- 在最后总结本题的关键知识点

【题目】
{problem.question}

请给出详细讲解："""


class MathSolver:
    """数学解题器核心类"""

    def __init__(self, llm_client=None, enable_visualization_check=True):
        """
        初始化解题器

        Args:
            llm_client: LLM客户端实例
            enable_visualization_check: 是否启用可视化判断（Milestone 2）
        """
        self.llm_client = llm_client
        self.prompt_template = PromptTemplate()
        self.enable_visualization_check = enable_visualization_check and VISUALIZATION_AVAILABLE

        # 初始化可视化判断器
        if self.enable_visualization_check:
            self.viz_judge = VisualizationJudge()
        else:
            self.viz_judge = None

    def solve(
        self,
        problem: MathProblem,
        mode: SolverMode = SolverMode.BRIEF
    ) -> SolutionResponse:
        """
        解答数学问题

        Args:
            problem: 数学问题
            mode: 解题模式

        Returns:
            SolutionResponse: 解题结果
        """
        # 根据模式获取对应的prompt
        if mode == SolverMode.HINT:
            user_prompt = self.prompt_template.get_hint_prompt(problem)
        elif mode == SolverMode.BRIEF:
            user_prompt = self.prompt_template.get_brief_prompt(problem)
        elif mode == SolverMode.DETAILED:
            user_prompt = self.prompt_template.get_detailed_prompt(problem)
        else:
            raise ValueError(f"不支持的模式: {mode}")

        # 调用LLM获取回答
        system_prompt = self.prompt_template.get_system_prompt()
        content = self._call_llm(system_prompt, user_prompt)

        # 判断是否需要可视化（Milestone 2）
        needs_viz = False
        if self.enable_visualization_check and self.viz_judge:
            needs_viz = self.viz_judge.should_visualize(
                problem.question,
                content
            )

        # 构建响应
        response = SolutionResponse(
            mode=mode,
            content=content,
            problem=problem,
            needs_visualization=needs_viz
        )

        return response

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        调用LLM API

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词

        Returns:
            str: LLM的回答
        """
        if self.llm_client is None:
            # 如果没有配置LLM客户端，返回模拟响应
            return self._mock_response(user_prompt)

        # 调用LLM客户端
        return self.llm_client.chat(system_prompt, user_prompt)

    def _mock_response(self, prompt: str) -> str:
        """模拟LLM响应，用于测试"""
        return f"[模拟响应] 这是对以下prompt的回答：\n{prompt[:100]}..."


# 便捷函数
def solve_math_problem(
    question: str,
    mode: str = "brief",
    **kwargs
) -> dict:
    """
    便捷的解题函数

    Args:
        question: 题目内容
        mode: 解题模式 ("hint", "brief", "detailed")
        **kwargs: 其他问题属性

    Returns:
        dict: 解题结果的字典表示
    """
    problem = MathProblem(question=question, **kwargs)
    solver = MathSolver()
    mode_enum = SolverMode(mode)

    response = solver.solve(problem, mode_enum)

    return {
        "mode": response.mode.value,
        "content": response.content,
        "question": response.problem.question,
        "needs_visualization": response.needs_visualization
    }
