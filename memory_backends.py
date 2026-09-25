"""Memory backend protocol and implementations."""

from abc import ABC, abstractmethod
from typing import Optional
import json
import os

class MemoryBackend(ABC):
    """Protocol for memory storage and retrieval."""

    @abstractmethod
    def recall(self, query: str, history: list[dict]) -> str:
        """Retrieve relevant memories for injection into context."""
        pass

    @abstractmethod
    def store(self, user_msg: str, assistant_msg: str, history: list[dict]):
        """Store facts from this conversation turn."""
        pass

    @abstractmethod
    def clear_session(self):
        """Reset memory for a new conversation."""
        pass

class DictBackend(MemoryBackend):
    """In-memory dict for quick testing."""

    def __init__(self, seed_file: Optional[str] = None):
        self.facts = {}  # {fact: weight}

        # Load seed facts if provided
        if seed_file and os.path.exists(seed_file):
            self._load_seed_file(seed_file)

    def _load_seed_file(self, path: str):
        """Load facts from seed file."""
        with open(path) as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#"):
                    self.facts[line] = 1.0

    def recall(self, query: str, history: list[dict]) -> str:
        """Return all facts as context."""
        if not self.facts:
            return ""

        sorted_facts = sorted(self.facts.items(), key=lambda x: x[1], reverse=True)
        facts_text = "\n".join(f"- {fact}" for fact, _ in sorted_facts[:5])
        return f"<memory>\n{facts_text}\n</memory>"

    def store(self, user_msg: str, assistant_msg: str, history: list[dict]):
        """Simple keyword-based extraction."""
        # Look for preference indicators
        keywords = ["prefer", "like", "want", "need", "use", "work with", "am a", "i'm a"]

        for keyword in keywords:
            if keyword in user_msg.lower():
                # Store the user message as a fact
                self.facts[user_msg] = 1.0
                break

    def clear_session(self):
        """Clear all facts."""
        self.facts = {}

class TextFileBackend(MemoryBackend):
    """Line-based fact storage in a text file."""

    def __init__(self, path: str, extractor_backend: Optional['AgentBackend'] = None, seed_file: Optional[str] = None):
        self.path = path
        self.extractor = extractor_backend
        self.facts = []

        # Load seed facts first if provided
        if seed_file and os.path.exists(seed_file):
            self._load_seed_file(seed_file)

        # Then load any existing facts from the storage file
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.facts.append(line)

    def _load_seed_file(self, path: str):
        """Load facts from seed file (skip comments and empty lines)."""
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    self.facts.append(line)

    def recall(self, query: str, history: list[dict]) -> str:
        """Return all facts as context (no semantic search)."""
        if not self.facts:
            return ""

        facts_text = "\n".join(f"- {fact}" for fact in self.facts[-10:])  # last 10
        return f"<memory>\n{facts_text}\n</memory>"

    def store(self, user_msg: str, assistant_msg: str, history: list[dict]):
        """Extract facts with LLM if available, otherwise use keywords."""
        if self.extractor:
            extraction_prompt = f"""Extract facts to remember from this exchange.
Output one fact per line, or "NONE" if nothing to store.

User: {user_msg}
Assistant: {assistant_msg}

Facts to remember:"""

            response = self.extractor.send([
                {"role": "user", "content": extraction_prompt}
            ])

            lines = response.content.strip().split("\n")
            facts = [
                line.strip().lstrip("- ").strip()
                for line in lines
                if line.strip() and line.strip().upper() != "NONE"
            ]

            if facts:
                self.facts.extend(facts)
                with open(self.path, "a") as f:
                    for fact in facts:
                        f.write(fact + "\n")
        else:
            # Fallback: keyword-based extraction
            keywords = ["prefer", "like", "am a", "i'm a", "work with"]
            if any(kw in user_msg.lower() for kw in keywords):
                self.facts.append(user_msg)
                with open(self.path, "a") as f:
                    f.write(user_msg + "\n")

    def clear_session(self):
        """Keep facts but reset conversation state (file-backed facts persist)."""
        pass

class MemoryHubBackend(MemoryBackend):
    """MemoryHub MCP server backend."""

    def __init__(self, mcp_url: str, api_key: str, user_id: str = "demo"):
        self.mcp_url = mcp_url
        self.api_key = api_key
        self.user_id = user_id
        self.session_id = None

        # Import MemoryHub client (will implement when MemoryHub SDK is ready)
        # For now, placeholder
        self.client = None

    def recall(self, query: str, history: list[dict]) -> str:
        """Search MemoryHub and format results."""
        # Placeholder - will implement with real MCP client
        return "<memory>\n(MemoryHub integration pending)\n</memory>"

    def store(self, user_msg: str, assistant_msg: str, history: list[dict]):
        """Extract and write memories via dreaming."""
        # Placeholder - will implement with real MCP client
        pass

    def clear_session(self):
        """End session (memories persist per user)."""
        self.session_id = None

def create_memory_backend(config: dict, extractor_backend: Optional['AgentBackend'] = None, seed_file: Optional[str] = None) -> Optional[MemoryBackend]:
    """Factory function to create memory backends from config."""
    backend_type = config.get("type")

    if backend_type is None or backend_type == "none":
        return None
    elif backend_type == "dict":
        return DictBackend(seed_file=seed_file)
    elif backend_type == "file":
        return TextFileBackend(
            path=config.get("path", "./memory/facts.txt"),
            extractor_backend=extractor_backend,
            seed_file=seed_file
        )
    elif backend_type == "memoryhub":
        return MemoryHubBackend(
            mcp_url=config["url"],
            api_key=config["api_key"],
            user_id=config.get("user_id", "demo")
        )
    else:
        raise ValueError(f"Unknown memory backend type: {backend_type}")
