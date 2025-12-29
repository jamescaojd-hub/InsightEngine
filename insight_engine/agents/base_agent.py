"""
Base agent implementation for the reasoning evaluator.
"""

from typing import Optional
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from insight_engine.config import EvaluatorConfig


class BaseAgent(ABC):
    """Base class for all evaluation agents."""
    
    def __init__(self, config: EvaluatorConfig):
        """
        Initialize the base agent.
        
        Args:
            config: Evaluator configuration
        """
        self.config = config
        self.llm = ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            api_key=config.openai_api_key,
        )
    
    @abstractmethod
    def analyze(self, article_text: str) -> dict:
        """
        Analyze the article and return results.
        
        Args:
            article_text: The article text to analyze
            
        Returns:
            Analysis results as a dictionary
        """
        pass
    
    def _create_prompt(self, template: str, **kwargs) -> str:
        """
        Create a prompt from a template.
        
        Args:
            template: Prompt template
            **kwargs: Variables to fill in the template
            
        Returns:
            Formatted prompt
        """
        prompt = ChatPromptTemplate.from_template(template)
        return prompt.format(**kwargs)
