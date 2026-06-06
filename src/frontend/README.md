# Math Tutor Frontend

Milestone 3 的前端原型，使用 `React + TypeScript + TailwindCSS + KaTeX`。

## 当前能力

- 题目文本输入
- 三种解题模式切换
- LaTeX 公式渲染
- 可视化提示展示
- 图形区域占位

## 当前限制

- 依赖本地 Python 后端服务
- 图片题目识别质量取决于 OCR 配置
- 图形绘制仍是占位区域

## 对接后端

默认接口地址：`http://127.0.0.1:8000`

可通过环境变量覆盖：

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 启动方式

```bash
npm install
npm run dev
```

默认地址：`http://localhost:5173`
