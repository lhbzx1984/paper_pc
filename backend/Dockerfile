FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（python-docx 和 PyPDF2 的底层 C 库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用 Docker 层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 使用 uvicorn 启动，支持多 worker
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
