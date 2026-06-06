"""
数学公式格式化工具模块

提供公式提取、验证和转换功能
"""

import re
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class FormulaMatch:
    """公式匹配结果"""
    content: str      # 公式内容（不含标记符号）
    start: int        # 起始位置
    end: int          # 结束位置
    is_display: bool  # 是否为独立显示公式（$$...$$）


class FormulaExtractor:
    """公式提取器"""

    # LaTeX公式正则表达式
    DISPLAY_PATTERN = r'\$\$(.*?)\$\$'      # 独立公式 $$...$$
    INLINE_PATTERN = r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)'  # 行内公式 $...$

    @staticmethod
    def extract_formulas(text: str) -> List[FormulaMatch]:
        """
        提取文本中的所有LaTeX公式

        Args:
            text: 文本内容

        Returns:
            List[FormulaMatch]: 公式匹配列表
        """
        formulas = []

        # 先提取独立公式（$$...$$）
        for match in re.finditer(FormulaExtractor.DISPLAY_PATTERN, text, re.DOTALL):
            formulas.append(FormulaMatch(
                content=match.group(1).strip(),
                start=match.start(),
                end=match.end(),
                is_display=True
            ))

        # 再提取行内公式（$...$），但排除已经被$$...$$覆盖的部分
        display_ranges = [(f.start, f.end) for f in formulas]

        for match in re.finditer(FormulaExtractor.INLINE_PATTERN, text):
            # 检查是否在$$...$$范围内
            in_display = any(start <= match.start() < end for start, end in display_ranges)
            if not in_display:
                formulas.append(FormulaMatch(
                    content=match.group(1).strip(),
                    start=match.start(),
                    end=match.end(),
                    is_display=False
                ))

        # 按位置排序
        formulas.sort(key=lambda x: x.start)
        return formulas

    @staticmethod
    def has_latex_formulas(text: str) -> bool:
        """
        检查文本是否包含LaTeX公式

        Args:
            text: 文本内容

        Returns:
            bool: 是否包含LaTeX公式
        """
        return bool(re.search(FormulaExtractor.DISPLAY_PATTERN, text) or
                    re.search(FormulaExtractor.INLINE_PATTERN, text))

    @staticmethod
    def count_formulas(text: str) -> Tuple[int, int]:
        """
        统计公式数量

        Args:
            text: 文本内容

        Returns:
            Tuple[int, int]: (行内公式数, 独立公式数)
        """
        formulas = FormulaExtractor.extract_formulas(text)
        inline_count = sum(1 for f in formulas if not f.is_display)
        display_count = sum(1 for f in formulas if f.is_display)
        return inline_count, display_count


class FormulaValidator:
    """公式验证器"""

    # 常见LaTeX命令
    COMMON_COMMANDS = {
        'frac', 'sqrt', 'sum', 'int', 'lim', 'sin', 'cos', 'tan',
        'log', 'ln', 'exp', 'max', 'min', 'inf', 'sup',
        'alpha', 'beta', 'gamma', 'theta', 'pi', 'omega',
        'Delta', 'Sigma', 'Omega', 'infty',
        'cdot', 'times', 'div', 'pm', 'leq', 'geq', 'neq',
        'rightarrow', 'leftarrow', 'Rightarrow', 'Leftarrow',
    }

    @staticmethod
    def validate_latex(formula: str) -> Tuple[bool, str]:
        """
        验证LaTeX公式的基本语法

        Args:
            formula: 公式内容

        Returns:
            Tuple[bool, str]: (是否有效, 错误信息)
        """
        # 检查括号匹配
        brackets = {'(': ')', '{': '}', '[': ']'}
        stack = []

        for char in formula:
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                if not stack:
                    return False, f"不匹配的右括号: {char}"
                left = stack.pop()
                if brackets[left] != char:
                    return False, f"括号不匹配: {left} 与 {char}"

        if stack:
            return False, f"未闭合的左括号: {stack[0]}"

        # 检查基本的LaTeX命令格式
        # \command 或 \command{...}
        invalid_commands = re.findall(r'\\([a-zA-Z]+)', formula)
        unknown_commands = [cmd for cmd in invalid_commands
                           if cmd not in FormulaValidator.COMMON_COMMANDS]

        if unknown_commands and len(unknown_commands) > 3:
            # 如果有很多未知命令，可能是误报或高级用法，只给警告
            return True, f"警告：包含不常见的LaTeX命令: {', '.join(unknown_commands[:3])}"

        return True, ""


class FormulaRenderer:
    """公式渲染器（占位，前端实现）"""

    @staticmethod
    def to_html_preview(text: str, placeholder: str = "[公式]") -> str:
        """
        将文本中的LaTeX公式替换为占位符（用于纯文本预览）

        Args:
            text: 包含LaTeX公式的文本
            placeholder: 占位符文本

        Returns:
            str: 替换后的文本
        """
        # 替换独立公式
        text = re.sub(FormulaExtractor.DISPLAY_PATTERN, f'\n{placeholder}\n', text, flags=re.DOTALL)
        # 替换行内公式
        text = re.sub(FormulaExtractor.INLINE_PATTERN, placeholder, text)
        return text

    @staticmethod
    def to_plain_text(text: str) -> str:
        """
        将LaTeX公式转为简化的纯文本（移除$符号，保留LaTeX内容）

        Args:
            text: 包含LaTeX公式的文本

        Returns:
            str: 纯文本版本
        """
        # 移除$符号但保留公式内容
        text = re.sub(r'\$\$(.*?)\$\$', r'\n\1\n', text, flags=re.DOTALL)
        text = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', r'\1', text)
        return text


class FormulaFormatter:
    """公式格式化器（完整功能）"""

    def __init__(self):
        self.extractor = FormulaExtractor()
        self.validator = FormulaValidator()
        self.renderer = FormulaRenderer()

    def analyze(self, text: str) -> dict:
        """
        分析文本中的公式使用情况

        Args:
            text: 文本内容

        Returns:
            dict: 分析结果
        """
        formulas = self.extractor.extract_formulas(text)
        inline_count, display_count = self.extractor.count_formulas(text)

        # 验证每个公式
        validation_results = []
        for formula in formulas:
            is_valid, message = self.validator.validate_latex(formula.content)
            validation_results.append({
                'formula': formula.content,
                'is_display': formula.is_display,
                'is_valid': is_valid,
                'message': message
            })

        return {
            'has_formulas': len(formulas) > 0,
            'total_count': len(formulas),
            'inline_count': inline_count,
            'display_count': display_count,
            'formulas': validation_results
        }


# 便捷函数
def extract_formulas(text: str) -> List[str]:
    """
    提取文本中的所有公式内容

    Args:
        text: 文本内容

    Returns:
        List[str]: 公式内容列表
    """
    extractor = FormulaExtractor()
    matches = extractor.extract_formulas(text)
    return [m.content for m in matches]


def validate_formula(formula: str) -> bool:
    """
    验证公式是否有效

    Args:
        formula: 公式内容

    Returns:
        bool: 是否有效
    """
    validator = FormulaValidator()
    is_valid, _ = validator.validate_latex(formula)
    return is_valid


def has_formulas(text: str) -> bool:
    """
    检查文本是否包含公式

    Args:
        text: 文本内容

    Returns:
        bool: 是否包含公式
    """
    extractor = FormulaExtractor()
    return extractor.has_latex_formulas(text)
