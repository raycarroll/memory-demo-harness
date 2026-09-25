"""Agent backend protocol and implementations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class Response:
    """Agent response with metadata."""
    content: str
    model: str
    tokens_in: int = 0
    tokens_out: int = 0

class AgentBackend(ABC):
    """Protocol for agent execution engines."""

    @abstractmethod
    def send(self, messages: list[dict], system: Optional[str] = None) -> Response:
        """Send messages, return response with metadata."""
        pass

class DirectLLMBackend(AgentBackend):
    """Direct LLM API call."""

    def __init__(self, provider: str, model: str, system_prompt: str = "You are a helpful assistant."):
        self.provider = provider
        self.model = model
        self.system = system_prompt

        if provider == "anthropic":
            import anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = anthropic.Anthropic(api_key=api_key)
        elif provider == "openai":
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def send(self, messages: list[dict], system: Optional[str] = None) -> Response:
        """Send messages to LLM."""
        system_prompt = system or self.system

        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=messages
            )

            return Response(
                content=response.content[0].text,
                model=self.model,
                tokens_in=response.usage.input_tokens,
                tokens_out=response.usage.output_tokens
            )

        elif self.provider == "openai":
            # OpenAI puts system prompt in messages
            messages_with_system = [
                {"role": "system", "content": system_prompt}
            ] + messages

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages_with_system
            )

            return Response(
                content=response.choices[0].message.content,
                model=self.model,
                tokens_in=response.usage.prompt_tokens,
                tokens_out=response.usage.completion_tokens
            )

def create_agent_backend(config: dict) -> AgentBackend:
    """Factory function to create agent backends from config."""
    agent_type = config.get("type", "direct")

    if agent_type == "direct":
        return DirectLLMBackend(
            provider=config["provider"],
            model=config["model"],
            system_prompt=config.get("system_prompt", "You are a helpful assistant.")
        )
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
