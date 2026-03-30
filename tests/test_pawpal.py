import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Owner, Pet, Task, Scheduler


def make_owner():
    """Create a minimal Owner with one Pet for testing."""
    owner = Owner(name="Test Owner", email="test@example.com")
    pet = Pet(name="Test Pet", species="Dog", breed="Mixed", age=1)
    owner.add_pet(pet)
    return owner


def make_task(title="Sample Task", priority="medium", pet_name="Test Pet"):
    """Create a minimal Task with no schedule."""
    return Task(title=title, description="A test task", priority=priority, pet_name=pet_name)


def test_task_completion():
    """Verify that complete_task() changes the task's completed status to True."""
    owner = make_owner()
    pet = owner.get_pets()[0]

    task = make_task(pet_name=pet.name)
    pet.add_task(task)

    scheduler = Scheduler(owner)
    assert task.completed == False, "Task should start as incomplete"

    scheduler.complete_task(task)
    assert task.completed == True, "Task should be completed after complete_task()"

    print("PASS: test_task_completion")


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Test Pet", species="Cat", breed="Mixed", age=1)

    initial_count = len(pet.get_tasks())

    pet.add_task(make_task(title="First Task", pet_name=pet.name))
    assert len(pet.get_tasks()) == initial_count + 1, "Task count should increase by 1 after first add"

    pet.add_task(make_task(title="Second Task", pet_name=pet.name))
    assert len(pet.get_tasks()) == initial_count + 2, "Task count should increase by 2 after second add"

    print("PASS: test_task_addition")


if __name__ == "__main__":
    test_task_completion()
    test_task_addition()
