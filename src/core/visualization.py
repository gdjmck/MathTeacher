"""
可视化判断与绘图模块

用于判断数学问题是否需要图形辅助理解，并提供绘图接口
"""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass


class VisualizationType(Enum):
    """可视化类型枚举"""
    NONE = "none"                      # 不需要可视化
    GEOMETRY = "geometry"              # 几何图形
    FUNCTION_GRAPH = "function_graph"  # 函数图像
    COORDINATE = "coordinate"          # 坐标系
    STATISTICS = "statistics"          # 统计图表
    NUMBER_LINE = "number_line"        # 数轴
    VECTOR = "vector"                  # 向量图


@dataclass
class VisualizationHint:
    """可视化提示信息"""
    needed: bool                           # 是否需要可视化
    viz_type: VisualizationType           # 可视化类型
    description: str                       # 描述
    keywords: List[str]                    # 识别的关键词


class VisualizationJudge:
    """可视化判断器"""

    # 关键词映射表
    KEYWORD_PATTERNS = {
        VisualizationType.GEOMETRY: [
            '三角形', '正方形', '长方形', '圆', '椭圆', '多边形',
            '角度', '面积', '周长', '体积', '表面积',
            '平行', '垂直', '相交', '切线', '弦',
            '几何', '图形', '作图', '画出',
            'triangle', 'square', 'rectangle', 'circle', 'polygon',
            'angle', 'area', 'perimeter', 'volume'
        ],
        VisualizationType.FUNCTION_GRAPH: [
            '函数', '图像', '曲线', '抛物线', '双曲线',
            '极值', '单调', '增减', '对称', '渐近线',
            '导数', '切线', '斜率', '交点',
            'y=', 'f(x)', 'g(x)', 'h(x)',
            'function', 'graph', 'curve', 'parabola', 'slope'
        ],
        VisualizationType.COORDINATE: [
            '坐标', '点', '直线', '平面', '向量',
            '坐标系', '象限', 'x轴', 'y轴', 'z轴',
            '原点', '距离', '中点',
            'coordinate', 'point', 'axis', 'origin'
        ],
        VisualizationType.STATISTICS: [
            '统计', '数据', '频率', '概率', '分布',
            '柱状图', '折线图', '饼图', '散点图',
            '平均', '方差', '标准差', '中位数',
            'statistics', 'data', 'frequency', 'probability',
            'histogram', 'chart', 'mean', 'median'
        ],
        VisualizationType.NUMBER_LINE: [
            '数轴', '不等式', '区间', '绝对值',
            '大于', '小于', '范围',
            'number line', 'inequality', 'interval', 'range'
        ],
        VisualizationType.VECTOR: [
            '向量', '方向', '模', '夹角',
            '向量和', '向量差', '数量积', '向量积',
            'vector', 'direction', 'magnitude', 'dot product'
        ],
    }

    def judge(
        self,
        question: str,
        answer_content: Optional[str] = None
    ) -> VisualizationHint:
        """
        判断是否需要可视化

        Args:
            question: 题目内容
            answer_content: 答案内容（可选，用于更准确的判断）

        Returns:
            VisualizationHint: 可视化提示信息
        """
        # 组合题目和答案内容
        text_to_analyze = question.lower()
        if answer_content:
            text_to_analyze += " " + answer_content.lower()

        # 检查每种类型的关键词
        matched_types = {}
        for viz_type, keywords in self.KEYWORD_PATTERNS.items():
            matched_keywords = [
                kw for kw in keywords
                if kw.lower() in text_to_analyze
            ]
            if matched_keywords:
                matched_types[viz_type] = matched_keywords

        # 如果没有匹配，返回不需要可视化
        if not matched_types:
            return VisualizationHint(
                needed=False,
                viz_type=VisualizationType.NONE,
                description="该题目不需要图形辅助",
                keywords=[]
            )

        # 选择匹配度最高的类型（匹配关键词最多的）
        best_type = max(matched_types.items(), key=lambda x: len(x[1]))
        viz_type, keywords = best_type

        # 生成描述
        descriptions = {
            VisualizationType.GEOMETRY: "建议绘制几何图形辅助理解",
            VisualizationType.FUNCTION_GRAPH: "建议绘制函数图像",
            VisualizationType.COORDINATE: "建议绘制坐标系图",
            VisualizationType.STATISTICS: "建议绘制统计图表",
            VisualizationType.NUMBER_LINE: "建议绘制数轴",
            VisualizationType.VECTOR: "建议绘制向量图",
        }

        return VisualizationHint(
            needed=True,
            viz_type=viz_type,
            description=descriptions[viz_type],
            keywords=keywords
        )

    def should_visualize(self, question: str, answer_content: Optional[str] = None) -> bool:
        """
        简化的判断方法，只返回是否需要可视化

        Args:
            question: 题目内容
            answer_content: 答案内容（可选）

        Returns:
            bool: 是否需要可视化
        """
        hint = self.judge(question, answer_content)
        return hint.needed


class VisualizationPlaceholder:
    """
    可视化占位类

    预留绘图接口，实际绘图功能待实现
    支持 matplotlib 或 GPT Image 两种方式
    """

    def __init__(self, backend: str = "matplotlib"):
        """
        初始化可视化器

        Args:
            backend: 绘图后端 ("matplotlib" 或 "gpt_image")
        """
        self.backend = backend

    def plot(
        self,
        viz_type: VisualizationType,
        data: dict,
        **kwargs
    ) -> str:
        """
        绘图接口（占位）

        Args:
            viz_type: 可视化类型
            data: 绘图数据
            **kwargs: 其他参数

        Returns:
            str: 图像路径或URL
        """
        # TODO: 实现实际的绘图逻辑
        return f"[占位] 使用 {self.backend} 绘制 {viz_type.value} 图"

    def plot_geometry(self, shapes: List[dict], **kwargs) -> str:
        """绘制几何图形（占位）"""
        return self.plot(VisualizationType.GEOMETRY, {"shapes": shapes}, **kwargs)

    def plot_function(self, functions: List[str], x_range: tuple, **kwargs) -> str:
        """绘制函数图像（占位）"""
        return self.plot(
            VisualizationType.FUNCTION_GRAPH,
            {"functions": functions, "x_range": x_range},
            **kwargs
        )

    def plot_coordinate(self, points: List[tuple], **kwargs) -> str:
        """绘制坐标图（占位）"""
        return self.plot(VisualizationType.COORDINATE, {"points": points}, **kwargs)

    def plot_statistics(self, data: dict, chart_type: str, **kwargs) -> str:
        """绘制统计图表（占位）"""
        return self.plot(
            VisualizationType.STATISTICS,
            {"data": data, "chart_type": chart_type},
            **kwargs
        )


# 便捷函数
def check_visualization_need(question: str, answer: Optional[str] = None) -> dict:
    """
    便捷函数：检查是否需要可视化

    Args:
        question: 题目内容
        answer: 答案内容

    Returns:
        dict: 可视化判断结果
    """
    judge = VisualizationJudge()
    hint = judge.judge(question, answer)

    return {
        "needed": hint.needed,
        "type": hint.viz_type.value,
        "description": hint.description,
        "keywords": hint.keywords
    }
