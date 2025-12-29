"""
Logical Fallacy Agent - Detects logical fallacies in reasoning.
"""

import json
from typing import Dict, List
from insight_engine.agents.base_agent import BaseAgent
from insight_engine.models.evaluation import LogicalFallacy, LogicalFallacyType


class LogicalFallacyAgent(BaseAgent):
    """Agent for detecting logical fallacies in articles."""
    
    def analyze(self, article_text: str) -> Dict:
        """
        Detect logical fallacies in an article.
        
        Args:
            article_text: The article text to analyze
            
        Returns:
            Analysis results including detected fallacies
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
                "fallacies": [],
                "fallacy_explanation": f"Error during analysis: {str(e)}"
            }
    
    def _create_analysis_prompt(self, article_text: str) -> str:
        """Create the analysis prompt for logical fallacy detection."""
        template = """你是一位专业的财经文章评审专家，专门检测文章中的逻辑谬误（Logical Fallacies）。

请分析以下财经文章，检测可能存在的逻辑谬误，包括但不限于：

1. **以偏概全** (overgeneralization): 从少数案例推广到全体
2. **因果倒置** (causal_reversal): 混淆因果关系的方向
3. **非此即彼** (false_dilemma): 错误地将问题简化为两个选项
4. **滑坡谬误** (slippery_slope): 认为一个小变化会导致连锁的极端后果
5. **循环论证** (circular_reasoning): 用结论来证明结论
6. **轻率概括** (hasty_generalization): 基于不充分的证据得出结论
7. **后此谬误** (post_hoc): 认为先后发生的事件必然有因果关系

文章内容：
{article_text}

请以JSON格式返回分析结果：
{{
    "score": 0.0-1.0的评分（1.0表示没有谬误，0.0表示严重谬误）,
    "fallacies": [
        {{
            "type": "谬误类型（使用英文代码）",
            "location": "谬误出现的位置描述",
            "description": "谬误的详细描述",
            "severity": 0.0-1.0的严重程度
        }},
        ...
    ],
    "fallacy_explanation": "总体说明检测到的逻辑谬误情况"
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
            
            # Parse fallacies
            fallacies = []
            for f in result.get("fallacies", []):
                if isinstance(f, dict):
                    fallacy_dict = {
                        "type": f.get("type", "overgeneralization"),
                        "location": f.get("location", ""),
                        "description": f.get("description", ""),
                        "severity": max(0.0, min(1.0, float(f.get("severity", 0.5))))
                    }
                    fallacies.append(fallacy_dict)
            
            # Calculate score (inverse of average severity)
            if fallacies:
                avg_severity = sum(f["severity"] for f in fallacies) / len(fallacies)
                score = max(0.0, 1.0 - avg_severity)
            else:
                score = 1.0
            
            return {
                "score": max(0.0, min(1.0, float(result.get("score", score)))),
                "fallacies": fallacies,
                "fallacy_explanation": str(result.get("fallacy_explanation", ""))
            }
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Return a default result if parsing fails
            return {
                "score": 0.7,
                "fallacies": [],
                "fallacy_explanation": f"Failed to parse analysis result: {str(e)}"
            }
