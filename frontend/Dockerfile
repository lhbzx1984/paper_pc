FROM node:18-alpine as build

WORKDIR /app

# 先复制依赖文件，利用 Docker 层缓存
# npm 使用腾讯云镜像加速（境外服务器可删除 registry 配置）
COPY package*.json ./
RUN npm config set registry https://mirrors.cloud.tencent.com/npm/ \
    && npm install --legacy-peer-deps

# 复制源代码并构建
COPY . .
RUN npm run build

# --- 生产阶段：Nginx 托管静态文件 ---
FROM nginx:alpine

# 复制构建产物
COPY --from=build /app/build /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
