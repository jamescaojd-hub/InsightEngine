"""
Consistency Agent - Checks for internal consistency and contradictions.
"""

import json
from typing import Dict, List
from insight_engine.agents.base_agent import BaseAgent


class ConsistencyAgent(BaseAgent):
    """Agent for checking consistency in articles."""
    
    def analyze(self, article_text: str) -> Dict:
        """
        Check consistency in an article.
        
        Args:
            article_text: The article text to analyze
            
        Returns:
            Analysis results including contradiction detection
        """
        prompt = self._create_analysis_prompt(article_text)
        
        try:
            response = self.llm.invoke(prompt)
            result = self._parse_response(response.content)
            return result
        except Exception as e:
            # Fallback result in case of error
            return {
                "score": 0.7,
                "contradictions": [],
                "consistency_explanation": f"Error during analysis: {str(e)}"
            }
    
    def _create_analysis_prompt(self, article_text: str) -> str:
        """Create the analysis prompt for consistency checking."""
        template = """你是一位专业的财经文章评审专家，专门检查文章的内部一致性（Consistency）。

请分析以下财经文章，检查是否存在内部矛盾或不一致的地方，包括：

1. **论述矛盾**: 文章前后论述是否相互矛盾
2. **数据矛盾**: 引用的数据、事实是否前后一致
3. **立场矛盾**: 文章的观点和立场是否一致
4. **逻辑矛盾**: 推理过程是否自洽
5. **结论与论据的一致性**: 结论是否与前文论据相符

文章内容：
{article_text}

请以JSON格式返回分析结果：
{{
    "score": 0.0-1.0的评分（1.0表示完全一致，0.0表示严重矛盾）,
    "contradictions": [
        "检测到的矛盾描述1",
        "检测到的矛盾描述2",
        ...
    ],
    "consistency_explanation": "详细解释一致性检查的结果，包括具体例子"
}}

只返回JSON，不要其他内容。"""
        
        return template.format(article_text=article_text)
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse the LLM response into structured data."""
        try:
            # Try to extract JSON from the response
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            
            # Validate and normalize the result
            contradictions = result.get("contradictions", [])
            if not isinstance(contradictions, list):
                contradictions = []
            
            return {
                "score": max(0.0, min(1.0, float(result.get("score", 0.7)))),
                "contradictions": [str(c) for c in contradictions],
                "consistency_explanation": str(result.get("consistency_explanation", ""))
            }
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Return a default result if parsing fails
            return {
                "score": 0.7,
                "contradictions": [],
                "consistency_explanation": f"Failed to parse analysis result: {str(e)}"
            }
