# CSC299 Final Project: AI-Powered PKMS & Task Manager

This repository contains the complete iterative development process for the CSC299 final project. The goal was to plan, specify, develop, and test a personal knowledge and task management system (PKMS) built in Python.

The final application is a terminal-based, chat-style app that allows a user to manage tasks and notes, link them together, and use AI agents to plan complex tasks and summarize notes.

## 🚀 Final Product

The final, feature-complete version of the software is located in the `/Final_Product` directory.

**To run the application, please see the `README.md` file inside the `/Final_Product` directory for full setup and usage instructions.**

---

## 🗂️ Project Deliverables

As required by the project instructions, the following files are also located in the root of this repository:

* **`SUMMARY.md`**: A detailed summary of the development process, including how AI-coding assistants were used, what worked, and what did not.
* **`video.txt`**: A file containing the URL to the 6-8 minute YouTube video demonstrating the software and its development.

---

## 👣 Development History & Prototypes

This project was built in stages, with each major prototype and preliminary task saved in its own self-contained directory.

### Main Prototypes (The Final App)

* **`/Prototype_1`**: The initial setup of the core application using `uv`, `typer`, and `sqlmodel` (SQLite) for basic task/note creation.
* **`/Prototype_2`**: Iteration 2. Added `done`/`delete` commands, the `pytest` test suite, and the AI note summarization agent.
* **`/Prototype_3`**: Iteration 3. Implemented the main "chat" REPL (Read-Eval-Print Loop) interface.
* **`/Final_Product`**: Iteration 4. Added the final features: data linking (tasks to notes), `search` commands, and the AI planning agent.

### Preliminary Tasks (Experiments)

* **`/tasks1`**: A basic CLI task manager using a JSON file for storage.
* **`/tasks2`**: An iteration on `tasks1` to add `done`, `delete`, and `search` functionality.
* **`/tasks3`**: A standalone experiment for setting up a `uv` package and integrating `pytest`.
* **`/tasks4`**: A standalone experiment for connecting to the OpenAI Chat Completions API.