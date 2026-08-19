import openai
from typing import Dict, List


class LLMClient:
    """大模型客户端"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.client = openai.OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
    
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """调用大模型进行对话"""
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                temperature=self.config.get("temperature", 0.3),
                max_tokens=self.config.get("max_tokens", 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"大模型调用失败: {str(e)}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """生成文本嵌入向量"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            # 如果embedding失败，返回空列表
            return []
