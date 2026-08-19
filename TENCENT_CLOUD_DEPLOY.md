# 腾讯云部署指南

本文档指导你在腾讯云服务器上一键部署论文评审系统。

---

## 一、服务器准备

### 1.1 购买服务器

| 项目 | 推荐配置 |
|------|----------|
| 产品 | 轻量应用服务器 / 云服务器 CVM |
| 操作系统 | Ubuntu 22.04 LTS |
| CPU | 2 核 |
| 内存 | 4 GB |
| 磁盘 | 50 GB SSD |
| 带宽 | 5 Mbps 起 |

> 评审过程需要调用大模型 API，对服务器 CPU 要求不高，2 核 4G 足够。

### 1.2 安全组配置

在腾讯云控制台 → 安全组中，放行以下端口：

| 端口 | 协议 | 用途 | 是否必须 |
|------|------|------|----------|
| 80 | TCP | 前端 HTTP 访问 | ✅ 必须 |
| 443 | TCP | HTTPS（可选） | 可选 |
| 8000 | TCP | 后端 API 直连 | 可选 |
| 22 | TCP | SSH 远程连接 | ✅ 必须 |

> 轻量应用服务器在「防火墙」页面配置，CVM 在「安全组」页面配置。

---

## 二、一键部署

### 2.1 连接服务器

```bash
ssh ubuntu@你的服务器公网IP
```

### 2.2 上传项目代码

**方式一：Git 克隆（推荐）**

如果代码已推送到 GitHub/Gitee：

```bash
git clone https://github.com/你的用户名/毕业设计论文评审系统.git
cd 毕业设计论文评审系统
```

**方式二：本地打包上传**

```bash
# 在本地执行（排除不需要的文件）
cd C:\Users\Dell\Desktop\毕业设计论文评审系统
# 用 scp 或其他工具上传到服务器
scp -r . ubuntu@你的服务器IP:~/thesis-review/
```

### 2.3 执行部署

```bash
cd 毕业设计论文评审系统   # 进入项目目录
chmod +x deploy.sh        # 赋予执行权限
./deploy.sh               # 一键部署
```

脚本会自动完成：
1. 安装 Docker 和 Docker Compose（如未安装）
2. 配置腾讯云内网镜像加速
3. 创建 `.env` 配置文件
4. 构建 Docker 镜像
5. 启动前后端服务
6. 健康检查并输出访问地址

### 2.4 配置 API Key

首次运行脚本会提示你编辑 `.env` 文件：

```bash
nano .env
```

填入你的大模型配置：

```env
LLM_API_KEY=sk-your-actual-api-key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

保存后再次运行部署脚本：

```bash
./deploy.sh
```

---

## 三、访问系统

部署完成后，在浏览器中访问：

| 地址 | 说明 |
|------|------|
| `http://你的服务器IP` | 前端界面 |
| `http://你的服务器IP:8000/docs` | API 文档（Swagger） |

---

## 四、运维管理

### 4.1 常用命令

```bash
# 查看服务状态
docker compose ps

# 查看实时日志
docker compose logs -f

# 仅查看后端日志
docker logs -f thesis-review-backend

# 仅查看前端日志
docker logs -f thesis-review-frontend

# 重启所有服务
docker compose restart

# 停止所有服务
docker compose down

# 重新构建并启动（代码更新后）
docker compose up -d --build
```

### 4.2 更新代码

```bash
git pull                    # 拉取最新代码
docker compose up -d --build  # 重新构建并启动
```

### 4.3 备份配置

评审标准和 LLM 配置存储在 `backend/config.yaml`，通过导入功能修改的标准会持久化到此文件：

```bash
# 备份配置
cp backend/config.yaml backend/config.yaml.bak

# 恢复配置
cp backend/config.yaml.bak backend/config.yaml
docker compose restart backend
```

### 4.4 修改 API Key

编辑 `.env` 文件后重启：

```bash
nano .env                    # 修改 LLM_API_KEY
docker compose restart backend
```

---

## 五、架构说明

```
用户浏览器
    │
    ▼
┌──────────────────────────────────┐
│  前端容器 (Nginx, 端口 80)        │
│  ├─ / → React 静态文件            │
│  └─ /api → 反向代理到后端         │
└──────────┬───────────────────────┘
           │ 内部网络
           ▼
┌──────────────────────────────────┐
│  后端容器 (FastAPI/Uvicorn, 8000) │
│  ├─ /api/upload → 论文评审        │
│  ├─ /api/config → 配置管理        │
│  ├─ /api/criteria/export → 导出   │
│  └─ /api/criteria/import → 导入   │
└──────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  大模型 API (DeepSeek/OpenAI)     │
└──────────────────────────────────┘
```

- **前端容器**：Nginx 托管 React 构建产物，同时反向代理 `/api` 请求到后端
- **后端容器**：FastAPI + Uvicorn，处理文档解析和 LLM 评审
- **配置持久化**：`config.yaml` 通过 Docker volume 挂载，容器重建不丢失配置
- **环境变量**：API Key 通过 `.env` 注入，不写入镜像

---

## 六、常见问题

### Q1: 访问 http://服务器IP 显示 502 Bad Gateway

后端尚未启动完成，等待 30 秒后刷新。如持续报错：

```bash
docker logs thesis-review-backend  # 查看后端日志
```

### Q2: 论文评审报错 "评审失败"

检查 API Key 是否正确：

```bash
cat .env  # 确认 LLM_API_KEY 配置正确
docker compose restart backend
```

### Q3: 文件上传报错 413 Request Entity Too Large

Nginx 已配置 `client_max_body_size 100m`。如仍报错，检查是否有多层 Nginx 代理。

### Q4: 评审耗时很长

正常现象。系统对每项评审标准逐一调用大模型，11 项标准约需 1-3 分钟。可通过「系统配置」页面减少评审标准数量来加快速度。

### Q5: Docker 构建很慢

脚本已配置腾讯云镜像加速。如仍慢，可手动配置：

```bash
sudo tee /etc/docker/daemon.json > /dev/null <<'EOF'
{"registry-mirrors": ["https://mirror.ccs.tencentyun.com"]}
EOF
sudo systemctl restart docker
```

### Q6: 如何配置 HTTPS

使用 Caddy 或 Nginx + Let's Encrypt：

```bash
# 安装 Caddy
sudo apt install -y caddy

# 配置反向代理
sudo tee /etc/caddy/Caddyfile > /dev/null <<'EOF'
your-domain.com {
    reverse_proxy localhost:80
}
EOF

sudo systemctl restart caddy
```

---

## 七、文件清单

部署相关文件说明：

| 文件 | 用途 |
|------|------|
| `deploy.sh` | 一键部署脚本 |
| `.env.example` | 环境变量模板 |
| `.env` | 实际环境变量（不入版本控制） |
| `docker-compose.yml` | Docker Compose 编排文件 |
| `backend/Dockerfile` | 后端镜像构建文件 |
| `backend/.dockerignore` | 后端构建排除规则 |
| `frontend/Dockerfile` | 前端镜像构建文件 |
| `frontend/.dockerignore` | 前端构建排除规则 |
| `frontend/nginx.conf` | Nginx 配置（静态托管 + API 反代） |
