# InsightEngine

A professional human-level engine for producing insights into the latest trends, with a focus on evaluating the reasoning and logic quality of financial articles.

## 概述 (Overview)

InsightEngine 是一个基于大语言模型（LLM）的智能评估系统，专门用于评估财经文章的推理与逻辑质量。该系统采用多智能体（Multi-Agent）架构，从多个维度对文章进行深度分析。

InsightEngine is an intelligent evaluation system based on Large Language Models (LLMs), specifically designed to assess the reasoning and logic quality of financial articles. The system uses a multi-agent architecture to provide in-depth analysis across multiple dimensions.

## 核心功能 (Core Features)

### 1. 推理深度分析 (Reasoning Depth Analysis)
- 多角度分析检测
- 多层次分析评估
- 因果关系识别
- 比较分析检测

### 2. 论证结构分析 (Argument Structure Analysis)
- 逻辑次序评估
- 段落连贯性分析
- 论点-论据-结论关系验证
- 论证完整性检查

### 3. 逻辑谬误检测 (Logical Fallacy Detection)
- 以偏概全 (Overgeneralization)
- 因果倒置 (Causal Reversal)
- 非此即彼 (False Dilemma)
- 滑坡谬误 (Slippery Slope)
- 循环论证 (Circular Reasoning)
- 其他常见逻辑谬误

### 4. 一致性检查 (Consistency Check)
- 内部矛盾检测
- 论述一致性验证
- 数据一致性检查

## 架构设计 (Architecture)

系统采用模块化设计，包含以下核心组件：

```
insight_engine/
├── agents/              # 专业评估代理
│   ├── base_agent.py
│   ├── reasoning_depth_agent.py
│   ├── argument_structure_agent.py
│   ├── logical_fallacy_agent.py
│   └── consistency_agent.py
├── evaluators/          # 主评估器
│   └── reasoning_logic_evaluator.py
├── models/              # 数据模型
│   └── evaluation.py
├── utils/               # 工具函数
│   └── text_utils.py
└── config.py            # 配置管理
```

## 安装 (Installation)

### 前置要求 (Prerequisites)
- Python 3.8+
- OpenAI API Key

### 安装步骤 (Setup Steps)

1. 克隆仓库：
```bash
git clone https://github.com/jamescaojd-hub/InsightEngine.git
cd InsightEngine
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 OpenAI API Key
```

## 快速开始 (Quick Start)

### 基础用法

```python
from insight_engine.evaluators import ReasoningLogicEvaluator
from insight_engine.config import EvaluatorConfig
import os

# 创建配置
config = EvaluatorConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4-turbo-preview",
)

# 初始化评估器
evaluator = ReasoningLogicEvaluator(config)

# 评估文章
article_text = """
你的财经文章内容...
"""

result = evaluator.evaluate(
    article_text=article_text,
    article_title="文章标题"
)

# 输出评估结果
print(result.get_summary())
```

### 完整示例

查看 `examples/` 目录获取更多示例：
- `basic_usage.py` - 基础使用示例
- `advanced_usage.py` - 高级用法，包括多篇文章对比

## 评估维度详解 (Evaluation Dimensions)

### 1. 推理深度 (Reasoning Depth)
评分标准：
- 0.8-1.0: 深入、多层次、多角度分析
- 0.6-0.8: 有一定深度，但可以更全面
- 0.4-0.6: 分析较浅，主要是事实罗列
- 0.0-0.4: 缺乏深度分析

### 2. 论证结构 (Argument Structure)
评分标准：
- 0.8-1.0: 结构清晰，逻辑严密，论证完整
- 0.6-0.8: 结构基本合理，有少量改进空间
- 0.4-0.6: 结构有待优化，论证链条不够紧密
- 0.0-0.4: 结构混乱，缺乏逻辑性

### 3. 一致性 (Consistency)
评分标准：
- 0.9-1.0: 完全一致，无矛盾
- 0.7-0.9: 基本一致，有极少量不一致
- 0.5-0.7: 存在一些不一致之处
- 0.0-0.5: 有明显矛盾

### 4. 逻辑谬误 (Logical Fallacies)
评分标准：
- 0.9-1.0: 无明显逻辑谬误
- 0.7-0.9: 有轻微谬误，影响不大
- 0.5-0.7: 有明显谬误，需要修正
- 0.0-0.5: 严重逻辑谬误

## API 文档 (API Documentation)

### ReasoningLogicEvaluator

主要评估器类。

#### 初始化
```python
evaluator = ReasoningLogicEvaluator(config: EvaluatorConfig)
```

#### 评估方法
```python
result = evaluator.evaluate(
    article_text: str,
    article_title: Optional[str] = None
) -> ReasoningLogicEvaluation
```

**参数：**
- `article_text`: 要评估的文章文本
- `article_title`: 文章标题（可选）

**返回：**
- `ReasoningLogicEvaluation` 对象，包含完整的评估结果

### ReasoningLogicEvaluation

评估结果对象。

**主要属性：**
- `overall_score`: 总体评分 (0.0-1.0)
- `reasoning_depth`: 推理深度分析结果
- `argument_structure`: 论证结构分析结果
- `consistency`: 一致性检查结果
- `logical_fallacies`: 逻辑谬误检测结果
- `strengths`: 优点列表
- `weaknesses`: 缺点列表
- `recommendations`: 改进建议列表

**主要方法：**
- `get_summary()`: 获取评估结果的可读摘要

## 配置选项 (Configuration Options)

可以通过 `EvaluatorConfig` 类自定义评估器配置：

```python
config = EvaluatorConfig(
    # OpenAI 配置
    openai_api_key="your-api-key",
    model_name="gpt-4-turbo-preview",  # 或其他模型
    temperature=0.3,  # 0.0-1.0
    
    # 评估阈值
    min_reasoning_depth_score=0.6,
    min_structure_score=0.6,
    min_consistency_score=0.7,
    
    # 代理配置
    max_retries=3,
    timeout=60,
)
```

## 最佳实践 (Best Practices)

1. **文章长度**：建议评估的文章长度在 500-5000 字之间，以获得最佳结果
2. **API 配额**：每次评估会调用多次 API，请注意 API 使用限制
3. **模型选择**：推荐使用 GPT-4 或更高版本以获得更准确的评估
4. **批量评估**：对于大量文章，建议添加适当的延迟以避免速率限制

## 技术原理 (Technical Approach)

InsightEngine 采用基于 LLM 的多智能体架构：

1. **专业化代理**：每个代理专注于特定的评估维度
2. **并行分析**：多个代理可以并行工作，提高效率
3. **结构化输出**：使用 JSON 格式确保输出的一致性和可解析性
4. **加权评分**：综合多个维度的评分，计算总体质量分数

## 贡献指南 (Contributing)

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证 (License)

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式 (Contact)

项目链接: [https://github.com/jamescaojd-hub/InsightEngine](https://github.com/jamescaojd-hub/InsightEngine)

## 致谢 (Acknowledgments)

- OpenAI GPT-4 提供强大的语言理解能力
- LangChain 框架简化了 LLM 应用开发
- 财经分析领域的最佳实践和评估标准
