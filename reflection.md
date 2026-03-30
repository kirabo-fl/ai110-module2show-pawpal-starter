# PawPal+ Project Reflection

## 1. System Design

#### Actions
- Entering pet info
- Add tasks
- Add a schedule for tasks

**a. Initial design**

```mermaid
classDiagram
    class Owner {
        +String name
        +String email
        +addPet(pet: Pet)
    }

    class Pet {
        +String name
        +String species
        +String breed
        +int age
    }

    class Task {
        +String title
        +String description
        +String priority
    }

    class Schedule {
        +Date startDate
        +String frequency
        +String time
    }

    Owner "1" --> "many" Pet : has
    Pet "1" --> "many" Task : has
    Task "1" --> "1" Schedule : scheduled by
```

- Briefly describe your initial UML design.

The initial design uses four classes: `Owner`, `Pet`, `Task`, and `Schedule`. An Owner holds a list of Pets, each Pet holds a list of Tasks, and each Task optionally links to one Schedule. This chain reflects the three core actions in the app, entering pet info, adding tasks, and scheduling those tasks.

- What classes did you include, and what responsibilities did you assign to each?

| Class | Responsibility |
|-------|----------------|
| `Owner` | Represents the app user; manages their collection of pets |
| `Pet` | Stores pet info (name, species, breed, age); owns its tasks |
| `Task` | Represents a single care action (e.g. feed, walk); holds title, description, and priority |
| `Schedule` | Holds when and how often a task runs (start date, frequency, time) |

**b. Design changes**

- Did your design change during implementation?

Yes, three changes were made after reviewing the initial skeleton.

- If yes, describe at least one change and why you made it.

**Change 1 — Added `end_date` to `Schedule`**
The initial `Schedule` only had `start_date`, `frequency`, and `time`. Without an `end_date`, there was no way to stop a recurring task. For example, a medication task that runs daily for two weeks would have no defined endpoint. Adding `end_date` as an optional field (defaulting to `None` for open-ended tasks) fixes this without overcomplicating the class.

**Change 2 — Added `pet_name` to `Task`**
The initial design had `Task` floating without any reference back to the `Pet` it belonged to. This would make it impossible to display or filter tasks by pet without scanning every pet's task list. Adding `pet_name` gives each task a direct link to its owner.

**Change 3 — Added `get_pet_by_name()` to `Owner`**
Without this method, the only way to access a specific pet was to loop through `owner.pets` every time. Since tasks and schedules are always tied to a specific pet, this lookup would be needed repeatedly. Adding the method prevents that bottleneck from spreading through the rest of the code.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
