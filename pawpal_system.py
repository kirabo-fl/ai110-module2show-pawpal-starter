from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Schedule:
    start_date: date
    frequency: str  # e.g. "daily", "weekly", "once"
    time: str       # e.g. "08:00"


@dataclass
class Task:
    title: str
    description: str
    priority: str   # e.g. "low", "medium", "high"
    schedule: Optional[Schedule] = None


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass
