"""
Milestone 2 综合示例：展示可视化判断功能

演示如何结合解题器和可视化判断
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import (
    MathSolver,
    MathProblem,
    SolverMode,
    VisualizationJudge,
    VisualizationType
)
from core.llm_client import MockLLMClient


def print_header():
    """打印程序头部"""
    print("\n" + "=" * 70)
    print(" " * 10 + "Math Tutor - Milestone 2 可视化功能演示")
    print("=" * 70)
    print("\n本演示展示数学解题器如何自动判断题目是否需要图形辅助\n")


def demo_visualization_detection():
    """演示可视化检测功能"""
    print("=" * 70)
    print("1. 可视化类型识别演示")
    print("=" * 70)

    judge = VisualizationJudge()

    examples = [
        ("求解方程：x² - 5x + 6 = 0", "代数方程"),
        ("在△ABC中，AB=5，AC=12，BC=13，求△ABC的面积", "几何问题"),
        ("画出函数 f(x) = sin(x) 在 [0, 2π] 上的图像", "函数图像"),
        ("点P(3,4)关于原点对称的点是什么？", "坐标问题"),
        ("某次考试成绩：优秀20人，良好30人，及格15人，不及格5人", "统计数据"),
    ]

    for question, category in examples:
        print(f"\n{'─' * 70}")
        print(f"【类别】{category}")
        print(f"【题目】{question}")

        hint = judge.judge(question)

        if hint.needed:
            print(f"【判断】✓ 需要可视化")
            print(f"【类型】{hint.viz_type.value}")
            print(f"【说明】{hint.description}")
            print(f"【关键词】{', '.join(hint.keywords[:3])}")
        else:
            print(f"【判断】✗ 不需要可视化")


def demo_integrated_solver():
    """演示集成解题器"""
    print("\n\n" + "=" * 70)
    print("2. 集成解题器演示")
    print("=" * 70)
    print("\n展示解题器如何自动判断并标记需要可视化的题目\n")

    mock_client = MockLLMClient()
    solver = MathSolver(llm_client=mock_client, enable_visualization_check=True)

    test_problems = [
        {
            "question": "求圆 (x-2)² + (y-3)² = 16 的圆心和半径",
            "subject": "解析几何",
            "mode": SolverMode.BRIEF
        },
        {
            "question": "解方程组：x + y = 5, 2x - y = 1",
            "subject": "方程组",
            "mode": SolverMode.HINT
        },
        {
            "question": "已知抛物线 y = ax² + bx + c 经过点(0,3)、(1,2)、(2,3)，求抛物线方程",
            "subject": "二次函数",
            "mode": SolverMode.DETAILED
        },
    ]

    mode_names = {
        SolverMode.HINT: "思路提示",
        SolverMode.BRIEF: "简略思路",
        SolverMode.DETAILED: "详细详解"
    }

    for idx, prob_data in enumerate(test_problems, 1):
        print(f"\n{'━' * 70}")
        print(f"示例 {idx}")
        print('━' * 70)

        problem = MathProblem(
            question=prob_data["question"],
            subject=prob_data["subject"]
        )

        print(f"\n【题目】{problem.question}")
        print(f"【学科】{problem.subject}")
        print(f"【模式】{mode_names[prob_data['mode']]}")

        response = solver.solve(problem, prob_data["mode"])

        print(f"\n【回答】")
        print(response.content[:200] + "..." if len(response.content) > 200 else response.content)

        print(f"\n【可视化建议】", end="")
        if response.needs_visualization:
            print(" ✓ 建议添加图形辅助理解")
            print("   📊 可使用 matplotlib 或 GPT Image 生成图形")
        else:
            print(" ✗ 文字说明已足够")


def demo_visualization_types():
    """演示所有可视化类型"""
    print("\n\n" + "=" * 70)
    print("3. 支持的可视化类型")
    print("=" * 70)

    viz_types = {
        VisualizationType.GEOMETRY: {
            "name": "几何图形",
            "example": "三角形、圆、多边形等几何图形",
            "tools": "matplotlib.patches, matplotlib.pyplot"
        },
        VisualizationType.FUNCTION_GRAPH: {
            "name": "函数图像",
            "example": "y=f(x) 的函数曲线",
            "tools": "matplotlib.pyplot, numpy"
        },
        VisualizationType.COORDINATE: {
            "name": "坐标系",
            "example": "点、直线、向量在坐标系中的表示",
            "tools": "matplotlib.pyplot"
        },
        VisualizationType.STATISTICS: {
            "name": "统计图表",
            "example": "柱状图、饼图、折线图",
            "tools": "matplotlib.pyplot, seaborn"
        },
        VisualizationType.NUMBER_LINE: {
            "name": "数轴",
            "example": "不等式解集在数轴上的表示",
            "tools": "matplotlib.pyplot"
        },
        VisualizationType.VECTOR: {
            "name": "向量图",
            "example": "向量的方向和大小",
            "tools": "matplotlib.pyplot, matplotlib.patches"
        },
    }

    for viz_type, info in viz_types.items():
        print(f"\n📌 {info['name']}")
        print(f"   类型代码: {viz_type.value}")
        print(f"   示例: {info['example']}")
        print(f"   绘图工具: {info['tools']}")


def demo_next_steps():
    """展示下一步计划"""
    print("\n\n" + "=" * 70)
    print("4. Milestone 2 完成情况与后续计划")
    print("=" * 70)

    print("\n✅ 已完成:")
    print("   • 自动判断题目是否需要可视化")
    print("   • 识别6种常见可视化类型")
    print("   • 与解题器无缝集成")
    print("   • 基于关键词的智能匹配")
    print("   • 预留绘图接口架构")

    print("\n📋 待实现（未来扩展）:")
    print("   • matplotlib 实际绘图功能")
    print("   • GPT Image API 集成")
    print("   • 更智能的判断逻辑（使用LLM辅助）")
    print("   • 图形参数的自动提取")
    print("   • 多图形组合绘制")

    print("\n⏭️  下一个里程碑: Milestone 3")
    print("   • TypeScript + TailwindCSS 前端界面")
    print("   • 用户交互设计")
    print("   • 可视化图形的展示")


def main():
    """主函数"""
    print_header()
    demo_visualization_detection()
    demo_integrated_solver()
    demo_visualization_types()
    demo_next_steps()

    print("\n\n" + "=" * 70)
    print("演示完成！")
    print("\n要查看更多示例，运行：")
    print("  python tests/test_visualization.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
