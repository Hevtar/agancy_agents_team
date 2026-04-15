"""
API routes for the Agency system.
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import (
    authenticate_user, create_access_token, get_current_user, 
    get_current_active_user, Token, UserResponse, UserInDB, UserCreate,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from api.models import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList,
    TaskCreate, TaskUpdate, TaskResponse, TaskList,
    BlockerCreate, BlockerUpdate, BlockerResponse, BlockerList,
    DashboardStats, TokenStats, SystemHealth, AgentInfo, AgentList
)
from api import crud

router = APIRouter()


# ── Authentication ──────────────────────────────────────────────

@router.post("/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserInDB = Depends(get_current_active_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role
    )


# ── Dashboard ───────────────────────────────────────────────────

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(current_user: UserInDB = Depends(get_current_active_user)):
    """Get dashboard statistics."""
    return crud.get_dashboard_stats()


@router.get("/system/status", response_model=SystemHealth)
async def get_system_status(current_user: UserInDB = Depends(get_current_active_user)):
    """Get system health status."""
    return crud.get_system_health()


@router.get("/tokens/stats", response_model=TokenStats)
async def get_token_stats(
    days: int = Query(7, ge=1, le=30, description="Number of days"),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get token usage statistics."""
    return crud.get_token_stats(days)


# ── Projects ────────────────────────────────────────────────────

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Create a new project."""
    return crud.create_project(project)


@router.get("/projects", response_model=ProjectList)
async def list_projects(
    status: Optional[str] = None,
    phase: Optional[str] = None,
    project_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """List all projects with filtering and pagination."""
    items, total = crud.list_projects(
        status=status,
        phase=phase,
        project_type=project_type,
        page=page,
        page_size=page_size
    )
    return ProjectList(items=items, total=total, page=page, page_size=page_size)


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get project by ID."""
    project = crud.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Update a project."""
    updated = crud.update_project(project_id, project)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Delete a project."""
    success = crud.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}


# ── Tasks ───────────────────────────────────────────────────────

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Create a new task."""
    return crud.create_task(task)


@router.get("/tasks", response_model=TaskList)
async def list_tasks(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    assigned_agent: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """List all tasks with filtering and pagination."""
    items, total = crud.list_tasks(
        project_id=project_id,
        status=status,
        assigned_agent=assigned_agent,
        page=page,
        page_size=page_size
    )
    return TaskList(items=items, total=total, page=page, page_size=page_size)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get task by ID."""
    task = crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task: TaskUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Update a task."""
    updated = crud.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Delete a task."""
    success = crud.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}


# ── Blockers ────────────────────────────────────────────────────

@router.post("/blockers", response_model=BlockerResponse, status_code=status.HTTP_201_CREATED)
async def create_blocker(
    blocker: BlockerCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Create a new blocker."""
    return crud.create_blocker(blocker)


@router.get("/blockers", response_model=BlockerList)
async def list_blockers(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """List all blockers with filtering and pagination."""
    items, total = crud.list_blockers(
        project_id=project_id,
        status=status,
        severity=severity,
        page=page,
        page_size=page_size
    )
    return BlockerList(items=items, total=total, page=page, page_size=page_size)


@router.get("/blockers/{blocker_id}", response_model=BlockerResponse)
async def get_blocker(
    blocker_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get blocker by ID."""
    blocker = crud.get_blocker(blocker_id)
    if not blocker:
        raise HTTPException(status_code=404, detail="Blocker not found")
    return blocker


@router.put("/blockers/{blocker_id}", response_model=BlockerResponse)
async def update_blocker(
    blocker_id: str,
    blocker: BlockerUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Update a blocker."""
    updated = crud.update_blocker(blocker_id, blocker)
    if not updated:
        raise HTTPException(status_code=404, detail="Blocker not found")
    return updated


@router.delete("/blockers/{blocker_id}")
async def delete_blocker(
    blocker_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Delete a blocker."""
    success = crud.delete_blocker(blocker_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blocker not found")
    return {"message": "Blocker deleted"}


# ── Agents ──────────────────────────────────────────────────────

@router.get("/agents", response_model=AgentList)
async def list_agents(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """List all agents."""
    agents = crud.get_agents()
    return AgentList(items=agents, total=len(agents))


@router.get("/agents/{agent_name}", response_model=AgentInfo)
async def get_agent(
    agent_name: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get agent by name."""
    agent = crud.get_agents()
    for a in agent:
        if a.name == agent_name:
            return a
    raise HTTPException(status_code=404, detail="Agent not found")