"""Dual driver for parallel execution with and without memory."""

from typing import Optional, Tuple
from agent_backends import AgentBackend, Response
from memory_backends import MemoryBackend
from judge import ResponseJudge, JudgeVerdict

class DualDriver:
    """Execute prompts through memory-enabled and baseline agents in parallel."""

    def __init__(
        self,
        agent_backend: AgentBackend,
        memory_backend: Optional[MemoryBackend] = None,
        judge: Optional[ResponseJudge] = None
    ):
        self.agent = agent_backend
        self.memory = memory_backend
        self.judge = judge
        self.left_history = []   # WITH memory
        self.right_history = []  # WITHOUT memory
        self.verdicts = []       # Judge verdicts per turn
        self.left_tokens = []    # Token usage per turn (left)
        self.right_tokens = []   # Token usage per turn (right)

    def execute(self, prompt: str) -> Tuple[Response, Response, Optional[JudgeVerdict]]:
        """Send same prompt to both agents, return both responses and optional verdict."""

        # Build message histories
        left_messages = self._build_messages(self.left_history, prompt, with_memory=True)
        right_messages = self._build_messages(self.right_history, prompt, with_memory=False)

        # Execute in parallel (for now, sequential - can parallelize later)
        left_resp = self.agent.send(left_messages)
        right_resp = self.agent.send(right_messages)

        # Evaluate responses if judge is enabled
        verdict = None
        if self.judge:
            # Get current memories for context
            memories = None
            if self.memory:
                memories = self.memory.recall(prompt, self.left_history)

            verdict = self.judge.evaluate(
                user_query=prompt,
                left_response=left_resp.content,
                right_response=right_resp.content,
                memories=memories
            )
            self.verdicts.append(verdict)

        # Track token usage
        self.left_tokens.append({
            "in": left_resp.tokens_in,
            "out": left_resp.tokens_out,
            "total": left_resp.tokens_in + left_resp.tokens_out
        })
        self.right_tokens.append({
            "in": right_resp.tokens_in,
            "out": right_resp.tokens_out,
            "total": right_resp.tokens_in + right_resp.tokens_out
        })

        # Store facts from left agent's interaction
        if self.memory:
            self.memory.store(prompt, left_resp.content, self.left_history)

        # Update histories
        self.left_history.append({"role": "user", "content": prompt})
        self.left_history.append({"role": "assistant", "content": left_resp.content})
        self.right_history.append({"role": "user", "content": prompt})
        self.right_history.append({"role": "assistant", "content": right_resp.content})

        return left_resp, right_resp, verdict

    def _build_messages(
        self,
        history: list[dict],
        prompt: str,
        with_memory: bool
    ) -> list[dict]:
        """Build message list with optional memory injection."""
        messages = history.copy()

        if with_memory and self.memory:
            # Recall memories and prepend to first message
            context = self.memory.recall(prompt, history)

            if context:
                # Inject memory context before the new prompt
                if messages:
                    # Modify the system message or first user message
                    # For simplicity, we'll add a memory context message
                    messages.append({"role": "user", "content": f"{context}\n\n{prompt}"})
                else:
                    # First message
                    messages.append({"role": "user", "content": f"{context}\n\n{prompt}"})
            else:
                messages.append({"role": "user", "content": prompt})
        else:
            messages.append({"role": "user", "content": prompt})

        return messages

    def reset(self):
        """Clear conversation histories."""
        self.left_history = []
        self.right_history = []
        self.verdicts = []
        self.left_tokens = []
        self.right_tokens = []
        if self.memory:
            self.memory.clear_session()

    def get_stats(self) -> dict:
        """Get statistics including judge scores and token usage."""
        stats = {
            "left_turns": len([m for m in self.left_history if m["role"] == "user"]),
            "right_turns": len([m for m in self.right_history if m["role"] == "user"]),
        }

        # Add token statistics
        if self.left_tokens:
            left_total = sum(t["total"] for t in self.left_tokens)
            right_total = sum(t["total"] for t in self.right_tokens)

            stats.update({
                "left_tokens_total": left_total,
                "right_tokens_total": right_total,
                "token_delta": left_total - right_total,
                "token_efficiency": round((1 - left_total / right_total) * 100, 1) if right_total > 0 else 0
            })

        # Add judge statistics
        if self.verdicts:
            avg_left = sum(v.left_score for v in self.verdicts) / len(self.verdicts)
            avg_right = sum(v.right_score for v in self.verdicts) / len(self.verdicts)
            avg_delta = sum(v.memory_alignment_delta for v in self.verdicts) / len(self.verdicts)

            stats.update({
                "avg_left_score": round(avg_left, 1),
                "avg_right_score": round(avg_right, 1),
                "avg_memory_delta": round(avg_delta, 1),
                "total_evaluations": len(self.verdicts)
            })

        return stats
