"""
绘图生成模块 - Milestone 5

支持两种绘图方式：
1. OpenAI GPT Image 2 - 适合概念性图示
2. Matplotlib代码生成 - 适合精确的数学图形
"""

from __future__ import annotations

import base64
import io
import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')  # 无GUI后端
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class PlotMethod(Enum):
    """绘图方法枚举"""
    GPT_IMAGE = "gpt_image2"    # OpenAI GPT Image 2图像生成
    MATPLOTLIB = "matplotlib"   # Matplotlib代码生成
    NONE = "none"              # 不生成图像


@dataclass
class PlotResult:
    """绘图结果"""
    method: PlotMethod        # 使用的方法
    image_data: Optional[str] # Base64编码的图像数据
    image_url: Optional[str]  # 图像URL（OpenAI图像模型）
    code: Optional[str]       # 生成的代码（Matplotlib）
    error: Optional[str]      # 错误信息
    success: bool             # 是否成功


class PlotMethodSelector:
    """绘图方法选择器 - 根据问题类型选择最合适的绘图方法"""

    # 适合GPT Image 2的关键词（概念性、示意性）
    GPT_IMAGE_KEYWORDS = [
        '示意图', '概念图', '流程图', '思维导图',
        '图解', '演示', '展示',
        'diagram', 'illustration', 'concept', 'flowchart'
    ]

    # 适合Matplotlib的关键词（精确数学图形）
    MATPLOTLIB_KEYWORDS = [
        '函数', '图像', '曲线', '抛物线', '双曲线', '圆',
        '坐标', '点', '直线', '三角形', '多边形',
        '统计', '柱状图', '折线图', '散点图', '饼图',
        '数轴', '向量', '图表',
        'function', 'graph', 'curve', 'plot', 'chart',
        'coordinate', 'line', 'circle', 'triangle'
    ]

    @staticmethod
    def select_method(
        question: str,
        visualization_type: str,
        answer_content: Optional[str] = None
    ) -> PlotMethod:
        """
        根据问题和可视化类型选择绘图方法

        Args:
            question: 题目内容
            visualization_type: 可视化类型（来自VisualizationJudge）
            answer_content: 答案内容（可选）

        Returns:
            PlotMethod: 选择的绘图方法
        """
        text = question.lower()
        if answer_content:
            text += " " + answer_content.lower()

        # 优先检查明确的关键词
        gpt_image_matches = sum(1 for kw in PlotMethodSelector.GPT_IMAGE_KEYWORDS if kw in text)
        matplotlib_matches = sum(1 for kw in PlotMethodSelector.MATPLOTLIB_KEYWORDS if kw in text)

        # 如果Matplotlib关键词明显更多，选择Matplotlib
        if matplotlib_matches > gpt_image_matches:
            return PlotMethod.MATPLOTLIB

        # 根据可视化类型决定
        # 精确的数学图形用Matplotlib
        if visualization_type in ['function_graph', 'coordinate', 'statistics', 'number_line', 'vector']:
            return PlotMethod.MATPLOTLIB

        # 几何图形可以两者都用，但Matplotlib更精确
        if visualization_type == 'geometry':
            # 如果有精确的数值，用Matplotlib
            if re.search(r'\d+', question):
                return PlotMethod.MATPLOTLIB
            # 否则可以用GPT Image 2生成示意图
            return PlotMethod.GPT_IMAGE

        # 默认使用Matplotlib（更可靠）
        return PlotMethod.MATPLOTLIB


