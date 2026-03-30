from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, time

def test_mark_complete():
    task = Task("Morning walk", time(7, 0), date.today(), 30, "medium", "daily")
    task.mark_complete()
    assert task.completed == True

def test_add_task_increases_count():
    pet = Pet("Mochi", "cat")
    task = Task("Medication", time(9, 0), date.today(), 5, "high", "daily")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1