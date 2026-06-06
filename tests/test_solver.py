"""
Math Solver 核心逻辑测试
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core import MathSolver, MathProblem, SolverMode, solve_math_problem
from src.core.llm_client import MockLLMClient


def test_solver_modes():
    """测试三种解题模式"""
    print("=" * 60)
    print("测试 Math Solver 三种模式")
    print("=" * 60)

    # 创建带有Mock LLM的解题器
    mock_client = MockLLMClient()
    solver = MathSolver(llm_client=mock_client)

    # 测试问题
    problem = MathProblem(
        question="求解方程：2x + 5 = 15",
        subject="代数",
        grade_level="初中"
    )

    print(f"\n【题目】{problem.question}\n")

    # 测试模式1：思路提示
    print("\n" + "-" * 60)
    print("模式1: 思路提示 (HINT)")
    print("-" * 60)
    response = solver.solve(problem, SolverMode.HINT)
    print(response.content)

    # 测试模式2：简略思路
    print("\n" + "-" * 60)
    print("模式2: 简略思路 (BRIEF)")
    print("-" * 60)
    response = solver.solve(problem, SolverMode.BRIEF)
    print(response.content)

    # 测试模式3：详细详解
    print("\n" + "-" * 60)
    print("模式3: 详细详解 (DETAILED)")
    print("-" * 60)
    response = solver.solve(problem, SolverMode.DETAILED)
    print(response.content)

    print("\n" + "=" * 60)
    print("✓ 测试完成")
    print("=" * 60)


def test_convenience_function():
    """测试便捷函数"""
    print("\n\n" + "=" * 60)
    print("测试便捷函数 solve_math_problem()")
    print("=" * 60)

    result = solve_math_problem(
        question="计算：(3 + 5) × 2 - 4",
        mode="brief",
        subject="算术"
    )

    print(f"\n问题：{result['question']}")
    print(f"模式：{result['mode']}")
    print(f"需要可视化：{result['needs_visualization']}")
    print(f"\n回答：\n{result['content']}")

    print("\n" + "=" * 60)
    print("✓ 便捷函数测试完成")
    print("=" * 60)


def test_prompt_templates():
    """测试Prompt模板生成"""
    print("\n\n" + "=" * 60)
    print("测试 Prompt 模板")
    print("=" * 60)

    from src.core.solver import PromptTemplate

    problem = MathProblem(
        question="证明：对于任意实数a和b，(a+b)² = a² + 2ab + b²"
    )

    print("\n【系统Prompt】")
    print("-" * 60)
    print(PromptTemplate.get_system_prompt())

    print("\n\n【思路提示模式的Prompt】")
    print("-" * 60)
    print(PromptTemplate.get_hint_prompt(problem))

    print("\n\n【简略思路模式的Prompt】")
    print("-" * 60)
    print(PromptTemplate.get_brief_prompt(problem))

    print("\n\n【详细详解模式的Prompt】")
    print("-" * 60)
    print(PromptTemplate.get_detailed_prompt(problem))

    print("\n" + "=" * 60)
    print("✓ Prompt模板测试完成")
    print("=" * 60)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Math Tutor - Milestone 1 核心逻辑测试")
    print("=" * 60)

    test_solver_modes()
    test_convenience_function()
    test_prompt_templates()

    print("\n\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
