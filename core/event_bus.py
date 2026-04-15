"""
Event Bus for inter-agent communication.
"""
import asyncio
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import json
from enum import Enum


class EventType(str, Enum):
    """Types of events in the system."""
    TASK_ASSIGNED = "task_assigned"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    AGENT_BLOCKED = "agent_blocked"
    AGENT_UNBLOCKED = "agent_unblocked"
    BLOCKER_TRIGGERED = "blocker_triggered"
    MESSAGE = "message"
    BROADCAST = "broadcast"
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    TOKEN_BUDGET_WARNING = "token_budget_warning"
    CUSTOM = "custom"


class Event(BaseModel):
    """Event structure for the event bus."""
    id: str = Field(default_factory=lambda: str(id(datetime.utcnow())))
    type: EventType
    source: str  # Agent or system that emitted the event
    target: Optional[str] = None  # Target agent (None for broadcast)
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None  # For tracking related events
    requires_ack: bool = False
    ttl_seconds: int = 300  # Time to live in seconds


class EventHandler(BaseModel):
    """Handler for events."""
    callback: Callable
    event_types: List[EventType] = []
    agent_name: Optional[str] = None  # Filter by agent name
    priority: int = 0  # Higher priority handlers run first
    
    class Config:
        arbitrary_types_allowed = True


class EventBus:
    """Event bus for inter-agent communication."""
    
    def __init__(self):
        self._handlers: List[EventHandler] = []
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._event_history: List[Event] = []
        self._max_history = 1000
        self._subscriptions: Dict[str, List[EventHandler]] = {}
    
    def subscribe(
        self,
        callback: Callable,
        event_types: List[EventType] = None,
        agent_name: str = None,
        priority: int = 0
    ):
        """Subscribe to events.
        
        Args:
            callback: Function to call when event is received
            event_types: List of event types to subscribe to (None for all)
            agent_name: Only receive events for this agent (None for all)
            priority: Handler priority (higher runs first)
        """
        handler = EventHandler(
            callback=callback,
            event_types=event_types or [],
            agent_name=agent_name,
            priority=priority
        )
        self._handlers.append(handler)
        self._handlers.sort(key=lambda h: h.priority, reverse=True)
        
        return handler
    
    def unsubscribe(self, handler: EventHandler):
        """Unsubscribe from events."""
        if handler in self._handlers:
            self._handlers.remove(handler)
    
    def subscribe_agent(self, agent_name: str, callback: Callable, event_types: List[EventType] = None):
        """Subscribe an agent to events targeted at them."""
        self.subscribe(
            callback=callback,
            event_types=event_types,
            agent_name=agent_name,
            priority=10  # Agent-specific handlers have higher priority
        )
    
    async def publish(self, event: Event):
        """Publish an event to the event bus."""
        # Add to history
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history:]
        
        # Put in queue for processing
        await self._event_queue.put(event)
    
    async def publish_sync(self, event: Event):
        """Publish an event and wait for all handlers to complete."""
        await self.publish(event)
        await self._process_event(event)
    
    async def _process_event(self, event: Event):
        """Process a single event by calling all matching handlers."""
        matching_handlers = [
            h for h in self._handlers
            if self._handler_matches(h, event)
        ]
        
        # Execute handlers in priority order
        tasks = []
        for handler in matching_handlers:
            try:
                if asyncio.iscoroutinefunction(handler.callback):
                    tasks.append(handler.callback(event))
                else:
                    handler.callback(event)
            except Exception as e:
                print(f"Error in event handler: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def _handler_matches(self, handler: EventHandler, event: Event) -> bool:
        """Check if a handler should receive an event."""
        # Check event type
        if handler.event_types and event.type not in handler.event_types:
            return False
        
        # Check agent name (target)
        if handler.agent_name and event.target != handler.agent_name:
            return False
        
        return True
    
    async def start(self):
        """Start the event bus processor."""
        self._running = True
        asyncio.create_task(self._run_processor())
    
    async def _run_processor(self):
        """Main event processing loop."""
        while self._running:
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
                await self._process_event(event)
                self._event_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error processing event: {e}")
    
    def stop(self):
        """Stop the event bus processor."""
        self._running = False
    
    def get_event_history(
        self,
        event_type: EventType = None,
        source: str = None,
        target: str = None,
        limit: int = 100
    ) -> List[Event]:
        """Get event history with optional filtering."""
        events = self._event_history
        
        if event_type:
            events = [e for e in events if e.type == event_type]
        if source:
            events = [e for e in events if e.source == source]
        if target:
            events = [e for e in events if e.target == target]
        
        return events[-limit:]
    
    def create_event(
        self,
        event_type: EventType,
        source: str,
        target: str = None,
        data: Dict[str, Any] = None,
        correlation_id: str = None,
        requires_ack: bool = False
    ) -> Event:
        """Helper to create an event."""
        return Event(
            type=event_type,
            source=source,
            target=target,
            data=data or {},
            correlation_id=correlation_id,
            requires_ack=requires_ack
        )


# Singleton instance
_event_bus: Optional[EventBus] = None

def get_event_bus() -> EventBus:
    """Get or create the event bus singleton."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus