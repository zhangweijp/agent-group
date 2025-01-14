import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey

# Database models define the structure and relationships of database tables
# These models are used for database operations and data persistence
# They serve as the foundation for the schema models in schemas/project_schemas.py
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship
from core.database import Base

# Project
class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
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
    created_at = Column(DATETIME, server_default=func.now())
    updated_at = Column(DATETIME, server_default=func.now(), onupdate=func.now())

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

class ProjectMember(Base):
    __tablename__ = 'project_members'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey('projects.id', ondelete='CASCADE'))
    member_id = Column(String, nullable=False)
    member_type = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DATETIME, server_default=func.now())
