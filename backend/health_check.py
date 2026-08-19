"""
健康检查脚本
用于检查系统各组件是否正常运行
"""
import sys
import yaml
import requests
from pathlib import Path

def check_config():
    """检查配置文件"""
    print("🔍 检查配置文件...")
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        print("❌ config.yaml 不存在")
        return False
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        # 检查必要的配置项
        if "llm" not in config:
            print("❌ 缺少 llm 配置")
            return False
        
        if config["llm"]["api_key"] == "your-api-key-here":
            print("⚠️  警告: API Key 未配置")
            return False
        
        print("✅ 配置文件正常")
        return True
    except Exception as e:
        print(f"❌ 配置文件解析失败: {e}")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "yaml",
        "docx",
        "PyPDF2",
        "openai",
        "langchain"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ 缺少依赖包: {', '.join(missing)}")
        print("   运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def check_backend():
    """检查后端服务"""
    print("\n🔍 检查后端服务...")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务运行正常")
            return True
        else:
            print(f"⚠️  后端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
        print("   请确保后端服务已启动: python main.py")
        return False
    except Exception as e:
        print(f"❌ 检查后端服务失败: {e}")
        return False

def check_frontend():
    """检查前端服务"""
    print("\n🔍 检查前端服务...")
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务运行正常")
            return True
        else:
            print(f"⚠️  前端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端服务")
        print("   请确保前端服务已启动: npm start")
        return False
    except Exception as e:
        print(f"❌ 检查前端服务失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("🏥 系统健康检查")
    print("=" * 50)
    
    results = []
    
    # 检查配置
    results.append(check_config())
    
    # 检查依赖
    results.append(check_dependencies())
    
    # 检查后端
    results.append(check_backend())
    
    # 检查前端
    results.append(check_frontend())
    
    # 总结
    print("\n" + "=" * 50)
    if all(results):
        print("✅ 所有检查通过！系统运行正常")
        print("=" * 50)
        return 0
    else:
        print("❌ 部分检查未通过，请根据上述提示修复问题")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    sys.exit(main())
