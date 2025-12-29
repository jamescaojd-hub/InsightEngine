# API Reference

## Core Classes

### ReasoningLogicEvaluator

Main evaluator class that orchestrates all evaluation agents.

#### Constructor

```python
ReasoningLogicEvaluator(config: Optional[EvaluatorConfig] = None)
```

**Parameters**:
- `config` (Optional[EvaluatorConfig]): Configuration object. If None, uses default configuration.

**Example**:
```python
from insight_engine.evaluators import ReasoningLogicEvaluator
from insight_engine.config import EvaluatorConfig

config = EvaluatorConfig(openai_api_key="your-key")
evaluator = ReasoningLogicEvaluator(config)
```

#### Methods

##### evaluate()

Evaluate an article's reasoning and logic quality.

```python
evaluate(
    article_text: str,
    article_title: Optional[str] = None
) -> ReasoningLogicEvaluation
```

**Parameters**:
- `article_text` (str): The full text of the article to evaluate
- `article_title` (Optional[str]): Title of the article (optional)

**Returns**:
- `ReasoningLogicEvaluation`: Complete evaluation result object

**Example**:
```python
result = evaluator.evaluate(
    article_text="Your article content...",
    article_title="Article Title"
)
```

---

### EvaluatorConfig

Configuration class for the evaluator.

#### Constructor

```python
EvaluatorConfig(
    openai_api_key: Optional[str] = None,
    model_name: str = "gpt-4-turbo-preview",
    temperature: float = 0.3,
    min_reasoning_depth_score: float = 0.6,
    min_structure_score: float = 0.6,
    min_consistency_score: float = 0.7,
    max_retries: int = 3,
    timeout: int = 60
)
```

**Parameters**:
- `openai_api_key` (Optional[str]): OpenAI API key
- `model_name` (str): LLM model to use (default: "gpt-4-turbo-preview")
- `temperature` (float): Temperature for generation (0.0-1.0, default: 0.3)
- `min_reasoning_depth_score` (float): Minimum acceptable reasoning depth score
- `min_structure_score` (float): Minimum acceptable structure score
- `min_consistency_score` (float): Minimum acceptable consistency score
- `max_retries` (int): Maximum retry attempts for API calls
- `timeout` (int): Timeout in seconds for API calls

---

## Data Models

### ReasoningLogicEvaluation

Complete evaluation result.

#### Attributes

- `article_title` (Optional[str]): Title of the evaluated article
- `overall_score` (float): Overall score (0.0-1.0)
- `reasoning_depth` (ReasoningDepthResult): Reasoning depth analysis
- `argument_structure` (ArgumentStructureResult): Structure analysis
- `consistency` (ConsistencyResult): Consistency check results
- `logical_fallacies` (LogicalFallacyResult): Fallacy detection results
- `strengths` (List[str]): Identified strengths
- `weaknesses` (List[str]): Identified weaknesses
- `recommendations` (List[str]): Improvement recommendations

#### Methods

##### get_summary()

Get a human-readable summary of the evaluation.

```python
get_summary() -> str
```

**Returns**:
- `str`: Formatted summary text

**Example**:
```python
summary = result.get_summary()
print(summary)
```

---

### ReasoningDepthResult

Reasoning depth analysis result.

#### Attributes

- `score` (float): Depth score (0.0-1.0)
- `has_causal_analysis` (bool): Whether causal analysis is present
- `has_comparative_analysis` (bool): Whether comparative analysis is present
- `analysis_levels` (int): Number of analysis levels (1-5)
- `depth_explanation` (str): Detailed explanation

---

### ArgumentStructureResult

Argument structure analysis result.

#### Attributes

- `score` (float): Structure quality score (0.0-1.0)
- `has_clear_structure` (bool): Whether structure is clear
- `paragraph_coherence` (float): Paragraph coherence score (0.0-1.0)
- `argument_components` (List[ArgumentComponent]): Identified components
- `structure_explanation` (str): Detailed explanation

---

### ConsistencyResult

Consistency analysis result.

#### Attributes

- `score` (float): Consistency score (0.0-1.0)
- `contradictions` (List[str]): Detected contradictions
- `consistency_explanation` (str): Detailed explanation

---

### LogicalFallacyResult

Logical fallacy detection result.

#### Attributes

- `score` (float): Score (0.0-1.0, higher is better)
- `fallacies` (List[LogicalFallacy]): Detected fallacies
- `fallacy_explanation` (str): Detailed explanation

---

### LogicalFallacy

A detected logical fallacy.

#### Attributes

- `type` (LogicalFallacyType): Type of fallacy
- `location` (str): Location in the article
- `description` (str): Description of the fallacy
- `severity` (float): Severity score (0.0-1.0)

---

### LogicalFallacyType

Enumeration of logical fallacy types.

#### Values

- `OVERGENERALIZATION`: 以偏概全
- `CAUSAL_REVERSAL`: 因果倒置
- `FALSE_DILEMMA`: 非此即彼
- `SLIPPERY_SLOPE`: 滑坡谬误
- `AD_HOMINEM`: 人身攻击
- `CIRCULAR_REASONING`: 循环论证
- `STRAWMAN`: 稻草人谬误
- `HASTY_GENERALIZATION`: 轻率概括
- `POST_HOC`: 后此谬误

---

### ArgumentComponent

A component of an argument.

#### Attributes

- `type` (str): Component type ("claim", "evidence", "reasoning", "conclusion")
- `content` (str): The actual content
- `location` (str): Location in the article

---

## Agent Classes

### BaseAgent

Abstract base class for all agents.

#### Methods

##### analyze()

Analyze an article (must be implemented by subclasses).

```python
analyze(article_text: str) -> dict
```

---

### ReasoningDepthAgent

Agent for analyzing reasoning depth.

Inherits from `BaseAgent`.

---

### ArgumentStructureAgent

Agent for analyzing argument structure.

Inherits from `BaseAgent`.

---

### LogicalFallacyAgent

Agent for detecting logical fallacies.

Inherits from `BaseAgent`.

---

### ConsistencyAgent

Agent for checking consistency.

Inherits from `BaseAgent`.

---

## Utility Functions

### truncate_text()

Truncate text to a maximum length.

```python
truncate_text(text: str, max_length: int = 100) -> str
```

### extract_article_sections()

Extract sections from an article.

```python
extract_article_sections(article_text: str) -> dict
```

**Returns**:
Dictionary with keys: "title", "introduction", "body", "conclusion"
