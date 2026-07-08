# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule
Plan for Alex (55/60 min used):

Daily plan for Rex (Labrador):
Walk Rex (30 min) [priority: high]

Daily plan for Luna (Siamese):
Feed Luna (10 min) [priority: high]
Clean Luna's litter box (15 min) [priority: low]

## 🧪 Testing PawPal+

PS C:\Codepath class\ai110-module2show-pawpal-starter> python -m pytest tests\test_pawpal.py
=================================== test session starts ===================================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Codepath class\ai110-module2show-pawpal-starter
collected 5 items

tests\test_pawpal.py ..... [100%]

==================================== 5 passed in 0.04s ====================================

**Test 1**: test_sort_by_time()
Tests to see if tasks given out of order is sorted in chronological order by the start time.

**Test2**: test_recurring_tasks()
Tests to see if completing a daily task spawns a new task due the following day.

**Test3**: test_detect_time_conflicts()
Tests to see if two tasks scheduled at the same start time produce a single conflict warning.

**Test 4**:test_task_completion()
Tests if a status of a task is updated correctly

**Test 5**: def test_task_addition()
Tests if a task is being added to a pet correctly when adding new task

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s)                                 | Notes                        |
| ----------------- | ----------------------------------------- | ---------------------------- |
| Task sorting      | produce_plan(), sort_by_time()            | Priority, then chronological |
| Filtering         | get_tasks_by_completion(), produce_plan() | Pending and due tasks only   |
| Conflict handling | detect_time_conflicts()                   | Warns on same time slot      |
| Recurring tasks   | get_next_due_date(), complete_task()      | Daily/weekly using timedelta |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
