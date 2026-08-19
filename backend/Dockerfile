FROM python:3.11-slim

WORKDIR /app

# 先复制依赖文件，利用 Docker 层缓存
# 注意：所有依赖在 linux/amd64 + Python 3.11 均有预编译 wheel，无需 gcc
# pip 使用腾讯云内网镜像加速（境外服务器可改回默认源）
COPY requirements.txt .
RUN pip install --no-cache-dir \
    -i https://mirrors.cloud.tencent.com/pypi/simple \
    -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 使用 uvicorn 启动，支持多 worker
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
