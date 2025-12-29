"""
Advanced example: Evaluating multiple articles and comparing results.
"""

import os
from dotenv import load_dotenv
from insight_engine.evaluators import ReasoningLogicEvaluator
from insight_engine.config import EvaluatorConfig


def evaluate_multiple_articles():
    """Evaluate multiple articles and compare results."""
    # Load environment variables
    load_dotenv()
    
    # Create configuration
    config = EvaluatorConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
    )
    
    # Initialize evaluator
    evaluator = ReasoningLogicEvaluator(config)
    
    # Sample articles
    articles = {
        "Article A - Strong Reasoning": """
        中国新能源汽车市场深度分析
        
        一、市场现状与规模
        2024年前三季度，中国新能源汽车销量达到680万辆，同比增长37.5%。市场渗透率
        突破35%，远超全球平均水平的14%。这一增长背后有三个主要驱动因素：
        
        首先，政策支持持续加码。政府不仅延续了购置税减免政策至2027年，还在充电基础
        设施建设上投入超过500亿元。其次，技术进步显著。电池能量密度提升至300Wh/kg，
        成本下降至80美元/kWh，使得电动车在总拥有成本上开始优于燃油车。第三，消费者
        认知转变。随着产品成熟度提高和充电网络完善，消费者对电动车的接受度大幅提升。
        
        二、竞争格局演变
        与传统汽车市场不同，新能源市场呈现"百花齐放"的竞争态势。比亚迪以32%的市场
        份额领先，特斯拉、理想、蔚来等分别占据8-12%的份额。这种格局的形成有其内在
        逻辑：
        
        首先，技术路线多样化为不同企业提供了差异化竞争空间。比亚迪的刀片电池技术主打
        安全性和成本优势，而宁德时代的麒麟电池则强调能量密度。其次，智能化成为新的
        竞争维度。理想和小鹏在辅助驾驶功能上的投入，开辟了新的价值空间。
        
        但是，这种多元竞争格局可能不会长期持续。历史经验表明，汽车行业最终会走向
        集中。手机行业从百家争鸣到苹果、三星主导的演变路径可能会重演。当前的技术
        和商业模式差异化空间，可能在5-10年内收窄。
        
        三、未来趋势预判
        基于对供需两端的分析，我们认为未来3-5年中国新能源汽车市场将经历三个阶段：
        
        第一阶段（2024-2025）：渗透率快速提升。预计2025年新能源车渗透率将达到45-50%，
        销量突破1000万辆。这一判断基于：1）现有车型矩阵日益完善；2）充电基础设施
        持续改善；3）换购需求开始释放。
        
        第二阶段（2026-2027）：市场分化加剧。一方面，头部企业凭借规模效应和技术积累
        强化优势；另一方面，尾部企业面临淘汰压力。这种分化的必然性在于：规模化生产
        带来的成本优势是线性的，而研发投入的边际收益是递增的。
        
        第三阶段（2028-2030）：走向成熟稳定。新能源车市场占有率稳定在70-80%，增速
        放缓至个位数。此时竞争重点将从产品本身转向生态系统，包括充电网络、自动驾驶、
        车联网服务等。
        
        四、投资建议
        对于投资者而言，应采取差异化策略：
        
        在整车制造领域，关注具有技术护城河和规模效应的头部企业。评估标准包括：研发
        投入占比（建议>5%）、电池自主化程度、智能驾驶技术储备。
        
        在产业链上游，电池材料和核心零部件企业存在结构性机会。特别是具有全球竞争力
        的隔膜、电解液供应商，以及掌握IGBT、激光雷达等核心技术的企业。
        
        但需警惕两大风险：一是政策支持力度减弱可能带来的需求波动；二是全球化进程中
        可能遇到的贸易壁垒。建议保持5-10年的投资周期，而非短期博弈。
        """,
        
        "Article B - Weak Reasoning": """
        电动汽车市场看好
        
        电动汽车是未来趋势，所以我们应该投资电动汽车公司。特斯拉股价上涨了很多，说明
        电动汽车前景很好。
        
        比亚迪最近销量很高，因此比亚迪是最好的投资标的。中国政府支持新能源，所以新能源
        汽车一定会成功。
        
        传统汽车公司都要倒闭了，因为电动车会取代所有燃油车。马斯克说未来所有汽车都将
        是电动的，他是专家，所以这一定会发生。
        
        投资电动汽车不会有风险，因为这是大势所趋。我的朋友买了特斯拉股票赚了很多钱，
        所以这是个好投资。电池技术在进步，因此电动车会越来越便宜。
        
        总之，现在就应该买入电动汽车股票，不会错的。
        """,
    }
    
    print("=" * 80)
    print("Comparing Multiple Articles")
    print("=" * 80)
    
    results = {}
    
    for title, text in articles.items():
        print(f"\n\nEvaluating: {title}")
        print("-" * 80)
        result = evaluator.evaluate(article_text=text, article_title=title)
        results[title] = result
        
        print(f"\nOverall Score: {result.overall_score:.2f}")
        print(f"  - Reasoning Depth: {result.reasoning_depth.score:.2f}")
        print(f"  - Argument Structure: {result.argument_structure.score:.2f}")
        print(f"  - Consistency: {result.consistency.score:.2f}")
        print(f"  - Logical Soundness: {result.logical_fallacies.score:.2f}")
        
        if result.weaknesses:
            print(f"\nKey Weaknesses:")
            for weakness in result.weaknesses[:3]:
                print(f"  • {weakness}")
    
    # Comparison
    print("\n\n" + "=" * 80)
    print("Comparison Summary")
    print("=" * 80)
    
    for title, result in results.items():
        print(f"\n{title}:")
        print(f"  Overall: {result.overall_score:.2f}")
        print(f"  Strengths: {len(result.strengths)} identified")
        print(f"  Weaknesses: {len(result.weaknesses)} identified")
        print(f"  Fallacies: {len(result.logical_fallacies.fallacies)} detected")


if __name__ == "__main__":
    evaluate_multiple_articles()
