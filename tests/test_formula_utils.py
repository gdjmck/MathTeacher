"""
公式格式化工具测试
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.formula_utils import (
    FormulaExtractor,
    FormulaValidator,
    FormulaRenderer,
    FormulaFormatter,
    extract_formulas,
    validate_formula,
    has_formulas
)


def test_formula_extraction():
    """测试公式提取"""
    print("=" * 70)
    print("测试公式提取功能")
    print("=" * 70)

    test_cases = [
        {
            "text": "方程 $x^2 + 2x + 1 = 0$ 的解为 $x = -1$",
            "expected_count": 2,
            "description": "行内公式"
        },
        {
            "text": "二次公式：$$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$",
            "expected_count": 1,
            "description": "独立公式"
        },
        {
            "text": "勾股定理：$a^2 + b^2 = c^2$，证明如下：$$a^2 + b^2 = c^2$$",
            "expected_count": 2,
            "description": "混合公式"
        },
        {
            "text": "普通文本，没有公式",
            "expected_count": 0,
            "description": "无公式"
        },
    ]

    extractor = FormulaExtractor()
    passed = 0
    failed = 0

    for idx, case in enumerate(test_cases, 1):
        print(f"\n{'-' * 70}")
        print(f"测试用例 {idx}: {case['description']}")
        print(f"文本: {case['text'][:50]}...")

        formulas = extractor.extract_formulas(case['text'])
        count = len(formulas)

        print(f"提取到 {count} 个公式:")
        for i, formula in enumerate(formulas, 1):
            print(f"  {i}. {'[独立]' if formula.is_display else '[行内]'} {formula.content}")

        if count == case['expected_count']:
            print("✓ 通过")
            passed += 1
        else:
            print(f"✗ 失败 (预期 {case['expected_count']}，实际 {count})")
            failed += 1

    print(f"\n{'=' * 70}")
    print(f"提取测试: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")
    print("=" * 70)


def test_formula_validation():
    """测试公式验证"""
    print("\n\n" + "=" * 70)
    print("测试公式验证功能")
    print("=" * 70)

    test_cases = [
        {
            "formula": "x^2 + 2x + 1",
            "expected_valid": True,
            "description": "简单公式"
        },
        {
            "formula": "\\frac{a+b}{c}",
            "expected_valid": True,
            "description": "分数"
        },
        {
            "formula": "\\sqrt{x^2 + y^2}",
            "expected_valid": True,
            "description": "根号"
        },
        {
            "formula": "\\int_{0}^{\\infty} e^{-x} dx",
            "expected_valid": True,
            "description": "积分"
        },
        {
            "formula": "\\frac{a+b}{c",
            "expected_valid": False,
            "description": "括号不匹配"
        },
    ]

    validator = FormulaValidator()
    passed = 0
    failed = 0

    for idx, case in enumerate(test_cases, 1):
        print(f"\n{'-' * 70}")
        print(f"测试用例 {idx}: {case['description']}")
        print(f"公式: {case['formula']}")

        is_valid, message = validator.validate_latex(case['formula'])

        print(f"验证结果: {'有效' if is_valid else '无效'}")
        if message:
            print(f"信息: {message}")

        if is_valid == case['expected_valid']:
            print("✓ 通过")
            passed += 1
        else:
            print(f"✗ 失败")
            failed += 1

    print(f"\n{'=' * 70}")
    print(f"验证测试: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")
    print("=" * 70)


def test_formula_formatter():
    """测试格式化器"""
    print("\n\n" + "=" * 70)
    print("测试公式格式化器")
    print("=" * 70)

    text = """
解题步骤：

1. 设方程为 $ax^2 + bx + c = 0$
2. 使用求根公式：
$$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$
3. 代入 $a=1, b=2, c=1$，得：
$$x = \\frac{-2 \\pm \\sqrt{4-4}}{2} = -1$$

因此方程的解为 $x = -1$（重根）。
"""

    formatter = FormulaFormatter()
    analysis = formatter.analyze(text)

    print(f"\n分析结果:")
    print(f"  包含公式: {analysis['has_formulas']}")
    print(f"  总数: {analysis['total_count']}")
    print(f"  行内公式: {analysis['inline_count']}")
    print(f"  独立公式: {analysis['display_count']}")

    print(f"\n公式详情:")
    for i, formula_info in enumerate(analysis['formulas'], 1):
        print(f"  {i}. {'[独立]' if formula_info['is_display'] else '[行内]'}")
        print(f"     内容: {formula_info['formula']}")
        print(f"     状态: {'✓ 有效' if formula_info['is_valid'] else '✗ 无效'}")
        if formula_info['message']:
            print(f"     信息: {formula_info['message']}")

    print(f"\n{'=' * 70}")
    print("✓ 格式化器测试完成")
    print("=" * 70)


def test_convenience_functions():
    """测试便捷函数"""
    print("\n\n" + "=" * 70)
    print("测试便捷函数")
    print("=" * 70)

    text = "勾股定理：$a^2 + b^2 = c^2$"

    print(f"\n文本: {text}")
    print(f"包含公式: {has_formulas(text)}")
    print(f"提取的公式: {extract_formulas(text)}")

    formula = "\\frac{a+b}{c}"
    print(f"\n公式: {formula}")
    print(f"是否有效: {validate_formula(formula)}")

    print(f"\n{'=' * 70}")
    print("✓ 便捷函数测试完成")
    print("=" * 70)


def test_rendering():
    """测试渲染功能"""
    print("\n\n" + "=" * 70)
    print("测试渲染功能")
    print("=" * 70)

    text = "方程 $x^2 + 1 = 0$ 的解为：$$x = \\pm i$$"

    renderer = FormulaRenderer()

    print(f"\n原文本:")
    print(text)

    print(f"\n占位符预览:")
    print(renderer.to_html_preview(text, "[公式]"))

    print(f"\n纯文本版本:")
    print(renderer.to_plain_text(text))

    print(f"\n{'=' * 70}")
    print("✓ 渲染测试完成")
    print("=" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Math Tutor - 公式格式化工具测试")
    print("=" * 70)

    test_formula_extraction()
    test_formula_validation()
    test_formula_formatter()
    test_convenience_functions()
    test_rendering()

    print("\n\n" + "=" * 70)
    print("所有测试完成！")
    print("=" * 70)
