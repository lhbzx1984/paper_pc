# 快速入门指南

## 5分钟快速上手

### 第一步：安装依赖

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

如果安装速度慢，可以使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 前端依赖
```bash
cd frontend
npm install
```

如果安装速度慢，可以使用国内镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```

### 第二步：配置大模型API

编辑 `backend/config.yaml` 文件：

```yaml
llm:
  api_key: "sk-xxxxxxxxxxxxxxxx"  # 替换为你的API Key
  base_url: "https://api.openai.com/v1"  # 或其他兼容的API地址
  model: "gpt-4"  # 或 gpt-3.5-turbo
```

#### 常用大模型配置示例

**OpenAI**
```yaml
api_key: "sk-xxxxxxxxxxxxxxxx"
base_url: "https://api.openai.com/v1"
model: "gpt-4"
```

**通义千问（兼容OpenAI格式）**
```yaml
api_key: "sk-xxxxxxxxxxxxxxxx"
base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
model: "qwen-plus"
```

**智谱AI**
```yaml
api_key: "xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx"
base_url: "https://open.bigmodel.cn/api/paas/v4"
model: "glm-4"
```

### 第三步：启动服务

#### Windows用户
双击运行以下文件：
1. `start_backend.bat` - 启动后端（等待显示"Application startup complete"）
2. `start_frontend.bat` - 启动前端（会自动打开浏览器）

#### Mac/Linux用户

终端1（后端）：
```bash
cd backend
python main.py
```

终端2（前端）：
```bash
cd frontend
npm start
```

### 第四步：使用系统

1. 浏览器自动打开 http://localhost:3000
2. 点击"系统配置"标签，确认配置正确
3. 点击"论文评审"标签
4. 上传一篇论文（支持Word、PDF、WPS格式）
5. 等待1-3分钟，查看评审结果

## 常见问题

### Q1: 后端启动失败
**错误：ModuleNotFoundError**
- 解决：确保已安装所有依赖 `pip install -r requirements.txt`

**错误：端口8000被占用**
- 解决：修改 `backend/main.py` 最后一行的端口号

### Q2: 前端启动失败
**错误：npm install失败**
- 解决：删除 `node_modules` 文件夹，重新运行 `npm install`
- 或使用 `npm install --legacy-peer-deps`

**错误：端口3000被占用**
- 解决：系统会提示使用其他端口，输入 `y` 确认

### Q3: 上传论文后报错
**错误：大模型调用失败**
- 检查API Key是否正确
- 检查网络连接
- 确认API账户有余额

**错误：文档解析失败**
- 确保文件格式正确
- 尝试转换为PDF格式再上传
- 检查文件是否损坏

### Q4: 评审结果不理想
- 确保论文内容完整
- 检查论文格式是否规范
- 尝试使用更强大的模型（如GPT-4）
- 调整 `config.yaml` 中的 `temperature` 参数

## 测试API

运行测试脚本验证后端是否正常：

```bash
cd backend
python test_api.py
```

## 下一步

- 阅读 [使用指南](USAGE.md) 了解详细功能
- 阅读 [部署指南](DEPLOYMENT.md) 了解生产环境部署
- 自定义评审标准（修改 `config.yaml`）
- 查看 [项目结构](PROJECT_STRUCTURE.md) 了解代码组织

## 获取帮助

如果遇到问题：
1. 检查后端控制台的错误信息
2. 检查浏览器控制台（F12）的错误信息
3. 查看 `backend/config.yaml` 配置是否正确
4. 确认大模型API可以正常访问

## 性能优化建议

1. **使用更快的模型**：gpt-3.5-turbo 比 gpt-4 快很多
2. **减少文本长度**：只上传论文正文，去掉封面、目录等
3. **调整参数**：降低 `max_tokens` 可以加快响应速度
4. **本地部署**：使用本地大模型（如Ollama）可以避免网络延迟

## 成本控制

- GPT-4：约 $0.03-0.06 每篇论文
- GPT-3.5-turbo：约 $0.002-0.005 每篇论文
- 国内模型：通常更便宜，具体查看各平台定价

建议：
- 开发测试使用 GPT-3.5-turbo
- 正式评审使用 GPT-4
- 或使用国内模型降低成本
