# 毕业论文智能评审系统

基于大模型和RAG技术的高校本科毕业设计论文评审系统

## 📋 项目简介

本系统是一个智能化的毕业论文评审工具，利用大语言模型（LLM）和检索增强生成（RAG）技术，对本科毕业论文进行多维度、智能化的评审和评分。系统可以自动分析论文内容，给出详细的评分和改进建议，大大提高评审效率。

## ✨ 功能特性

- 📄 **多格式支持**：支持Word (.doc, .docx)、WPS (.wps)、PDF格式论文上传
- 🎯 **多维度评审**：从选题、文献、方法、结构、内容、规范等6个维度评审
- 🤖 **智能评分**：基于大模型的智能评分系统
- 💡 **详细反馈**：提供每个维度的详细评价和改进建议
- ⚙️ **灵活配置**：支持自定义评审标准和权重
- 🔌 **API兼容**：支持OpenAI及兼容接口的各类大模型
- 🎨 **友好界面**：基于Ant Design的现代化UI

## 🛠 技术栈

### 后端
- **FastAPI** - 高性能Web框架
- **LangChain** - LLM应用开发框架
- **ChromaDB** - 向量数据库
- **python-docx** - Word文档处理
- **PyPDF2** - PDF文档处理
- **OpenAI** - 大模型API客户端

### 前端
- **React 18** - UI框架
- **TypeScript** - 类型安全
- **Ant Design** - 企业级UI组件库
- **Axios** - HTTP客户端

## 🚀 快速开始

### 三步启动系统

#### 1️⃣ 安装依赖
```bash
# Windows用户：双击运行
install.bat

# 或手动安装
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

#### 2️⃣ 配置API
编辑 `backend/config.yaml`，填入你的大模型API Key：
```yaml
llm:
  api_key: "你的API-Key"  # ⚠️ 必须修改
  base_url: "https://api.openai.com/v1"
  model: "gpt-4"
```

#### 3️⃣ 启动服务
```bash
# Windows用户：双击运行
start_backend.bat  # 启动后端
start_frontend.bat # 启动前端

# Mac/Linux用户
cd backend && python main.py      # 终端1
cd frontend && npm start          # 终端2
```

### 访问系统
- 🌐 前端界面：http://localhost:3000
- 🔧 后端API：http://localhost:8000
- 📖 API文档：http://localhost:8000/docs

> 💡 **第一次使用？** 查看 [GET_STARTED.md](GET_STARTED.md) 获取详细指导

## 📖 使用说明

### 1. 配置大模型
首次使用需要在"系统配置"页面配置大模型API：
- API Key：你的大模型访问密钥
- API Base URL：API服务地址
- 模型名称：使用的模型版本（如gpt-4）

### 2. 上传论文
在"论文评审"页面：
1. 拖拽或点击上传论文文件
2. 等待系统自动评审（1-3分钟）
3. 查看详细的评审结果

### 3. 查看结果
评审结果包括：
- 总分和等级
- 6个维度的详细评分
- 每个维度的评价和建议
- 总体评价和改进方向

## 📊 评审标准

系统默认包含6个评审维度：

| 维度 | 权重 | 说明 |
|------|------|------|
| 选题质量 | 15% | 选题的创新性、实用性和可行性 |
| 文献综述 | 15% | 文献调研的全面性和深度 |
| 研究方法 | 20% | 研究方法的科学性和合理性 |
| 论文结构 | 15% | 论文结构的完整性和逻辑性 |
| 内容质量 | 25% | 论文内容的深度和创新性 |
| 写作规范 | 10% | 格式规范、语言表达和引用规范 |

评分等级：
- 90-100分：优秀
- 80-89分：良好
- 70-79分：中等
- 60-69分：及格
- 0-59分：不及格

## 🐳 Docker部署

使用Docker Compose一键部署：

```bash
docker-compose up -d
```

访问 http://localhost 即可使用系统。

## 📚 文档

| 文档 | 说明 |
|------|------|
| [GET_STARTED.md](GET_STARTED.md) | 🚀 新手必读 - 快速开始指南 |
| [QUICKSTART.md](QUICKSTART.md) | ⚡ 5分钟快速上手教程 |
| [USAGE.md](USAGE.md) | 📖 完整的使用指南 |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 🐳 生产环境部署说明 |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 🏗️ 项目代码结构 |
| [OVERVIEW.md](OVERVIEW.md) | 🎯 项目总览和架构 |
| [CHECKLIST.md](CHECKLIST.md) | ✅ 完整检查清单 |
| [CHANGELOG.md](CHANGELOG.md) | 📝 版本更新日志 |

## 🔧 配置说明

编辑 `backend/config.yaml` 自定义评审标准：

```yaml
evaluation:
  criteria:
    - name: "评审项名称"
      weight: 0.20        # 权重（总和为1）
      max_score: 100      # 满分
      description: "评审说明"
```

## 🤝 支持的大模型

- OpenAI (GPT-4, GPT-3.5)
- Azure OpenAI
- 通义千问
- 文心一言
- 智谱AI
- 讯飞星火
- 其他兼容OpenAI API的模型

## ⚠️ 注意事项

1. 评审结果仅供参考，不能完全替代人工评审
2. 请妥善保管API Key，不要泄露
3. 注意API调用费用
4. 建议论文格式规范，以获得更准确的评审结果

## 📝 许可证

MIT License

## 🙏 致谢

感谢所有开源项目的贡献者
