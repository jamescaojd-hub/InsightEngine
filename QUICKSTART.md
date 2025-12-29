# Quick Start Guide

5分钟快速上手 InsightEngine

## Step 1: 安装 (Installation)

```bash
# 克隆仓库
git clone https://github.com/jamescaojd-hub/InsightEngine.git
cd InsightEngine

# 安装依赖
pip install -r requirements.txt
```

## Step 2: 配置 (Configuration)

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env`，添加你的 OpenAI API Key：

```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

## Step 3: 运行示例 (Run Example)

```bash
python examples/basic_usage.py
```

## Step 4: 在你的代码中使用 (Use in Your Code)

```python
from insight_engine.evaluators import ReasoningLogicEvaluator
from insight_engine.config import EvaluatorConfig
import os
from dotenv import load_dotenv

# 加载配置
load_dotenv()
config = EvaluatorConfig(openai_api_key=os.getenv("OPENAI_API_KEY"))

# 创建评估器
evaluator = ReasoningLogicEvaluator(config)

# 评估文章
article = """
你的财经文章内容...
"""

result = evaluator.evaluate(article, "文章标题")

# 查看结果
print(result.get_summary())
print(f"\n总体评分: {result.overall_score:.2f}")
```

## 理解评分 (Understanding Scores)

- **0.8-1.0**: 优秀 - 推理严密，逻辑清晰
- **0.6-0.8**: 良好 - 整体不错，有改进空间
- **0.4-0.6**: 中等 - 需要较多改进
- **0.0-0.4**: 较差 - 存在明显问题

## 评估维度 (Evaluation Dimensions)

1. **推理深度** (Reasoning Depth) - 分析的深度和全面性
2. **论证结构** (Argument Structure) - 逻辑结构的清晰度
3. **一致性** (Consistency) - 内部是否矛盾
4. **逻辑严密性** (Logical Soundness) - 是否存在逻辑谬误

## 查看详细结果 (View Details)

```python
# 各维度评分
print(f"推理深度: {result.reasoning_depth.score:.2f}")
print(f"论证结构: {result.argument_structure.score:.2f}")
print(f"一致性: {result.consistency.score:.2f}")
print(f"逻辑严密性: {result.logical_fallacies.score:.2f}")

# 优缺点
print("\n优点:", result.strengths)
print("缺点:", result.weaknesses)
print("建议:", result.recommendations)

# 逻辑谬误
if result.logical_fallacies.fallacies:
    print("\n检测到的逻辑谬误:")
    for fallacy in result.logical_fallacies.fallacies:
        print(f"  - {fallacy.type}: {fallacy.description}")
```

## 批量评估 (Batch Evaluation)

```python
articles = [
    ("文章1", "内容1..."),
    ("文章2", "内容2..."),
    ("文章3", "内容3..."),
]

for title, content in articles:
    result = evaluator.evaluate(content, title)
    print(f"{title}: {result.overall_score:.2f}")
```

## 下一步 (Next Steps)

- 📖 阅读完整文档: [docs/USAGE.md](docs/USAGE.md)
- 🔧 查看API参考: [docs/API.md](docs/API.md)
- 🏗️ 了解架构设计: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 💡 查看更多示例: [examples/](examples/)

## 常见问题 (FAQ)

**Q: 评估需要多久？**
A: 通常20-60秒，取决于文章长度。

**Q: 支持哪些模型？**
A: 支持所有OpenAI模型，推荐使用 GPT-4 获得最佳效果。

**Q: 评分标准是什么？**
A: 基于推理深度、论证结构、一致性、逻辑严密性四个维度的加权平均。

**Q: 如何提高准确性？**
A: 使用 GPT-4 模型，降低 temperature (0.2-0.3)，确保文章格式清晰。

## 获取帮助 (Get Help)

遇到问题？

- 📝 查看文档: [docs/](docs/)
- 💬 提交Issue: [GitHub Issues](https://github.com/jamescaojd-hub/InsightEngine/issues)
- 📧 联系作者: 通过 GitHub

---

祝你使用愉快！Happy evaluating! 🚀
