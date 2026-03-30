from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import date, time, timedelta
import datetime


@dataclass
class Task:
    title: str
    time: time           # e.g. time(8, 0) for 08:00
    date: date           # e.g. date.today()
    duration: int        # in minutes
    priority: str        # "high", "medium", "low"
    frequency: str       # "daily", "weekly", "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def end_time(self) -> time:
        """Return the time at which this task ends (start + duration)."""
        start_dt = datetime.datetime.combine(self.date, self.time)
        end_dt = start_dt + timedelta(minutes=self.duration)
        return end_dt.time()


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return a shallow copy of this pet's task list."""
        return list(self.tasks)


class Owner:
    def __init__(self, name: str) -> None:
        """Initialize an owner with a name and an empty pet list."""
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's roster."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all of this owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with the owner whose pets it will manage."""
        self.owner: Owner = owner

    def _collect_all_tasks(self) -> List[Task]:
        """Private helper — single traversal to avoid duplicate walks."""
        return self.owner.get_all_tasks()

    def get_todays_tasks(self) -> List[Task]:
        """Return all tasks scheduled for today across every pet."""
        today = date.today()
        return [t for t in self._collect_all_tasks() if t.date == today]

    def sort_by_time(self) -> List[Task]:
        """Return today's tasks sorted ascending by start time."""
        return sorted(self.get_todays_tasks(), key=lambda t: t.time)

    def filter_tasks(self, criteria: str) -> List[Task]:
        """Filter today's tasks by a 'field:value' string (e.g. 'priority:high', 'species:dog')."""
        tasks = self.get_todays_tasks()
        if ":" not in criteria:
            return tasks

        field_name, value = criteria.split(":", 1)
        field_name = field_name.strip().lower()
        value = value.strip().lower()

        if field_name == "priority":
            return [t for t in tasks if t.priority.lower() == value]
        elif field_name == "frequency":
            return [t for t in tasks if t.frequency.lower() == value]
        elif field_name == "completed":
            flag = value in ("true", "1", "yes")
            return [t for t in tasks if t.completed == flag]
        elif field_name == "species":
            # Tasks don't carry a pet reference, so traverse owner → pet
            today = date.today()
            result: List[Task] = []
            for pet in self.owner.pets:
                if pet.species.lower() == value:
                    result.extend(t for t in pet.get_tasks() if t.date == today)
            return result
        else:
            return tasks

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return every pair of today's tasks whose time windows overlap."""
        todays = self.sort_by_time()  # pre-sorted so inner loop starts tight
        conflicts: List[Tuple[Task, Task]] = []

        for i in range(len(todays)):
            for j in range(i + 1, len(todays)):
                a, b = todays[i], todays[j]
                a_start = a.time.hour * 60 + a.time.minute
                a_end = a_start + a.duration
                b_start = b.time.hour * 60 + b.time.minute
                b_end = b_start + b.duration
                # Overlap: neither task ends before the other starts
                if a_start < b_end and a_end > b_start:
                    conflicts.append((a, b))

        return conflicts

    def handle_recurring_tasks(self) -> None:
        """Clone past recurring tasks into today's schedule if not already present."""
        today = date.today()

        for pet in self.owner.pets:
            existing_today = {t.title for t in pet.tasks if t.date == today}
            to_add: List[Task] = []

            for task in pet.tasks:
                if task.date >= today:
                    continue
                if task.title in existing_today:
                    continue

                if task.frequency == "daily":
                    to_add.append(Task(
                        title=task.title,
                        time=task.time,
                        date=today,
                        duration=task.duration,
                        priority=task.priority,
                        frequency=task.frequency,
                    ))
                    existing_today.add(task.title)

                elif task.frequency == "weekly":
                    if task.date.weekday() == today.weekday():
                        to_add.append(Task(
                            title=task.title,
                            time=task.time,
                            date=today,
                            duration=task.duration,
                            priority=task.priority,
                            frequency=task.frequency,
                        ))
                        existing_today.add(task.title)

            for new_task in to_add:
                pet.add_task(new_task)
