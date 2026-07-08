# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

  My intial UML design was fairly simple consisting of the four entinties: Owner, Task, Scheduler, Pet.

  Relationships:
  1. An Owner can own multiple pets
  2. An Owner use one scheduler.
  3. Pet can have many tasks
  4. Scheduler accesses Tasks

- What classes did you include, and what responsibilities did you assign to each?

Classes: Owner, Task, Scheduler, Pet

1. Owner class is responsible for keeping track of their pets, and using the Scheduler
2. Scheduler is responsible with editing Tasks including its status and frequency, producing a plan, and explaining the plan.
3. Pet class is responsible for the creation of all the Pet objects, and keeping track of which tasks are assigned to each Pet.
4. Task class is responsible for creation of all Task objects, which represents a single activity.

**b. Design changes**

- Did your design change during implementation? Yes

- If yes, describe at least one change and why you made it.
  The Task class went through significant changes as the responsibilities were being shifted for better functionaity. For instance, when creating the alogrithm for recurring tasks, I initially had one boolean value handle the completion status. Inorder to accodomate for the recurring nature of each task, I created a new function, complete_task(Pet, task), which handles the completion status but also add the next Task instance to the right pet.

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

I used Claude Code as the primary AI tool throughout the project including design, brainstorming, debugging, and refactoring. I used AI during design process, when I had ideas as to how the functions should behave, and UI components should be designed, but lacked the coding knowledge. AI came in handy when I was brainstorming during the UML design, since I was confused whether to assign certain responsibilities to Task or Scheduler. It saved me a lot of time with debugging, when some of the functions where not working after clicking the right buttons, and it helped me understand how to solve such problems. Finally, when I was tasked with refactoring the code and implementing new algorithms, I consulted AI to improve the functionality and scope of the classes compared to their initial design. Overall, I feel like I was able to accelerate the outcome of the project with the right prompts and questions.

- What kinds of prompts or questions were most helpful?
  The most direct and carefully written prompts seemed have been the most helpful, becasue if the prompt is too vague, AI tends to hallucinate a bit more exhausting a lot of tokens. This was espcially true, when AI would go through entire files when not given exactly where to look. Follow up questions to edits, and asking it suggestions based on our own observations, tends to increase the debugging speed compared to a simple "fix it" prompt.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

  When reviewing our UML design, the AI suggested splitting Scheduler into a fifth class to separate task management from plan generation, since Scheduler was handling three distinct responsibilities. I rejected this since the assignment scope was fixed at four classes, and instead suggested a simpler fix. I ended up moving markComplete(), updateFrequency(), and setPriority() onto Task itself, since those methods only mutated a task's own state and didn't actually need Scheduler at all. Even though this design choice evolved over time, it did stop the project from deviating and using an unnecessary fifth class.

- How did you evaluate or verify what the AI suggested?
  I would always run the app myself immediately after AI writes its code, and also have the AI perform sanity checks in the terminal to ensure the code never breaks.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  I tested mainly for the functionality of the sorting, filtering, and recurring task algorithms.

- Why were these tests important?
  These tests were important for the Scheduler to ensure it always generates a properly scheduled plan, and the tasks to managed appropriately so that the owner is reminded to do it next day if it is recurring. I also tested some basic behaviors like adding task, and marking them complete to decide that the Scheduler can perform more complex behaviors.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  On a scale of 1-5, I would say 4.

- What edge cases would you test next if you had more time?

An edge case I would test if I had more time is if two pets with the same name/task could the cause the scheduler to get confused when creating the plan, and if the remove/mark complete feature would update the wrong task.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  Seeing the UI components associated with the functions created in pawpal_system, working as intended.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  If I had another iteration, I would redisgn the time slot assignment of each task. Currently, the app asign its own time based on the priority and the duration, making it easier for the scheduler to create a plan and resolve any conflicts. In the next iteration, I would make the owner assign their own time, making it more interactive and increasing the scope of the project. It would have also improved the effectiveness of the conflict resolving algorithm.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I realized is that it is important to brainstorm ideas, clearly specifying the goals before AI writes code, and ask questions about the generated code all the time. These three actions will make sure the right features are being created and the project doesn't move in the wrong direction.
