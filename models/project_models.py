import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey

# Database models define the structure and relationships of database tables
# These models are used for database operations and data persistence
# They serve as the foundation for the schema models in schemas/project_schemas.py
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship
from core.database import Base

# 增删改查
# 
class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id = Column(String, ForeignKey('users.id', ondelete='SET NULL'))
    name = Column(String(255), nullable=False)
    creator = relationship("User", back_populates="projects")
    description = Column(Text)
    status = Column(String(50), nullable=False, default='INIT')
    current_stage = Column(String(255))
    created_at = Column(DATETIME, server_default=func.now())
    updated_at = Column(DATETIME, server_default=func.now(), onupdate=func.now())

class Stage(Base):
    __tablename__ = 'stages'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey('projects.id', ondelete='CASCADE'))
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default='NOT_STARTED')
    start_date = Column(DATETIME)
    end_date = Column(DATETIME)
    modifier_id = Column(String, ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(DATETIME, server_default=func.now())
    updated_at = Column(DATETIME, server_default=func.now(), onupdate=func.now())
    modifier = relationship("User", foreign_keys=[modifier_id])

class TaskAssignee(Base):
    __tablename__ = 'task_assignees'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey('tasks.id', ondelete='CASCADE'))
    assignee_id = Column(String, nullable=False)
    assignee_type = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DATETIME, server_default=func.now())

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey('projects.id', ondelete='CASCADE'))
    stage_id = Column(String, ForeignKey('stages.id', ondelete='SET NULL'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False, default='TODO')
    priority = Column(Integer)
    created_at = Column(DATETIME, server_default=func.now())
    updated_at = Column(DATETIME, server_default=func.now(), onupdate=func.now())
    assignees = relationship('TaskAssignee', backref='task', cascade='all, delete-orphan')

class ProjectPermission(Base):
    """Defines available permissions that can be assigned to project members.
    Acts as a permission template that can be reused across projects.
    """
    __tablename__ = 'project_permissions'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True)  # Unique permission name (e.g. 'task_create')
    description = Column(Text)  # Human-readable description of the permission
    created_at = Column(DATETIME, server_default=func.now())

class ProjectMemberPermission(Base):
    """Links project members to their specific permissions.
    Represents the actual assignment of a permission to a member.
    """
    __tablename__ = 'project_member_permissions'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    member_id = Column(String, ForeignKey('project_members.id', ondelete='CASCADE'))  # Reference to project member
    permission_id = Column(String, ForeignKey('project_permissions.id', ondelete='CASCADE'))  # Reference to permission
    created_at = Column(DATETIME, server_default=func.now())
    permission = relationship("ProjectPermission")  # Relationship to permission details

class ProjectMember(Base):
    """Represents a member of a project and their permissions.
    Links a user to a project and manages their access rights.
    """
    __tablename__ = 'project_members'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey('projects.id', ondelete='CASCADE'))  # Reference to project
    member_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'))  # Reference to user
    member_type = Column(String(50), nullable=False)  # Type of member (e.g. 'USER', 'AGENT')
    role = Column(String(50), nullable=False)  # Member's role in the project
    created_at = Column(DATETIME, server_default=func.now())
    member = relationship("User", foreign_keys=[member_id])  # Relationship to user details
    permissions = relationship(
        "ProjectMemberPermission", 
        cascade="all, delete-orphan"  # Automatically delete permissions when member is deleted
    )
