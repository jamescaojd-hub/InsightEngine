"""
Argument Structure Agent - Analyzes the logical structure and coherence.
"""

import json
from typing import Dict, List
from insight_engine.agents.base_agent import BaseAgent
from insight_engine.models.evaluation import ArgumentComponent


class ArgumentStructureAgent(BaseAgent):
    """Agent for analyzing argument structure in articles."""
    
    def analyze(self, article_text: str) -> Dict:
        """
        Analyze the argument structure of an article.
        
        Args:
            article_text: The article text to analyze
            
        Returns:
            Analysis results including structure score and components
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
                "has_clear_structure": False,
                "paragraph_coherence": 0.5,
                "argument_components": [],
                "structure_explanation": f"Error during analysis: {str(e)}"
            }
    
    def _create_analysis_prompt(self, article_text: str) -> str:
        """Create the analysis prompt for argument structure evaluation."""
        template = """你是一位专业的财经文章评审专家，专门评估文章的论证结构（Argument Structure）。

请分析以下财经文章的论证结构质量，评估标准包括：

1. **逻辑次序**: 文章各部分是否按合理的逻辑顺序排列
2. **段落衔接**: 段落之间的衔接是否自然流畅
3. **论点-论据-结论关系**: 三者关系是否严密，论据是否充分支持论点
4. **结构清晰度**: 整体结构是否清晰，读者能否轻松跟随论证思路
5. **论证完整性**: 从问题到结论的论证链条是否完整

文章内容：
{article_text}

请以JSON格式返回分析结果：
{{
    "score": 0.0-1.0的评分,
    "has_clear_structure": true/false,
    "paragraph_coherence": 0.0-1.0的段落连贯性评分,
    "argument_components": [
        {{"type": "claim/evidence/reasoning/conclusion", "content": "内容摘要", "location": "位置描述"}},
        ...
    ],
    "structure_explanation": "详细解释论证结构的评估，包括具体例子和改进建议"
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
                "has_clear_structure": bool(result.get("has_clear_structure", False)),
                "paragraph_coherence": max(0.0, min(1.0, float(result.get("paragraph_coherence", 0.5)))),
                "argument_components": self._parse_components(result.get("argument_components", [])),
                "structure_explanation": str(result.get("structure_explanation", ""))
            }
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Return a default result if parsing fails
            return {
                "score": 0.5,
                "has_clear_structure": False,
                "paragraph_coherence": 0.5,
                "argument_components": [],
                "structure_explanation": f"Failed to parse analysis result: {str(e)}"
            }
    
    def _parse_components(self, components_data: List) -> List[Dict]:
        """Parse argument components from the response."""
        parsed = []
        for comp in components_data:
            if isinstance(comp, dict):
                parsed.append({
                    "type": comp.get("type", "unknown"),
                    "content": comp.get("content", ""),
                    "location": comp.get("location", "")
                })
        return parsed
