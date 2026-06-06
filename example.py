"""
Math Tutor 非交互式示例演示

展示三种解题模式的完整示例
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import MathSolver, MathProblem, SolverMode
from core.llm_client import MockLLMClient


def main():
    """运行示例演示"""
    print("\n" + "=" * 70)
    print(" " * 15 + "Math Tutor - 数学解题助手示例")
    print("=" * 70)
    print("\n使用模拟LLM演示三种解题模式\n")

    # 创建Mock LLM客户端和解题器
    mock_client = MockLLMClient()
    solver = MathSolver(llm_client=mock_client)

    # 示例问题
    examples = [
        {
            "question": "求解方程：3x - 7 = 11",
            "mode": SolverMode.HINT,
            "subject": "代数",
            "grade_level": "初中"
        },
        {
            "question": "计算：sin²θ + cos²θ",
            "mode": SolverMode.BRIEF,
            "subject": "三角函数",
            "grade_level": "高中"
        },
        {
            "question": "证明：√2是无理数",
            "mode": SolverMode.DETAILED,
            "subject": "数论",
            "grade_level": "高中"
        },
    ]

    mode_names = {
        SolverMode.HINT: "思路提示",
        SolverMode.BRIEF: "简略思路",
        SolverMode.DETAILED: "详细详解"
    }

    for idx, example in enumerate(examples, 1):
        print("\n" + "=" * 70)
        print(f"示例 {idx}/{len(examples)}")
        print("=" * 70)

        problem = MathProblem(
            question=example["question"],
            subject=example.get("subject"),
            grade_level=example.get("grade_level")
        )

        print(f"\n【题目】{problem.question}")
        print(f"【学科】{problem.subject}")
        print(f"【年级】{problem.grade_level}")
        print(f"【模式】{mode_names[example['mode']]}")
        print("-" * 70)

        response = solver.solve(problem, example["mode"])
        print(response.content)

        if response.needs_visualization:
            print("\n💡 提示：此题目可能需要图形辅助理解")

        print("=" * 70)

    print("\n" + "=" * 70)
    print("所有示例演示完毕！")
    print("\nMilestone 1 核心功能已实现：")
    print("  ✓ 思路提示模式")
    print("  ✓ 简略思路模式")
    print("  ✓ 详细详解模式")
    print("  ✓ LLM客户端架构（支持OpenAI、Anthropic、Mock）")
    print("  ✓ 灵活的Prompt模板系统")
    print("\n下一步：实现Milestone 2（绘图判断逻辑）")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
