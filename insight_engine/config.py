"""
Configuration module for the reasoning and logic evaluator.
"""

from typing import Optional
from pydantic import BaseModel, Field


class EvaluatorConfig(BaseModel):
    """Configuration for the reasoning and logic evaluator."""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    model_name: str = Field(default="gpt-4-turbo-preview", description="LLM model to use")
    temperature: float = Field(default=0.3, description="Temperature for LLM generation")
    
    # Evaluation Configuration
    min_reasoning_depth_score: float = Field(default=0.6, description="Minimum acceptable reasoning depth score")
    min_structure_score: float = Field(default=0.6, description="Minimum acceptable structure score")
    min_consistency_score: float = Field(default=0.7, description="Minimum acceptable consistency score")
    
    # Agent Configuration
    max_retries: int = Field(default=3, description="Maximum retries for agent calls")
    timeout: int = Field(default=60, description="Timeout for agent calls in seconds")
    
    class Config:
        arbitrary_types_allowed = True


# Default configuration
DEFAULT_CONFIG = EvaluatorConfig()
