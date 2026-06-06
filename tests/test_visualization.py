"""
可视化判断功能测试
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.visualization import (
    VisualizationJudge,
    VisualizationType,
    check_visualization_need
)


def test_visualization_judge():
    """测试可视化判断器"""
    print("=" * 70)
    print("测试可视化判断功能")
    print("=" * 70)

    judge = VisualizationJudge()

    # 测试用例
    test_cases = [
        {
            "question": "求解方程：2x + 5 = 15",
            "expected_viz": False,
            "description": "普通代数方程"
        },
        {
            "question": "计算三角形ABC的面积，其中AB=3, AC=4, ∠A=90°",
            "expected_viz": True,
            "expected_type": VisualizationType.GEOMETRY,
            "description": "几何图形题"
        },
        {
            "question": "画出函数 y = x² - 2x + 1 的图像，并找出其顶点",
            "expected_viz": True,
            "expected_type": VisualizationType.FUNCTION_GRAPH,
            "description": "函数图像题"
        },
        {
            "question": "在坐标系中，点A(2,3)和点B(5,7)之间的距离是多少？",
            "expected_viz": True,
            "expected_type": VisualizationType.COORDINATE,
            "description": "坐标系题"
        },
        {
            "question": "某班级数学成绩分布：90-100分10人，80-90分15人，70-80分12人，60-70分8人",
            "expected_viz": True,
            "expected_type": VisualizationType.STATISTICS,
            "description": "统计题"
        },
        {
            "question": "解不等式：-3 < 2x - 1 ≤ 5",
            "expected_viz": True,
            "expected_type": VisualizationType.NUMBER_LINE,
            "description": "不等式题（数轴）"
        },
        {
            "question": "向量a=(3,4)，向量b=(1,2)，求a+b的模",
            "expected_viz": True,
            "expected_type": VisualizationType.VECTOR,
            "description": "向量题"
        },
        {
            "question": "化简：(a+b)²",
            "expected_viz": False,
            "description": "代数化简"
        },
    ]

    passed = 0
    failed = 0

    for idx, case in enumerate(test_cases, 1):
        print(f"\n{'-' * 70}")
        print(f"测试用例 {idx}: {case['description']}")
        print(f"题目: {case['question']}")

        hint = judge.judge(case['question'])

        print(f"判断结果: {'需要可视化' if hint.needed else '不需要可视化'}")
        if hint.needed:
            print(f"可视化类型: {hint.viz_type.value}")
            print(f"描述: {hint.description}")
            print(f"匹配关键词: {', '.join(hint.keywords[:5])}")

        # 验证结果
        viz_correct = hint.needed == case['expected_viz']
        type_correct = True
        if hint.needed and 'expected_type' in case:
            type_correct = hint.viz_type == case['expected_type']

        if viz_correct and type_correct:
            print("✓ 通过")
            passed += 1
        else:
            print("✗ 失败")
            if not viz_correct:
                print(f"  预期需要可视化: {case['expected_viz']}, 实际: {hint.needed}")
            if not type_correct:
                print(f"  预期类型: {case['expected_type'].value}, 实际: {hint.viz_type.value}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"测试完成: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")
    print("=" * 70)

    return failed == 0


def test_convenience_function():
    """测试便捷函数"""
    print("\n\n" + "=" * 70)
    print("测试便捷函数 check_visualization_need()")
    print("=" * 70)

    result = check_visualization_need(
        question="画出圆 x² + y² = 25 在坐标系中的图像",
        answer="这是一个圆心在原点、半径为5的圆"
    )

    print(f"\n问题: 画出圆 x² + y² = 25 在坐标系中的图像")
    print(f"需要可视化: {result['needed']}")
    print(f"类型: {result['type']}")
    print(f"描述: {result['description']}")
    print(f"关键词: {', '.join(result['keywords'][:5])}")

    print("\n✓ 便捷函数测试完成")
    print("=" * 70)


def test_integration_with_solver():
    """测试与解题器的集成"""
    print("\n\n" + "=" * 70)
    print("测试可视化判断与解题器集成")
    print("=" * 70)

    from src.core import MathSolver, MathProblem, SolverMode
    from src.core.llm_client import MockLLMClient

    mock_client = MockLLMClient()
    solver = MathSolver(llm_client=mock_client, enable_visualization_check=True)

    # 测试需要可视化的题目
    problem1 = MathProblem(
        question="在直角三角形ABC中，∠C=90°，AC=3，BC=4，求AB的长度"
    )
    response1 = solver.solve(problem1, SolverMode.BRIEF)

    print(f"\n【题目1】{problem1.question}")
    print(f"需要可视化: {response1.needs_visualization}")
    print("✓ 正确识别为需要几何图形" if response1.needs_visualization else "✗ 未识别出需要可视化")

    # 测试不需要可视化的题目
    problem2 = MathProblem(
        question="计算：125 × 8"
    )
    response2 = solver.solve(problem2, SolverMode.BRIEF)

    print(f"\n【题目2】{problem2.question}")
    print(f"需要可视化: {response2.needs_visualization}")
    print("✓ 正确识别为不需要可视化" if not response2.needs_visualization else "✗ 错误识别为需要可视化")

    print("\n" + "=" * 70)
    print("✓ 集成测试完成")
    print("=" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Math Tutor - Milestone 2 可视化判断测试")
    print("=" * 70)

    success = test_visualization_judge()
    test_convenience_function()
    test_integration_with_solver()

    print("\n\n" + "=" * 70)
    if success:
        print("所有测试完成！✓")
    else:
        print("部分测试失败，请检查")
    print("=" * 70)
