from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Schema models define the structure and validation rules for API requests/responses
# These models are used for data validation and serialization in the API layer
# They are based on the database models defined in models/project_models.py

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    creator_id: Optional[str] = Field(None)

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    status: str
    current_stage: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    creator_id: Optional[str] = None

    class Config:
        orm_mode = True

class StageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class StageCreate(StageBase):
    pass

class Stage(StageBase):
    id: str
    project_id: str
    status: str
    modifier_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TaskAssigneeBase(BaseModel):
    assignee_id: str
    assignee_type: str = Field(..., regex="^(USER|AGENT)$")
    role: str = Field(..., min_length=1, max_length=50)

class TaskAssigneeCreate(TaskAssigneeBase):
    pass

class TaskAssignee(TaskAssigneeBase):
    id: str
    task_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    stage_id: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    assignees: Optional[List[TaskAssigneeCreate]] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    project_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    assignees: List[TaskAssignee]

    class Config:
        orm_mode = True

class PermissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class MemberPermissionBase(BaseModel):
    permission_id: str

class MemberPermissionCreate(MemberPermissionBase):
    pass

class MemberPermission(MemberPermissionBase):
    id: str
    member_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class MemberBase(BaseModel):
    member_id: str
    member_type: str = Field(..., regex="^(USER|AGENT)$")
    role: str = Field(..., min_length=1, max_length=50)
    permissions: Optional[List[MemberPermissionCreate]] = None

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: str
    project_id: str
    member_id: str
    created_at: datetime
    permissions: List[MemberPermission]

    class Config:
        orm_mode = True
