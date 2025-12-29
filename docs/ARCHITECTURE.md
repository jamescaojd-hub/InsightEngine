# Architecture Overview

## System Design

InsightEngine uses a multi-agent architecture to evaluate financial articles across multiple dimensions of reasoning and logic quality.

## Agent-Based Design

### Why Multi-Agent?

1. **Specialization**: Each agent focuses on a specific evaluation dimension
2. **Modularity**: Easy to add, remove, or modify individual agents
3. **Parallelization**: Agents can work independently and in parallel
4. **Maintainability**: Clear separation of concerns

### Agent Types

#### 1. ReasoningDepthAgent
**Responsibility**: Evaluate the depth and thoroughness of reasoning

**Analysis Criteria**:
- Multi-angle analysis
- Multi-level depth
- Causal relationships
- Comparative analysis
- Logical inference quality

**Output**: 
- Score (0.0-1.0)
- Boolean flags for analysis types
- Number of analysis levels detected
- Detailed explanation

#### 2. ArgumentStructureAgent
**Responsibility**: Analyze logical structure and coherence

**Analysis Criteria**:
- Logical ordering
- Paragraph coherence
- Claim-evidence-conclusion relationships
- Overall structure clarity

**Output**:
- Score (0.0-1.0)
- Structure clarity flag
- Paragraph coherence score
- List of identified argument components
- Detailed explanation

#### 3. LogicalFallacyAgent
**Responsibility**: Detect logical fallacies

**Detectable Fallacies**:
- Overgeneralization (以偏概全)
- Causal reversal (因果倒置)
- False dilemma (非此即彼)
- Slippery slope (滑坡谬误)
- Circular reasoning (循环论证)
- Hasty generalization (轻率概括)
- Post hoc (后此谬误)
- Ad hominem (人身攻击)
- Strawman (稻草人谬误)

**Output**:
- Score (0.0-1.0, where 1.0 means no fallacies)
- List of detected fallacies with locations and severity
- Detailed explanation

#### 4. ConsistencyAgent
**Responsibility**: Check internal consistency

**Analysis Criteria**:
- Argument consistency
- Data consistency
- Position consistency
- Logical coherence
- Conclusion-evidence alignment

**Output**:
- Score (0.0-1.0)
- List of detected contradictions
- Detailed explanation

## Data Flow

```
Input: Article Text
    |
    v
ReasoningLogicEvaluator (Orchestrator)
    |
    +-- ReasoningDepthAgent
    |
    +-- ArgumentStructureAgent
    |
    +-- LogicalFallacyAgent
    |
    +-- ConsistencyAgent
    |
    v
Score Aggregation & Analysis
    |
    v
Output: ReasoningLogicEvaluation
```

## Component Interaction

### 1. Initialization Phase
- User creates `EvaluatorConfig` with API keys and settings
- `ReasoningLogicEvaluator` initializes all agents with the config
- Each agent creates its own LLM client

### 2. Evaluation Phase
- User calls `evaluator.evaluate(article_text)`
- Orchestrator dispatches article to each agent
- Each agent:
  - Constructs a specialized prompt
  - Calls LLM for analysis
  - Parses and validates response
  - Returns structured results
- Orchestrator collects all results

### 3. Aggregation Phase
- Calculate weighted overall score
- Identify strengths and weaknesses
- Generate recommendations
- Create final evaluation object

### 4. Output Phase
- Return `ReasoningLogicEvaluation` object
- User can call `get_summary()` for readable output
- User can access individual component scores

## Extension Points

### Adding New Agents

To add a new evaluation dimension:

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `analyze()` method
3. Define appropriate data models in `models/evaluation.py`
4. Add the agent to `ReasoningLogicEvaluator`
5. Update score calculation to include new dimension

Example:
```python
class NewDimensionAgent(BaseAgent):
    def analyze(self, article_text: str) -> Dict:
        # Implement analysis logic
        pass
```

### Customizing Prompts

Each agent's prompt can be customized by modifying the `_create_analysis_prompt()` method.

### Adjusting Weights

Modify the weights in `_calculate_overall_score()` to change the relative importance of different dimensions:

```python
weights = {
    "reasoning_depth": 0.30,
    "argument_structure": 0.30,
    "consistency": 0.25,
    "logical_fallacies": 0.15,
}
```

## Performance Considerations

### API Calls
- Each evaluation makes 4 LLM API calls (one per agent)
- Consider implementing caching for repeated evaluations
- Use batch processing for multiple articles

### Response Times
- Typical evaluation: 20-60 seconds
- Depends on article length and LLM response time
- Can be optimized with:
  - Parallel agent execution
  - Smaller context windows
  - Faster models for less critical dimensions

### Cost Optimization
- Use GPT-4 for critical evaluations
- Use GPT-3.5-turbo for preliminary screening
- Implement result caching
- Truncate very long articles

## Error Handling

### Graceful Degradation
- If an agent fails, it returns a default score
- Other agents continue to function
- Final evaluation includes partial results

### Retry Logic
- Configurable retry attempts for API failures
- Exponential backoff between retries
- Detailed error logging

## Future Enhancements

### Planned Features
1. **Batch Processing**: Evaluate multiple articles efficiently
2. **Incremental Updates**: Update evaluations as articles are edited
3. **Custom Rubrics**: Allow users to define custom evaluation criteria
4. **Visualization**: Generate visual reports of evaluation results
5. **Comparative Analysis**: Compare multiple articles side-by-side
6. **Historical Tracking**: Track evaluation scores over time
7. **Integration APIs**: REST API for easy integration
8. **Fine-tuned Models**: Train specialized models for financial domain
