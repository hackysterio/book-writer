#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from pathlib import Path
import subprocess
import json
import os
from datetime import datetime

from book_project.crews.research.research import Research
from book_project.crews.writing.writing import Writing


class BookState(BaseModel):
    topic: str = ""
    author_name: str = ""
    research_results: dict = {}
    chapters_content: dict = {}
    book_toc: str = ""
    final_book: str = ""
    output_directory: str = ""
    current_chapter: int = 1
    total_chapters: int = 0
    pages_per_chapter: int = 0


class BookFlow(Flow[BookState]):
    @start()
    def initialize_project(self):
        try:
            print("\n=== Initializing Book Project: Zero to Hero Series ===")
            self.state.topic = input("Enter the book topic: ")
            self.state.author_name = input("Enter the author name: ")
            self.state.total_chapters = int(input("Enter the total number of chapters: "))
            if self.state.total_chapters <= 0:
                raise ValueError("Number of chapters must be positive")
            
            self.state.pages_per_chapter = int(input("Enter approximate pages per chapter: "))
            if self.state.pages_per_chapter <= 0:
                raise ValueError("Pages per chapter must be positive")
            
            # Create output directory with sanitized topic name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_topic = self.state.topic.replace(" ", "_").lower()
            self.state.output_directory = os.path.join(
                "output",
                f"book_{sanitized_topic}_{timestamp}"
            )
            os.makedirs(self.state.output_directory, exist_ok=True)
            
            print(f"\nProject initialized for {self.state.total_chapters} chapters")
            print(f"Target length: {self.state.pages_per_chapter} pages per chapter")
            print(f"Output will be saved to: {self.state.output_directory}")
        except ValueError as e:
            print(f"Invalid input: {e}")
            return self.initialize_project()

    @listen(initialize_project)
    def conduct_research(self):
        print("\n=== Phase 1: Conducting Chapter-by-Chapter Research ===")
        
        for chapter in range(1, self.state.total_chapters + 1):
            self.state.current_chapter = chapter
            print(f"\nResearching Chapter {chapter}/{self.state.total_chapters}")
            
            result = (
                Research(inputs={
                    "topic": self.state.topic,
                    "chapter_number": chapter,
                    "pages": self.state.pages_per_chapter,
                    "total_chapters": self.state.total_chapters
                })
                .crew()
                .kickoff()
            )
            
            research_file = os.path.join(
                self.state.output_directory, 
                f"chapter_{chapter}_research.md"
            )
            with open(research_file, 'w', encoding='utf-8') as f:
                f.write(result.raw)
            
            self.state.research_results[f"chapter_{chapter}"] = result.raw
            print(f"✓ Chapter {chapter} research completed")

    @listen(conduct_research)
    def create_book(self):
        print("\n=== Phase 2: Chapter-by-Chapter Writing ===")
        
        for chapter in range(1, self.state.total_chapters + 1):
            self.state.current_chapter = chapter
            print(f"\nWriting Chapter {chapter}/{self.state.total_chapters}")
            
            # Pass research results to the writing crew
            result = (
                Writing(inputs={
                    "topic": self.state.topic,
                    "author_name": self.state.author_name,
                    "chapter_number": chapter,
                    "pages": self.state.pages_per_chapter,
                    "total_chapters": self.state.total_chapters,
                    "research_results": self.state.research_results.get(f"chapter_{chapter}", "")
                })
                .crew()
                .kickoff()
            )
            
            chapter_file = os.path.join(
                self.state.output_directory, 
                f"chapter_{chapter}_final.md"
            )
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(result.raw)
            
            self.state.chapters_content[f"chapter_{chapter}"] = result.raw
            print(f"✓ Chapter {chapter} completed")
        
        # Combine all chapters into final book
        self.assemble_final_book()

    def assemble_final_book(self):
        print("\n=== Assembling Final Book ===")
        
        # Create table of contents and combine chapters
        final_content = [
            f"# {self.state.topic}",
            f"By {self.state.author_name}\n\n",
            "## Table of Contents\n"
        ]
        
        for chapter in range(1, self.state.total_chapters + 1):
            final_content.append(self.state.chapters_content[f"chapter_{chapter}"])
        
        self.state.final_book = "\n\n".join(final_content)
        
        sanitized_topic = self.state.topic.replace(" ", "_").lower()
        book_md = os.path.join(
            self.state.output_directory, 
            f"book_{sanitized_topic}.md"
        )
        with open(book_md, 'w', encoding='utf-8') as f:
            f.write(self.state.final_book)
        print(f"\n✓ Complete book assembled and saved to: {book_md}")
        
        # Convert markdown to PDF
        self.convert_to_pdf(book_md)

    def convert_to_pdf(self, markdown_file):
        """Convert the markdown file to PDF using pandoc."""
        try:
            pdf_file = markdown_file.replace('.md', '.pdf')
            print("\n=== Converting to PDF ===")
            subprocess.run([
                'pandoc',
                markdown_file,
                '-o', pdf_file,
                '--pdf-engine=xelatex',
                '--toc',
                '--toc-depth=2',
                '-V', 'geometry:margin=1in'
            ], check=True)
            print(f"✓ PDF version saved to: {pdf_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting to PDF: {e}")
            print("Please ensure pandoc and a LaTeX distribution are installed:")
            print("- Install pandoc: https://pandoc.org/installing.html")
            print("- Install LaTeX: https://www.latex-project.org/get/")
        except Exception as e:
            print(f"An unexpected error occurred during PDF conversion: {e}")

    def _format_task_config(self, task):
        """Format task configuration with current chapter and topic"""
        if hasattr(task, 'config') and task.config:
            # Get all required variables
            inputs = {
                'chapter_number': self.inputs.get('chapter_number'),
                'topic': self.inputs.get('topic'),
                'pages': self.inputs.get('pages'),
                'total_chapters': self.inputs.get('total_chapters')
            }
            
            # Format description
            if 'description' in task.config:
                task.config['description'] = task.config['description'].format(**inputs)
            
            # Format output file
            if 'output_file' in task.config:
                task.config['output_file'] = task.config['output_file'].format(**inputs)


def kickoff():
    try:
        print("\nWelcome to the Book Generator!")
        print("This tool will help you create a comprehensive book on any topic.")
        print("Expected duration: Several hours for a 500+ page book")
        book_flow = BookFlow()
        book_flow.kickoff()
    except KeyboardInterrupt:
        print("\n\nBook creation interrupted. Progress has been saved.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        raise


def plot():
    book_flow = BookFlow()
    book_flow.plot()


if __name__ == "__main__":
    kickoff()
