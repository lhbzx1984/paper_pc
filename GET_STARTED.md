# 🚀 开始使用

欢迎使用毕业论文智能评审系统！这是一个快速指南，帮助你在5分钟内启动系统。

## 📖 第一次使用？

### 步骤 1: 安装依赖

**Windows用户（推荐）**
```bash
双击运行 install.bat
```

**手动安装**
```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 步骤 2: 配置API

编辑 `backend/config.yaml`：
```yaml
llm:
  api_key: "你的API-Key"  # ⚠️ 必须修改
  base_url: "https://api.openai.com/v1"
  model: "gpt-4"
```

💡 **提示**: 可以参考 `backend/config.example.yaml` 查看更多配置示例

### 步骤 3: 启动服务

**Windows用户**
1. 双击 `start_backend.bat` 启动后端
2. 双击 `start_frontend.bat` 启动前端

**Mac/Linux用户**
```bash
# 终端1
cd backend && python main.py

# 终端2
cd frontend && npm start
```

### 步骤 4: 开始使用

浏览器会自动打开 http://localhost:3000

1. 点击"系统配置"确认配置
2. 点击"论文评审"上传论文
3. 等待评审结果

## 🎯 快速链接

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目介绍和概述 |
| [QUICKSTART.md](QUICKSTART.md) | 详细的快速入门 |
| [USAGE.md](USAGE.md) | 完整使用指南 |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 部署说明 |
| [CHECKLIST.md](CHECKLIST.md) | 检查清单 |

## ❓ 遇到问题？

### 常见问题

**Q: 后端启动失败？**
```bash
# 检查Python版本
python --version  # 需要 3.9+

# 重新安装依赖
cd backend
pip install -r requirements.txt
```

**Q: 前端启动失败？**
```bash
# 检查Node版本
node --version  # 需要 16+

# 清理并重新安装
cd frontend
rm -rf node_modules
npm install
```

**Q: 评审失败？**
- 检查 API Key 是否正确
- 确认网络连接正常
- 查看后端控制台的错误信息

### 健康检查

运行健康检查脚本：
```bash
# Windows
health_check.bat

# Mac/Linux
cd backend && python health_check.py
```

## 📚 学习路径

### 初学者
1. ✅ 阅读 [README.md](README.md)
2. ✅ 按照本文档启动系统
3. ✅ 上传一篇测试论文
4. ✅ 查看 [USAGE.md](USAGE.md) 了解详细功能

### 进阶用户
1. ✅ 阅读 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
2. ✅ 自定义评审标准
3. ✅ 尝试不同的大模型
4. ✅ 优化评审参数

### 开发者
1. ✅ 阅读 [OVERVIEW.md](OVERVIEW.md)
2. ✅ 了解代码结构
3. ✅ 修改和扩展功能
4. ✅ 贡献代码

## 🎓 示例场景

### 场景1: 学生自查
```
1. 完成论文初稿
2. 上传到系统评审
3. 查看评分和建议
4. 根据建议修改
5. 重新评审对比
```

### 场景2: 教师批量评审
```
1. 配置评审标准
2. 逐个上传学生论文
3. 记录评审结果
4. 生成评审报告
5. 反馈给学生
```

### 场景3: 教务质量监控
```
1. 收集所有论文
2. 批量评审
3. 统计分析
4. 识别问题
5. 改进指导
```

## 💡 最佳实践

### 论文准备
- ✅ 使用标准格式
- ✅ 内容完整
- ✅ 转换为PDF（推荐）
- ✅ 文件大小 < 50MB

### 配置优化
- ✅ 开发测试用 gpt-3.5-turbo（快速、便宜）
- ✅ 正式评审用 gpt-4（准确、全面）
- ✅ temperature 设为 0.3（稳定输出）
- ✅ 根据需要调整权重

### 结果解读
- ✅ 重点关注低分项
- ✅ 仔细阅读改进建议
- ✅ 结合人工判断
- ✅ 多次评审对比

## 🔧 系统要求

### 最低配置
- CPU: 双核
- 内存: 4GB
- 硬盘: 10GB
- 网络: 稳定的互联网连接

### 推荐配置
- CPU: 四核或更高
- 内存: 8GB或更高
- 硬盘: 20GB或更高
- 网络: 高速互联网连接

## 📞 获取帮助

1. 查看文档目录中的相关文档
2. 运行健康检查脚本诊断问题
3. 查看后端和前端的错误日志
4. 搜索常见问题解答

## 🎉 开始你的第一次评审！

现在你已经准备好了，开始评审你的第一篇论文吧！

```bash
# 1. 启动后端
start_backend.bat

# 2. 启动前端
start_frontend.bat

# 3. 打开浏览器
http://localhost:3000

# 4. 上传论文，开始评审！
```

祝你使用愉快！ 🎓✨
