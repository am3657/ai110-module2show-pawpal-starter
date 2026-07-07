import streamlit as st
from pawlpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if task_pet_name is None:
        st.warning("Add a pet before adding tasks.")
    else:
        # task_pet_name only gives us a name string from the selectbox, so look up
        # the actual Pet object it refers to before attaching a task to it.
        pet = next(p for p in owner.pets if p.name == task_pet_name)
        task = Task(description=task_title, duration=int(duration), frequency="daily")
        task.set_priority(priority)
        # Scheduler owns task add/remove; Pet's own tasks list is the single source
        # of truth (no separate task list lives on Scheduler or Owner).
        scheduler.add_task(pet, task)

# Read tasks straight from the Pet objects rather than a separate session_state
# list, so this table can never drift out of sync with what the scheduler sees.
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": t.description,
                "duration_minutes": t.duration,
                "priority": t.priority,
                "completed": t.completion_status,
            }
            for pet in owner.pets
            for t in pet.tasks
        ]
    )

    task_pairs = [(pet, t) for pet in owner.pets for t in pet.tasks]
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
            task.mark_complete()
            st.rerun()
    with action_col2:
        if st.button("Remove task"):
            pet, task = task_pairs[task_index]
            scheduler.remove_task(pet, task)
            st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate today's schedule based on priority and available time.")

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        # explain_plan internally calls produce_plan (priority sort + time-budget
        # fit) and formats the result, so this one call gives us the full plan.
        st.text(scheduler.explain_plan(owner))