"""
Base Agent class for the Agency system.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import json
import uuid

from pydantic import BaseModel, Field


class AgentMemory(BaseModel):
    """Short-term memory for an agent."""
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.updated_at = datetime.utcnow()
    
    def get_recent_messages(self, n: int = 10) -> List[Dict[str, str]]:
        """Get the n most recent messages."""
        return self.conversation_history[-n:]
    
    def clear(self):
        """Clear the conversation history."""
        self.conversation_history = []
        self.context = {}
        self.updated_at = datetime.utcnow()


class AgentState(BaseModel):
    """State tracking for an agent."""
    is_blocked: bool = False
    block_reason: Optional[str] = None
    current_task: Optional[str] = None
    task_started_at: Optional[datetime] = None
    last_active: datetime = Field(default_factory=datetime.utcnow)
    total_tokens_used: int = 0
    requests_count: int = 0


class BaseAgent(ABC):
    """Abstract base class for all agents in the agency."""
    
    def __init__(
        self,
        name: str,
        role: str,
        description: str = "",
        tools: List[Callable] = None
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.description = description
        self.tools = tools or []
        
        # Memory and state
        self.memory = AgentMemory()
        self.state = AgentState()
        
        # Callbacks
        self.on_task_start: Optional[Callable] = None
        self.on_task_complete: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass
    
    def get_full_prompt(self, user_message: str = "") -> List[Dict[str, str]]:
        """Get the full prompt including system prompt and conversation history."""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add recent conversation history
        messages.extend(self.memory.get_recent_messages(20))
        
        # Add current user message if provided
        if user_message:
            messages.append({"role": "user", "content": user_message})
        
        return messages
    
    async def process_task(
        self,
        task: str,
        context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Process a task and return the result."""
        # Check if agent is blocked
        if self.state.is_blocked:
            raise RuntimeError(f"Agent {self.name} is blocked: {self.state.block_reason}")
        
        # Update state
        self.state.current_task = task
        self.state.task_started_at = datetime.utcnow()
        self.state.last_active = datetime.utcnow()
        self.state.requests_count += 1
        
        # Add to memory
        self.memory.add_message("user", task)
        
        # Call on_task_start callback
        if self.on_task_start:
            self.on_task_start(self, task)
        
        try:
            # Get the response using the abstract method
            response = await self._execute(task, context, **kwargs)
            
            # Add response to memory
            self.memory.add_message("assistant", str(response))
            
            # Call on_task_complete callback
            if self.on_task_complete:
                self.on_task_complete(self, task, response)
            
            return {
                "agent_name": self.name,
                "agent_role": self.role,
                "task": task,
                "response": response,
                "timestamp": datetime.utcnow().isoformat(),
                "tokens_used": self.state.total_tokens_used
            }
            
        except Exception as e:
            # Call on_error callback
            if self.on_error:
                self.on_error(self, task, e)
            
            raise
    
    @abstractmethod
    async def _execute(
        self,
        task: str,
        context: Dict[str, Any] = None,
        **kwargs
    ) -> Any:
        """Execute the agent's logic. To be implemented by subclasses."""
        pass
    
    def add_tool(self, tool: Callable):
        """Add a tool to the agent's toolkit."""
        self.tools.append(tool)
    
    def remove_tool(self, tool_name: str):
        """Remove a tool by name."""
        self.tools = [t for t in self.tools if t.__name__ != tool_name]
    
    def block(self, reason: str = ""):
        """Block the agent from processing tasks."""
        self.state.is_blocked = True
        self.state.block_reason = reason
    
    def unblock(self):
        """Unblock the agent."""
        self.state.is_blocked = False
        self.state.block_reason = None
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "is_blocked": self.state.is_blocked,
            "current_task": self.state.current_task,
            "total_tokens_used": self.state.total_tokens_used,
            "requests_count": self.state.requests_count,
            "last_active": self.state.last_active.isoformat(),
            "memory_size": len(self.memory.conversation_history)
        }
    
    def reset(self):
        """Reset the agent's state and memory."""
        self.memory.clear()
        self.state = AgentState()
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', role='{self.role}')>"