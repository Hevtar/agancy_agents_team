"""
Tools Registry for managing all available tools.
"""
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
import inspect
import json
from datetime import datetime


@dataclass
class ToolDefinition:
    """Definition of a tool."""
    name: str
    description: str
    func: Callable
    category: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    requires_auth: bool = False
    rate_limit: Optional[int] = None  # Calls per minute
    is_async: bool = False
    
    @classmethod
    def from_function(cls, func: Callable, category: str = "general", **kwargs):
        """Create a ToolDefinition from a function."""
        sig = inspect.signature(func)
        parameters = {}
        
        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue
            
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else Any
            default = param.default if param.default != inspect.Parameter.empty else None
            
            parameters[param_name] = {
                "type": param_type.__name__ if hasattr(param_type, '__name__') else str(param_type),
                "description": f"Parameter {param_name}",
                "required": default is None,
                "default": default
            }
        
        return cls(
            name=func.__name__,
            description=func.__doc__ or f"Tool {func.__name__}",
            func=func,
            category=category,
            parameters=parameters,
            is_async=inspect.iscoroutinefunction(func),
            **kwargs
        )


class ToolsRegistry:
    """Registry for all available tools."""
    
    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(
        self,
        func: Callable = None,
        *,
        name: str = None,
        category: str = "general",
        description: str = None,
        requires_auth: bool = False,
        rate_limit: Optional[int] = None
    ):
        """Decorator to register a tool.
        
        Usage:
            @tools_registry.register(category="analytics")
            def my_tool(param1: str) -> str:
                '''Tool description'''
                return result
            
            # Or without decorator:
            tools_registry.register(my_tool, category="analytics")
        """
        def _register(fn: Callable):
            tool_def = ToolDefinition.from_function(
                fn,
                category=category,
                name=name or fn.__name__,
                description=description,
                requires_auth=requires_auth,
                rate_limit=rate_limit
            )
            
            self._tools[tool_def.name] = tool_def
            
            if category not in self._categories:
                self._categories[category] = []
            self._categories[category].append(tool_def.name)
            
            return fn
        
        if func is not None:
            return _register(func)
        return _register
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_tools_by_category(self, category: str) -> List[ToolDefinition]:
        """Get all tools in a category."""
        return [self._tools[name] for name in self._categories.get(category, [])]
    
    def list_categories(self) -> List[str]:
        """List all available categories."""
        return list(self._categories.keys())
    
    def list_tools(self, category: str = None) -> List[Dict[str, Any]]:
        """List all tools with optional category filter."""
        tools = []
        for name, tool_def in self._tools.items():
            if category and tool_def.category != category:
                continue
            
            tools.append({
                "name": tool_def.name,
                "description": tool_def.description,
                "category": tool_def.category,
                "parameters": tool_def.parameters,
                "requires_auth": tool_def.requires_auth,
                "is_async": tool_def.is_async
            })
        
        return tools
    
    async def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool by name with given arguments."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        
        # Filter kwargs to only include parameters the tool expects
        valid_kwargs = {k: v for k, v in kwargs.items() if k in tool.parameters}
        
        if tool.is_async:
            return await tool.func(**valid_kwargs)
        else:
            return tool.func(**valid_kwargs)
    
    def get_tool_schema(self, name: str) -> Dict[str, Any]:
        """Get JSON schema for a tool."""
        tool = self.get_tool(name)
        if not tool:
            return {}
        
        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {
                    param_name: {
                        "type": param_info["type"],
                        "description": param_info["description"]
                    }
                    for param_name, param_info in tool.parameters.items()
                },
                "required": [
                    param_name for param_name, param_info in tool.parameters.items()
                    if param_info["required"]
                ]
            }
        }
    
    def export_for_llm(self, category: str = None) -> str:
        """Export tools as a formatted string for LLM prompts."""
        tools = self.list_tools(category)
        
        if not tools:
            return "No tools available."
        
        output = "Available Tools:\n\n"
        for tool in tools:
            output += f"Tool: {tool['name']}\n"
            output += f"Description: {tool['description']}\n"
            
            if tool['parameters']:
                output += "Parameters:\n"
                for param_name, param_info in tool['parameters'].items():
                    required = " (required)" if param_info["required"] else ""
                    output += f"  - {param_name}: {param_info['type']}{required}\n"
            
            output += "\n"
        
        return output


# Singleton instance
_tools_registry: Optional[ToolsRegistry] = None

def get_tools_registry() -> ToolsRegistry:
    """Get or create the tools registry singleton."""
    global _tools_registry
    if _tools_registry is None:
        _tools_registry = ToolsRegistry()
    return _tools_registry


# Convenience decorator
def tool(category: str = "general", **kwargs):
    """Decorator to register a tool function."""
    registry = get_tools_registry()
    return registry.register(category=category, **kwargs)