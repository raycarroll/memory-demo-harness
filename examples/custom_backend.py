"""
Example: Custom Memory Backend Implementation

This shows how to integrate your own memory system with the demo harness.
"""

from memory_backends import MemoryBackend
from typing import Optional

class CustomMemoryBackend(MemoryBackend):
    """
    Example custom backend - replace with your actual memory system client.
    """

    def __init__(self, api_key: str, endpoint: str, user_id: str = "demo"):
        """
        Initialize your memory system client.

        Args:
            api_key: API key for authentication
            endpoint: API endpoint URL
            user_id: User identifier
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.user_id = user_id
        self.session_id = None

        # Initialize your client here
        # self.client = YourMemoryClient(api_key, endpoint)

    def recall(self, query: str, history: list[dict]) -> str:
        """
        Retrieve relevant memories for the current query.

        Args:
            query: Current user message
            history: Conversation history so far

        Returns:
            String to inject into context (typically wrapped in <memory> tags)
        """
        # Example: Search your memory system
        # results = self.client.search(
        #     query=query,
        #     user_id=self.user_id,
        #     limit=5
        # )

        # For this example, return empty
        results = []

        if not results:
            return ""

        # Format memories for injection
        memories = "\n".join(f"- {result['content']}" for result in results)
        return f"<memory>\n{memories}\n</memory>"

    def store(self, user_msg: str, assistant_msg: str, history: list[dict]):
        """
        Store facts from this conversation turn.

        Args:
            user_msg: User's message
            assistant_msg: Assistant's response
            history: Full conversation history
        """
        # Example: Extract and store facts
        # facts = self._extract_facts(user_msg, assistant_msg)
        # for fact in facts:
        #     self.client.store(
        #         content=fact,
        #         user_id=self.user_id,
        #         metadata={"turn": len(history)}
        #     )

        # For this example, do nothing
        pass

    def clear_session(self):
        """
        Reset session state.

        Note: This should NOT delete stored memories, just reset session-specific state.
        """
        self.session_id = None

    def _extract_facts(self, user_msg: str, assistant_msg: str) -> list[str]:
        """
        Optional: Extract facts from messages.

        Your memory system might handle this internally, or you might
        use an LLM to extract facts here.
        """
        # Placeholder - implement your extraction logic
        facts = []

        # Example keyword-based extraction
        if any(kw in user_msg.lower() for kw in ["prefer", "like", "use"]):
            facts.append(user_msg)

        return facts


# Register in memory_backends.py:
#
# def create_memory_backend(config, ...):
#     ...
#     elif backend_type == "custom":
#         return CustomMemoryBackend(
#             api_key=config["api_key"],
#             endpoint=config["endpoint"],
#             user_id=config.get("user_id", "demo")
#         )
