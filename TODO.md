# Math Tutor 项目待办与进度

## 项目概述
数学解题智能体 - 提供3种解题模式的AI辅助工具

## 里程碑进度

### Milestone 1: 纯算法逻辑实现 ✅ (已完成)
- [x] 实现核心解题逻辑
- [x] 集成LLM API调用
- [x] 实现3种模式：
  - [x] 思路提示模式
  - [x] 简略完整答题思路模式
  - [x] 详细知识点详解模式

### Milestone 2: 绘图辅助功能 ✅ (已完成)
- [x] 判断是否需要绘图的逻辑
- [x] 预留绘图接口（GPT Image 或 matplotlib）
- [x] 识别6种可视化类型（几何、函数、坐标、统计、数轴、向量）
- [x] 与解题器集成

### Milestone 3: 前端界面 📋
- [ ] TypeScript + TailwindCSS 实现
- [ ] 用户交互界面设计

### Milestone 4: 后端集成 📋
- [ ] Python 后端接口
- [ ] 支持文字输入
- [ ] 支持图片输入

## 待明确问题

### LLM选择
- [ ] 使用哪个LLM API？（OpenAI GPT-4, Claude, 国内大模型等）
- [ ] API密钥配置方式
- [ ] 调用参数配置（temperature, max_tokens等）

### 数据格式
- [ ] 数学题目的输入格式（纯文本、LaTeX、MathML？）
- [ ] 输出格式的具体要求

### 3种模式的详细定义
- [x] 思路提示：2-3个关键提示点，不直接给出完整解答
- [x] 简略思路：300字以内，包含完整步骤但简明扼要
- [x] 详细详解：详细讲解每步，总结知识点，指出易错点

### 绘图需求
- [ ] 哪些题型需要绘图？（几何、函数图像、统计图表等）
- [ ] 绘图工具的优先级选择

## 开发日志

### 2026-06-06
- 项目启动
- 创建基础文档结构
- **Milestone 1 完成**：
  - 实现了核心解题逻辑 (`src/core/solver.py`)
  - 创建了LLM客户端抽象层 (`src/core/llm_client.py`)
    - 支持OpenAI、Anthropic、Mock三种客户端
    - 使用工厂模式创建客户端
  - 实现了三种解题模式的Prompt模板
  - 创建了测试套件 (`tests/test_solver.py`)
  - 创建了演示程序 (`demo.py`, `example.py`)
  - 所有测试通过 ✓
- **Milestone 2 完成**：
  - 实现了可视化判断模块 (`src/core/visualization.py`)
    - 基于关键词匹配的智能判断算法
    - 支持6种可视化类型识别
    - 提供判断提示信息（类型、描述、关键词）
  - 集成到核心解题器中
  - 创建了可视化测试套件 (`tests/test_visualization.py`)
  - 创建了综合演示 (`milestone2_demo.py`)
  - 所有测试通过 (8/8) ✓
