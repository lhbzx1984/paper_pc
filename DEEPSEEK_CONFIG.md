# DeepSeek 配置指南

## 🚀 为什么选择 DeepSeek？

- ✅ **性价比高**：比 GPT-4 便宜很多
- ✅ **中文友好**：对中文支持非常好
- ✅ **速度快**：响应速度快
- ✅ **效果好**：评审质量优秀

## 📝 配置步骤

### 1. 获取 API Key

1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制 API Key（格式类似：`sk-xxxxxxxxxxxxxxxx`）

### 2. 修改配置文件

编辑 `backend/config.yaml`：

```yaml
llm:
  api_key: "sk-xxxxxxxxxxxxxxxx"  # 你的 DeepSeek API Key
  base_url: "https://api.deepseek.com"
  model: "deepseek-chat"
  temperature: 0.3
  max_tokens: 2000
```

### 3. 模型选择

DeepSeek 提供多个模型：

#### deepseek-chat（推荐）
- **用途**：通用对话和文本生成
- **适合**：论文评审、内容分析
- **价格**：¥1/百万tokens（输入），¥2/百万tokens（输出）

```yaml
model: "deepseek-chat"
```

#### deepseek-coder
- **用途**：代码相关任务
- **适合**：如果论文是计算机相关的技术论文
- **价格**：¥1/百万tokens（输入），¥2/百万tokens（输出）

```yaml
model: "deepseek-coder"
```

## 💰 成本估算

### 每篇论文评审成本

假设一篇论文约 10,000 字：

- **输入 tokens**：约 15,000 tokens
- **输出 tokens**：约 3,000 tokens
- **总成本**：约 ¥0.021（2分钱）

对比：
- DeepSeek：¥0.02/篇
- GPT-3.5-turbo：¥0.03/篇
- GPT-4：¥0.60/篇

**DeepSeek 比 GPT-4 便宜 30 倍！**

## 🔧 完整配置示例

```yaml
# 大模型配置
llm:
  api_key: "sk-xxxxxxxxxxxxxxxx"
  base_url: "https://api.deepseek.com"
  model: "deepseek-chat"
  temperature: 0.3  # 0-1，越低越稳定
  max_tokens: 2000  # 最大输出长度

# 评审标准配置（保持不变）
evaluation:
  criteria:
    - name: "选题质量"
      weight: 0.15
      max_score: 100
      description: "选题的创新性、实用性和可行性"
    # ... 其他标准
```

## ⚙️ 参数调优

### temperature（温度）
- **0.1-0.3**：更稳定、一致（推荐用于评审）
- **0.5-0.7**：平衡创造性和稳定性
- **0.8-1.0**：更有创造性，但可能不稳定

### max_tokens（最大输出长度）
- **1500**：简短评价
- **2000**：标准评价（推荐）
- **3000**：详细评价

## 🧪 测试配置

配置完成后，测试是否正常：

```bash
cd backend
python test_api.py
```

或运行健康检查：

```bash
.\health_check.bat
```

## 🔍 常见问题

### Q: API Key 无效？
A: 
1. 检查 API Key 是否正确复制
2. 确认 API Key 是否已激活
3. 检查账户余额是否充足

### Q: 连接超时？
A: 
1. 检查网络连接
2. 确认 base_url 是否正确
3. 尝试使用代理

### Q: 评审质量不理想？
A: 
1. 调整 temperature 参数（降低到 0.2）
2. 增加 max_tokens（提高到 2500）
3. 优化评审标准描述

### Q: 如何切换回 OpenAI？
A: 修改配置：
```yaml
llm:
  api_key: "sk-xxxxxxxxxxxxxxxx"
  base_url: "https://api.openai.com/v1"
  model: "gpt-4"
```

## 📊 性能对比

| 指标 | DeepSeek | GPT-3.5 | GPT-4 |
|------|----------|---------|-------|
| 中文理解 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 评审质量 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 响应速度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 性价比 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 成本/篇 | ¥0.02 | ¥0.03 | ¥0.60 |

## 🎯 推荐配置

### 开发测试
```yaml
model: "deepseek-chat"
temperature: 0.5
max_tokens: 1500
```

### 正式评审
```yaml
model: "deepseek-chat"
temperature: 0.3
max_tokens: 2000
```

### 详细评审
```yaml
model: "deepseek-chat"
temperature: 0.2
max_tokens: 2500
```

## 🔗 相关链接

- [DeepSeek 官网](https://www.deepseek.com/)
- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [API 文档](https://platform.deepseek.com/api-docs/)
- [定价说明](https://platform.deepseek.com/pricing)

## 💡 使用建议

1. **首次使用**：先用少量余额测试
2. **批量评审**：充值足够余额，避免中断
3. **成本控制**：设置 API 使用限额
4. **质量监控**：定期检查评审结果质量
5. **参数调优**：根据实际效果调整参数

## 🎉 开始使用

配置完成后：

1. 保存 `config.yaml` 文件
2. 启动后端：`.\start_backend.bat`
3. 启动前端：`.\start_frontend.bat`
4. 访问：http://localhost:3000
5. 上传论文开始评审！

---

**提示**：DeepSeek 对中文论文的评审效果非常好，而且成本很低，非常适合高校使用！
