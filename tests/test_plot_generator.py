"""
Milestone 5 绘图生成功能测试
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.plot_generator import (
    PlotMethod,
    PlotMethodSelector,
    MatplotlibPlotter,
    PlotGenerator,
    PlotResult
)
from src.core.llm_client import MockLLMClient


def test_method_selector():
    """测试绘图方法选择器"""
    print("=" * 70)
    print("测试绘图方法选择")
    print("=" * 70)

    selector = PlotMethodSelector()

    test_cases = [
        {
            "question": "画出函数 y = x^2 的图像",
            "viz_type": "function_graph",
            "expected": PlotMethod.MATPLOTLIB,
            "description": "函数图像"
        },
        {
            "question": "在坐标系中标出点A(2,3)和点B(5,7)",
            "viz_type": "coordinate",
            "expected": PlotMethod.MATPLOTLIB,
            "description": "坐标点"
        },
        {
            "question": "绘制三角形ABC的示意图",
            "viz_type": "geometry",
            "expected": PlotMethod.GPT_IMAGE,
            "description": "几何示意图"
        },
        {
            "question": "在直角三角形中，AB=3，AC=4，求BC",
            "viz_type": "geometry",
            "expected": PlotMethod.MATPLOTLIB,
            "description": "带数值的几何题"
        },
    ]

    passed = 0
    for idx, case in enumerate(test_cases, 1):
        print(f"\n{'-' * 70}")
        print(f"测试 {idx}: {case['description']}")
        print(f"题目: {case['question']}")

        method = selector.select_method(case['question'], case['viz_type'])

        print(f"选择方法: {method.value}")
        print(f"预期方法: {case['expected'].value}")

        if method == case['expected']:
            print("✓ 通过")
            passed += 1
        else:
            print("✗ 失败")

    print(f"\n{'=' * 70}")
    print(f"选择器测试: {passed}/{len(test_cases)} 通过")
    print("=" * 70)


def test_matplotlib_code_generation():
    """测试Matplotlib代码生成"""
    print("\n\n" + "=" * 70)
    print("测试Matplotlib代码生成")
    print("=" * 70)

    # 创建Mock LLM返回matplotlib代码
    mock_code = """
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8, 6))

x = np.linspace(-5, 5, 100)
y = x**2

ax.plot(x, y, 'b-', linewidth=2, label='y = x²')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('函数 y = x² 的图像')
ax.legend()
"""

    mock_client = MockLLMClient(mock_response=mock_code)

    try:
        plotter = MatplotlibPlotter(mock_client)

        result = plotter.generate(
            question="画出函数 y = x^2 的图像",
            answer_content="这是一个开口向上的抛物线",
            visualization_type="function_graph"
        )

        print(f"\n生成成功: {result.success}")
        print(f"方法: {result.method.value}")
        print(f"代码长度: {len(result.code) if result.code else 0} 字符")
        print(f"图像数据长度: {len(result.image_data) if result.image_data else 0} 字符")

        if result.success:
            print("\n✓ Matplotlib代码生成和执行成功")
        else:
            print(f"\n✗ 失败: {result.error}")

    except ImportError as e:
        print(f"\n⚠️  跳过测试: {e}")
        print("提示: pip install matplotlib numpy")

    print("\n" + "=" * 70)


def test_plot_generator_integration():
    """测试PlotGenerator集成"""
    print("\n\n" + "=" * 70)
    print("测试PlotGenerator集成")
    print("=" * 70)

    mock_client = MockLLMClient()

    try:
        generator = PlotGenerator(
            llm_client=mock_client,
            openai_api_key=None  # 不测试GPT Image 2
        )

        print(f"\n可用方法:")
        print(f"  GPT Image 2: {'✓' if generator.openai_image_plotter else '✗'}")
        print(f"  Matplotlib: {'✓' if generator.matplotlib_plotter else '✗'}")

        if generator.matplotlib_plotter:
            print("\n测试生成图像...")
            result = generator.generate_plot(
                question="画出函数 y = sin(x) 的图像",
                answer_content="这是一个正弦曲线",
                visualization_type="function_graph"
            )

            print(f"\n结果:")
            print(f"  成功: {result.success}")
            print(f"  方法: {result.method.value}")
            if result.error:
                print(f"  错误: {result.error}")

            if result.success:
                print("\n✓ PlotGenerator集成测试通过")
        else:
            print("\n⚠️  Matplotlib不可用，跳过集成测试")

    except Exception as e:
        print(f"\n✗ 集成测试失败: {e}")

    print("\n" + "=" * 70)


def test_fallback_mechanism():
    """测试降级机制"""
    print("\n\n" + "=" * 70)
    print("测试降级机制")
    print("=" * 70)

    mock_client = MockLLMClient()

    # 创建只有Matplotlib的生成器
    generator = PlotGenerator(
        llm_client=mock_client,
        openai_api_key=None
    )

    print("\n场景: 请求GPT Image 2但不可用，应降级到Matplotlib")

    try:
        result = generator.generate_plot(
            question="画出示意图",
            answer_content="简单的几何图",
            visualization_type="geometry",
            preferred_method=PlotMethod.GPT_IMAGE  # 明确请求GPT Image 2
        )

        print(f"\n请求方法: GPT_IMAGE")
        print(f"实际方法: {result.method.value}")
        print(f"成功: {result.success}")

        if result.method == PlotMethod.MATPLOTLIB:
            print("\n✓ 降级机制工作正常")
        else:
            print("\n✗ 降级失败")

    except Exception as e:
        print(f"\n⚠️  测试异常: {e}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Math Tutor - Milestone 5 绘图功能测试")
    print("=" * 70)

    test_method_selector()
    test_matplotlib_code_generation()
    test_plot_generator_integration()
    test_fallback_mechanism()

    print("\n\n" + "=" * 70)
    print("测试完成")
    print("\n提示:")
    print("  - 完整测试需要: pip install matplotlib numpy")
    print("  - GPT Image 2测试需要: OPENAI_API_KEY环境变量")
    print("=" * 70)
