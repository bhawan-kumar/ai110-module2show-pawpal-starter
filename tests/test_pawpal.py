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