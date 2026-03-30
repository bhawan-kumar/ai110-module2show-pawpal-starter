# PawPal+ Project Reflection

## 1. System Design

1. Add a pet – The user can enter a pet's name, species, and basic info to register them in the system.
2. Schedule a task – The user can create a care task (walk, feeding, medication, etc.) with a time, duration, and priority level and assign it to a pet.
3. View today's schedule – The user can see all tasks for the day across all pets, sorted by time and organized clearly.

**a. Initial design**

- Briefly describe your initial UML design.
  My initial UML design consisted of four classes connected by ownership relationships:
  Owner holds a list of Pets, each Pet holds a list of Tasks, and a Scheduler
  manages the Owner to access everything.

- What classes did you include, and what responsibilities did you assign to each?
  I designed four classes:
- Task: Holds the details of a single care activity (title, time, duration, priority, frequency, completed status) and can mark itself complete.
- Pet: Represents a pet with a name and species, holds a list of Tasks, and can add and retrieve tasks.
- Owner: Represents the pet owner, holds a list of Pets, and can add pets and retrieve all tasks across all pets.
- Scheduler: The brain of the system — it takes an Owner and can retrieve, sort, filter, and detect conflicts in tasks, and handle recurring tasks.

**b. Design changes**

- Did your design change during implementation?'
  Yes, the design changed after AI reviewed the skeleton. Two changes were made.
- If yes, describe at least one change and why you made it.
  The two changes are:
- The `time` field on `Task` was changed from a plain `str` to `datetime.time` because string comparison would break sorting and conflict detection.
- A `date` field was added to `Task` because without it, recurring tasks had nowhere to attach the next scheduled occurrence.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- My scheduler considers time (no overlapping tasks), priority (high priority tasks surface first when two tasks share the same start time), and completion status (tasks can be filtered by done or incomplete).

- How did you decide which constraints mattered most?
- Time was the most important constraint because overlapping tasks are physically impossible to complete. Priority was second because it helps the owner decide what matters most when tasks start at the same time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- The scheduler uses a simple O(n²) nested loop for conflict detection instead of a more optimized early-exit version.

- Why is that tradeoff reasonable for this scenario?
- This is reasonable because a typical pet owner will have very few tasks per day, so the performance difference is negligible and the simpler version is easier to read and maintain.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
