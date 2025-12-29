# Usage Guide

## 概述 (Overview)

本指南将帮助你快速上手使用 InsightEngine 评估财经文章的推理与逻辑质量。

This guide will help you get started with using InsightEngine to evaluate the reasoning and logic quality of financial articles.

## 安装 (Installation)

### 1. 克隆仓库 (Clone Repository)

```bash
git clone https://github.com/jamescaojd-hub/InsightEngine.git
cd InsightEngine
```

### 2. 安装依赖 (Install Dependencies)

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key (Configure API Key)

创建 `.env` 文件并配置你的 OpenAI API Key：

```bash
cp .env.example .env
# 编辑 .env 文件
```

`.env` 文件内容：
```
OPENAI_API_KEY=your_actual_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
```

## 基础使用 (Basic Usage)

### 方式一：使用默认配置 (Using Default Configuration)

```python
from insight_engine.evaluators import ReasoningLogicEvaluator
from insight_engine.config import EvaluatorConfig
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建配置
config = EvaluatorConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# 初始化评估器
evaluator = ReasoningLogicEvaluator(config)

# 准备文章
article_text = """
特斯拉第三季度财报分析

特斯拉公司发布了2024年第三季度财报...
"""

# 评估文章
result = evaluator.evaluate(
    article_text=article_text,
    article_title="特斯拉第三季度财报分析"
)

# 打印结果
print(result.get_summary())
```

### 方式二：自定义配置 (Custom Configuration)

```python
from insight_engine.evaluators import ReasoningLogicEvaluator
from insight_engine.config import EvaluatorConfig

config = EvaluatorConfig(
    openai_api_key="your_api_key",
    model_name="gpt-4-turbo-preview",  # 或 "gpt-3.5-turbo"
    temperature=0.3,  # 降低温度获得更稳定的评估
    min_reasoning_depth_score=0.6,
    min_structure_score=0.6,
    min_consistency_score=0.7,
)

evaluator = ReasoningLogicEvaluator(config)
result = evaluator.evaluate(article_text)
```

## 使用场景 (Use Cases)

### 场景 1：单篇文章评估 (Single Article Evaluation)

```python
# 评估单篇文章
result = evaluator.evaluate(article_text, "文章标题")

# 访问总体评分
print(f"总体评分: {result.overall_score:.2f}")

# 访问各维度评分
print(f"推理深度: {result.reasoning_depth.score:.2f}")
print(f"论证结构: {result.argument_structure.score:.2f}")
print(f"一致性: {result.consistency.score:.2f}")
print(f"逻辑严密性: {result.logical_fallacies.score:.2f}")

# 查看优缺点
print("\n优点:")
for strength in result.strengths:
    print(f"  ✓ {strength}")

print("\n缺点:")
for weakness in result.weaknesses:
    print(f"  ✗ {weakness}")

# 查看建议
print("\n改进建议:")
for i, rec in enumerate(result.recommendations, 1):
    print(f"  {i}. {rec}")
```

### 场景 2：批量评估 (Batch Evaluation)

```python
articles = {
    "Article 1": "文章1内容...",
    "Article 2": "文章2内容...",
    "Article 3": "文章3内容...",
}

results = {}
for title, text in articles.items():
    print(f"评估: {title}")
    result = evaluator.evaluate(text, title)
    results[title] = result
    print(f"  评分: {result.overall_score:.2f}\n")

# 找出最高分和最低分的文章
best = max(results.items(), key=lambda x: x[1].overall_score)
worst = min(results.items(), key=lambda x: x[1].overall_score)

print(f"最佳文章: {best[0]} (评分: {best[1].overall_score:.2f})")
print(f"最差文章: {worst[0]} (评分: {worst[1].overall_score:.2f})")
```

### 场景 3：质量把关 (Quality Control)

```python
def check_article_quality(article_text, min_score=0.6):
    """检查文章是否达到质量标准"""
    result = evaluator.evaluate(article_text)
    
    if result.overall_score >= min_score:
        print("✓ 文章通过质量检查")
        return True
    else:
        print("✗ 文章未达到质量标准")
        print("\n需要改进的地方:")
        for weakness in result.weaknesses:
            print(f"  • {weakness}")
        print("\n建议:")
        for rec in result.recommendations:
            print(f"  • {rec}")
        return False

# 使用
article_passed = check_article_quality(article_text, min_score=0.7)
```

### 场景 4：详细分析报告 (Detailed Analysis Report)

