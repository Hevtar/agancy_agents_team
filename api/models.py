"""
Data models for the Agency system frontend panel.
"""
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from enum import Enum


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectPhase(str, Enum):
    INITIATION = "initiation"
    PLANNING = "planning"
    EXECUTION = "execution"
    REVIEW = "review"
    COMPLETED = "completed"


class ProjectType(str, Enum):
    PRODUCT = "PRODUCT"
    MARKETING = "MARKETING"
    ANALYTICS = "ANALYTICS"
    CONSULTING = "CONSULTING"
    INTERNAL = "INTERNAL"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BlockerSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BlockerStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class HealthStatus(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


# ── Project Models ──────────────────────────────────────────────

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_type: ProjectType = ProjectType.MARKETING
    priority: int = Field(ge=1, le=10, default=5)
    token_budget: int = Field(ge=0, default=500000)
    deadline: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[ProjectType] = None
    status: Optional[ProjectStatus] = None
    phase: Optional[ProjectPhase] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    token_budget: Optional[int] = None
    deadline: Optional[datetime] = None


class ProjectResponse(ProjectBase):
    project_id: str
    status: ProjectStatus = ProjectStatus.PLANNING
    phase: ProjectPhase = ProjectPhase.INITIATION
    health: HealthStatus = HealthStatus.GREEN
    tokens_used: int = 0
    created_at: datetime
    updated_at: datetime
    assigned_agents: List[str] = []

    class Config:
        from_attributes = True


class ProjectList(BaseModel):
    items: List[ProjectResponse]
    total: int
    page: int
    page_size: int


# ── Task Models ─────────────────────────────────────────────────

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    project_id: str
    assigned_agent: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_agent: Optional[str] = None


class TaskResponse(TaskBase):
    task_id: str
    project_id: str
    status: TaskStatus = TaskStatus.TODO
    assigned_agent: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int


# ── Blocker Models ──────────────────────────────────────────────

class BlockerBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: BlockerSeverity = BlockerSeverity.MEDIUM


class BlockerCreate(BlockerBase):
    project_id: str


class BlockerUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[BlockerSeverity] = None
    status: Optional[BlockerStatus] = None
    resolution: Optional[str] = None


class BlockerResponse(BlockerBase):
    blocker_id: str
    project_id: str
    status: BlockerStatus = BlockerStatus.OPEN
    resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BlockerList(BaseModel):
    items: List[BlockerResponse]
    total: int
    page: int
    page_size: int


# ── Dashboard Models ────────────────────────────────────────────

class DashboardStats(BaseModel):
    active_projects: int
    total_projects: int
    red_projects: int
    pending_tasks: int
    total_tasks: int
    open_blockers: int
    critical_blockers: int
    agents_busy: int
    agents_total: int
    tokens_used_today: int
    daily_token_budget: int


class TokenStat(BaseModel):
    date: str
    tokens_used: int


class TokenStats(BaseModel):
    daily: List[TokenStat]
    total_used: int
    total_budget: int


class SystemHealth(BaseModel):
    status: str
    version: str
    agents_available: int
    agents_busy: int
    database_connected: bool
    redis_connected: bool
    uptime_seconds: int


# ── Agent Models ────────────────────────────────────────────────

class AgentInfo(BaseModel):
    name: str
    role: str
    status: Literal["idle", "busy", "offline"] = "idle"
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tokens_used: int = 0


class AgentList(BaseModel):
    items: List[AgentInfo]
    total: int