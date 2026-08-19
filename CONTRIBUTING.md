# 贡献指南

感谢你对本项目的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告问题 (Bug Report)

如果你发现了bug，请创建一个Issue，包含：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（操作系统、Python版本、Node版本等）
- 截图或日志（如果有）

### 功能建议 (Feature Request)

如果你有新功能的想法，请创建一个Issue，包含：
- 功能描述
- 使用场景
- 预期效果
- 可能的实现方案

### 提交代码 (Pull Request)

1. Fork本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📝 代码规范

### Python代码规范

遵循PEP 8规范：
```python
# 好的示例
def evaluate_paper(text: str) -> Dict[str, Any]:
    """评审论文
    
    Args:
        text: 论文文本内容
        
    Returns:
        评审结果字典
    """
    result = process_text(text)
    return result

# 避免
def eval(t):
    r=process(t)
    return r
```

### TypeScript代码规范

```typescript
// 好的示例
interface EvaluationResult {
  totalScore: number;
  grade: string;
}

const evaluatePaper = async (file: File): Promise<EvaluationResult> => {
  const result = await uploadFile(file);
  return result;
};

// 避免
const eval = async (f: any) => {
  return await upload(f);
};
```

### 命名规范

- **文件名**: 小写字母，下划线分隔 (`document_parser.py`)
- **类名**: 大驼峰 (`DocumentParser`)
- **函数名**: 小写字母，下划线分隔 (`parse_document`)
- **变量名**: 小写字母，下划线分隔 (`total_score`)
- **常量名**: 大写字母，下划线分隔 (`MAX_FILE_SIZE`)

## 🧪 测试

### 运行测试

```bash
# 后端测试
cd backend
python test_api.py

# 健康检查
python health_check.py
```

### 添加测试

为新功能添加测试：
```python
def test_new_feature():
    """测试新功能"""
    result = new_feature()
    assert result is not None
    assert result.status == "success"
```

## 📚 文档

### 更新文档

如果你的修改影响了用户使用，请更新相应文档：
- README.md - 项目介绍
- USAGE.md - 使用说明
- DEPLOYMENT.md - 部署说明
- 其他相关文档

### 文档规范

- 使用清晰的标题层级
- 提供代码示例
- 包含截图（如果需要）
- 保持简洁明了

## 🎨 提交信息规范

使用语义化的提交信息：

```
feat: 添加批量评审功能
fix: 修复PDF解析错误
docs: 更新使用文档
style: 格式化代码
refactor: 重构评审逻辑
test: 添加单元测试
chore: 更新依赖包
```

## 🔍 代码审查

Pull Request会经过以下审查：
- [ ] 代码符合规范
- [ ] 功能正常工作
- [ ] 测试通过
- [ ] 文档已更新
- [ ] 无安全问题
- [ ] 性能可接受

## 🌟 贡献者

感谢所有贡献者！

## 📞 联系方式

如有问题，可以通过以下方式联系：
- 创建Issue
- 发送邮件
- 加入讨论组

## 📜 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们承诺：
- 尊重不同的观点和经验
- 接受建设性的批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性暗示的语言或图像
- 人身攻击或侮辱性评论
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他不道德或不专业的行为

## 🎯 优先级

我们特别欢迎以下方面的贡献：

### 高优先级
- [ ] Bug修复
- [ ] 性能优化
- [ ] 安全改进
- [ ] 文档完善

### 中优先级
- [ ] 新功能开发
- [ ] UI/UX改进
- [ ] 测试覆盖
- [ ] 代码重构

### 低优先级
- [ ] 代码风格调整
- [ ] 注释补充
- [ ] 示例添加

## 💡 开发建议

### 环境搭建

1. 安装依赖
```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

2. 配置开发环境
```bash
# 复制配置文件
cp backend/config.example.yaml backend/config.yaml
# 编辑配置文件
```

3. 启动开发服务
```bash
# 后端
cd backend
python main.py

# 前端
cd frontend
npm start
```

### 调试技巧

**后端调试**
```python
# 添加日志
import logging
logging.info(f"Processing: {variable}")

# 使用断点
import pdb; pdb.set_trace()
```

**前端调试**
```typescript
// 使用console
console.log('Debug:', variable);

// 使用React DevTools
// Chrome扩展：React Developer Tools
```

### 常见问题

**Q: 如何添加新的评审维度？**
A: 修改 `backend/config.yaml` 中的 `evaluation.criteria`

**Q: 如何支持新的文档格式？**
A: 在 `backend/services/document_parser.py` 中添加解析方法

**Q: 如何更换UI组件？**
A: 修改 `frontend/src/components/` 中的相应组件

## 🚀 发布流程

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建Git标签
4. 构建发布包
5. 发布到仓库

## 📊 项目统计

- 总代码行数: ~3000行
- 后端代码: ~1500行
- 前端代码: ~1500行
- 文档: ~5000行

## 🎓 学习资源

### 推荐阅读
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [React文档](https://react.dev/)
- [LangChain文档](https://python.langchain.com/)
- [Ant Design文档](https://ant.design/)

### 相关项目
- LangChain
- ChromaDB
- OpenAI API

## 🙏 致谢

感谢以下开源项目：
- FastAPI
- React
- LangChain
- Ant Design
- 以及所有依赖的库

---

再次感谢你的贡献！让我们一起让这个项目变得更好！ 🎉
