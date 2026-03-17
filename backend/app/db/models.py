# backend/app/db/models.py

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, 
    ForeignKey, Enum, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class TaskStatus(enum.Enum):
    pending = "pending"
    running = "running"
    done = "done"
    failed = "failed"


class User(Base):
    __tablename__ = "users"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email            = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password  = Column(String(255), nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationship
    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic      = Column(String(500), nullable=False)
    status     = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    user   = relationship("User", back_populates="tasks")
    report = relationship("Report", back_populates="task", uselist=False)


class Report(Base):
    __tablename__ = "reports"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id      = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, unique=True)
    content      = Column(Text, nullable=False)
    sources      = Column(JSON, nullable=True)   
    agent_steps  = Column(JSON, nullable=True)   
    created_at   = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationship
    task = relationship("Task", back_populates="report")