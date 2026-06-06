# 数学公式格式化问题与解决方案

## 问题描述
LLM回复中的数学公式对用户不友好，纯文本格式（如 x^2 + 2x + 1）难以阅读，特别是复杂公式。

## 解决方案

### 方案1：LaTeX格式化（推荐）✅
**原理**：引导LLM使用LaTeX数学公式语法，在前端用渲染引擎显示

**优点**：
- LaTeX是数学排版的黄金标准
- 支持复杂公式、分数、根号、积分等
- 前端有成熟渲染库（MathJax、KaTeX）
- 即使在纯文本中，LaTeX也比纯文本清晰

**实现**：
1. 修改Prompt模板，要求LLM使用LaTeX格式
2. 使用标准标记：
   - 行内公式：`$...$` 或 `\\(...\\)`
   - 独立公式：`$$...$$` 或 `\\[...\\]`
3. 前端用MathJax或KaTeX渲染

**示例**：
```
纯文本：x^2 + 2x + 1 = 0
LaTeX：  $x^2 + 2x + 1 = 0$

纯文本：sqrt(x^2 + y^2)
LaTeX：  $\\sqrt{x^2 + y^2}$

纯文本：(a+b)/c
LaTeX：  $\\frac{a+b}{c}$
```

### 方案2：后处理转换
**原理**：识别纯文本公式，自动转换为LaTeX

**优点**：
- 不依赖LLM配合
- 可处理旧数据

**缺点**：
- 转换规则复杂，容易出错
- 无法处理所有情况
- 维护成本高

### 方案3：Unicode数学符号
**原理**：使用Unicode数学符号（如 ² ³ √ ∫ ∑）

**优点**：
- 无需渲染库
- 纯文本即可显示

**缺点**：
- 支持有限，复杂公式仍难以表达
- 输入不便

### 方案4：富文本格式（HTML）
**原理**：使用HTML标签（`<sup>`, `<sub>`, `<fraction>`等）

**优点**：
- 浏览器原生支持

**缺点**：
- 表达能力有限
- 不如LaTeX专业
- 混合HTML和文本内容复杂

## 推荐方案：LaTeX + 前端渲染

### 后端改进
1. 修改Prompt模板，明确要求LaTeX格式
2. 添加公式格式验证和提取工具
3. 提供纯文本降级方案

### 前端集成（Milestone 3）
```javascript
// 使用 KaTeX（更快）
import katex from 'katex';

// 或使用 MathJax（更完整）
import { MathJax } from 'mathjax3';

// 渲染公式
renderMath(text);
```

### 兼容性考虑
- 纯文本环境：LaTeX语法本身已比纯文本清晰
- Web环境：使用渲染库显示漂亮的公式
- 移动端：KaTeX更轻量，适合移动端

## 实施计划
1. ✅ 更新Prompt模板
2. ✅ 创建公式格式化工具模块
3. ✅ 更新测试用例
4. 📋 Milestone 3前端集成渲染库

## 相关资源
- LaTeX数学公式语法：https://katex.org/docs/supported.html
- KaTeX：https://katex.org/
- MathJax：https://www.mathjax.org/
