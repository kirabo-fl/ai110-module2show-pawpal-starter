from dataclasses import dataclass, field
from datetime import date
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

    def complete_task(self, task: Task) -> None:
        """Mark a task as completed."""
        task.completed = True
