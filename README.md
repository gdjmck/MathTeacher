# Math Tutor - 数学解题智能体

## 项目简介

Math Tutor 是一个面向学生的数学解题辅助工具。用户可以输入题目或上传题目图片，系统会根据选择的讲解模式生成答案，并在需要时自动生成辅助图形，帮助理解题目结构和关键步骤。

当前系统已完成前端、后端、核心解题流程、图片输入、可视化判断和生图结果渲染的初版闭环。

## 当前功能

### 解题模式

1. **思路提示**：给出关键切入点，引导学生自主思考。
2. **简略思路**：提供完整但简洁的解题步骤。
3. **详细详解**：逐步解释推理过程，并总结相关知识点。

### 输入方式

- 文本输入数学题目。
- 上传图片或文本文件，由后端提取题目内容后解答。

### 可视化与生图

- 后端会根据题目和答案自动判断是否需要图形辅助。
- 需要图形时，系统自动选择合适的生图方式。
- 支持两类生图路线：
  - **GPT Image 2**：适合概念图、示意图等表达型图形。
  - **Matplotlib + LLM 代码生成**：适合函数图像、坐标系、统计图等精确数学图形。
- 前端已接入生图结果渲染，可展示后端返回的图片。

### 前端体验

- React + TypeScript + TailwindCSS 实现。
- 支持公式渲染。
- 生成答案时使用深色状态，完成后切换为米白色结果状态，帮助用户区分系统状态。
- 界面已减少内部技术术语，突出输入、讲解和辅助图。

## 技术栈

- **核心逻辑**: Python
- **后端服务**: FastAPI
- **前端界面**: React + TypeScript + TailwindCSS
- **公式渲染**: KaTeX
- **LLM**: OpenAI / Mock
- **图片理解**: OpenAI / Tesseract
- **生图**: GPT Image 2 / Matplotlib
- **测试**: pytest + FastAPI TestClient

## 项目结构

```text
MathTeacher/
├── rpd                 # 产品需求文档
├── README.md           # 项目说明
├── TODO.md             # 进度记录
├── docs/               # Milestone 与实现文档
├── src/
│   ├── core/           # 解题、可视化判断、生图核心逻辑
│   ├── backend/        # FastAPI 后端接口
│   └── frontend/       # React 前端应用
└── tests/              # 后端与核心功能测试
```

## 快速开始

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

如需使用 Matplotlib 生图，请确保环境中安装：

```bash
pip install matplotlib numpy
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

常用配置：

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
ENABLE_PLOT_GENERATION=true
```

如果不配置真实模型，系统可以使用 `mock` 模式进行本地流程验证。

### 3. 启动后端

```bash
uvicorn src.backend.app:app --reload
```

默认地址：`http://127.0.0.1:8000`

健康检查：`http://127.0.0.1:8000/api/health`

### 4. 启动前端

```bash
cd src/frontend
npm install
npm run dev
```

默认地址：`http://localhost:5173`

## API 概览

### 文本解题

```http
POST /api/solve
```

请求示例：

```json
{
  "question": "画出函数 y=x^2 的图像，并说明顶点和开口方向。",
  "mode": "brief",
  "generate_plot": true
}
```

### 图片解题

```http
POST /api/solve/image
```

使用 `multipart/form-data` 上传文件，并可传入：

- `mode`: `hint` / `brief` / `detailed`
- `generate_plot`: `true` / `false`

## 测试

运行后端与生图相关测试：

```bash
python -m pytest tests/test_plot_generator.py tests/test_backend_api.py
```

运行前端构建检查：

```bash
cd src/frontend
npm run build
```

## 项目进度

- ✅ **Milestone 1**: 核心解题逻辑 - [查看详情](./docs/MILESTONE1.md)
- ✅ **Milestone 2**: 可视化判断 - [查看详情](./docs/MILESTONE2.md)
- ✅ **Milestone 3**: 前端界面 - [查看详情](./docs/MILESTONE3.md)
- ✅ **Milestone 4**: 后端接口与图片输入 - [查看详情](./docs/MILESTONE4.md)
- ✅ **Milestone 5**: 绘图生成功能 - [查看详情](./docs/MILESTONE5.md)

## 当前状态

系统功能初版已完成，当前重点从功能闭环进入体验优化阶段，包括界面排版、状态感知、文案精简和生图结果展示优化。
