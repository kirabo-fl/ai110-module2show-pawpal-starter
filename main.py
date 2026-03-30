from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler


# --- Setup ---
owner = Owner(name="Faith", email="faith@example.com")

buddy = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3)
mochi = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2)

owner.add_pet(buddy)
owner.add_pet(mochi)

# --- Buddy's tasks ---
buddy.add_task(Task(
    title="Morning Walk",
    description="30-minute walk around the block",
    priority="high",
    pet_name="Buddy",
    schedule=Schedule(start_date=date.today(), frequency="daily", time="07:00")
))

buddy.add_task(Task(
    title="Flea Medication",
    description="Apply topical flea treatment",
    priority="medium",
    pet_name="Buddy",
    schedule=Schedule(start_date=date.today(), frequency="once", time="09:00")
))

# Deliberate conflict: same pet (Buddy), same time as Morning Walk (07:00)
buddy.add_task(Task(
    title="Vet Appointment",
    description="Annual check-up",
    priority="high",
    pet_name="Buddy",
    schedule=Schedule(start_date=date.today(), frequency="once", time="07:00")
))

# --- Mochi's tasks ---
mochi.add_task(Task(
    title="Feed Breakfast",
    description="Half cup of dry food",
    priority="high",
    pet_name="Mochi",
    schedule=Schedule(start_date=date.today(), frequency="daily", time="08:00")
))

mochi.add_task(Task(
    title="Brush Fur",
    description="Brush coat to prevent matting",
    priority="low",
    pet_name="Mochi",
    schedule=Schedule(start_date=date.today(), frequency="weekly", time="18:00")
))

# Deliberate conflict: different pets (Buddy + Mochi) both at 09:00
mochi.add_task(Task(
    title="Nail Trim",
    description="Trim front and back claws",
    priority="medium",
    pet_name="Mochi",
    schedule=Schedule(start_date=date.today(), frequency="once", time="09:00")
))

scheduler = Scheduler(owner)


# --- Helper to print a task list ---
def print_tasks(tasks: list, label: str) -> None:
    print("=" * 50)
    print(f"  {label}")
    print("=" * 50)
    if not tasks:
        print("  (none)")
    else:
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            time = task.schedule.time if task.schedule else "--:--"
            print(f"  {status} {time}  [{task.pet_name}]  {task.title}")
            print(f"           Priority : {task.priority}")
            print(f"           Note     : {task.description}")
            print()
    print()


# --- 1. Today's full schedule sorted by time ---
todays_tasks = scheduler.get_tasks_for_date(date.today())
sorted_today = scheduler.sort_by_time(todays_tasks)
print_tasks(sorted_today, f"Today's Schedule — {date.today()}  (sorted by time)")

# --- 2. Conflict detection ---
print("=" * 50)
print("  Conflict Check")
print("=" * 50)
conflicts = scheduler.get_conflicts()
if not conflicts:
    print("  No scheduling conflicts found.")
else:
    for warning in conflicts:
        print(f"  {warning}")
print()

# --- 3. Summary ---
print("=" * 50)
print(f"  Total tasks today : {len(sorted_today)}")
print(f"  Conflicts found   : {len(conflicts)}")
print("=" * 50)
