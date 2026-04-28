from datetime import date
import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler
from ai_advisor import ask_advisor

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── Session-state bootstrap ────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

st.title("🐾 PawPal+")

# ── Owner + Scheduler setup ────────────────────────────────────────────────
with st.expander("Owner setup", expanded=st.session_state.owner is None):
    with st.form("owner_form"):
        _name  = st.text_input("Owner name",  value="Faith")
        _email = st.text_input("Owner email", value="faith@example.com")
        _pet_name    = st.text_input("Pet name",  value="Mochi")
        _pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        _pet_breed   = st.text_input("Breed",  value="Ragdoll")
        _pet_age     = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
        if st.form_submit_button("Save owner & pet"):
            _owner = Owner(name=_name, email=_email)
            _owner.add_pet(Pet(name=_pet_name, species=_pet_species,
                               breed=_pet_breed, age=_pet_age))
            st.session_state.owner     = _owner
            st.session_state.scheduler = Scheduler(_owner)
            st.success(f"Saved {_name} with pet {_pet_name}.")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Time (HH:MM)", value="08:00")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    task_freq = st.selectbox("Frequency", ["daily", "weekly", "once"])
with col5:
    task_desc = st.text_input("Description", value="")

if st.button("Add task"):
    if st.session_state.owner is not None:
        pet = st.session_state.owner.get_pets()[0] if st.session_state.owner.get_pets() else None
        if pet:
            pet.add_task(Task(
                title=task_title,
                description=task_desc,
                priority=priority,
                pet_name=pet.name,
                schedule=Schedule(
                    start_date=date.today(),
                    frequency=task_freq,
                    time=task_time,
                ),
            ))
            st.session_state.tasks.append(
                {"title": task_title, "time": task_time,
                 "frequency": task_freq, "priority": priority}
            )
        else:
            st.warning("No pet found. Complete owner setup first.")
    else:
        st.session_state.tasks.append(
            {"title": task_title, "time": task_time,
             "frequency": task_freq, "priority": priority}
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    # Colour-code the Priority column so high/medium/low stand out at a glance
    import pandas as pd

    def _highlight_priority(val: str) -> str:
        colours = {"high": "background-color:#ffd6d6", # red tint
                   "medium": "background-color:#fff4cc", # yellow tint
                   "low": "background-color:#d6f5d6"}    # green tint
        return colours.get(val, "")

    df = pd.DataFrame(st.session_state.tasks)
    st.dataframe(
        df.style.applymap(_highlight_priority, subset=["priority"]),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if st.session_state.scheduler is None:
        st.warning("Complete owner setup first.")
    else:
        scheduler: Scheduler = st.session_state.scheduler

        # Conflict warnings (get_conflicts)
        conflicts = scheduler.get_conflicts(date.today())
        if conflicts:
            with st.container(border=True):
                st.markdown("**⚠️ Scheduling Conflicts Detected**")
                for w in conflicts:
                    st.error(w, icon="🚨")
        else:
            st.success("No scheduling conflicts today.", icon="✅")

        # Today's tasks sorted by time (sort_by_time)
        todays_tasks  = scheduler.get_tasks_for_date(date.today())
        sorted_tasks  = scheduler.sort_by_time(todays_tasks)

        if not sorted_tasks:
            st.info("No tasks scheduled for today.", icon="📋")
        else:
            st.markdown("#### 📅 Today's Plan")

            # One styled card per task — colour driven by priority & completion
            for task in sorted_tasks:
                time_str = task.schedule.time if task.schedule else "--:--"
                label    = f"**{time_str}** &nbsp; `{task.pet_name}` — {task.title}"
                detail   = f"_{task.priority} priority_ · {task.description}"

                if task.completed:
                    st.success(f"✅ {label}\n\n{detail}")
                elif task.priority == "high":
                    st.error(f"🔴 {label}\n\n{detail}")
                elif task.priority == "medium":
                    st.warning(f"🟡 {label}\n\n{detail}")
                else:
                    st.info(f"🟢 {label}\n\n{detail}")

            st.divider()

            # Summary metrics
            pending = scheduler.filter_tasks(completed=False)   # filter_tasks
            done    = scheduler.filter_tasks(completed=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Total today", len(sorted_tasks))
            c2.metric("Pending",     len(pending))
            c3.metric("Completed",   len(done))

            # Filtered table view
            st.markdown("#### 🔍 Filter Tasks")
            f1, f2 = st.columns(2)
            with f1:
                pet_options = ["All pets"] + [p.name for p in st.session_state.owner.get_pets()]
                sel_pet = st.selectbox("By pet", pet_options, key="filter_pet")
            with f2:
                sel_status = st.selectbox("By status", ["All", "Pending", "Completed"],
                                          key="filter_status")

            pet_arg      = None if sel_pet    == "All pets"  else sel_pet
            complete_arg = None if sel_status == "All"       else (sel_status == "Completed")
            filtered     = scheduler.filter_tasks(completed=complete_arg, pet_name=pet_arg)
            filtered     = scheduler.sort_by_time(filtered)

            if filtered:
                import pandas as pd
                rows = [{"Time":      t.schedule.time if t.schedule else "--:--",
                         "Pet":       t.pet_name,
                         "Task":      t.title,
                         "Priority":  t.priority,
                         "Frequency": t.schedule.frequency if t.schedule else "—",
                         "Done":      "Yes" if t.completed else "No"}
                        for t in filtered]

                def _colour(val: str) -> str:
                    return {"high":   "background-color:#ffd6d6",
                            "medium": "background-color:#fff4cc",
                            "low":    "background-color:#d6f5d6"}.get(val, "")

                st.dataframe(
                    pd.DataFrame(rows).style.applymap(_colour, subset=["Priority"]),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No tasks match the selected filters.")

st.divider()

# ── AI Care Advisor ────────────────────────────────────────────────────────
st.subheader("🤖 AI Care Advisor")
st.caption(
    "Ask any pet care question. The advisor retrieves relevant facts from a "
    "built-in knowledge base and answers using the Gemini API."
)

with st.form("advisor_form"):
    question = st.text_input(
        "Your question",
        placeholder="e.g. How often should I brush my Ragdoll cat?",
    )
    ask_btn = st.form_submit_button("Ask")

if ask_btn:
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        # Build pet context from session state if available
        pet_context = ""
        if st.session_state.owner:
            pets = st.session_state.owner.get_pets()
            if pets:
                p = pets[0]
                pet_context = f"{p.name}, {p.species}, {p.breed}, age {p.age}"

        with st.spinner("Thinking..."):
            result = ask_advisor(question, pet_context)

        if result["status"] == "rejected":
            st.warning(f"🚫 {result['reason']}")

        elif result["status"] == "error":
            st.error(f"⚠️ {result['reason']}")

        elif result["status"] == "flagged":
            st.warning(result["answer"])

        else:
            st.success(result["answer"])

        if result["retrieved_facts"]:
            with st.expander("📚 Knowledge base facts used"):
                for fact in result["retrieved_facts"]:
                    st.markdown(f"- {fact}")
