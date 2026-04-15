"""
CRUD operations for the Agency system.
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from api.models import (
    ProjectResponse, ProjectCreate, ProjectUpdate, ProjectStatus, ProjectPhase, ProjectType, HealthStatus,
    TaskResponse, TaskCreate, TaskUpdate, TaskStatus,
    BlockerResponse, BlockerCreate, BlockerUpdate, BlockerStatus,
    DashboardStats, TokenStat, TokenStats, SystemHealth, AgentInfo
)


# ── In-Memory Storage (replace with real DB in production) ─────

projects_db: Dict[str, ProjectResponse] = {}
tasks_db: Dict[str, TaskResponse] = {}
blockers_db: Dict[str, BlockerResponse] = {}
agent_statuses: Dict[str, AgentInfo] = {}

# Initialize some mock agents
def init_agents():
    agent_names = [
        ("marketing_strategist", "Маркетолог-стратег"),
        ("content_manager", "Контент-менеджер"),
        ("seo_copywriter", "SEO-копирайтер"),
        ("social_media_manager", "SMM-менеджер"),
        ("data_analyst", "Дата-аналитик"),
        ("seo_specialist", "SEO-специалист"),
        ("email_marketing_manager", "Email-маркетолог"),
        ("ppc_specialist", "PPC-специалист"),
        ("ux_designer", "UX-дизайнер"),
        ("brand_manager", "Бренд-менеджер"),
        ("cro_specialist", "CRO-специалист"),
        ("customer_support_agent", "Поддержка клиентов"),
        ("report_generator", "Генератор отчетов"),
        ("project_manager", "Проектный менеджер"),
    ]
    for name, role in agent_names:
        agent_statuses[name] = AgentInfo(
            name=name,
            role=role,
            status="idle"
        )

init_agents()


# ── Project CRUD ────────────────────────────────────────────────

def create_project(data: ProjectCreate) -> ProjectResponse:
    project_id = f"PRJ-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.utcnow()
    project = ProjectResponse(
        project_id=project_id,
        **data.model_dump(),
        status=ProjectStatus.PLANNING,
        phase=ProjectPhase.INITIATION,
        health=HealthStatus.GREEN,
        tokens_used=0,
        created_at=now,
        updated_at=now,
        assigned_agents=[]
    )
    projects_db[project_id] = project
    return project


def get_project(project_id: str) -> Optional[ProjectResponse]:
    return projects_db.get(project_id)


def list_projects(
    status: Optional[ProjectStatus] = None,
    phase: Optional[ProjectPhase] = None,
    project_type: Optional[ProjectType] = None,
    page: int = 1,
    page_size: int = 20
) -> List[ProjectResponse]:
    items = list(projects_db.values())
    
    if status:
        items = [p for p in items if p.status == status]
    if phase:
        items = [p for p in items if p.phase == phase]
    if project_type:
        items = [p for p in items if p.project_type == project_type]
    
    # Sort by updated_at desc
    items.sort(key=lambda x: x.updated_at, reverse=True)
    
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], len(items)


def update_project(project_id: str, data: ProjectUpdate) -> Optional[ProjectResponse]:
    project = projects_db.get(project_id)
    if not project:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(project, field, value)
    
    project.updated_at = datetime.utcnow()
    projects_db[project_id] = project
    return project


def delete_project(project_id: str) -> bool:
    if project_id in projects_db:
        del projects_db[project_id]
        return True
    return False


# ── Task CRUD ───────────────────────────────────────────────────

def create_task(data: TaskCreate) -> TaskResponse:
    task_id = f"TSK-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.utcnow()
    task = TaskResponse(
        task_id=task_id,
        **data.model_dump(),
        status=TaskStatus.TODO,
        created_at=now,
        updated_at=now,
        completed_at=None
    )
    tasks_db[task_id] = task
    return task


def get_task(task_id: str) -> Optional[TaskResponse]:
    return tasks_db.get(task_id)


def list_tasks(
    project_id: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    assigned_agent: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
) -> List[TaskResponse]:
    items = list(tasks_db.values())
    
    if project_id:
        items = [t for t in items if t.project_id == project_id]
    if status:
        items = [t for t in items if t.status == status]
    if assigned_agent:
        items = [t for t in items if t.assigned_agent == assigned_agent]
    
    # Sort by priority then updated_at
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    items.sort(key=lambda x: (priority_order.get(x.priority.value, 2), x.updated_at), reverse=True)
    
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], len(items)


def update_task(task_id: str, data: TaskUpdate) -> Optional[TaskResponse]:
    task = tasks_db.get(task_id)
    if not task:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    if task.status == TaskStatus.DONE and not task.completed_at:
        task.completed_at = datetime.utcnow()
    
    tasks_db[task_id] = task
    return task


def delete_task(task_id: str) -> bool:
    if task_id in tasks_db:
        del tasks_db[task_id]
        return True
    return False


# ── Blocker CRUD ────────────────────────────────────────────────

def create_blocker(data: BlockerCreate) -> BlockerResponse:
    blocker_id = f"BLK-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.utcnow()
    blocker = BlockerResponse(
        blocker_id=blocker_id,
        **data.model_dump(),
        status=BlockerStatus.OPEN,
        resolution=None,
        created_at=now,
        updated_at=now,
        resolved_at=None
    )
    blockers_db[blocker_id] = blocker
    return blocker


def get_blocker(blocker_id: str) -> Optional[BlockerResponse]:
    return blockers_db.get(blocker_id)


def list_blockers(
    project_id: Optional[str] = None,
    status: Optional[BlockerStatus] = None,
    severity: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
) -> List[BlockerResponse]:
    items = list(blockers_db.values())
    
    if project_id:
        items = [b for b in items if b.project_id == project_id]
    if status:
        items = [b for b in items if b.status == status]
    if severity:
        items = [b for b in items if b.severity.value == severity]
    
    # Sort by severity then created_at
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    items.sort(key=lambda x: (severity_order.get(x.severity.value, 2), x.created_at), reverse=True)
    
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], len(items)


def update_blocker(blocker_id: str, data: BlockerUpdate) -> Optional[BlockerResponse]:
    blocker = blockers_db.get(blocker_id)
    if not blocker:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(blocker, field, value)
    
    blocker.updated_at = datetime.utcnow()
    if blocker.status in [BlockerStatus.RESOLVED, BlockerStatus.CLOSED] and not blocker.resolved_at:
        blocker.resolved_at = datetime.utcnow()
    
    blockers_db[blocker_id] = blocker
    return blocker


def delete_blocker(blocker_id: str) -> bool:
    if blocker_id in blockers_db:
        del blockers_db[blocker_id]
        return True
    return False


# ── Dashboard & Stats ───────────────────────────────────────────

def get_dashboard_stats() -> DashboardStats:
    all_projects = list(projects_db.values())
    all_tasks = list(tasks_db.values())
    all_blockers = list(blockers_db.values())
    all_agents = list(agent_statuses.values())
    
    active_projects = len([p for p in all_projects if p.status == ProjectStatus.ACTIVE])
    red_projects = len([p for p in all_projects if p.health == HealthStatus.RED])
    pending_tasks = len([t for t in all_tasks if t.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS]])
    open_blockers = len([b for b in all_blockers if b.status == BlockerStatus.OPEN])
    critical_blockers = len([b for b in all_blockers if b.severity == "CRITICAL" and b.status == BlockerStatus.OPEN])
    agents_busy = len([a for a in all_agents if a.status == "busy"])
    
    # Mock token stats
    tokens_used_today = sum(a.tokens_used for a in all_agents)
    daily_token_budget = 1000000
    
    return DashboardStats(
        active_projects=active_projects,
        total_projects=len(all_projects),
        red_projects=red_projects,
        pending_tasks=pending_tasks,
        total_tasks=len(all_tasks),
        open_blockers=open_blockers,
        critical_blockers=critical_blockers,
        agents_busy=agents_busy,
        agents_total=len(all_agents),
        tokens_used_today=tokens_used_today,
        daily_token_budget=daily_token_budget
    )


def get_token_stats(days: int = 7) -> TokenStats:
    # Generate mock token usage data
    daily = []
    base_date = datetime.utcnow()
    for i in range(days - 1, -1, -1):
        date = base_date - timedelta(days=i)
        # Mock data with some variation
        tokens_used = 50000 + (i * 5000) + (hash(str(date.date())) % 20000)
        daily.append(TokenStat(
            date=date.strftime("%Y-%m-%d"),
            tokens_used=tokens_used
        ))
    
    total_used = sum(d.tokens_used for d in daily)
    total_budget = 1000000 * days
    
    return TokenStats(
        daily=daily,
        total_used=total_used,
        total_budget=total_budget
    )


def get_system_health() -> SystemHealth:
    all_agents = list(agent_statuses.values())
    agents_busy = len([a for a in all_agents if a.status == "busy"])
    
    return SystemHealth(
        status="healthy",
        version="1.0.0",
        agents_available=len([a for a in all_agents if a.status == "idle"]),
        agents_busy=agents_busy,
        database_connected=True,
        redis_connected=True,
        uptime_seconds=86400  # 1 day mock
    )


def get_agents() -> List[AgentInfo]:
    return list(agent_statuses.values())


def update_agent_status(agent_name: str, status: str, current_task: Optional[str] = None) -> Optional[AgentInfo]:
    agent = agent_statuses.get(agent_name)
    if not agent:
        return None
    
    agent.status = status  # type: ignore
    agent.current_task = current_task
    if status == "idle":
        agent.tasks_completed += 1
    return agent