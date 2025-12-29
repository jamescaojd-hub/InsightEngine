"""
Example usage of the Reasoning and Logic Evaluator.

This script demonstrates how to use the evaluator to assess
the reasoning and logic quality of a financial article.
"""

import os
from dotenv import load_dotenv
from insight_engine.evaluators import ReasoningLogicEvaluator
from insight_engine.config import EvaluatorConfig


def main():
    """Main example function."""
    # Load environment variables
    load_dotenv()
    
    # Create configuration
    config = EvaluatorConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
    )
    
    # Initialize evaluator
    evaluator = ReasoningLogicEvaluator(config)
    
    # Example article (Chinese financial article)
    article_text = """
    特斯拉第三季度财报分析
    
    特斯拉公司发布了2024年第三季度财报，营收达到250亿美元，同比增长15%。这一增长主要来自于
    Model 3和Model Y的销量提升。根据数据显示，第三季度特斯拉交付了46万辆汽车，超出市场预期。
    
    从盈利能力来看，特斯拉的毛利率为19.8%，相比去年同期的25.1%有所下降。这主要是由于原材料
    成本上升和价格战的影响。与此同时，运营费用增加了12%，主要用于研发和工厂扩建。
    
    特斯拉在电动汽车市场的领先地位面临挑战。比亚迪等中国竞争对手快速崛起，在价格和技术上
    都有竞争力。特斯拉需要继续创新，保持技术优势，同时控制成本。
    
    展望未来，特斯拉计划在2025年推出更低价位的车型，以扩大市场份额。同时，自动驾驶技术的
    商业化将成为新的增长点。但是，监管环境和技术成熟度仍是关键挑战。
    
    综合来看，特斯拉虽然面临竞争压力和成本挑战，但其在技术创新和品牌影响力方面仍具优势。
    投资者应关注其成本控制能力和新产品推出情况。
    """
    
    print("=" * 60)
    print("Reasoning & Logic Evaluator - Example Usage")
    print("=" * 60)
    print("\nEvaluating article...")
    print("-" * 60)
    
    # Evaluate the article
    result = evaluator.evaluate(
        article_text=article_text,
        article_title="特斯拉第三季度财报分析"
    )
    
    # Print results
    print("\n" + result.get_summary())
    
    print("\n" + "=" * 60)
    print("Detailed Component Analysis")
    print("=" * 60)
    
    # Reasoning Depth Details
    print("\n1. Reasoning Depth Analysis:")
    print(f"   Score: {result.reasoning_depth.score:.2f}")
    print(f"   Has Causal Analysis: {result.reasoning_depth.has_causal_analysis}")
    print(f"   Has Comparative Analysis: {result.reasoning_depth.has_comparative_analysis}")
    print(f"   Analysis Levels: {result.reasoning_depth.analysis_levels}")
    print(f"   Explanation: {result.reasoning_depth.depth_explanation[:200]}...")
    
    # Argument Structure Details
    print("\n2. Argument Structure Analysis:")
    print(f"   Score: {result.argument_structure.score:.2f}")
    print(f"   Clear Structure: {result.argument_structure.has_clear_structure}")
    print(f"   Paragraph Coherence: {result.argument_structure.paragraph_coherence:.2f}")
    print(f"   Components Identified: {len(result.argument_structure.argument_components)}")
    
    # Consistency Details
    print("\n3. Consistency Analysis:")
    print(f"   Score: {result.consistency.score:.2f}")
    print(f"   Contradictions Found: {len(result.consistency.contradictions)}")
    if result.consistency.contradictions:
        for i, contradiction in enumerate(result.consistency.contradictions, 1):
            print(f"     {i}. {contradiction}")
    
    # Logical Fallacies Details
    print("\n4. Logical Fallacy Detection:")
    print(f"   Score: {result.logical_fallacies.score:.2f}")
    print(f"   Fallacies Found: {len(result.logical_fallacies.fallacies)}")
    if result.logical_fallacies.fallacies:
        for i, fallacy in enumerate(result.logical_fallacies.fallacies, 1):
            print(f"     {i}. Type: {fallacy.type}")
            print(f"        Location: {fallacy.location}")
            print(f"        Severity: {fallacy.severity:.2f}")
            print(f"        Description: {fallacy.description}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
