from app.celery.worker import celery_app
from app.db.database import SessionLocal
from app.db.models import TaskStatus
from app.db import crud
import logging

logger = logging.getLogger(__name__)

@celery_app.task(
    bind=True,
    name="app.celery.tasks.run_agent_task",
    max_retries=3,
    default_retry_delay=5
)
def run_agent_task(self, task_id: int, topic: str, user_id: int):
    db = SessionLocal()
    try:
        # ── 1. mark task as running ──────────────────────
        crud.update_task_status(db, task_id, TaskStatus.running)
        logger.info(f"Task {task_id} started for topic: {topic}")

        # ── 2. run LangGraph agent (placeholder for now) ─
        # we will replace this in Step 6 with real agent
        from app.agent.graph import run_agent
        result = run_agent(
            task_id=task_id,
            topic=topic,
            user_id=user_id
        )

         # ── 3. save report to DB ─────────────────────────
        crud.create_report(
            db=db,
            task_id=task_id,
            content=result["content"],
            sources=result["sources"],
            agent_steps=result["agent_steps"]
        )

        # ── 4. mark task as done ─────────────────────────
        crud.update_task_status(db, task_id, TaskStatus.done)
        logger.info(f"Task {task_id} completed successfully")

        return {"status": "done", "task_id": task_id}
    except Exception as e:
        # ── mark task as failed ──────────────────────────
        crud.update_task_status(db, task_id, TaskStatus.failed)
        logger.error(f"Task {task_id} failed: {str(e)}")

        # retry if attempts remaining
        raise self.retry(exc=e)
    finally:
        db.close()
# ```

# ---

# **Step 4c: Agent Route**
# ```
# backend/app/api/routes/agent.py        