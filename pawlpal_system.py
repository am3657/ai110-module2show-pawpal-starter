from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    duration: int
    frequency: str
    completion_status: bool = False
    priority: str = ""

    def mark_complete(self) -> None:
        self.completion_status = True

    def update_frequency(self, frequency: str) -> None:
        self.frequency = frequency

    def set_priority(self, priority: str) -> None:
        self.priority = priority


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
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2, "": 3}

    def add_task(self, pet: Pet, task: Task) -> None:
        pet.tasks.append(task)

    def remove_task(self, pet: Pet, task: Task) -> None:
        pet.tasks.remove(task)

    def produce_plan(self, owner: Owner) -> List[Task]:
        pending_tasks = [task for task in owner.get_all_tasks() if not task.completion_status]
        pending_tasks.sort(key=lambda task: self.PRIORITY_ORDER.get(task.priority, 3))

        plan: List[Task] = []
        remaining_time = owner.time_available
        for task in pending_tasks:
            if task.duration <= remaining_time:
                plan.append(task)
                remaining_time -= task.duration

        return plan

    def explain_plan(self, owner: Owner) -> str:
        plan = self.produce_plan(owner)
        if not plan:
            return "No tasks fit within the available time."

        total_time = sum(task.duration for task in plan)
        lines = [f"Plan for {owner.name} ({total_time}/{owner.time_available} min used):"]

        for pet in owner.pets:
            pet_tasks = [task for task in plan if task in pet.tasks]
            if not pet_tasks:
                continue

            lines.append(f"\nDaily plan for {pet.name} ({pet.breed}):")
            for task in pet_tasks:
                lines.append(
                    f"  {task.description} ({task.duration} min) [priority: {task.priority or 'none'}]"
                )

        return "\n".join(lines)
