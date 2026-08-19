"""
API测试脚本
用于测试后端API功能
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """测试根路径"""
    response = requests.get(f"{BASE_URL}/")
    print("测试根路径:")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_get_config():
    """测试获取配置"""
    response = requests.get(f"{BASE_URL}/api/config")
    print("测试获取配置:")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    print()

def test_upload_file(file_path):
    """测试文件上传"""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    print("测试文件上传:")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    else:
        print(f"错误: {response.text}")
    print()

def test_update_config():
    """测试更新配置"""
    data = {
        "llm_model": "gpt-3.5-turbo"
    }
    response = requests.post(f"{BASE_URL}/api/config", json=data)
    print("测试更新配置:")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("开始测试API")
    print("=" * 50)
    print()
    
    # 测试基本功能
    test_root()
    test_get_config()
    
    # 如果有测试文件，可以测试上传
    # test_upload_file("test_paper.pdf")
    
    print("=" * 50)
    print("测试完成")
    print("=" * 50)