class OpenAIImagePlotter:
    """OpenAI GPT Image 2图像生成器"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "gpt-image-2",
    ):
        """
        初始化OpenAI图像绘图器

        Args:
            api_key: OpenAI API密钥
            base_url: OpenAI API基础地址
            model: GPT Image模型版本
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("需要安装 openai 库: pip install openai")

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        if not self.api_key:
            raise ValueError("需要提供OpenAI API密钥")

        self.model = model
        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        self.client = OpenAI(**client_kwargs)

    def generate(
        self,
        question: str,
        answer_content: str,
        visualization_type: str
    ) -> PlotResult:
        """
        使用GPT Image 2生成图像

        Args:
            question: 题目内容
            answer_content: 答案内容
            visualization_type: 可视化类型

        Returns:
            PlotResult: 绘图结果
        """
        try:
            # 构建图像生成提示
            prompt = self._build_prompt(question, answer_content, visualization_type)

            # 调用OpenAI图像生成API
            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size="1024x1024",
                n=1,
            )

            image = response.data[0]
            image_data = getattr(image, "b64_json", None)
            image_url = getattr(image, "url", None)

            return PlotResult(
                method=PlotMethod.GPT_IMAGE,
                image_data=image_data,
                image_url=image_url,
                code=None,
                error=None if image_data or image_url else "OpenAI图像模型未返回图像数据",
                success=bool(image_data or image_url)
            )

        except Exception as e:
            return PlotResult(
                method=PlotMethod.GPT_IMAGE,
                image_data=None,
                image_url=None,
                code=None,
                error=str(e),
                success=False
            )

    def _build_prompt(
        self,
        question: str,
        answer_content: str,
        visualization_type: str
    ) -> str:
        """构建GPT Image 2图像生成提示"""
        # 提取关键信息
        prompt = f"Create a clear mathematical diagram for: {question}\n"
        prompt += f"Type: {visualization_type}\n"
        prompt += "Style: Clean, educational, with clear labels and annotations.\n"
        prompt += "Include: Grid lines, axes labels, key measurements."

        return prompt


class MatplotlibPlotter:
    """Matplotlib代码生成与执行绘图器"""

    def __init__(self, llm_client):
        """
        初始化Matplotlib绘图器

        Args:
            llm_client: LLM客户端（用于生成matplotlib代码）
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("需要安装 matplotlib 和 numpy: pip install matplotlib numpy")

        self.llm_client = llm_client

    def generate(
        self,
        question: str,
        answer_content: str,
        visualization_type: str
    ) -> PlotResult:
        """
        使用LLM生成matplotlib代码并执行

        Args:
            question: 题目内容
            answer_content: 答案内容
            visualization_type: 可视化类型

        Returns:
            PlotResult: 绘图结果
        """
        try:
            # 1. 使用LLM生成matplotlib代码
            code = self._generate_code(question, answer_content, visualization_type)

            # 2. 执行代码生成图像
            image_data = self._execute_code(code)

            return PlotResult(
                method=PlotMethod.MATPLOTLIB,
                image_data=image_data,
                image_url=None,
                code=code,
                error=None,
                success=True
            )

        except Exception as e:
            return PlotResult(
                method=PlotMethod.MATPLOTLIB,
                image_data=None,
                image_url=None,
                code=code if 'code' in locals() else None,
                error=str(e),
                success=False
            )

    def _generate_code(
        self,
        question: str,
        answer_content: str,
        visualization_type: str
    ) -> str:
        """使用LLM生成matplotlib代码"""
        system_prompt = """你是一个Python matplotlib绘图专家。
根据数学题目生成清晰、准确的matplotlib绘图代码。

要求：
1. 代码必须是完整的、可执行的Python代码
2. 使用 matplotlib.pyplot 和 numpy
3. 设置中文字体支持
4. 添加网格线、坐标轴标签、标题
5. 使用合适的颜色和线型
6. 代码中不要有 plt.show()，只需要配置好图形
7. 返回纯Python代码，不要有markdown标记

示例格式：
```python
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘图代码
fig, ax = plt.subplots(figsize=(8, 6))
...
```
"""

        user_prompt = f"""请为以下数学问题生成matplotlib绘图代码：

【题目】
{question}

【答案内容】
{answer_content[:500]}

【可视化类型】
{visualization_type}

