import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.


"""
)



st.divider()

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value="Jordan")
owner_age = st.number_input("Owner age", min_value=0, max_value=120, value=30)
time_available = st.number_input(
    "Time available today (minutes)", min_value=0, max_value=600, value=60
)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name,
        age=int(owner_age),
        pets=[],
        scheduler=st.session_state.scheduler,
        time_available=int(time_available),
    )

owner = st.session_state.owner
scheduler = st.session_state.scheduler
owner.time_available = int(time_available)

st.markdown("### Add a Pet")
pet_col1, pet_col2, pet_col3, pet_col4 = st.columns(4)
with pet_col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with pet_col2:
    breed = st.text_input("Breed", value="Mixed")
with pet_col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])
    # "other" is a placeholder value, not a real species, so ask for the actual
    # name and use that instead when it's selected.
    if species == "other":
        species = st.text_input("Species name", value="")
with pet_col4:
    pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=2)

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, breed=breed, species=species, age=int(pet_age)))

if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": p.name, "breed": p.breed, "species": p.species, "age": p.age} for p in owner.pets]
    )

    pet_index = st.selectbox(
        "Remove a pet",
        range(len(owner.pets)),
        format_func=lambda i: owner.pets[i].name,
        key="pet_to_remove",
    )
    if st.button("Remove pet"):
        owner.remove_pet(owner.pets[pet_index])
        st.rerun()
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed directly into your scheduler.")

# A task must belong to a specific pet (Scheduler.add_task requires one), so block
# task creation until at least one pet exists.
task_pet_name = st.selectbox("Pet for this task", [p.name for p in owner.pets]) if owner.pets else None

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=0, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    # "one-time" isn't in Task.FREQUENCY_INTERVALS, so it just never recurs.
    frequency = st.selectbox("Frequency", ["daily", "weekly", "one-time"], index=0)

if st.button("Add task"):
    if task_pet_name is None:
        st.warning("Add a pet before adding tasks.")
    else:
        # task_pet_name only gives us a name string from the selectbox, so look up
        # the actual Pet object it refers to before attaching a task to it.
        pet = next(p for p in owner.pets if p.name == task_pet_name)
        task = Task(description=task_title, duration=int(duration), frequency=frequency)
        task.set_priority(priority)
        # Scheduler owns task add/remove; Pet's own tasks list is the single source
        # of truth (no separate task list lives on Scheduler or Owner).
        scheduler.add_task(pet, task)

# Read tasks straight from the Pet objects rather than a separate session_state
# list, so this table can never drift out of sync with what the scheduler sees.
all_tasks = owner.get_all_tasks()
if all_tasks:
    status_filter = st.radio(
        "Filter tasks", ["All", "Pending", "Completed"], horizontal=True, key="task_status_filter"
    )
    # Filter on completion_status directly (mirrors Owner.get_tasks_by_completion's
    # own logic) so we can keep each task's pet alongside it for the table/selector.
    all_pairs = [(pet, t) for pet in owner.pets for t in pet.tasks]
    if status_filter == "Pending":
        task_pairs = [(pet, t) for pet, t in all_pairs if not t.completion_status]
    elif status_filter == "Completed":
        task_pairs = [(pet, t) for pet, t in all_pairs if t.completion_status]
    else:
        task_pairs = all_pairs

    st.write("Current tasks:")
    if task_pairs:
        st.table(
            [
                {
                    "pet": pet.name,
                    "task": t.description,
                    "duration_minutes": t.duration,
                    "priority": t.priority,
                    "frequency": t.frequency,
                    "due_date": t.due_date,
                    "completed": t.completion_status,
                }
                for pet, t in task_pairs
            ]
        )

        task_index = st.selectbox(
            "Select a task",
            range(len(task_pairs)),
            format_func=lambda i: f"{task_pairs[i][0].name}: {task_pairs[i][1].description} ({task_pairs[i][1].duration} min)",
            key="task_to_manage",
        )

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("Mark complete"):
                pet, task = task_pairs[task_index]
                # complete_task (not task.mark_complete()) so a recurring task's
                # next occurrence actually gets spawned and registered on the pet.
                next_task = scheduler.complete_task(pet, task)
                if next_task is not None:
                    st.toast(
                        f"'{task.description}' recurs — next occurrence due {next_task.due_date}.",
                        icon="🔁",
                    )
                st.rerun()
        with action_col2:
            if st.button("Remove task"):
                pet, task = task_pairs[task_index]
                scheduler.remove_task(pet, task)
                st.rerun()
    else:
        st.info("No tasks match this filter.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption(
    "Generate today's schedule based on priority and available time. "
    "Tasks are ordered by priority, then sorted chronologically within each pet's plan."
)

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        # explain_plan internally calls produce_plan (priority sort + time-budget
        # fit) and formats the result, so this one call gives us the full plan.
        schedule_text = scheduler.explain_plan(owner)
        st.text(schedule_text)

        # explain_plan already embeds any "⚠ Warning: ..." lines from
        # detect_time_conflicts inline; surface them as popups too so a
        # conflict isn't easy to miss in a long schedule.
        conflict_lines = [line for line in schedule_text.splitlines() if line.startswith("⚠ Warning:")]
        for warning in conflict_lines:
            st.toast(warning.removeprefix("⚠ Warning: "), icon="⚠️")