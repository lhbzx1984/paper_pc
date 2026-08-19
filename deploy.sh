#!/bin/bash
#=============================================================================
# 论文评审系统 - 一键部署脚本
# 适用于腾讯云 CVM / 轻量应用服务器 (Ubuntu 20.04 / 22.04 / 24.04)
# 用法: chmod +x deploy.sh && ./deploy.sh
#=============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
print_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
print_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_info "=========================================="
print_info "  论文评审系统 - 一键部署"
print_info "=========================================="
echo ""

#---------------------------------------------
# 1. 检查操作系统
#---------------------------------------------
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    print_info "操作系统: $NAME $VERSION"
else
    print_warn "无法检测操作系统，继续执行..."
fi
echo ""

#---------------------------------------------
# 2. 检查并安装 Docker
#---------------------------------------------
print_info "步骤 1/4: 检查 Docker 环境..."

if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    print_ok "Docker 已安装 (版本 $DOCKER_VERSION)"
else
    print_warn "Docker 未安装，正在自动安装..."
    
    # 腾讯云内网镜像加速
    if curl -s --max-time 2 http://mirrors.tencentyun.com/ > /dev/null 2>&1; then
        print_info "检测到腾讯云环境，使用内网镜像加速..."
        curl -fsSL https://mirrors.tencentyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg 2>/dev/null || true
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.tencentyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    else
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg 2>/dev/null || true
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    fi
    
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # 配置 Docker 镜像加速
    sudo mkdir -p /etc/docker
    sudo tee /etc/docker/daemon.json > /dev/null <<'EOF'
{
    "registry-mirrors": [
        "https://mirror.ccs.tencentyun.com"
    ],
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}
EOF
    sudo systemctl daemon-reload
    sudo systemctl enable docker
    sudo systemctl restart docker
    
    print_ok "Docker 安装完成"
fi

#---------------------------------------------
# 3. 检查 Docker Compose
#---------------------------------------------
print_info "步骤 2/4: 检查 Docker Compose..."

# 优先使用 docker compose (v2 插件)
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
    print_ok "Docker Compose (plugin) 可用"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
    print_ok "Docker Compose (standalone) 可用"
else
    print_warn "Docker Compose 未安装，正在安装插件..."
    sudo apt-get install -y docker-compose-plugin
    COMPOSE_CMD="docker compose"
    print_ok "Docker Compose 插件安装完成"
fi
echo ""

#---------------------------------------------
# 4. 检查 .env 配置文件
#---------------------------------------------
print_info "步骤 3/4: 检查环境配置..."

if [[ ! -f .env ]]; then
    print_warn ".env 文件不存在，从模板创建..."
    cp .env.example .env
    print_warn "请编辑 .env 文件填入你的 API Key，然后重新运行此脚本！"
    print_info "命令: nano .env"
    echo ""
    print_info "示例配置："
    echo "  LLM_API_KEY=sk-your-actual-api-key"
    echo "  LLM_BASE_URL=https://api.deepseek.com/v1"
    echo "  LLM_MODEL=deepseek-chat"
    echo ""
    print_info "配置完成后重新运行: ./deploy.sh"
    exit 0
else
    # 检查 API Key 是否已填写
    if grep -q "your-api-key-here" .env 2>/dev/null; then
        print_warn ".env 中的 LLM_API_KEY 仍为默认值，请先编辑 .env 填入真实 API Key！"
        print_info "命令: nano .env"
        exit 1
    fi
    print_ok ".env 配置文件已就绪"
fi
echo ""

#---------------------------------------------
# 5. 构建并启动服务
#---------------------------------------------
print_info "步骤 4/4: 构建并启动服务..."

print_info "正在构建 Docker 镜像（首次构建需要 5-10 分钟）..."
$COMPOSE_CMD build --no-cache 2>&1 | tail -5

print_info "正在启动服务..."
$COMPOSE_CMD up -d

echo ""
print_info "等待服务启动..."

# 等待后端健康检查通过
MAX_WAIT=60
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        break
    fi
    sleep 2
    WAITED=$((WAITED + 2))
    echo -n "."
done
echo ""

if [ $WAITED -ge $MAX_WAIT ]; then
    print_warn "后端服务启动较慢，请稍后检查: docker logs thesis-review-backend"
fi

#---------------------------------------------
# 6. 验证并输出结果
#---------------------------------------------
echo ""
print_info "=========================================="
print_info "  部署状态检查"
print_info "=========================================="

# 获取服务器公网 IP
PUBLIC_IP=$(curl -s http://metadata.tencentyun.com/latest/meta-data/public-ipv4 2>/dev/null || curl -s ifconfig.me 2>/dev/null || echo "localhost")

# 检查后端
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    print_ok "后端服务: 运行中 (端口 8000)"
else
    print_error "后端服务: 未响应"
    print_info "查看日志: docker logs thesis-review-backend"
fi

# 检查前端
if curl -s http://localhost:80 > /dev/null 2>&1; then
    print_ok "前端服务: 运行中 (端口 80)"
else
    print_error "前端服务: 未响应"
    print_info "查看日志: docker logs thesis-review-frontend"
fi

echo ""
print_info "=========================================="
print_ok  "部署完成！"
print_info "=========================================="
echo ""
echo -e "  ${GREEN}访问地址:${NC}"
echo -e "    前端界面:  http://${PUBLIC_IP}"
echo -e "    后端API:   http://${PUBLIC_IP}:8000"
echo -e "    API文档:   http://${PUBLIC_IP}:8000/docs"
echo ""
echo -e "  ${YELLOW}重要提示:${NC}"
echo -e "    请确保腾讯云安全组已放行以下端口:"
echo -e "    - TCP 80  (HTTP 前端访问)"
echo -e "    - TCP 8000 (API 直连, 可选)"
echo ""
echo -e "  ${BLUE}常用命令:${NC}"
echo -e "    查看日志:   $COMPOSE_CMD logs -f"
echo -e "    停止服务:   $COMPOSE_CMD down"
echo -e "    重启服务:   $COMPOSE_CMD restart"
echo -e "    重新构建:   $COMPOSE_CMD up -d --build"
echo ""
