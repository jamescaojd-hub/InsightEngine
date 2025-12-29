"""
Main evaluator that orchestrates all agents to provide comprehensive evaluation.
"""

from typing import Optional, List
from insight_engine.config import EvaluatorConfig
from insight_engine.agents import (
    ReasoningDepthAgent,
    ArgumentStructureAgent,
    LogicalFallacyAgent,
    ConsistencyAgent,
)
from insight_engine.models.evaluation import (
    ReasoningLogicEvaluation,
    ReasoningDepthResult,
    ArgumentStructureResult,
    ConsistencyResult,
    LogicalFallacyResult,
    ArgumentComponent,
    LogicalFallacy,
)


class ReasoningLogicEvaluator:
    """
    Main evaluator for reasoning and logic quality of financial articles.
    
    This evaluator orchestrates multiple specialized agents to provide
    a comprehensive evaluation of an article's reasoning and logic quality.
    """
    
    def __init__(self, config: Optional[EvaluatorConfig] = None):
        """
        Initialize the evaluator.
        
        Args:
            config: Evaluator configuration. If None, uses default config.
        """
        if config is None:
            from insight_engine.config import DEFAULT_CONFIG
            config = DEFAULT_CONFIG
        
        self.config = config
        
        # Initialize agents
        self.reasoning_depth_agent = ReasoningDepthAgent(config)
        self.argument_structure_agent = ArgumentStructureAgent(config)
        self.logical_fallacy_agent = LogicalFallacyAgent(config)
        self.consistency_agent = ConsistencyAgent(config)
    
    def evaluate(self, article_text: str, article_title: Optional[str] = None) -> ReasoningLogicEvaluation:
        """
        Evaluate an article's reasoning and logic quality.
        
        Args:
            article_text: The article text to evaluate
            article_title: Optional title of the article
            
        Returns:
            Complete evaluation result
        """
        # Run all agents in parallel (conceptually - LangChain handles this)
        print("Analyzing reasoning depth...")
        reasoning_depth_data = self.reasoning_depth_agent.analyze(article_text)
        reasoning_depth = ReasoningDepthResult(**reasoning_depth_data)
        
        print("Analyzing argument structure...")
        argument_structure_data = self.argument_structure_agent.analyze(article_text)
        # Convert argument components to proper objects
        components = [
            ArgumentComponent(**comp) 
            for comp in argument_structure_data.pop("argument_components", [])
        ]
        argument_structure = ArgumentStructureResult(
            **argument_structure_data,
            argument_components=components
        )
        
        print("Detecting logical fallacies...")
        logical_fallacy_data = self.logical_fallacy_agent.analyze(article_text)
        # Convert fallacies to proper objects
        fallacies = [
            LogicalFallacy(**f)
            for f in logical_fallacy_data.pop("fallacies", [])
        ]
        logical_fallacies = LogicalFallacyResult(
            **logical_fallacy_data,
            fallacies=fallacies
        )
        
        print("Checking consistency...")
        consistency_data = self.consistency_agent.analyze(article_text)
        consistency = ConsistencyResult(**consistency_data)
        
        # Calculate overall score (weighted average)
        overall_score = self._calculate_overall_score(
            reasoning_depth, argument_structure, consistency, logical_fallacies
        )
        
        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses(
            reasoning_depth, argument_structure, consistency, logical_fallacies
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            reasoning_depth, argument_structure, consistency, logical_fallacies
        )
        
        # Create final evaluation result
        evaluation = ReasoningLogicEvaluation(
            article_title=article_title,
            overall_score=overall_score,
            reasoning_depth=reasoning_depth,
            argument_structure=argument_structure,
            consistency=consistency,
            logical_fallacies=logical_fallacies,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )
        
        return evaluation
    
    def _calculate_overall_score(
        self,
        reasoning_depth: ReasoningDepthResult,
        argument_structure: ArgumentStructureResult,
        consistency: ConsistencyResult,
        logical_fallacies: LogicalFallacyResult,
    ) -> float:
        """Calculate the overall score as a weighted average."""
        # Weights for different dimensions
        weights = {
            "reasoning_depth": 0.30,
            "argument_structure": 0.30,
            "consistency": 0.25,
            "logical_fallacies": 0.15,
        }
        
        overall = (
            reasoning_depth.score * weights["reasoning_depth"]
            + argument_structure.score * weights["argument_structure"]
            + consistency.score * weights["consistency"]
            + logical_fallacies.score * weights["logical_fallacies"]
        )
        
        return round(overall, 3)
    
    def _identify_strengths_weaknesses(
        self,
        reasoning_depth: ReasoningDepthResult,
        argument_structure: ArgumentStructureResult,
        consistency: ConsistencyResult,
        logical_fallacies: LogicalFallacyResult,
    ) -> tuple[List[str], List[str]]:
        """Identify strengths and weaknesses based on component scores."""
        strengths = []
        weaknesses = []
        
        # Reasoning depth
        if reasoning_depth.score >= 0.7:
            if reasoning_depth.has_causal_analysis:
                strengths.append("包含清晰的因果分析")
            if reasoning_depth.has_comparative_analysis:
                strengths.append("进行了有效的比较分析")
            if reasoning_depth.analysis_levels >= 3:
                strengths.append(f"具有{reasoning_depth.analysis_levels}层次的深入分析")
        else:
            if not reasoning_depth.has_causal_analysis:
                weaknesses.append("缺乏因果关系分析")
            if not reasoning_depth.has_comparative_analysis:
                weaknesses.append("缺少比较分析")
            if reasoning_depth.analysis_levels < 2:
                weaknesses.append("分析层次不够深入")
        
        # Argument structure
        if argument_structure.score >= 0.7:
            if argument_structure.has_clear_structure:
                strengths.append("论证结构清晰有序")
            if argument_structure.paragraph_coherence >= 0.7:
                strengths.append("段落衔接自然流畅")
        else:
            if not argument_structure.has_clear_structure:
                weaknesses.append("论证结构不够清晰")
            if argument_structure.paragraph_coherence < 0.6:
                weaknesses.append("段落衔接有待改进")
        
        # Consistency
        if consistency.score >= 0.8:
            strengths.append("内部逻辑一致，无明显矛盾")
        elif consistency.contradictions:
            weaknesses.append(f"存在{len(consistency.contradictions)}处内部矛盾")
        
        # Logical fallacies
        if logical_fallacies.score >= 0.8:
            strengths.append("论证严谨，无明显逻辑谬误")
        elif logical_fallacies.fallacies:
            weaknesses.append(f"检测到{len(logical_fallacies.fallacies)}个逻辑谬误")
        
        return strengths, weaknesses
    
    def _generate_recommendations(
        self,
        reasoning_depth: ReasoningDepthResult,
        argument_structure: ArgumentStructureResult,
        consistency: ConsistencyResult,
        logical_fallacies: LogicalFallacyResult,
    ) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []
        
        # Reasoning depth recommendations
        if reasoning_depth.score < 0.7:
            if not reasoning_depth.has_causal_analysis:
                recommendations.append("增加因果关系分析，探讨现象背后的原因和影响")
            if not reasoning_depth.has_comparative_analysis:
                recommendations.append("加入比较分析，如历史对比或同行业对比")
            if reasoning_depth.analysis_levels < 2:
                recommendations.append("深化分析层次，从表面现象深入到深层原因和潜在影响")
        
        # Argument structure recommendations
        if argument_structure.score < 0.7:
            if not argument_structure.has_clear_structure:
                recommendations.append("优化文章结构，确保论点、论据、结论的逻辑顺序清晰")
            if argument_structure.paragraph_coherence < 0.6:
                recommendations.append("改善段落间的衔接，使用过渡句使论述更流畅")
        
        # Consistency recommendations
        if consistency.score < 0.8 and consistency.contradictions:
            recommendations.append("检查并解决内部矛盾，确保论述前后一致")
        
        # Logical fallacy recommendations
        if logical_fallacies.fallacies:
            for fallacy in logical_fallacies.fallacies[:2]:  # Show top 2
                recommendations.append(f"修正逻辑谬误：{fallacy.description}")
        
        return recommendations
