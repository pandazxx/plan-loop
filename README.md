# Plan-loop

## Objective

- Use mini-swe-agent as orchestrator (named _swe_ for short). It runs a LLM agent (named _swe-agent_) to instruct another LLM agent (named _target-agent_) to plan and execute.
- The prompt that _swe_ feed to _swe-agent_, the _swe-agent_ feed to _target-agent_ and the planning result will be further training material. The prompt that _swe_ feed to _swe-agent_ is the optimization target.

## Terminologies

Terminologies are very important for communication and understanding of this project. All key entities, components, actors, concepts, etc. should be maintained in this canoniccal table for reference.

- _swe_: this project
- _user_: The human
- _task_: The job that _user_ wants to get done. The base unit of the journey.
- _swe-llm_: The LLM model that act as the brain of _swe_. Understands the _user_ requirement and instructs the _work-llm_. **NEVER** does the actual implementation. It's _work-llm_'s job.
- _work-llm_: The LLM model that does the job with the instruction from _swe-llm_.
- _action-plan_: The plan that _work-llm_ generates by following the instruction from _swe-llm_. This will be the instruction for implementation if approved by _user_.


## Typical workflow

1. User assigns _task_ to _swe_
2. _swe_ uses _plan-task-prompt_ to instruct _swe-llm_ to generate the prompt to _work-llm_ to plan the action for the _task_
3. _work-llm_ returns the _action-plan_ for user to review
4. User gives feedbacks
5. _swe_ tag this _action-plan_ as _non-accepted_
6. _swe_ use _plan-amend-prompt_ to instruct _swe-llm_ to generate the prompt to _work-llm_ to amend the _action-plan_
7. _work-llm_ revises the _action-plan_ and returns it to user for review
8. Loops until user approves the _action-plan_
9. _swe_ tag the approved _action-plan_ as _accepted_
10. _swe_ send the approved _action-plan_ to _work-llm_ to fulfill the task


