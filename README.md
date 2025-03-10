# Book Writing Project

Welcome to the Book Writing Project, powered by [crewAI](https://crewai.com). This project is designed to help you write a book on any topic of your choice, regardless of how many chapters and pages you want. It aims to make a deeper understanding of concepts easier. The goal of the book is to take you from zero to hero on any concept with the power of AI agents that are researching and writing the book.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- **Writing Tasks and Agents:**
  - Modify `src/book_project/crews/writing/config/agents.yaml` to define your writing agents
  - Modify `src/book_project/crews/writing/config/tasks.yaml` to define your writing tasks

- **Research Tasks and Agents:**
  - Modify `src/book_project/crews/research/config/agents.yaml` to define your research agents
  - Modify `src/book_project/crews/research/config/tasks.yaml` to define your research tasks

- (Check if `crew.py` should exist or be created)
- Modify `src/book_project/main.py` to add custom inputs for your agents and tasks

## Running the Project

To start the book writing process and begin task execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the Book Writing Project, assembling the agents and assigning them tasks as defined in your configuration. The system will generate the output of your book writing process in the `output` folder.

## Understanding Your Project

The Book Writing Project is composed of multiple AI agents, each with unique roles, goals, and tools. These agents are organized into two different crews: one dedicated to research and the other to writing. 

- **Writing Crew:**
  - The writing crew's tasks are defined in `src/book_project/crews/writing/config/tasks.yaml`.
  - The writing agents' capabilities and configurations are outlined in `src/book_project/crews/writing/config/agents.yaml`.

- **Research Crew:**
  - The research crew's tasks are defined in `src/book_project/crews/research/config/tasks.yaml`.
  - The research agents' capabilities and configurations are outlined in `src/book_project/crews/research/config/agents.yaml`.

Each crew is connected through flows to ensure seamless collaboration, contributing to the overall goal of writing a comprehensive book.

## Support

For support, questions, or feedback regarding the Book Writing Project:

- Reach out to me via [LinkedIn](https://www.linkedin.com/in/isu-momodu/)
- Visit [crewAI documentation](https://docs.crewai.com)
- [Chat with crewAI docs](https://chatg.pt/DWjSBZn)
