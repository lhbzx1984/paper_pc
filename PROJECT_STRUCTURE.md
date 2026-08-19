# 项目结构说明

```
thesis-review-system/
│
├── backend/                          # 后端服务
│   ├── main.py                      # FastAPI主应用
│   ├── config.yaml                  # 配置文件
│   ├── requirements.txt             # Python依赖
│   └── services/                    # 业务逻辑层
│       ├── __init__.py
│       ├── document_parser.py       # 文档解析服务
│       ├── llm_client.py           # 大模型客户端
│       └── rag_evaluator.py        # RAG评审服务
│
├── frontend/                         # 前端应用
│   ├── public/                      # 静态资源
│   │   └── index.html
│   ├── src/                         # 源代码
│   │   ├── components/              # React组件
│   │   │   ├── UploadPage.tsx      # 上传页面
│   │   │   └── ConfigPage.tsx      # 配置页面
│   │   ├── App.tsx                 # 主应用组件
│   │   ├── App.css                 # 样式文件
│   │   ├── index.tsx               # 入口文件
│   │   └── index.css               # 全局样式
│   ├── package.json                 # 项目配置
│   └── tsconfig.json               # TypeScript配置
│
├── README.md                         # 项目说明
├── DEPLOYMENT.md                     # 部署指南
├── USAGE.md                         # 使用指南
├── PROJECT_STRUCTURE.md             # 项目结构说明
├── .gitignore                       # Git忽略文件
├── start_backend.bat                # Windows后端启动脚本
└── start_frontend.bat               # Windows前端启动脚本
```

## 核心模块说明

### 后端 (Backend)

#### main.py
- FastAPI应用入口
- API路由定义
- CORS配置
- 文件上传处理
- 配置管理

#### services/document_parser.py
- 支持多种文档格式解析
- Word文档解析 (python-docx)
- PDF文档解析 (PyPDF2)
- WPS文档解析

#### services/llm_client.py
- 大模型API调用封装
- 支持OpenAI兼容接口
- 对话生成
- 文本嵌入生成

#### services/rag_evaluator.py
- RAG评审核心逻辑
- 文本分块处理
- 多维度评分
- 评价生成
- 总分计算

#### config.yaml
- 大模型配置
- 评审标准定义
- 评分权重设置
- 等级划分标准

### 前端 (Frontend)

#### components/UploadPage.tsx
- 文件上传界面
- 拖拽上传支持
- 评审结果展示
- 进度提示

#### components/ConfigPage.tsx
- 系统配置界面
- API配置表单
- 当前配置展示
- 评审标准查看

#### App.tsx
- 主应用布局
- 标签页切换
- 路由管理

## 技术架构

### 后端技术栈
- **FastAPI**: 现代化的Python Web框架
- **LangChain**: LLM应用开发框架
- **ChromaDB**: 向量数据库（用于RAG）
- **python-docx**: Word文档处理
- **PyPDF2**: PDF文档处理
- **OpenAI**: 大模型API客户端

### 前端技术栈
- **React 18**: UI框架
- **TypeScript**: 类型安全
- **Ant Design**: UI组件库
- **Axios**: HTTP客户端

## 数据流程

1. **文档上传**
   ```
   用户 → 前端上传组件 → 后端API → 文档解析器 → 文本内容
   ```

2. **评审处理**
   ```
   文本内容 → RAG评审器 → 文本分块 → LLM评分 → 结果聚合
   ```

3. **结果展示**
   ```
   评审结果 → 后端API → 前端组件 → 用户界面
   ```

## API接口

### POST /api/upload
上传论文并评审
- 请求: multipart/form-data (file)
- 响应: 评审结果JSON

### GET /api/config
获取当前配置
- 响应: 配置信息JSON

### POST /api/config
更新系统配置
- 请求: 配置更新JSON
- 响应: 操作结果

## 扩展建议

### 功能扩展
1. 批量评审功能
2. 历史记录管理
3. 评审报告导出
4. 用户权限管理
5. 评审模板自定义

### 技术优化
1. 添加Redis缓存
2. 异步任务队列
3. 数据库持久化
4. 日志系统完善
5. 性能监控

### 部署优化
1. Docker容器化
2. Kubernetes编排
3. 负载均衡
4. CDN加速
5. 自动化CI/CD
