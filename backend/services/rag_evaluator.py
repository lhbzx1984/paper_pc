import json
from typing import Dict, List
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGEvaluator:
    """基于RAG的论文评审器"""
    
    def __init__(self, config: Dict, llm_client):
        self.config = config
        self.llm_client = llm_client
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    async def evaluate(self, paper_text: str) -> Dict:
        """评审论文"""
        # 分割文本
        chunks = self.text_splitter.split_text(paper_text)
        
        # 对每个评审标准进行评分
        criteria_scores = []
        for criterion in self.config["criteria"]:
            score_data = await self._evaluate_criterion(
                paper_text, chunks, criterion
            )
            criteria_scores.append(score_data)
        
        # 计算总分（直接累加各项得分，因为max_score已经是实际分值）
        total_score = sum(
            item["score"]
            for item in criteria_scores
        )
        
        # 确定等级
        grade = self._get_grade(total_score)
        
        # 生成总体评价
        overall_comment = await self._generate_overall_comment(
            paper_text, criteria_scores, total_score, grade
        )
        
        return {
            "total_score": round(total_score, 2),
            "grade": grade,
            "criteria_scores": criteria_scores,
            "overall_comment": overall_comment
        }
    
    async def _evaluate_criterion(
        self, full_text: str, chunks: List[str], criterion: Dict
    ) -> Dict:
        """评估单个标准"""
        # 构建评审提示
        prompt = f"""
请作为一名资深的毕业论文评审专家，根据以下标准对论文进行评分：

评审标准：{criterion['name']}
标准说明：{criterion['description']}
本项满分：{criterion['max_score']}分（注意：不是100分，就是{criterion['max_score']}分）

论文内容（节选）：
{full_text[:3000]}...

重要提示：
- 本项满分是 {criterion['max_score']} 分，请严格按照这个满分评分
- 评分范围：0 到 {criterion['max_score']} 分
- 不要使用百分制（100分制），直接给出 0-{criterion['max_score']} 之间的分数

请给出：
1. 该项得分（必须在 0-{criterion['max_score']} 分之间的数字）
2. 详细评价（150字以内）
3. 改进建议（100字以内）

请以JSON格式返回：
{{
    "score": 分数（必须是0到{criterion['max_score']}之间的数字）,
    "comment": "评价",
    "suggestion": "建议"
}}
"""
        
        messages = [
            {"role": "system", "content": "你是一位专业的毕业论文评审专家。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.llm_client.chat(messages)
            print(f"[DEBUG] {criterion['name']} 原始响应: {response[:200]}...")  # 调试日志
            
            # 清理响应文本
            cleaned_response = response.strip()
            # 移除可能的markdown代码块标记
            if "```json" in cleaned_response:
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0]
            elif "```" in cleaned_response:
                cleaned_response = cleaned_response.split("```")[1].split("```")[0]
            
            # 尝试解析JSON
            result = json.loads(cleaned_response.strip())
            
            # 获取分数并验证
            raw_score = float(result.get("score", 0))
            max_score = criterion["max_score"]
            
            print(f"[DEBUG] {criterion['name']} 原始分数: {raw_score}, 满分: {max_score}")  # 调试日志
            
            # 如果分数超过满分，可能是按100分制给的，需要转换
            if raw_score > max_score:
                # 假设是按100分制给的，转换为实际满分
                score = (raw_score / 100.0) * max_score
                print(f"[DEBUG] {criterion['name']} 转换后分数: {score}")  # 调试日志
            else:
                score = raw_score
            
            # 确保分数在有效范围内
            score = max(0, min(score, max_score))
            
            comment = result.get("comment", "暂无评价")
            suggestion = result.get("suggestion", "暂无建议")
            
            print(f"[DEBUG] {criterion['name']} 最终分数: {score}, 评价长度: {len(comment)}, 建议长度: {len(suggestion)}")  # 调试日志
            
            return {
                "name": criterion["name"],
                "weight": criterion["weight"],
                "max_score": criterion["max_score"],
                "score": round(score, 1),
                "comment": comment if comment else "暂无评价",
                "suggestion": suggestion if suggestion else "暂无建议"
            }
        except json.JSONDecodeError as e:
            print(f"[ERROR] {criterion['name']} JSON解析失败: {e}")
            print(f"[ERROR] 响应内容: {response[:500]}")
            # JSON解析失败，尝试从文本中提取信息
            return {
                "name": criterion["name"],
                "weight": criterion["weight"],
                "max_score": criterion["max_score"],
                "score": criterion["max_score"] * 0.7,  # 默认给70%的分数
                "comment": "评审过程中JSON解析失败，请检查大模型配置或重新提交",
                "suggestion": "建议检查论文格式是否正确，或稍后重试"
            }
        except Exception as e:
            print(f"[ERROR] {criterion['name']} 评审失败: {type(e).__name__}: {e}")
            # 其他错误
            return {
                "name": criterion["name"],
                "weight": criterion["weight"],
                "max_score": criterion["max_score"],
                "score": criterion["max_score"] * 0.7,
                "comment": f"评审过程中出现错误: {type(e).__name__}",
                "suggestion": "建议重新提交或联系管理员"
            }
    
    async def _generate_overall_comment(
        self, paper_text: str, criteria_scores: List[Dict], 
        total_score: float, grade: str
    ) -> str:
        """生成总体评价"""
        scores_summary = "\n".join([
            f"- {item['name']}: {item['score']}/{item['max_score']}分"
            for item in criteria_scores
        ])
        
        prompt = f"""
作为毕业论文评审专家，请根据以下评分结果给出总体评价（200-300字）：

总分：{total_score}分
等级：{grade}

各项得分：
{scores_summary}

请给出：
1. 论文的主要优点
2. 存在的主要问题
3. 总体评价和建议
"""
        
        messages = [
            {"role": "system", "content": "你是一位专业的毕业论文评审专家。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.llm_client.chat(messages)
            return response
        except:
            return "总体评价生成失败，请检查大模型配置。"
    
    def _get_grade(self, score: float) -> str:
        """根据分数获取等级"""
        for level in self.config["grade_levels"]:
            if score >= level["min_score"]:
                return level["grade"]
        return "不及格"
