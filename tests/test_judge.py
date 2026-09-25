#!/usr/bin/env python3
"""Test judge functionality."""

from judge import ResponseJudge, JudgeVerdict
from agent_backends import Response

class MockAgent:
    """Mock agent for testing."""
    def send(self, messages, system=None):
        # Simulate judge output
        content = """
RESPONSE_A_SCORE: 8.5
RESPONSE_A_JUSTIFICATION: Used memory context effectively with specific examples.
MEMORY_INFLUENCED_SEGMENTS: ["with pandas", "pd.read_csv"]

RESPONSE_B_SCORE: 6.0
RESPONSE_B_JUSTIFICATION: Generic answer without considering user preferences.
"""
        return Response(content=content, model="mock", tokens_in=100, tokens_out=50)

def test_judge():
    """Test judge evaluation."""
    print("Testing ResponseJudge...")

    # Create judge with mock agent
    judge = ResponseJudge(MockAgent())

    # Test evaluation
    verdict = judge.evaluate(
        user_query="How do I read a CSV?",
        left_response="Here's how with pandas: pd.read_csv('file.csv')",
        right_response="You can use Python, R, or Excel to read CSV files.",
        memories="User prefers Python over R"
    )

    # Verify
    assert isinstance(verdict, JudgeVerdict)
    assert verdict.left_score == 8.5, f"Expected 8.5, got {verdict.left_score}"
    assert verdict.right_score == 6.0, f"Expected 6.0, got {verdict.right_score}"
    assert verdict.memory_alignment_delta == 2.5, f"Expected 2.5, got {verdict.memory_alignment_delta}"
    assert "memory context" in verdict.left_justification.lower()
    assert "generic" in verdict.right_justification.lower()
    assert len(verdict.memory_influenced_segments) == 2, f"Expected 2 segments, got {len(verdict.memory_influenced_segments)}"
    assert "pandas" in verdict.memory_influenced_segments[0].lower()

    print(f"✓ Judge evaluation working")
    print(f"  Left score: {verdict.left_score}/10")
    print(f"  Right score: {verdict.right_score}/10")
    print(f"  Delta: +{verdict.memory_alignment_delta}")
    print(f"  Left: {verdict.left_justification}")
    print(f"  Right: {verdict.right_justification}")
    print(f"  Segments: {verdict.memory_influenced_segments}")

if __name__ == "__main__":
    test_judge()
    print("\n🎉 Judge test passed!")
