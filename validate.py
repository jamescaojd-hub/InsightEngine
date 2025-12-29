"""
Validation script to check that all modules can be imported correctly.
"""

def validate_imports():
    """Validate that all modules can be imported."""
    print("Validating InsightEngine imports...")
    
    try:
        # Test core imports
        print("  ✓ Testing core module...")
        import insight_engine
        print(f"    Version: {insight_engine.__version__}")
        
        # Test config
        print("  ✓ Testing config module...")
        from insight_engine.config import EvaluatorConfig, DEFAULT_CONFIG
        
        # Test models
        print("  ✓ Testing models module...")
        from insight_engine.models import (
            LogicalFallacyType,
            LogicalFallacy,
            ArgumentComponent,
            ReasoningDepthResult,
            ArgumentStructureResult,
            ConsistencyResult,
            LogicalFallacyResult,
            ReasoningLogicEvaluation,
        )
        
        # Test agents
        print("  ✓ Testing agents module...")
        from insight_engine.agents import (
            BaseAgent,
            ReasoningDepthAgent,
            ArgumentStructureAgent,
            LogicalFallacyAgent,
            ConsistencyAgent,
        )
        
        # Test evaluators
        print("  ✓ Testing evaluators module...")
        from insight_engine.evaluators import ReasoningLogicEvaluator
        
        # Test utils
        print("  ✓ Testing utils module...")
        from insight_engine.utils import truncate_text, extract_article_sections
        
        print("\n✓ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


def validate_models():
    """Validate that models can be instantiated."""
    print("\nValidating model instantiation...")
    
    try:
        from insight_engine.models import (
            ReasoningDepthResult,
            ArgumentStructureResult,
            ConsistencyResult,
            LogicalFallacyResult,
            ReasoningLogicEvaluation,
            LogicalFallacy,
            ArgumentComponent,
            LogicalFallacyType,
        )
        
        # Test ReasoningDepthResult
        print("  ✓ Testing ReasoningDepthResult...")
        depth = ReasoningDepthResult(
            score=0.8,
            has_causal_analysis=True,
            has_comparative_analysis=True,
            analysis_levels=3,
            depth_explanation="Test explanation"
        )
        
        # Test ArgumentStructureResult
        print("  ✓ Testing ArgumentStructureResult...")
        structure = ArgumentStructureResult(
            score=0.7,
            has_clear_structure=True,
            paragraph_coherence=0.75,
            argument_components=[],
            structure_explanation="Test explanation"
        )
        
        # Test ConsistencyResult
        print("  ✓ Testing ConsistencyResult...")
        consistency = ConsistencyResult(
            score=0.9,
            contradictions=[],
            consistency_explanation="Test explanation"
        )
        
        # Test LogicalFallacyResult
        print("  ✓ Testing LogicalFallacyResult...")
        fallacies = LogicalFallacyResult(
            score=0.85,
            fallacies=[],
            fallacy_explanation="Test explanation"
        )
        
        # Test complete evaluation
        print("  ✓ Testing ReasoningLogicEvaluation...")
        evaluation = ReasoningLogicEvaluation(
            article_title="Test Article",
            overall_score=0.8,
            reasoning_depth=depth,
            argument_structure=structure,
            consistency=consistency,
            logical_fallacies=fallacies,
            strengths=["Good analysis"],
            weaknesses=["Could improve structure"],
            recommendations=["Add more examples"]
        )
        
        # Test get_summary
        summary = evaluation.get_summary()
        assert len(summary) > 0, "Summary should not be empty"
        
        print("\n✓ All models validated successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Model validation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_config():
    """Validate configuration."""
    print("\nValidating configuration...")
    
    try:
        from insight_engine.config import EvaluatorConfig
        
        # Test default config
        print("  ✓ Testing default configuration...")
        config = EvaluatorConfig()
        assert config.model_name == "gpt-4-turbo-preview"
        assert config.temperature == 0.3
        assert config.min_reasoning_depth_score == 0.6
        
        # Test custom config
        print("  ✓ Testing custom configuration...")
        custom_config = EvaluatorConfig(
            model_name="gpt-3.5-turbo",
            temperature=0.5,
            min_reasoning_depth_score=0.7
        )
        assert custom_config.model_name == "gpt-3.5-turbo"
        assert custom_config.temperature == 0.5
        
        print("\n✓ Configuration validated successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Configuration validation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("InsightEngine Validation Suite")
    print("=" * 60)
    
    results = []
    
    # Run validations
    results.append(("Imports", validate_imports()))
    results.append(("Models", validate_models()))
    results.append(("Config", validate_config()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All validations passed!")
    else:
        print("✗ Some validations failed!")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
