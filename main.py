from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler


# --- Setup ---
owner = Owner(name="Faith", email="faith@example.com")

buddy = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3)
mochi = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2)

owner.add_pet(buddy)
owner.add_pet(mochi)

# --- Tasks for Buddy ---
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

# --- Tasks for Mochi ---
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

# --- Print Today's Schedule ---
scheduler = Scheduler(owner)
todays_tasks = scheduler.get_tasks_for_date(date.today())
todays_tasks_sorted = sorted(todays_tasks, key=lambda t: t.schedule.time)

print("=" * 40)
print(f"   Today's Schedule — {date.today()}")
print("=" * 40)

if not todays_tasks_sorted:
    print("No tasks scheduled for today.")
else:
    for task in todays_tasks_sorted:
        status = "[x]" if task.completed else "[ ]"
        print(f"{status} {task.schedule.time}  [{task.pet_name}]  {task.title}")
        print(f"         Priority : {task.priority}")
        print(f"         Note     : {task.description}")
        print()

print("=" * 40)
print(f"Total tasks today: {len(todays_tasks_sorted)}")
print(f"Pending          : {len([t for t in todays_tasks_sorted if not t.completed])}")
print("=" * 40)
