from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, time

def make_task(title="Task", t=time(8, 0), duration=30, priority="medium", frequency="once"):
    return Task(title, t, date.today(), duration, priority, frequency)

def test_mark_complete():
    task = make_task()
    task.mark_complete()
    assert task.completed == True

def test_add_task_increases_count():
    pet = Pet("Mochi", "cat")
    pet.add_task(make_task())
    assert len(pet.get_tasks()) == 1


# --- Sorting ---

def test_sort_by_time_priority_tiebreak():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    pet.add_task(make_task("Low task",  t=time(8, 0), priority="low"))
    pet.add_task(make_task("High task", t=time(8, 0), priority="high"))
    pet.add_task(make_task("Mid task",  t=time(8, 0), priority="medium"))
    scheduler = Scheduler(owner)
    titles = [t.title for t in scheduler.sort_by_time()]
    assert titles == ["High task", "Mid task", "Low task"]


# --- Recurring tasks ---

def test_handle_recurring_weekly_task_wrong_day_not_added():
    from datetime import timedelta
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    yesterday = date.today() - timedelta(days=1)
    if yesterday.weekday() == date.today().weekday():
        yesterday = date.today() - timedelta(days=2)
    pet.add_task(Task("Weekly groom", time(10, 0), yesterday, 30, "medium", "weekly"))
    scheduler = Scheduler(owner)
    scheduler.handle_recurring_tasks()
    today_tasks = [t for t in pet.tasks if t.date == date.today()]
    assert len(today_tasks) == 0


# --- Conflict detection ---

def test_detect_conflicts_task_fully_contained():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    pet.add_task(make_task("Outer", t=time(8, 0),  duration=60))  # 08:00–09:00
    pet.add_task(make_task("Inner", t=time(8, 15), duration=30))  # 08:15–08:45 — fully inside
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    titles = {conflicts[0][0].title, conflicts[0][1].title}
    assert titles == {"Outer", "Inner"}


def test_handle_recurring_completed_daily_task_still_carried_forward():
    from datetime import timedelta
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    yesterday = date.today() - timedelta(days=1)
    past_task = Task("Daily feed", time(8, 0), yesterday, 10, "high", "daily")
    past_task.mark_complete()
    pet.add_task(past_task)
    scheduler = Scheduler(owner)
    scheduler.handle_recurring_tasks()
    today_tasks = [t for t in pet.tasks if t.date == date.today()]
    assert len(today_tasks) == 1
    assert today_tasks[0].completed == False


# --- Filter ---

def test_filter_tasks_pet_name_case_insensitive():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    pet.add_task(make_task("Feed Mochi"))
    scheduler = Scheduler(owner)
    assert len(scheduler.filter_tasks(pet_name="mochi")) == 1
    assert len(scheduler.filter_tasks(pet_name="MOCHI")) == 1