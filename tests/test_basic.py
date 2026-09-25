#!/usr/bin/env python3
"""Basic smoke test for memory demo harness components."""

import os
import sys

def test_imports():
    """Test that all modules import successfully."""
    print("Testing imports...")
    try:
        from agent_backends import AgentBackend, DirectLLMBackend, create_agent_backend
        from memory_backends import MemoryBackend, DictBackend, create_memory_backend
        from dual_driver import DualDriver
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_dict_backend():
    """Test in-memory dict backend."""
    print("\nTesting DictBackend...")
    try:
        from memory_backends import DictBackend

        backend = DictBackend()

        # Test empty recall
        result = backend.recall("test query", [])
        assert result == "", f"Expected empty string, got: {result}"

        # Test store
        backend.store("I prefer Python", "Got it!", [])

        # Test recall after store
        result = backend.recall("preferences", [])
        assert "I prefer Python" in result, f"Expected stored fact in: {result}"

        print("✓ DictBackend working")
        return True
    except Exception as e:
        print(f"✗ DictBackend failed: {e}")
        return False

def test_dual_driver_mock():
    """Test DualDriver with mock agent."""
    print("\nTesting DualDriver (with mock agent)...")
    try:
        from dual_driver import DualDriver
        from memory_backends import DictBackend
        from agent_backends import Response

        # Mock agent backend
        class MockAgent:
            def send(self, messages, system=None):
                # Just echo back the last message
                last_msg = messages[-1]["content"]
                return Response(
                    content=f"Echo: {last_msg}",
                    model="mock-model",
                    tokens_in=10,
                    tokens_out=10
                )

        memory = DictBackend()
        agent = MockAgent()
        driver = DualDriver(agent, memory)

        # Execute a turn
        left, right, verdict = driver.execute("I prefer Python")

        assert "Echo:" in left.content
        assert "Echo:" in right.content
        assert len(driver.left_history) == 2  # user + assistant
        assert len(driver.right_history) == 2
        assert verdict is None  # No judge enabled

        print("✓ DualDriver working")
        return True
    except Exception as e:
        print(f"✗ DualDriver failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Memory Demo Harness - Basic Component Tests")
    print("=" * 60)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("DictBackend", test_dict_backend()))
    results.append(("DualDriver", test_dual_driver_mock()))

    print("\n" + "=" * 60)
    print("Summary:")
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} - {name}")

    all_passed = all(r[1] for r in results)
    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
