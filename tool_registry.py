"""Tool registry for simulated mode - defines available tools."""

from dataclasses import dataclass
from typing import Optional
import yaml
from pathlib import Path


@dataclass
class Tool:
    """Definition of an available tool."""
    name: str
    description: str
    category: str
    enabled: bool = True


class ToolRegistry:
    """Registry of available tools for goal execution."""

    def __init__(self, tools: list[Tool]):
        self.tools = {tool.name: tool for tool in tools}
        self.categories = self._build_categories()

    def _build_categories(self) -> dict[str, list[Tool]]:
        """Group tools by category."""
        categories = {}
        for tool in self.tools.values():
            if tool.enabled:
                if tool.category not in categories:
                    categories[tool.category] = []
                categories[tool.category].append(tool)
        return categories

    @classmethod
    def from_config(cls, config_path: str = "config.yaml") -> "ToolRegistry":
        """Load tool registry from config file."""
        path = Path(config_path)

        if not path.exists():
            # Return default registry if config doesn't have tools section
            return cls.get_default_registry()

        with open(path) as f:
            config = yaml.safe_load(f)

        if "tools" not in config:
            return cls.get_default_registry()

        tools = []
        for category, tool_list in config["tools"].items():
            for tool_data in tool_list:
                tools.append(Tool(
                    name=tool_data["name"],
                    description=tool_data["description"],
                    category=category,
                    enabled=tool_data.get("enabled", True)
                ))

        return cls(tools)

    @classmethod
    def get_default_registry(cls) -> "ToolRegistry":
        """Get default tool registry."""
        default_tools = [
            # Infrastructure
            Tool("kubectl", "Kubernetes CLI - get/describe/logs/set resources", "infrastructure"),
            Tool("oc", "OpenShift CLI - deploy/rollout/project management", "infrastructure"),

            # Filesystem
            Tool("file_read", "Read file contents", "filesystem"),
            Tool("file_write", "Write/create files", "filesystem"),
            Tool("bash", "Execute bash commands", "filesystem"),

            # Research
            Tool("web_search", "Search the web for information", "research"),
            Tool("http_request", "Make HTTP API calls", "api"),

            # Data
            Tool("database_query", "Execute SQL queries", "data"),
            Tool("data_query", "Query data sources", "data"),

            # Visualization
            Tool("chart_generate", "Generate charts and visualizations", "visualization"),

            # Utilities
            Tool("calendar_read", "Read calendar/schedule", "utilities"),
        ]

        return cls(default_tools)

    def get_available_tools(self) -> list[str]:
        """Get list of available tool names."""
        return [name for name, tool in self.tools.items() if tool.enabled]

    def get_tools_by_category(self) -> dict[str, list[Tool]]:
        """Get tools grouped by category."""
        return self.categories

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name."""
        return self.tools.get(name)

    def get_description(self, name: str) -> str:
        """Get tool description."""
        tool = self.get_tool(name)
        return tool.description if tool else "Unknown tool"

    def validate_tools(self, requested_tools: list[str]) -> list[str]:
        """Validate requested tools exist. Returns list of missing tools."""
        available = set(self.get_available_tools())
        requested = set(requested_tools)
        missing = requested - available
        return list(missing)

    def is_available(self, tool_name: str) -> bool:
        """Check if a tool is available."""
        tool = self.get_tool(tool_name)
        return tool is not None and tool.enabled


# Template suggestions - pre-select tools based on goal template
TEMPLATE_TOOL_SUGGESTIONS = {
    "fix-pod": ["kubectl", "file_read", "bash"],
    "research-topic": ["web_search", "file_write", "file_read"],
    "make-decision": ["data_query", "file_write", "file_read"],
    "deploy-version": ["kubectl", "oc", "bash"],
    "create-document": ["data_query", "chart_generate", "file_write", "file_read"],
    "create-plan": ["calendar_read", "file_write", "file_read"],
    "custom": []
}


def get_suggested_tools(template: str) -> list[str]:
    """Get suggested tools for a template."""
    return TEMPLATE_TOOL_SUGGESTIONS.get(template, [])
