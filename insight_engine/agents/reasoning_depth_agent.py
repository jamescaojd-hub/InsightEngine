"""
Reasoning Depth Agent - Analyzes the depth and thoroughness of reasoning.
"""

import json
from typing import Dict
from insight_engine.agents.base_agent import BaseAgent
from insight_engine.models.evaluation import ReasoningDepthResult


class ReasoningDepthAgent(BaseAgent):
    """Agent for analyzing reasoning depth in articles."""
    
    def analyze(self, article_text: str) -> Dict:
        """
        Analyze the reasoning depth of an article.
        
        Args:
            article_text: The article text to analyze
            
        Returns:
            Analysis results including depth score and explanation
        """
        prompt = self._create_analysis_prompt(article_text)
        
        try:
            response = self.llm.invoke(prompt)
            result = self._parse_response(response.content)
            return result
        except Exception as e:
            # Fallback result in case of error
            return {
                "score": 0.5,
                "has_causal_analysis": False,
                "has_comparative_analysis": False,
                "analysis_levels": 1,
                "depth_explanation": f"Error during analysis: {str(e)}"
            }
    
    def _create_analysis_prompt(self, article_text: str) -> str:
        """Create the analysis prompt for reasoning depth evaluation."""
        template = """你是一位专业的财经文章评审专家，专门评估文章的推理深度（Reasoning Depth）。

请分析以下财经文章的推理深度，评估标准包括：

1. **多角度分析**: 文章是否从多个角度分析问题（如市场、政策、技术、竞争等）
2. **多层次分析**: 分析是否有层次递进（表面现象 → 深层原因 → 潜在影响）
3. **因果分析**: 是否进行了清晰的因果关系分析
4. **比较分析**: 是否进行了有意义的比较（如历史对比、同行对比等）
5. **深度推演**: 是否有深入的逻辑推演，而非仅仅罗列事实

文章内容：
{article_text}

请以JSON格式返回分析结果：
{{
    "score": 0.0-1.0的评分,
    "has_causal_analysis": true/false,
    "has_comparative_analysis": true/false,
    "analysis_levels": 检测到的分析层次数量（1-5）,
    "depth_explanation": "详细解释推理深度的评估，包括具体例子和改进建议"
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
            return {
                "score": max(0.0, min(1.0, float(result.get("score", 0.5)))),
                "has_causal_analysis": bool(result.get("has_causal_analysis", False)),
                "has_comparative_analysis": bool(result.get("has_comparative_analysis", False)),
                "analysis_levels": max(1, min(5, int(result.get("analysis_levels", 1)))),
                "depth_explanation": str(result.get("depth_explanation", ""))
            }
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Return a default result if parsing fails
            return {
                "score": 0.5,
                "has_causal_analysis": False,
                "has_comparative_analysis": False,
                "analysis_levels": 1,
                "depth_explanation": f"Failed to parse analysis result: {str(e)}"
            }
