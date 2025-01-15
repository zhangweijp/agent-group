from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.project_models import Project, Stage, Task, TaskAssignee, ProjectMember
from models.user_models import User
from schemas.project_schemas import (
    ProjectCreate,
    Project,
    StageCreate,
    Stage,
    TaskCreate,
    Task,
    TaskAssigneeCreate,
    TaskAssignee,
    MemberCreate,
    Member
)
from core.database import get_db
from fastapi_users import FastAPIUsers, models
from fastapi_users.manager import BaseUserManager
from fastapi_users.authentication import JWTAuthentication

def get_current_user(
    user: models.BaseUserDB = Depends(FastAPIUsers.get_current_user)
) -> models.BaseUserDB:
    return user

router = APIRouter(prefix="/api")

@router.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: models.BaseUserDB = Depends(get_current_user)
):
    db_project = Project(
        name=project.name,
        description=project.description,
        creator_id=current_user.id
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/projects", response_model=List[Project])
async def get_projects(
    page: int = 1,
    pageSize: int = 10,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * pageSize
    query = select(Project).join(User, Project.creator_id == User.id, isouter=True)
    if status:
        query = query.where(Project.status == status)
    projects = await db.execute(
        query.offset(offset).limit(pageSize)
    )
    return projects.scalars().all()

@router.get("/projects/{project_id}/stages", response_model=List[Stage])
async def get_stages(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    query = select(Stage).join(User, Stage.modifier_id == User.id, isouter=True)
    query = query.where(Stage.project_id == project_id)
    stages = await db.execute(query)
    return stages.scalars().all()

@router.post("/projects/{project_id}/stages", response_model=Stage, status_code=status.HTTP_201_CREATED)
async def create_stage(
    project_id: str,
    stage: StageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.BaseUserDB = Depends(get_current_user)
):
    db_stage = Stage(
        project_id=project_id,
        name=stage.name,
        start_date=stage.start_date,
        end_date=stage.end_date,
        modifier_id=current_user.id
    )
    db.add(db_stage)
    await db.commit()
    await db.refresh(db_stage)
    return db_stage

@router.post("/projects/{project_id}/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: str,
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        db_task = Task(
            project_id=project_id,
            stage_id=task.stage_id,
            name=task.name,
            description=task.description,
            priority=task.priority
        )
        db.add(db_task)
        await db.flush()
        
        if task.assignees:
            for assignee in task.assignees:
                db_assignee = TaskAssignee(
                    task_id=db_task.id,
                    assignee_id=assignee.assignee_id,
                    assignee_type=assignee.assignee_type,
                    role=assignee.role
                )
                db.add(db_assignee)
        
        await db.commit()
        await db.refresh(db_task)
        return db_task

@router.post("/tasks/{task_id}/assignees", response_model=TaskAssignee, status_code=status.HTTP_201_CREATED)
async def add_task_assignee(
    task_id: str,
    assignee: TaskAssigneeCreate,
    db: AsyncSession = Depends(get_db)
):
    db_assignee = TaskAssignee(
        task_id=task_id,
        assignee_id=assignee.assignee_id,
        assignee_type=assignee.assignee_type,
        role=assignee.role
    )
    db.add(db_assignee)
    await db.commit()
    await db.refresh(db_assignee)
    return db_assignee

@router.get("/tasks/{task_id}/assignees", response_model=List[TaskAssignee])
async def get_task_assignees(
    task_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TaskAssignee).where(TaskAssignee.task_id == task_id)
    )
    return result.scalars().all()

@router.put("/tasks/{task_id}/assignees/{assignee_id}", response_model=TaskAssignee)
async def update_task_assignee(
    task_id: str,
    assignee_id: str,
    assignee: TaskAssigneeCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TaskAssignee)
        .where(TaskAssignee.task_id == task_id)
        .where(TaskAssignee.id == assignee_id)
    )
    db_assignee = result.scalar_one_or_none()
    if not db_assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
    db_assignee.assignee_id = assignee.assignee_id
    db_assignee.assignee_type = assignee.assignee_type
    db_assignee.role = assignee.role
    
    await db.commit()
    await db.refresh(db_assignee)
    return db_assignee

@router.delete("/tasks/{task_id}/assignees/{assignee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task_assignee(
    task_id: str,
    assignee_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TaskAssignee)
        .where(TaskAssignee.task_id == task_id)
        .where(TaskAssignee.id == assignee_id)
    )
    db_assignee = result.scalar_one_or_none()
    if not db_assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
    await db.delete(db_assignee)
    await db.commit()

@router.post("/projects/{project_id}/members", response_model=Member, status_code=status.HTTP_201_CREATED)
async def add_member(
    project_id: str,
    member: MemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.BaseUserDB = Depends(get_current_user)
):
    async with db.begin():
        db_member = ProjectMember(
            project_id=project_id,
            member_id=member.member_id,
            member_type=member.member_type,
            role=member.role
        )
        db.add(db_member)
        await db.flush()
        
        if member.permissions:
            for permission in member.permissions:
                db_permission = ProjectMemberPermission(
                    member_id=db_member.id,
                    permission_id=permission.permission_id
                )
                db.add(db_permission)
        
        await db.commit()
        await db.refresh(db_member)
        return db_member

@router.get("/projects/{project_id}/members", response_model=List[Member])
async def get_members(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    query = select(ProjectMember).join(User, ProjectMember.member_id == User.id)
    query = query.where(ProjectMember.project_id == project_id)
    members = await db.execute(query)
    return members.scalars().all()

@router.post("/permissions", response_model=Permission, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission: PermissionCreate,
    db: AsyncSession = Depends(get_db)
):
    db_permission = ProjectPermission(
        name=permission.name,
        description=permission.description
    )
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    return db_permission

@router.get("/permissions", response_model=List[Permission])
async def get_permissions(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ProjectPermission))
    return result.scalars().all()

@router.post("/members/{member_id}/permissions", response_model=MemberPermission, status_code=status.HTTP_201_CREATED)
async def add_member_permission(
    member_id: str,
    permission: MemberPermissionCreate,
    db: AsyncSession = Depends(get_db)
):
    db_permission = ProjectMemberPermission(
        member_id=member_id,
        permission_id=permission.permission_id
    )
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    return db_permission

@router.get("/members/{member_id}/permissions", response_model=List[MemberPermission])
async def get_member_permissions(
    member_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProjectMemberPermission)
        .where(ProjectMemberPermission.member_id == member_id)
    )
    return result.scalars().all()
