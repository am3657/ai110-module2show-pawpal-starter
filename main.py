from pawlpal_system import Owner, Pet, Task, Scheduler


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


if __name__ == "__main__":
    main()
