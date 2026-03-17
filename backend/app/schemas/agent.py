# backend/app/schemas/agent.py

from pydantic import BaseModel
from datetime import datetime
from app.db.models import TaskStatus


class TaskSubmitRequest(BaseModel):
    topic: str


class TaskResponse(BaseModel):
    id: int
    topic: str
    status: TaskStatus
    created_at: datetime

    class Config:
        from_attributes = True


class TaskStatusResponse(BaseModel):
    id: int
    topic: str
    status: TaskStatus
    created_at: datetime

    class Config:
        from_attributes = True