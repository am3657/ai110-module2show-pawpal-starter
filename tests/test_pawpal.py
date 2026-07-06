from pawlpal_system import Pet, Scheduler, Task


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
