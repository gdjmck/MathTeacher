# Milestone 5 实现总结

## 完成时间
2026-06-06

## 实现内容

### 目标
生成绘图功能，支持两种技术路线并由agent自动选择：
1. **GPT Image 2** - 适合概念性、示意性图示
2. **Matplotlib代码生成** - 适合精确的数学图形

### 核心模块

#### 1. `src/core/plot_generator.py` - 绘图生成模块

**PlotMethod枚举** - 绘图方法
- `GPT_IMAGE` - OpenAI GPT Image 2图像生成
- `MATPLOTLIB` - Matplotlib代码生成执行
- `NONE` - 不生成图像

**PlotMethodSelector类** - 智能方法选择器
```python
def select_method(question, visualization_type, answer_content) -> PlotMethod
```

**选择逻辑**:
- 检查关键词（概念性 vs 精确数学）
- 根据可视化类型决策
- 函数图像、坐标、统计 → Matplotlib
- 几何示意图 → GPT Image 2
- 默认使用Matplotlib（更可靠）

**OpenAIImagePlotter类** - GPT Image 2绘图器
- 使用OpenAI图像生成API生成图像
- 构建专业的数学图像提示
- 返回图像Base64数据或URL

**MatplotlibPlotter类** - Matplotlib绘图器
- 使用LLM生成matplotlib代码
- 执行代码生成图像
- 返回Base64编码的PNG图像

**PlotGenerator类** - 统一接口
```python
def generate_plot(
    question, 
    answer_content, 
    visualization_type,
    preferred_method=None
) -> PlotResult
```
- 自动选择方法
- Fallback机制（GPT Image 2失败→Matplotlib）
- 统一的PlotResult返回

### 技术实现

#### 智能方法选择
**关键词匹配**:
```python
GPT_IMAGE_KEYWORDS = ['示意图', '概念图', '流程图', ...]
MATPLOTLIB_KEYWORDS = ['函数', '图像', '坐标', '统计', ...]
```

**类型判断**:
- `function_graph`, `coordinate`, `statistics` → Matplotlib
- `geometry` + 数值 → Matplotlib
- `geometry` 无数值 → GPT Image 2

#### Matplotlib代码生成流程
1. LLM生成完整的Python代码
2. 提取代码块（支持markdown格式）
3. 在隔离的命名空间中执行
4. 保存为PNG并Base64编码
5. 清理matplotlib资源

#### GPT Image 2图像生成流程
1. 构建专业的图像生成提示
2. 调用OpenAI Images API
3. 返回图像URL
4. 错误处理和重试

### 后端集成

#### 配置更新 (`config.py`)
```python
enable_plot_generation: bool = True  # 启用绘图
```

#### 服务层更新 (`services.py`)
```python
class SolverService:
    def __init__(...):
        self.plot_generator = PlotGenerator(llm_client, openai_api_key, openai_base_url)
    
    def solve(..., generate_plot=False):
        # 如果需要可视化且启用绘图
        if generate_plot and hint.needed:
            plot_result = self.plot_generator.generate_plot(...)
```

#### API更新 (`app.py`, `schemas.py`)
**请求参数**:
- `generate_plot: bool` - 是否生成绘图

**响应字段**:
```python
class PlotResponse:
    success: bool
    method: str  # "gpt_image2" | "matplotlib" | "none"
    image_data: Optional[str]  # Base64 PNG
    image_url: Optional[str]   # OpenAI图像URL
    code: Optional[str]        # Matplotlib代码
    error: Optional[str]
```

**健康检查**:
```python
class HealthResponse:
    plot_enabled: bool  # 绘图功能状态
```

### 测试实现

#### `tests/test_plot_generator.py`

**测试覆盖**:
1. ✅ 方法选择器测试（4/4通过）
   - 函数图像 → Matplotlib
   - 坐标点 → Matplotlib
   - 几何示意图 → GPT Image 2
   - 带数值几何 → Matplotlib

2. ✅ Matplotlib代码生成测试
   - LLM生成代码
   - 代码执行
   - 图像Base64编码

3. ✅ PlotGenerator集成测试
   - 自动方法选择
   - 图像生成
   - 结果返回

4. ✅ Fallback机制测试
   - GPT Image 2不可用时降级
   - 错误处理

## 技术特点

### 1. 智能技术路线选择
- 基于问题内容和类型
- 关键词匹配算法
- 可靠的默认策略

### 2. Fallback机制
```
首选GPT Image 2 → 失败 → 降级到Matplotlib
首选Matplotlib → 失败 → 返回错误
```

### 3. 代码隔离执行
- 安全的命名空间
- 资源自动清理
- 异常捕获处理

### 4. 灵活的配置
- 环境变量控制
- 可选功能
- 失败不影响核心

## 使用示例

### Python代码
```python
from src.core import PlotGenerator, create_llm_client

llm_client = create_llm_client("openai")
generator = PlotGenerator(llm_client, openai_api_key)

result = generator.generate_plot(
    question="画出函数 y=x^2 的图像",
    answer_content="这是一个抛物线",
    visualization_type="function_graph"
)

if result.success:
    print(f"方法: {result.method}")
    if result.image_data:
        # Base64解码并保存
        save_image(result.image_data)
    if result.image_url:
        # 显示URL
        display_url(result.image_url)
```

### API调用
```bash
# 文本解题 + 绘图
curl -X POST http://127.0.0.1:8000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "question": "画出函数 y=sin(x) 的图像",
    "mode": "brief",
    "generate_plot": true
  }'
```

### 响应示例
```json
{
  "mode": "brief",
  "content": "...",
  "needs_visualization": true,
  "plot": {
    "success": true,
    "method": "matplotlib",
    "image_data": "iVBORw0KGgoAAAANS...",
    "code": "import matplotlib.pyplot as plt..."
  }
}
```

## 环境配置

### 依赖安装
```bash
# Matplotlib支持
pip install matplotlib numpy

# GPT Image 2支持（复用LLM的OpenAI配置）
# 使用相同的OPENAI_API_KEY和OPENAI_BASE_URL
```

### 环境变量
```bash
# 启用绘图功能
ENABLE_PLOT_GENERATION=true

# OpenAI配置（用于LLM和GPT Image 2）
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_PROVIDER=openai
```

## 与PRD的对应

**PRD要求**: 
> 生成绘图增加gpt image2和llm通过matplotlib实现生图2种方式，并由agent根据问题进行技术路线选择；其中gpt image2使用llm相同的openai配置

**实现情况**:
- ✅ 支持GPT Image 2绘图
- ✅ 支持Matplotlib代码生成绘图
- ✅ Agent自动选择技术路线
- ✅ GPT Image 2使用相同的OpenAI API Key和Base URL配置
- ✅ 智能Fallback机制
- ✅ 完整的测试覆盖

## 项目文件

```
src/core/
└── plot_generator.py      # 绘图模块 (400+行)

tests/
└── test_plot_generator.py # 测试 (200+行)
```

## 测试结果

```bash
$ python tests/test_plot_generator.py

方法选择器: 4/4 通过
Matplotlib生成: ✓ 成功
PlotGenerator: ✓ 成功
Fallback机制: ✓ 正常
```

## 总结

Milestone 5圆满完成！

**关键成就**:
- ✅ 两种绘图方式完整实现
- ✅ 智能技术路线选择
- ✅ Fallback降级机制
- ✅ 后端API完全集成
- ✅ 完整的测试覆盖

**技术亮点**:
- 智能的方法选择算法
- 安全的代码执行环境
- 灵活的配置和降级
- 统一的接口设计

Math Tutor现在具备完整的可视化能力！🎨
