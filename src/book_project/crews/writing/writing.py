from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Writing():
	"""Writing crew for chapter-by-chapter book creation"""

	def __init__(self, inputs=None):
		self.inputs = inputs or {}
		super().__init__()

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def toc_writer(self) -> Agent:
		return Agent(config=self.agents_config['toc_writer'])

	@agent
	def chapter_writer(self) -> Agent:
		return Agent(config=self.agents_config['chapter_writer'])

	@task
	def develop_chapter_outlines(self) -> Task:
		task = Task(config=self.tasks_config['develop_chapter_outlines'])
		self._format_task_config(task)
		return task

	@task
	def write_chapter_content(self) -> Task:
		task = Task(config=self.tasks_config['write_chapter_content'])
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
				'author_name': self.inputs.get('author_name', ''),
				'research_results': self.inputs.get('research_results', '')
			}
			
			# Format all string values in the config
			for key, value in task.config.items():
				if isinstance(value, str):
					task.config[key] = value.format(**inputs)

	@crew
	def crew(self) -> Crew:
		"""Creates the Writing crew for the current chapter"""
		tasks = [
			self.develop_chapter_outlines(),
			self.write_chapter_content()
		]

		context = (
			f"Writing Chapter {self.inputs.get('chapter_number')} of {self.inputs.get('total_chapters')} "
			f"on topic: {self.inputs.get('topic')}. "
			f"Target length: {self.inputs.get('pages')} pages."
		)

		return Crew(
			agents=self.agents,
			tasks=tasks,
			process=Process.sequential,
			verbose=True,
			context=context
		)
