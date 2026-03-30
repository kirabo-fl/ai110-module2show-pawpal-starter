# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

Four features were added to the `Scheduler` class to make the daily plan more useful:

| Feature | Method | What it does |
|---|---|---|
| **Time sorting** | `sort_by_time(tasks)` | Orders any task list chronologically by `HH:MM` start time. Tasks without a schedule are placed at the end. |
| **Flexible filtering** | `filter_tasks(completed, pet_name)` | Returns tasks matching any combination of completion status and/or pet name. Both parameters are optional — omit either to skip that filter. |
| **Auto-rescheduling** | `complete_task(task)` | Marks a task done. For `daily` tasks a new instance is created for the next day; for `weekly` tasks, seven days ahead. `once` tasks are not rescheduled. Returns the new `Task` or `None`. |
| **Conflict detection** | `get_conflicts(target)` | Scans all tasks active on a given date and returns a list of human-readable warning strings for any time slot with two or more overlapping tasks (same or different pets). Never raises — returns an empty list when there are no conflicts. |

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
