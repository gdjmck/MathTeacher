"""
LLM客户端模块

支持多种LLM服务提供商的统一接口
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os

from openai import OpenAI


class BaseLLMClient(ABC):
    """LLM客户端基类"""

    @abstractmethod
    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """
        发送聊天请求

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            **kwargs: 其他参数

        Returns:
            str: LLM的回答
        """
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI API 客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        初始化OpenAI客户端

        Args:
            api_key: API密钥，如果为None则从环境变量读取
            base_url: API基础地址，如果为None则从环境变量读取
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        if not self.api_key:
            raise ValueError("需要提供OpenAI API密钥")

        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        self.client = OpenAI(**client_kwargs)

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """调用OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=kwargs.pop("temperature", self.temperature),
            max_tokens=kwargs.pop("max_tokens", self.max_tokens),
            **kwargs
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI 返回了空响应")

        return content


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude API 客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "claude-3-sonnet-20240229",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        初始化Anthropic客户端

        Args:
            api_key: API密钥，如果为None则从环境变量读取
            base_url: API基础地址，如果为None则从环境变量读取
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.getenv("ANTHROPIC_BASE_URL")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        if not self.api_key:
            raise ValueError("需要提供Anthropic API密钥")

        # TODO: 导入anthropic库
        # import anthropic
        # self.client = anthropic.Anthropic(
        #     api_key=self.api_key,
        #     base_url=self.base_url,
        # )

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """调用Anthropic API"""
        # TODO: 实现Anthropic API调用
        # response = self.client.messages.create(
        #     model=self.model,
        #     system=system_prompt,
        #     messages=[
        #         {"role": "user", "content": user_prompt}
        #     ],
        #     temperature=self.temperature,
        #     max_tokens=self.max_tokens,
        #     **kwargs
        # )
        # return response.content[0].text

        raise NotImplementedError("Anthropic客户端待实现")


class MockLLMClient(BaseLLMClient):
    """模拟LLM客户端，用于测试"""

    def __init__(self, mock_response: Optional[str] = None):
        """
        初始化模拟客户端

        Args:
            mock_response: 固定的模拟响应，如果为None则根据prompt生成
        """
        self.mock_response = mock_response

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """返回模拟响应"""
        if self.mock_response:
            return self.mock_response

        # 检查是否是matplotlib代码生成请求
        if "matplotlib" in user_prompt.lower() and "代码" in user_prompt:
            return """```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8, 6))

x = np.linspace(-5, 5, 100)
y = x**2

ax.plot(x, y, 'b-', linewidth=2, label='y = x^2')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Function Graph')
ax.legend()
```"""

        # 根据prompt类型返回不同的模拟响应（使用LaTeX格式）
        if "思路提示" in user_prompt:
            return """**解题思路提示：**

1. 观察题目的数学结构，识别问题类型
2. 回忆相关的公式和定理（如 $ax^2 + bx + c = 0$ 的求根公式）
3. 考虑是否可以通过代数变形简化问题"""

        elif "简洁完整" in user_prompt or "简略" in user_prompt:
            return """**解题步骤：**

1. **整理方程**：将方程整理为标准形式 $ax^2 + bx + c = 0$
2. **应用求根公式**：
   $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$
3. **代入计算**：代入系数值求解
4. **验证答案**：将解代入原方程验证

**答案**：$x = 5$"""

        elif "详细讲解" in user_prompt:
            return """**详细解题过程：**

**第一步：理解题意**
首先我们需要仔细阅读题目，提取关键信息。设未知数为 $x$。

**第二步：建立数学模型**
根据题目条件，我们可以列出方程：
$$2x + 5 = 15$$

这里使用的是代数方程的基本原理。

**第三步：求解过程**
移项得：
$$2x = 15 - 5$$
$$2x = 10$$

两边同时除以 $2$：
$$x = \\frac{10}{2} = 5$$

**第四步：验证答案**
将 $x = 5$ 代入原方程：
$$2 \\times 5 + 5 = 10 + 5 = 15$$ ✓

**知识点总结：**
1. 一元一次方程的求解方法
2. 移项法则：$a = b \\Rightarrow a + c = b + c$
3. 等式的性质：等式两边同时乘除同一个数（除数不为零）

**易错提醒：**
- 注意移项时要变号
- 注意运算顺序（先乘除后加减）
- 验证答案时要代入原方程，不是化简后的方程"""

        return "[模拟响应] 这是一个通用的数学问题解答。使用LaTeX格式：$x^2 + 1 = 0$"


def create_llm_client(
    provider: str = "mock",
    **kwargs
) -> BaseLLMClient:
    """
    工厂函数：创建LLM客户端

    Args:
        provider: 提供商名称 ("openai", "anthropic", "mock")
        **kwargs: 传递给客户端的参数

    Returns:
        BaseLLMClient: LLM客户端实例
    """
    if provider == "openai":
        return OpenAIClient(**kwargs)
    elif provider == "anthropic":
        return AnthropicClient(**kwargs)
    elif provider == "mock":
        return MockLLMClient(**kwargs)
    else:
        raise ValueError(f"不支持的LLM提供商: {provider}")
