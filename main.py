from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, time

# Create owner
owner = Owner("Jordan")

# Create pets
mochi = Pet("Mochi", "cat")
rex = Pet("Rex", "dog")

# Add tasks to Mochi
mochi.add_task(Task("Evening feeding", time(18, 0), date.today(), 10, "high", "daily"))
mochi.add_task(Task("Medication", time(9, 0), date.today(), 5, "high", "daily"))

# Add tasks to Rex
rex.add_task(Task("Morning walk", time(7, 0), date.today(), 30, "medium", "daily"))
rex.add_task(Task("Vet appointment", time(14, 0), date.today(), 60, "high", "once"))
rex.add_task(Task("Afternoon walk", time(16, 0), date.today(), 30, "medium", "daily"))

# Add pets to owner
owner.add_pet(mochi)
owner.add_pet(rex)

# Create scheduler
scheduler = Scheduler(owner)

# Print today's schedule
print("=== Today's Schedule ===")
for task in scheduler.sort_by_time():
    status = "done" if task.completed else "pending"
    print(f"{task.time.strftime('%H:%M')} | {task.title} ({task.duration} mins) [{task.priority}] - {status}")