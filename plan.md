# App Feature List

## CLI Interface
- **Command Execution** (`-c`):
  - Send specific commands directly to the database.
- **Focus Management** (`-f`):
  - Change the focus to a different task.
- **Quit Command** (`-q`):
  - Exit the CLI interface.
- **Entry Management**:
  - Add new entries to the database.
  - Entries will be linked to the currently focused task.
- **Day Summary Generation**:
  - Generate a summary of the upcoming day or what the day has looked like so far.
  - Output the summary in plain English or as a structured bullet list.
- **Contextual Prompts and Queries**:
  - Allow users to prompt or ask questions based on the current context within the CLI.

## Background Engine
- **Database Monitoring**:
  - Periodically checks for new entries in the SQLite database.
- **Chatbot Integration**:
  - **Task Management**:
    - Create new actions associated with existing tasks, including "Note" actions.
    - Create new subtasks under existing tasks.
    - Create entirely new tasks if they don’t relate to any existing ones.
    - If an entry is related to a subtask that isn't the current context, the engine will prompt the chatbot again using that subtask as the context to ensure thoroughness.
  - Logs chatbot-generated tasks, actions, or notes back into the database.
- **Processing**:
  - Olama generates processes that link context (tasks and entries) and store metadata like the raw response from the JSON model and the execution time of the process.

## Web Interface
- **Task Dashboard**:
  - **Base Route**:
    - Returns all tasks with no parents (root tasks).
  - **Task-Specific Route**:
    - Adding a task ID to the route focuses on that specific task.
    - Any entries added through the web interface will be linked to the focused task.
  - Displays all tasks with their current status.
  - Shows the current focus task.
  - Allows filtering and sorting of tasks.
- **Task Management**:
  - Enables users to change the current focus task.
  - Provides options to add, modify, and delete tasks.
  - View and add "Note" actions to tasks.
- **Day Summary Generation**:
  - Generate a summary of the upcoming day or what the day has looked like so far.
  - Display the summary in plain English or as a structured bullet list.
- **Contextual Prompts and Queries**:
  - Allow users to prompt or ask questions based on the current context within the web interface.
- **Real-Time Updates**:
  - Dynamically updates the task dashboard as changes occur.
  - Displays real-time processing status from the background engine.

## Database Structure
- **Entries**:
  - Stores the raw user input.
- **Tasks**:
  - Contains short, concise text with metadata about their creation.
- **Actions**:
  - Links tasks and entries together. Supports various operations such as creating and updating tasks.
- **Processing**:
  - Managed by Olama, links context (tasks and entries) and contains metadata like the raw JSON model response and execution time for process tracking.

---

# To-Do / Roadmap

1. **CLI Interface**
   - Implement basic command execution (`-c`, `-f`, `-q`).
   - Add entry management functionality.
   - Develop day summary generation (plain text and bullet list).
   - Implement contextual prompts and queries.

2. **Background Engine**
   - Set up database monitoring for new entries.
   - Integrate chatbot for task/action management.
   - Develop handling of tasks, subtasks, and thorough re-prompting for specific contexts.
   - Implement Olama processing for context and metadata.

3. **Web Interface**
   - Create the task dashboard with base and task-specific routes.
   - Implement task management features (add, modify, delete, note actions).
   - Develop day summary generation (plain text and bullet list).
   - Enable contextual prompts and queries.

4. **Database**
   - Design and implement tables for Entries, Tasks, Actions, and Processing.
   - Ensure proper linking between tasks and entries via actions.
   - Store and manage processing metadata generated by Olama.
