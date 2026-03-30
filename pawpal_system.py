from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Schedule:
    start_date: date
    frequency: str              # "daily", "weekly", "once"
    time: str                   # "08:00"
    end_date: Optional[date] = None  # None means open-ended


@dataclass
class Task:
    title: str
    description: str
    priority: str               # "low", "medium", "high"
    pet_name: str               # which pet this task belongs to
    schedule: Optional[Schedule] = None
    completed: bool = False


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        """Return the first pet matching the given name, or None."""
        return next((p for p in self.pets if p.name == name), None)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of an Owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across every pet, sorted by priority (high first)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: priority_order.get(t.priority, 3))

    def get_tasks_by_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks for a specific pet by name."""
        pet = self.owner.get_pet_by_name(pet_name)
        if pet is None:
            return []
        return pet.get_tasks()

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        """Return all tasks matching the given priority level."""
        return [t for t in self.owner.get_all_tasks() if t.priority == priority]

    def get_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks across every pet."""
        return [t for t in self.owner.get_all_tasks() if not t.completed]

    def get_tasks_for_date(self, target: date) -> list[Task]:
        """Return tasks whose schedule is active on the given date."""
        results = []
        for task in self.owner.get_all_tasks():
            if task.schedule is None:
                continue
            s = task.schedule
            if s.start_date > target:
                continue
            if s.end_date is not None and s.end_date < target:
                continue
            if s.frequency == "once" and s.start_date == target:
                results.append(task)
            elif s.frequency in ("daily", "weekly", "once"):
                # daily and weekly tasks are active throughout their date range
                results.append(task)
        return results

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Args:
            completed: True for completed tasks, False for pending,
                       None to include both.
            pet_name:  Only return tasks belonging to this pet.
                       None to include all pets.
        """
        tasks = self.owner.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        return tasks

    def get_conflicts(self, target: Optional[date] = None) -> list[str]:
        """Return a list of human-readable warning strings for time conflicts.

        A conflict is any two tasks (same pet or different pets) whose schedule
        is active on 'target' and share the same time slot. Never raises —
        returns an empty list when no conflicts exist.

        Args:
            target: The date to check. Defaults to today.
        """
        if target is None:
            target = date.today()

        # Collect all tasks active on target that have a scheduled time
        active = [t for t in self.get_tasks_for_date(target) if t.schedule]

        # Group by time slot: {"08:00": [task, task, ...], ...}
        by_time: dict[str, list[Task]] = {}
        for task in active:
            by_time.setdefault(task.schedule.time, []).append(task)

        warnings: list[str] = []
        for time_slot, tasks in sorted(by_time.items()):
            if len(tasks) < 2:
                continue
            names = ", ".join(f"[{t.pet_name}] {t.title}" for t in tasks)
            warnings.append(
                f"WARNING: {len(tasks)} tasks overlap at {time_slot} on {target}: {names}"
            )

        return warnings

    def sort_by_time(self, tasks: Optional[list[Task]] = None) -> list[Task]:
        """Return tasks sorted by scheduled time (HH:MM), earliest first.
        Tasks without a schedule are placed at the end."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.schedule.time if t.schedule else "99:99")

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task as completed.

        For 'daily' and 'weekly' recurring tasks, automatically creates and
        schedules a new Task instance for the next occurrence.

        Returns the newly created Task, or None for 'once' tasks / no schedule.
        """
        task.completed = True

        if task.schedule is None or task.schedule.frequency not in ("daily", "weekly"):
            return None

        interval = timedelta(days=1 if task.schedule.frequency == "daily" else 7)
        next_start = task.schedule.start_date + interval

        # Don't create a next occurrence past the schedule's end date
        if task.schedule.end_date is not None and next_start > task.schedule.end_date:
            return None

        next_task = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            pet_name=task.pet_name,
            schedule=Schedule(
                start_date=next_start,
                frequency=task.schedule.frequency,
                time=task.schedule.time,
                end_date=task.schedule.end_date,
            ),
        )

        pet = self.owner.get_pet_by_name(task.pet_name)
        if pet is not None:
            pet.add_task(next_task)

        return next_task
