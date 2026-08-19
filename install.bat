@echo off
echo ========================================
echo 毕业论文智能评审系统 - 自动安装
echo ========================================
echo.

echo [1/4] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)
echo.

echo [2/4] 安装后端依赖...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 后端依赖安装失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo 后端依赖安装完成！
echo.

echo [3/4] 检查Node.js环境...
node --version
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js 16+
    pause
    exit /b 1
)
echo.

echo [4/4] 安装前端依赖...
cd frontend
call npm install
if errorlevel 1 (
    echo 错误: 前端依赖安装失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo 前端依赖安装完成！
echo.

echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 下一步:
echo 1. 编辑 backend\config.yaml 配置大模型API
echo 2. 运行 start_backend.bat 启动后端
echo 3. 运行 start_frontend.bat 启动前端
echo 4. 访问 http://localhost:3000
echo.
echo 详细说明请查看 QUICKSTART.md
echo.
pause
