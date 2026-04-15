"""
Base Workflow class for orchestrating agent collaboration.
"""
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import asyncio
from core.event_bus import EventBus, Event


class BaseWorkflow:
    """
    Base class for workflows that orchestrate multiple agents.
    Provides common functionality for workflow execution, event handling, and state management.
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize workflow.
        
        Args:
            name: Workflow name
            description: Workflow description
        """
        self.name = name
        self.description = description
        self.agents: Dict[str, Any] = {}
        self.steps: List[Dict] = []
        self.state: str = "initialized"
        self.current_step: int = 0
        self.results: Dict[str, Any] = {}
        self.errors: List[Dict] = []
        self.event_bus = EventBus()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
    
    def add_agent(self, name: str, agent: Any) -> "BaseWorkflow":
        """
        Add an agent to the workflow.
        
        Args:
            name: Agent name/role in workflow
            agent: Agent instance
            
        Returns:
            Self for chaining
        """
        self.agents[name] = agent
        return self
    
    def add_step(
        self, 
        name: str, 
        agent_name: str, 
        method: str, 
        inputs: Optional[Dict] = None,
        depends_on: Optional[List[str]] = None
    ) -> "BaseWorkflow":
        """
        Add a step to the workflow.
        
        Args:
            name: Step name
            agent_name: Name of agent to execute step
            method: Method name to call on agent
            inputs: Input parameters for the method
            depends_on: List of step names this step depends on
            
        Returns:
            Self for chaining
        """
        self.steps.append({
            "name": name,
            "agent_name": agent_name,
            "method": method,
            "inputs": inputs or {},
            "depends_on": depends_on or [],
            "status": "pending",
            "result": None,
            "error": None
        })
        return self
    
    async def execute(self, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Args:
            context: Optional context data for workflow execution
            
        Returns:
            Workflow results
        """
        self.started_at = datetime.now()
        self.state = "running"
        self.context = context or {}
        
        # Emit workflow started event
        await self.event_bus.emit("workflow_started", {
            "workflow": self.name,
            "timestamp": self.started_at.isoformat(),
            "context": self.context
        })
        
        try:
            # Execute steps in order (simple sequential execution)
            for i, step in enumerate(self.steps):
                self.current_step = i
                await self._execute_step(step)
            
            self.state = "completed"
            self.completed_at = datetime.now()
            
            # Emit workflow completed event
            await self.event_bus.emit("workflow_completed", {
                "workflow": self.name,
                "duration": (self.completed_at - self.started_at).total_seconds(),
                "results": self.results
            })
            
        except Exception as e:
            self.state = "failed"
            self.completed_at = datetime.now()
            self.errors.append({
                "step": self.current_step,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            
            # Emit workflow failed event
            await self.event_bus.emit("workflow_failed", {
                "workflow": self.name,
                "error": str(e),
                "step": self.current_step
            })
        
        return {
            "workflow": self.name,
            "state": self.state,
            "results": self.results,
            "errors": self.errors,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration": (self.completed_at - self.started_at).total_seconds() if self.started_at and self.completed_at else None
        }
    
    async def _execute_step(self, step: Dict) -> Any:
        """
        Execute a single workflow step.
        
        Args:
            step: Step definition
            
        Returns:
            Step result
        """
        step["status"] = "running"
        
        # Emit step started event
        await self.event_bus.emit("step_started", {
            "workflow": self.name,
            "step": step["name"],
            "agent": step["agent_name"]
        })
        
        try:
            # Get agent
            agent = self.agents.get(step["agent_name"])
            if not agent:
                raise ValueError(f"Agent '{step['agent_name']}' not found")
            
            # Get method
            method = getattr(agent, step["method"], None)
            if not method or not callable(method):
                raise ValueError(f"Method '{step['method']}' not found on agent '{step['agent_name']}'")
            
            # Prepare inputs with context substitution
            inputs = self._prepare_inputs(step["inputs"])
            
            # Execute method
            if asyncio.iscoroutinefunction(method):
                result = await method(**inputs)
            else:
                result = method(**inputs)
            
            # Store result
            step["result"] = result
            step["status"] = "completed"
            self.results[step["name"]] = result
            
            # Emit step completed event
            await self.event_bus.emit("step_completed", {
                "workflow": self.name,
                "step": step["name"],
                "agent": step["agent_name"],
                "result": result
            })
            
            return result
            
        except Exception as e:
            step["error"] = str(e)
            step["status"] = "failed"
            
            # Emit step failed event
            await self.event_bus.emit("step_failed", {
                "workflow": self.name,
                "step": step["name"],
                "agent": step["agent_name"],
                "error": str(e)
            })
            
            raise
    
    def _prepare_inputs(self, inputs: Dict) -> Dict:
        """
        Prepare inputs by substituting context and previous results.
        
        Args:
            inputs: Raw input parameters
            
        Returns:
            Prepared input parameters
        """
        prepared = {}
        for key, value in inputs.items():
            if isinstance(value, str):
                # Substitute context variables
                for ctx_key, ctx_value in self.context.items():
                    value = value.replace(f"{{{{{ctx_key}}}}}", str(ctx_value))
                
                # Substitute previous step results
                for step_name, step_result in self.results.items():
                    if isinstance(step_result, dict):
                        for result_key, result_value in step_result.items():
                            value = value.replace(f"{{{{{step_name}.{result_key}}}}}", str(result_value))
            
            prepared[key] = value
        
        return prepared
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current workflow status.
        
        Returns:
            Workflow status information
        """
        return {
            "name": self.name,
            "state": self.state,
            "current_step": self.current_step,
            "total_steps": len(self.steps),
            "steps": [
                {
                    "name": step["name"],
                    "status": step["status"],
                    "agent": step["agent_name"],
                    "error": step.get("error")
                }
                for step in self.steps
            ],
            "results": self.results,
            "errors": self.errors
        }
    
    def on_event(self, event_type: str, callback: Callable) -> "BaseWorkflow":
        """
        Register an event handler.
        
        Args:
            event_type: Type of event to listen for
            callback: Callback function
            
        Returns:
            Self for chaining
        """
        self.event_bus.on(event_type, callback)
        return self