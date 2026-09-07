from datetime import datetime

from plan_loop.models import ActionPlan, ActionPlanStatus


def test_action_plan_defaults_are_constructible():
    plan = ActionPlan(
        id="plan-1",
        task_id="task-1",
        content="do the thing",
        status=ActionPlanStatus.DRAFT,
        prompt_template_version="v1",
        created_at=datetime.now(),
    )
    assert plan.status is ActionPlanStatus.DRAFT
