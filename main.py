from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, time

# Create owner
owner = Owner("Jordan")

# Create pets
mochi = Pet("Mochi", "cat")
rex = Pet("Rex", "dog")

# Add tasks OUT OF ORDER
mochi.add_task(Task("Evening feeding", time(18, 0), date.today(), 10, "high", "daily"))
mochi.add_task(Task("Medication", time(9, 0), date.today(), 5, "high", "daily"))
rex.add_task(Task("Afternoon walk", time(16, 0), date.today(), 30, "medium", "daily"))
rex.add_task(Task("Morning walk", time(7, 0), date.today(), 30, "medium", "daily"))
rex.add_task(Task("Vet appointment", time(14, 0), date.today(), 60, "high", "once"))

# Add pets to owner
owner.add_pet(mochi)
owner.add_pet(rex)

# Create scheduler
scheduler = Scheduler(owner)

# Print sorted schedule
print("=== Today's Schedule (Sorted) ===")
for task in scheduler.sort_by_time():
    print(f"{task.time.strftime('%H:%M')} | {task.title} ({task.duration} mins) [{task.priority}]")

# Print filtered by pet name
print("\n=== Mochi's Tasks ===")
for task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"{task.time.strftime('%H:%M')} | {task.title}")

# Print incomplete tasks
print("\n=== Incomplete Tasks ===")
for task in scheduler.filter_tasks(status="incomplete"):
    print(f"{task.time.strftime('%H:%M')} | {task.title}")