请生成完整的matplotlib代码："""

        response = self.llm_client.chat(system_prompt, user_prompt)

        # 提取代码块
        code = self._extract_code(response)

        return code

    def _extract_code(self, text: str) -> str:
        """从LLM响应中提取Python代码"""
        # 尝试提取markdown代码块
        code_match = re.search(r'```python\n(.*?)```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        code_match = re.search(r'```\n(.*?)```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        # 如果没有代码块标记，返回整个文本
        return text.strip()

    def _execute_code(self, code: str) -> str:
        """
        执行matplotlib代码并返回base64编码的图像

        Args:
            code: matplotlib代码

        Returns:
            str: Base64编码的PNG图像
        """
        # 创建一个干净的命名空间
        namespace = {
            'plt': plt,
            'np': np,
            'matplotlib': matplotlib,
        }

        # 执行代码
        exec(code, namespace)

        # 保存图像到内存
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        plt.close('all')  # 关闭所有图形，释放内存

        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return image_base64


class PlotGenerator:
    """统一的绘图生成器 - Milestone 5主接口"""

    def __init__(
        self,
        llm_client,
        openai_api_key: Optional[str] = None,
        openai_base_url: Optional[str] = None,
        image_model: str = "gpt-image-2"
    ):
        """
        初始化绘图生成器

        Args:
            llm_client: LLM客户端
            openai_api_key: OpenAI API密钥（用于GPT Image 2）
            openai_base_url: OpenAI API基础地址（用于GPT Image 2）
            image_model: GPT Image模型版本
        """
        self.llm_client = llm_client
        self.selector = PlotMethodSelector()
        resolved_openai_api_key = openai_api_key or getattr(llm_client, "api_key", None)
        resolved_openai_base_url = openai_base_url or getattr(llm_client, "base_url", None)

        # 初始化绘图器
        self.openai_image_plotter = None
        self.matplotlib_plotter = None

        # 尝试初始化GPT Image 2
        if OPENAI_AVAILABLE and resolved_openai_api_key:
            try:
                self.openai_image_plotter = OpenAIImagePlotter(
                    api_key=resolved_openai_api_key,
                    base_url=resolved_openai_base_url,
                    model=image_model,
                )
            except Exception:
                pass

        # 初始化Matplotlib
        if MATPLOTLIB_AVAILABLE:
            self.matplotlib_plotter = MatplotlibPlotter(llm_client)

    def generate_plot(
        self,
        question: str,
        answer_content: str,
        visualization_type: str,
        preferred_method: Optional[PlotMethod] = None
    ) -> PlotResult:
        """
        生成绘图

        Args:
            question: 题目内容
            answer_content: 答案内容
            visualization_type: 可视化类型
            preferred_method: 首选方法（可选，自动选择）

        Returns:
            PlotResult: 绘图结果
        """
        # 选择绘图方法
        if preferred_method is None:
            preferred_method = self.selector.select_method(
                question,
                visualization_type,
                answer_content
            )

        # 根据方法生成图像
        if preferred_method == PlotMethod.GPT_IMAGE:
            if self.openai_image_plotter:
                result = self.openai_image_plotter.generate(question, answer_content, visualization_type)
                # 如果GPT Image 2失败，fallback到Matplotlib
                if not result.success and self.matplotlib_plotter:
                    result = self.matplotlib_plotter.generate(question, answer_content, visualization_type)
            elif self.matplotlib_plotter:
                result = self.matplotlib_plotter.generate(question, answer_content, visualization_type)
            else:
                result = PlotResult(
                    method=PlotMethod.NONE,
                    image_data=None,
                    image_url=None,
                    code=None,
                    error="没有可用的绘图方法",
                    success=False
                )

        elif preferred_method == PlotMethod.MATPLOTLIB and self.matplotlib_plotter:
            result = self.matplotlib_plotter.generate(question, answer_content, visualization_type)

        else:
            # 无可用的绘图方法
            result = PlotResult(
                method=PlotMethod.NONE,
                image_data=None,
                image_url=None,
                code=None,
                error="没有可用的绘图方法",
                success=False
            )

        return result


# 便捷函数
def create_plot_generator(
    llm_client,
    openai_api_key: Optional[str] = None,
    openai_base_url: Optional[str] = None,
) -> PlotGenerator:
    """
    创建绘图生成器

    Args:
        llm_client: LLM客户端
        openai_api_key: OpenAI API密钥
        openai_base_url: OpenAI API基础地址

    Returns:
        PlotGenerator: 绘图生成器实例
    """
    return PlotGenerator(llm_client, openai_api_key, openai_base_url)
