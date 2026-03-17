# backend/app/db/crud.py

from sqlalchemy.orm import Session
from app.db.models import User, Task, Report, TaskStatus
from app.core.security import hash_password
from typing import Optional


# ─── USER CRUD ───────────────────────────────────────────

def create_user(db: Session, email: str, password: str) -> User:
    user = User(
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


# ─── TASK CRUD ───────────────────────────────────────────

def create_task(db: Session, user_id: int, topic: str) -> Task:
    task = Task(
        user_id=user_id,
        topic=topic,
        status=TaskStatus.pending
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks_by_user(db: Session, user_id: int) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .all()
    )


def update_task_status(db: Session, task_id: int, status: TaskStatus) -> Optional[Task]:
    task = get_task_by_id(db, task_id)
    if not task:
        return None
    task.status = status
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> bool:
    task = get_task_by_id(db, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True


# ─── REPORT CRUD ─────────────────────────────────────────

def create_report(
    db: Session,
    task_id: int,
    content: str,
    sources: list,
    agent_steps: list
) -> Report:
    report = Report(
        task_id=task_id,
        content=content,
        sources=sources,
        agent_steps=agent_steps
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_report_by_task_id(db: Session, task_id: int) -> Optional[Report]:
    return db.query(Report).filter(Report.task_id == task_id).first()


def get_reports_by_user(db: Session, user_id: int) -> list[Report]:
    return (
        db.query(Report)
        .join(Task)
        .filter(Task.user_id == user_id)
        .order_by(Report.created_at.desc())
        .all()
    )


def delete_report(db: Session, report_id: int) -> bool:
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        return False
    db.delete(report)
    db.commit()
    return True
# ```

# ---

# **Step 3a: Security**
# ```
# backend/app/core/security.py