```python
def generate_detailed_report(result):
    """生成详细的评估报告"""
    report = []
    
    report.append("=" * 80)
    report.append("详细评估报告")
    report.append("=" * 80)
    
    if result.article_title:
        report.append(f"\n文章标题: {result.article_title}")
    
    report.append(f"\n总体评分: {result.overall_score:.2f}/1.00")
    report.append(f"评级: {'优秀' if result.overall_score >= 0.8 else '良好' if result.overall_score >= 0.6 else '需改进'}")
    
    # 各维度详细分析
    report.append("\n" + "-" * 80)
    report.append("1. 推理深度分析")
    report.append("-" * 80)
    report.append(f"评分: {result.reasoning_depth.score:.2f}")
    report.append(f"因果分析: {'有' if result.reasoning_depth.has_causal_analysis else '无'}")
    report.append(f"比较分析: {'有' if result.reasoning_depth.has_comparative_analysis else '无'}")
    report.append(f"分析层次: {result.reasoning_depth.analysis_levels}层")
    report.append(f"说明: {result.reasoning_depth.depth_explanation}")
    
    report.append("\n" + "-" * 80)
    report.append("2. 论证结构分析")
    report.append("-" * 80)
    report.append(f"评分: {result.argument_structure.score:.2f}")
    report.append(f"结构清晰: {'是' if result.argument_structure.has_clear_structure else '否'}")
    report.append(f"段落连贯性: {result.argument_structure.paragraph_coherence:.2f}")
    report.append(f"论证组件数: {len(result.argument_structure.argument_components)}")
    
    if result.argument_structure.argument_components:
        report.append("\n识别的论证组件:")
        for comp in result.argument_structure.argument_components[:5]:  # 显示前5个
            report.append(f"  • {comp.type}: {comp.content[:50]}...")
    
    report.append("\n" + "-" * 80)
    report.append("3. 一致性检查")
    report.append("-" * 80)
    report.append(f"评分: {result.consistency.score:.2f}")
    report.append(f"矛盾数量: {len(result.consistency.contradictions)}")
    
    if result.consistency.contradictions:
        report.append("\n检测到的矛盾:")
        for i, contradiction in enumerate(result.consistency.contradictions, 1):
            report.append(f"  {i}. {contradiction}")
    
    report.append("\n" + "-" * 80)
    report.append("4. 逻辑谬误检测")
    report.append("-" * 80)
    report.append(f"评分: {result.logical_fallacies.score:.2f}")
    report.append(f"谬误数量: {len(result.logical_fallacies.fallacies)}")
    
    if result.logical_fallacies.fallacies:
        report.append("\n检测到的逻辑谬误:")
        for i, fallacy in enumerate(result.logical_fallacies.fallacies, 1):
            report.append(f"  {i}. 类型: {fallacy.type}")
            report.append(f"     位置: {fallacy.location}")
            report.append(f"     严重程度: {fallacy.severity:.2f}")
            report.append(f"     说明: {fallacy.description}")
    
    # 总结
    report.append("\n" + "=" * 80)
    report.append("总结")
    report.append("=" * 80)
    
    if result.strengths:
        report.append("\n优点:")
        for strength in result.strengths:
            report.append(f"  ✓ {strength}")
    
    if result.weaknesses:
        report.append("\n缺点:")
        for weakness in result.weaknesses:
            report.append(f"  ✗ {weakness}")
    
    if result.recommendations:
        report.append("\n改进建议:")
        for i, rec in enumerate(result.recommendations, 1):
            report.append(f"  {i}. {rec}")
    
    return "\n".join(report)

# 使用
result = evaluator.evaluate(article_text, "文章标题")
detailed_report = generate_detailed_report(result)
print(detailed_report)

# 保存到文件
with open("evaluation_report.txt", "w", encoding="utf-8") as f:
    f.write(detailed_report)
```

## 运行示例 (Run Examples)

项目包含两个示例脚本：

### 基础示例 (Basic Example)

```bash
python examples/basic_usage.py
```

这个示例展示了如何评估单篇文章并查看详细结果。

### 高级示例 (Advanced Example)

```bash
python examples/advanced_usage.py
```

这个示例展示了如何评估多篇文章并进行比较。

## 最佳实践 (Best Practices)

### 1. 文章长度建议

- **最佳长度**: 500-5000字
- **最短长度**: 至少200字，否则评估可能不够准确
- **最长长度**: 不超过10000字，避免超出token限制

### 2. 模型选择

- **GPT-4**: 推荐用于正式评估，准确度最高
- **GPT-3.5-turbo**: 可用于初步筛选，速度快但准确度略低

### 3. 评分阈值建议

- **优秀**: 0.8+
- **良好**: 0.6-0.8
- **需改进**: < 0.6

### 4. API 使用注意事项

- 每次评估调用4次API（每个agent一次）
- 注意API配额和速率限制
- 对于大量文章，建议添加延迟或使用批处理

### 5. 错误处理

```python
try:
    result = evaluator.evaluate(article_text)
except Exception as e:
    print(f"评估失败: {e}")
    # 处理错误
```

## 常见问题 (FAQ)

### Q1: 评估需要多长时间？
A: 通常20-60秒，取决于文章长度和API响应速度。

### Q2: 支持哪些语言？
A: 目前主要支持中文财经文章，但理论上可以评估任何语言的文章。

### Q3: 如何提高评估准确性？
A: 
- 使用GPT-4模型
- 确保文章格式清晰
- 提供完整的文章内容

### Q4: 评估结果是否稳定？
A: 由于使用LLM，结果可能有轻微波动。建议使用较低的temperature（0.2-0.3）以获得更稳定的结果。

### Q5: 如何解读评分？
A: 
- 0.8-1.0: 优秀，推理逻辑非常严密
- 0.6-0.8: 良好，有改进空间
- 0.4-0.6: 中等，需要较大改进
- 0.0-0.4: 较差，存在明显问题

## 进阶用法 (Advanced Usage)

### 自定义权重

如果你想调整各维度的权重，可以修改 `reasoning_logic_evaluator.py` 中的 `_calculate_overall_score` 方法。

### 添加新的评估维度

参考 `docs/ARCHITECTURE.md` 了解如何扩展系统。

### 集成到现有系统

```python
class ArticleQualityChecker:
    def __init__(self):
        self.evaluator = ReasoningLogicEvaluator(config)
    
    def check_before_publish(self, article):
        result = self.evaluator.evaluate(article.content)
        if result.overall_score < 0.6:
            return False, result.recommendations
        return True, []
```

## 获取帮助 (Getting Help)

如果遇到问题：

1. 查看文档: `docs/` 目录
2. 查看示例: `examples/` 目录
3. 提交Issue: GitHub Issues页面

## 下一步 (Next Steps)

- 查看 [API文档](docs/API.md) 了解详细的API接口
- 查看 [架构文档](docs/ARCHITECTURE.md) 了解系统设计
- 尝试运行示例代码
- 根据你的需求自定义配置
