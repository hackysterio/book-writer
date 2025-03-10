import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
from crewai_tools import SerperDevTool


@CrewBase
class Research():
	"""Research crew for chapter-by-chapter book content development"""

	def __init__(self, inputs=None):
		self.inputs = inputs or {}
		super().__init__()

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def toc_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['toc_researcher'],
			tools=[SerperDevTool()]
		)

	@agent
	def research_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['research_specialist'],
			tools=[SerperDevTool()]
		)

	@task
	def generate_toc(self) -> Task:
		task = Task(config=self.tasks_config['generate_toc'])
		self._format_task_config(task)
		return task

	@task
	def research_topics(self) -> Task:
		task = Task(config=self.tasks_config['research_topics'])
		self._format_task_config(task)
		return task

	def _format_task_config(self, task):
		"""Format task configuration with current chapter and topic"""
		if hasattr(task, 'config') and task.config:
			# Get all required variables
			inputs = {
				'chapter_number': self.inputs.get('chapter_number'),
				'topic': self.inputs.get('topic'),
				'pages': self.inputs.get('pages'),
				'total_chapters': self.inputs.get('total_chapters'),
				'research_results': self.inputs.get('research_results', ''),
				'author_name': self.inputs.get('author_name', '')
			}
			
			# Format all string values in the config
			for key, value in task.config.items():
				if isinstance(value, str):
					task.config[key] = value.format(**inputs)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research crew for the current chapter"""
		tasks = [
			self.generate_toc(),
			self.research_topics()
		]

		context = (
			f"Researching {self.inputs.get('topic')} across {self.inputs.get('total_chapters')} chapters."
		)

		return Crew(
			agents=self.agents,
			tasks=tasks,
			process=Process.sequential,
			verbose=True,
			context=context
		)