from datetime import date

from pawpal_system import Pet, Scheduler,Task, Owner


def test_sort_by_time():
    """Tasks given out of order are returned sorted chronologically by start time."""
    scheduler = Scheduler()
    early = Task(description="Feed breakfast", duration=10, frequency="")
    mid = Task(description="Walk", duration=20, frequency="")
    late = Task(description="Feed dinner", duration=15, frequency="")

    # Deliberately built out of order to confirm sort_by_time reorders them.
    start_times = {
        id(late): "18:00",
        id(early): "08:00",
        id(mid): "12:30",
    }

    sorted_tasks = scheduler.sort_by_time([late, early, mid], start_times)

    assert sorted_tasks == [early, mid, late]


def test_recurring_tasks():
    """Completing a daily task spawns a new task due the following day."""
    pet = Pet(name="Rex", breed="Labrador", species="Dog", age=3)
    scheduler = Scheduler()
    task = Task(description="Walk the dog", duration=20, frequency="daily", due_date=date(2026, 7, 7))
    scheduler.add_task(pet, task)

    next_task = scheduler.complete_task(pet, task)

    assert task.completion_status is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 8)
    assert next_task.completion_status is False
    assert next_task in pet.tasks


def test_detect_time_conflicts():
    """Two tasks scheduled at the same start time produce a single conflict warning."""
    scheduler = Scheduler()
    task_a = Task(description="Walk the dog", duration=0, frequency="")
    task_b = Task(description="Feed the cat", duration=0, frequency="")
    plan = [task_a, task_b]
    start_times = {id(task_a): "09:00", id(task_b): "09:00"}

    warnings = scheduler.detect_time_conflicts(plan, start_times)

    assert len(warnings) == 1
    assert "Conflict at 09:00" in warnings[0]
    assert "Walk the dog" in warnings[0]
    assert "Feed the cat" in warnings[0]


def test_task_completion():
    task = Task(description="Walk the dog", duration=20, frequency="daily")
    assert task.completion_status is False

    task.mark_complete()

    assert task.completion_status is True


def test_task_addition():
    pet = Pet(name="Rex", breed="Labrador", species="Dog", age=3)
    task = Task(description="Walk the dog", duration=20, frequency="daily")
    scheduler = Scheduler()

    assert len(pet.tasks) == 0

    scheduler.add_task(pet, task)

    assert len(pet.tasks) == 1
