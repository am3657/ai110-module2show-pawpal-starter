from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    task_type: str
    duration: int
    frequency: str
    completion_status: bool = False
    priority: str = ""

    def mark_complete(self) -> None:
        pass

    def update_frequency(self, frequency: str) -> None:
        pass

    def set_priority(self, priority: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)


class Owner:
    def __init__(
        self,
        name: str,
        age: int,
        pets: List[Pet],
        scheduler: "Scheduler",
        time_available: int,
    ) -> None:
        self.name = name
        self.age = age
        self.pets = pets
        self.scheduler = scheduler
        self.time_available = time_available

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def add_task(self, pet: Pet, task: Task) -> None:
        pass

    def remove_task(self, pet: Pet, task: Task) -> None:
        pass

    def produce_plan(self, owner: Owner) -> List[Task]:
        pass

    def explain_plan(self, owner: Owner) -> str:
        pass
