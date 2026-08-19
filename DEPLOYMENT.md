# 部署指南

## 环境要求

### 后端
- Python 3.9 或更高版本
- pip 包管理器

### 前端
- Node.js 16 或更高版本
- npm 或 yarn

## 安装步骤

### 1. 后端部署

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置大模型API
# 编辑 config.yaml 文件，填入你的API Key和配置
```

### 2. 前端部署

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 或使用 yarn
yarn install
```

## 配置说明

### 大模型配置 (backend/config.yaml)

```yaml
llm:
  api_key: "your-api-key-here"  # 替换为你的API Key
  base_url: "https://api.openai.com/v1"  # API地址
  model: "gpt-4"  # 模型名称
```

支持的大模型：
- OpenAI GPT-4 / GPT-3.5
- Azure OpenAI
- 其他兼容OpenAI API的模型（如通义千问、文心一言等）

### 评审标准配置

在 `config.yaml` 中可以自定义评审标准：
- 评审项名称
- 权重（总和为1）
- 满分
- 评审说明

## 启动服务

### Windows系统

双击运行：
- `start_backend.bat` - 启动后端
- `start_frontend.bat` - 启动前端

### Linux/Mac系统

```bash
# 启动后端
cd backend
python main.py

# 启动前端（新终端）
cd frontend
npm start
```

## 访问系统

- 前端地址: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 生产环境部署

### 后端

使用 gunicorn 或 uvicorn 部署：

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 前端

构建生产版本：

```bash
cd frontend
npm run build
```

使用 nginx 或其他 Web 服务器托管 `build` 目录。

## 常见问题

### 1. 文档解析失败
- 确保安装了 python-docx 和 PyPDF2
- 检查文件格式是否正确

### 2. 大模型调用失败
- 检查 API Key 是否正确
- 确认网络连接正常
- 查看 API 配额是否充足

### 3. 前端无法连接后端
- 确认后端服务已启动
- 检查端口是否被占用
- 查看 CORS 配置

## 安全建议

1. 不要将 API Key 提交到版本控制系统
2. 使用环境变量存储敏感信息
3. 在生产环境启用 HTTPS
4. 限制文件上传大小
5. 添加用户认证和授权机制
