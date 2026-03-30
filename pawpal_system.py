from dataclasses import dataclass, field
from typing import List
from datetime import date, time

@dataclass
class Task:
    title: str
    time: time         # e.g. time(8, 0) for 08:00
    date: date         # e.g. date.today()
    duration: int      # in minutes
    priority: str      # "high", "medium", "low"
    frequency: str     # "daily", "weekly", "once"
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner

    def get_todays_tasks(self) -> List[Task]:
        pass

    def sort_by_time(self) -> List[Task]:
        pass

    def filter_tasks(self, criteria: str) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[Task]:
        pass

    def handle_recurring_tasks(self) -> None:
        pass
