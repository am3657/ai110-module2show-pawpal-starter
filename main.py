from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    scheduler = Scheduler()
    owner = Owner(
        name="Alex",
        age=29,
        pets=[],
        scheduler=scheduler,
        time_available=60,
    )

    dog = Pet(name="Rex", breed="Labrador", species="Dog", age=3)
    cat = Pet(name="Luna", breed="Siamese", species="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    walk = Task(description="Walk Rex", duration=30, frequency="daily")
    feed = Task(description="Feed Luna", duration=10, frequency="daily")
    litter_box = Task(description="Clean Luna's litter box", duration=15, frequency="weekly")

    litter_box.set_priority("low")
    walk.set_priority("high")
    feed.set_priority("high")

    scheduler.add_task(cat, litter_box)
    scheduler.add_task(dog, walk)
    scheduler.add_task(cat, feed)

    print("Today's Schedule")
    print(scheduler.explain_plan(owner))

    # Completing a recurring task spawns its next occurrence automatically —
    # use complete_task() (not task.mark_complete()) so the new instance gets
    # registered on the pet and picked up by future plans.
    next_walk = scheduler.complete_task(dog, walk)
    if next_walk is not None:
        print(f"\n'{walk.description}' is done for today. Next occurrence due {next_walk.due_date}.")

    # Demonstrate conflict detection: both tasks have 0 duration, so the
    # scheduling clock doesn't advance between them and they land on the same
    # "HH:MM" slot — explain_plan should warn about it.
    medicine = Task(description="Give medicine", duration=0, frequency="")
    check_tags = Task(description="Check tags", duration=0, frequency="")
    scheduler.add_task(dog, medicine)
    scheduler.add_task(dog, check_tags)

    print("\nSchedule with a time conflict:")
    print(scheduler.explain_plan(owner))


if __name__ == "__main__":
    main()
