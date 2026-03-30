import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

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

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")

with st.form("add_task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5, col6 = st.columns(3)
    with col4:
        task_time = st.time_input("Start time", value=time(8, 0))
    with col5:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    submitted = st.form_submit_button("Add task")

if submitted:
    owner = st.session_state.owner
    new_start = task_time.hour * 60 + task_time.minute
    new_end = new_start + int(duration)

    # Check for time conflicts against all existing tasks today
    conflicts = [
        t for t in owner.get_all_tasks()
        if t.date == date.today()
        and new_start < (t.time.hour * 60 + t.time.minute + t.duration)
        and new_end > (t.time.hour * 60 + t.time.minute)
    ]

    if conflicts:
        for t in conflicts:
            t_start = t.time.hour * 60 + t.time.minute
            t_end = t_start + t.duration
            overlap = min(new_end, t_end) - max(new_start, t_start)
            earliest_start = t_end  # first free minute after the conflict
            earliest_h, earliest_m = divmod(earliest_start, 60)
            st.error(
                f"Conflict with '{t.title}' ({t.time.strftime('%H:%M')}–"
                f"{(t_end // 60):02d}:{(t_end % 60):02d}): "
                f"overlaps by {overlap} min. "
                f"Try starting at {earliest_h:02d}:{earliest_m:02d} or later."
            )
    else:
        pet = next((p for p in owner.pets if p.name == pet_name), None)
        if pet is None:
            pet = Pet(pet_name, species)
            owner.add_pet(pet)
        task = Task(
            title=task_title,
            time=task_time,
            date=date.today(),
            duration=int(duration),
            priority=priority,
            frequency=frequency,
        )
        pet.add_task(task)
        st.success(f"Added '{task_title}' to {pet_name}.")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([
        {
            "Pet": next(p.name for p in st.session_state.owner.pets if task in p.tasks),
            "Title": task.title,
            "Time": task.time.strftime("%H:%M"),
            "Duration (min)": task.duration,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Done": task.completed,
        }
        for task in all_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = st.session_state.scheduler
    scheduler.handle_recurring_tasks()

    conflicts = scheduler.detect_conflicts()
    for a, b in conflicts:
        st.warning(
            f"Conflict: '{a.title}' ({a.time.strftime('%H:%M')}) and "
            f"'{b.title}' ({b.time.strftime('%H:%M')}) overlap."
        )

    scheduled = scheduler.sort_by_time()
    if scheduled:
        st.table([
            {
                "Time": task.time.strftime("%H:%M"),
                "Title": task.title,
                "Duration (min)": task.duration,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Done": task.completed,
            }
            for task in scheduled
        ])
    else:
        st.info("No tasks scheduled for today.")
