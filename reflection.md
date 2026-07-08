# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation? Yes

- If yes, describe at least one change and why you made it.
  I had to modify certain attributes and behaviors of the Task Class and the Scheduler class. One notable change was adding

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler primarily considers priority and the time availabe for the owner as the primary constraints.

- How did you decide which constraints mattered most?
  Priority seemed like the best constraint to implement becasue it helps determine the order by which the tasks should be performed given an owner's availability.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  The scheduler values priority of tasks more than finding the most optimal plan for executing tasks based on the time. However, another major tradeoff that the scheduler makes is using duration to resolve conflicts instead of timestamps.

- Why is that tradeoff reasonable for this scenario?

  The first tradeoff is reasonable because the scheduler is following a greedy approach, ensuring all the high priority tasks are performed. Even though it is not the most optimal in generating a schedule where more tasks are performed in the available time, it is reasonble to have all the high priority tasks be completed first.

  The second tradeoff is reasonable becasue it creates a more simplistic yet efficient design, becasue the tasks will be automatically scheduled based on priority, so the only conflict that can arise now, is if the owner inputs 0 for duration or gives no time.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

Design

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
  I am most satisfied with creating behaviors

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
