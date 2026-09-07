"""Data model mirroring the terminology table in README.md.

Keep this in sync with README.md's Terminologies section — it is the
single source of truth for these names.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class ActionPlanStatus(StrEnum):
    DRAFT = "draft"
    NON_ACCEPTED = "non_accepted"
    ACCEPTED = "accepted"


class Task(BaseModel):
    id: str
    description: str
    created_at: datetime


class Feedback(BaseModel):
    action_plan_id: str
    content: str
    created_at: datetime


class ActionPlan(BaseModel):
    id: str
    task_id: str
    content: str
    status: ActionPlanStatus
    prompt_template_version: str
    created_at: datetime
