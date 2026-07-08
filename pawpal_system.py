from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    description: str
    duration: int
    frequency: str
    completion_status: bool = False
    priority: str = ""
    # Gates whether this task is eligible for today's plan, and is what lets a
    # recurring task's next instance stay hidden until it's actually due.
    due_date: date = field(default_factory=date.today)

    # How far out the next occurrence should be due, per frequency. A frequency
    # not listed here (e.g. "" or a one-time task) simply doesn't recur.
    FREQUENCY_INTERVALS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completion_status = True

    def get_next_due_date(self) -> Optional[date]:
        """Return the due date for this task's next occurrence, or None if it doesn't recur."""
        interval = self.FREQUENCY_INTERVALS.get(self.frequency)
        if interval is None:
            return None
        # Advance from this task's own due_date, not today, so completing a task
        # late doesn't shift the whole recurrence schedule forward.
        return self.due_date + interval

    def update_frequency(self, frequency: str) -> None:
        """Change how often this task recurs."""
        self.frequency = frequency

    def set_priority(self, priority: str) -> None:
        """Change this task's priority."""
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
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list of pets."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_tasks_by_completion(self, completed: bool) -> List[Task]:
        """Return all of this owner's tasks matching the given completion status."""
        return [task for task in self.get_all_tasks() if task.completion_status == completed]


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2, "": 3}
    DEFAULT_START_TIME = "08:00"

    def add_task(self, pet: Pet, task: Task) -> None:
        """Add a task to the given pet's task list."""
        pet.tasks.append(task)

    def remove_task(self, pet: Pet, task: Task) -> None:
        """Remove a task from the given pet's task list."""
        pet.tasks.remove(task)

    def complete_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a task complete, spawning its next occurrence if it recurs.

        This lives on Scheduler rather than Task.mark_complete() because a Task
        has no reference back to its owning Pet — only Scheduler (which already
        owns add_task/remove_task) can register the newly spawned instance.
        """
        task.mark_complete()
        next_due_date = task.get_next_due_date()
        if next_due_date is None:
            return None

        next_task = Task(
            description=task.description,
            duration=task.duration,
            frequency=task.frequency,
            priority=task.priority,
            due_date=next_due_date,
        )
        self.add_task(pet, next_task)
        return next_task

    def produce_plan(self, owner: Owner) -> List[Task]:
        """Build a priority-sorted list of tasks that fit within the owner's available time."""
        pending_tasks = owner.get_tasks_by_completion(completed=False)
        # A recurring task's next instance is created immediately with a future
        # due_date, so it must stay out of today's plan until that date arrives.
        today = date.today()
        pending_tasks = [task for task in pending_tasks if task.due_date <= today]
        pending_tasks.sort(key=lambda task: self.PRIORITY_ORDER.get(task.priority, 3))

        plan: List[Task] = []
        remaining_time = owner.time_available
        for task in pending_tasks:
            if task.duration <= remaining_time:
                plan.append(task)
                remaining_time -= task.duration

        return plan

    def sort_by_time(self, tasks: List[Task], start_times: dict) -> List[Task]:
        """Sort tasks chronologically by their "HH:MM" start time."""
        return sorted(tasks, key=lambda task: start_times[id(task)])

    def detect_time_conflicts(self, plan: List[Task], start_times: dict) -> List[str]:
        """Return one warning per start time slot claimed by more than one task.

        Tasks normally can't collide since the plan's clock only advances, but a
        zero-duration task (or a future change to how start times get assigned)
        could still put two tasks in the same slot — this is the safety net.
        """
        tasks_by_time: dict = {}
        for task in plan:
            tasks_by_time.setdefault(start_times[id(task)], []).append(task)

        warnings = []
        for time_slot, tasks in tasks_by_time.items():
            if len(tasks) > 1:
                names = ", ".join(task.description for task in tasks)
                warnings.append(f"Conflict at {time_slot}: {names} are scheduled at the same time.")
        return warnings

    def build_schedule(self, owner: Owner) -> dict:
        """Return the produced plan as structured data (not pre-formatted text).

        explain_plan renders this same structure as text; a UI can instead read
        it directly to build real widgets (tables, expanders, etc.) per pet.
        """
        plan = self.produce_plan(owner)
        if not plan:
            return {"total_time": 0, "conflicts": [], "pets": []}

        clock = datetime.strptime(self.DEFAULT_START_TIME, "%H:%M")
        start_times = {}
        for task in plan:
            start_times[id(task)] = clock.strftime("%H:%M")
            clock += timedelta(minutes=task.duration)

        pets = []
        for pet in owner.pets:
            pet_tasks = self.sort_by_time(
                [task for task in plan if task in pet.tasks], start_times
            )
            if not pet_tasks:
                continue

            pets.append(
                {
                    "pet": pet,
                    "tasks": [
                        {"time": start_times[id(task)], "task": task} for task in pet_tasks
                    ],
                }
            )

        return {
            "total_time": sum(task.duration for task in plan),
            "conflicts": self.detect_time_conflicts(plan, start_times),
            "pets": pets,
        }

    def explain_plan(self, owner: Owner) -> str:
        """Render the produced plan as a readable, per-pet daily schedule."""
        schedule = self.build_schedule(owner)
        if not schedule["pets"]:
            return "No tasks fit within the available time."

        lines = [f"Plan for {owner.name} ({schedule['total_time']}/{owner.time_available} min used):"]

        for warning in schedule["conflicts"]:
            lines.append(f"⚠ Warning: {warning}")

        for section in schedule["pets"]:
            pet = section["pet"]
            lines.append(f"\nDaily plan for {pet.name} ({pet.breed}):")
            for entry in section["tasks"]:
                task = entry["task"]
                lines.append(
                    f"  {entry['time']} — {task.description} ({task.duration} min) "
                    f"[priority: {task.priority or 'none'}]"
                )

        return "\n".join(lines)
