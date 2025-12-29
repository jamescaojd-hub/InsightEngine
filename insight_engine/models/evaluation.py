"""
Data models for the reasoning and logic evaluator.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum


class LogicalFallacyType(str, Enum):
    """Types of logical fallacies."""
    OVERGENERALIZATION = "overgeneralization"  # 以偏概全
    CAUSAL_REVERSAL = "causal_reversal"  # 因果倒置
    FALSE_DILEMMA = "false_dilemma"  # 非此即彼
    SLIPPERY_SLOPE = "slippery_slope"  # 滑坡谬误
    AD_HOMINEM = "ad_hominem"  # 人身攻击
    CIRCULAR_REASONING = "circular_reasoning"  # 循环论证
    STRAWMAN = "strawman"  # 稻草人谬误
    HASTY_GENERALIZATION = "hasty_generalization"  # 轻率概括
    POST_HOC = "post_hoc"  # 后此谬误


class LogicalFallacy(BaseModel):
    """Detected logical fallacy in the article."""
    type: LogicalFallacyType
    location: str = Field(description="Location in the article where the fallacy occurs")
    description: str = Field(description="Description of the fallacy")
    severity: float = Field(ge=0.0, le=1.0, description="Severity score (0-1)")


class ArgumentComponent(BaseModel):
    """Component of an argument (claim, evidence, reasoning)."""
    type: str = Field(description="Type: claim, evidence, reasoning, conclusion")
    content: str = Field(description="The actual content")
    location: str = Field(description="Location in the article")


class ReasoningDepthResult(BaseModel):
    """Result of reasoning depth analysis."""
    score: float = Field(ge=0.0, le=1.0, description="Overall reasoning depth score (0-1)")
    has_causal_analysis: bool = Field(description="Whether the article contains causal analysis")
    has_comparative_analysis: bool = Field(description="Whether the article contains comparative analysis")
    analysis_levels: int = Field(description="Number of analysis levels detected")
    depth_explanation: str = Field(description="Explanation of the depth assessment")


class ArgumentStructureResult(BaseModel):
    """Result of argument structure analysis."""
    score: float = Field(ge=0.0, le=1.0, description="Overall structure quality score (0-1)")
    has_clear_structure: bool = Field(description="Whether the article has a clear logical structure")
    paragraph_coherence: float = Field(ge=0.0, le=1.0, description="Paragraph coherence score")
    argument_components: List[ArgumentComponent] = Field(default_factory=list, description="Identified argument components")
    structure_explanation: str = Field(description="Explanation of structure quality")


class ConsistencyResult(BaseModel):
    """Result of consistency analysis."""
    score: float = Field(ge=0.0, le=1.0, description="Overall consistency score (0-1)")
    contradictions: List[str] = Field(default_factory=list, description="Detected contradictions")
    consistency_explanation: str = Field(description="Explanation of consistency assessment")


class LogicalFallacyResult(BaseModel):
    """Result of logical fallacy detection."""
    score: float = Field(ge=0.0, le=1.0, description="Overall score (1 - fallacy severity)")
    fallacies: List[LogicalFallacy] = Field(default_factory=list, description="Detected logical fallacies")
    fallacy_explanation: str = Field(description="Explanation of fallacies found")


class ReasoningLogicEvaluation(BaseModel):
    """Complete evaluation result for reasoning and logic."""
    article_title: Optional[str] = Field(default=None, description="Title of the article")
    overall_score: float = Field(ge=0.0, le=1.0, description="Overall reasoning and logic score (0-1)")
    
    # Component scores
    reasoning_depth: ReasoningDepthResult
    argument_structure: ArgumentStructureResult
    consistency: ConsistencyResult
    logical_fallacies: LogicalFallacyResult
    
    # Summary
    strengths: List[str] = Field(default_factory=list, description="Identified strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Identified weaknesses")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for improvement")
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the evaluation."""
        summary = f"Reasoning & Logic Evaluation Summary\n"
        summary += f"{'=' * 50}\n"
        if self.article_title:
            summary += f"Article: {self.article_title}\n\n"
        
        summary += f"Overall Score: {self.overall_score:.2f}/1.00\n\n"
        
        summary += f"Component Scores:\n"
        summary += f"  - Reasoning Depth: {self.reasoning_depth.score:.2f}\n"
        summary += f"  - Argument Structure: {self.argument_structure.score:.2f}\n"
        summary += f"  - Consistency: {self.consistency.score:.2f}\n"
        summary += f"  - Logical Soundness: {self.logical_fallacies.score:.2f}\n\n"
        
        if self.strengths:
            summary += f"Strengths:\n"
            for strength in self.strengths:
                summary += f"  ✓ {strength}\n"
            summary += "\n"
        
        if self.weaknesses:
            summary += f"Weaknesses:\n"
            for weakness in self.weaknesses:
                summary += f"  ✗ {weakness}\n"
            summary += "\n"
        
        if self.recommendations:
            summary += f"Recommendations:\n"
            for i, rec in enumerate(self.recommendations, 1):
                summary += f"  {i}. {rec}\n"
        
        return summary
