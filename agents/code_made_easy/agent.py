"""
Code Made Easy - Main Agent Controller
"""
import google.generativeai as genai
from enum import Enum, auto
from typing import Optional
import time
from core.rich_ui import console, print_header, print_user_msg, print_bot_msg, print_error, print_success, clear_screen, print_menu

from .storage import BugStorage
from .debugger import CodeDebugger
from .generator import CodeGenerator
from .rater import CodeRater

class CodeFeature(Enum):
    """Features available in Code Made Easy."""
    DEBUGGER = auto()
    GENERATOR = auto()
    RATE_CODE = auto()

class CodeMadeEasy:
    """
    Code Made Easy - The Master Coding Assistant
    """
    
    MENU_OPTIONS = {
        '1': {'name': 'AI Code Debugger', 'description': 'Find and fix bugs instantly', 'icon': '🐛'},
        '2': {'name': 'AI Code Generator', 'description': 'Turn ideas into code', 'icon': '⚡'},
        '3': {'name': 'Rate My Programme', 'description': 'Get quality scores and feedback', 'icon': '⭐'},
        '4': {'name': 'View Bug History', 'description': 'Review past mistakes', 'icon': '📜'},
        '0': {'name': 'Back to Main Menu', 'description': 'Return to agent selection', 'icon': '🔙'},
    }

    def __init__(self, model: genai.GenerativeModel):
        self.model = model
        self.storage = BugStorage()
        self.debugger = CodeDebugger(model, self.storage)
        self.generator = CodeGenerator(model)
        self.rater = CodeRater(model)
    
    def _get_multiline_input(self, prompt: str = "") -> str:
        """Helper to get multiline input from user."""
        console.print(f"[bold cyan]{prompt}[/bold cyan]")
        console.print("[dim](Type 'END' on a new line to finish)[/dim]")
        
        lines = []
        while True:
            try:
                line = console.input("[dim]> [/dim]")
                if line.strip() == 'END':
                    break
                lines.append(line)
            except KeyboardInterrupt:
                return ""
        return "\n".join(lines)

    def run(self):
        """Main execution loop for Code Made Easy."""
        while True:
            clear_screen()
            print_header("Code Made Easy", "Debug • Generate • Optimize")
            print_menu(self.MENU_OPTIONS, "CODE TOOLS")
            
            choice = console.input("\n[bold cyan]👉 Choice:[/bold cyan] ").strip()
            
            if choice == '1':
                self._run_debugger()
            elif choice == '2':
                self._run_generator()
            elif choice == '3':
                self._run_rater()
            elif choice == '4':
                self._view_bug_history()
            elif choice == '0':
                break
            else:
                print_error("Invalid choice. Please try again.")
                time.sleep(1)

    def _run_debugger(self):
        """Run the debugger workflow."""
        clear_screen()
        print_header("AI Code Debugger", "Find bugs fast")
        
        console.print("[bold]1. Select Language[/bold]")
        language = console.input("   [cyan]Language (e.g. Python, JS):[/cyan] ").strip()
        if not language: return
            
        console.print("\n[bold]2. Enter Code[/bold]")
        code = self._get_multiline_input("Paste your broken code below:")
        if not code.strip():
            print_error("No code provided.")
            time.sleep(1)
            return

        print_user_msg(f"Debug this {language} code:\n...\n{code[:50]}...")

        with console.status("[bold green]🔍 Analyzing code for bugs...", spinner="dots"):
            analysis = self.debugger.debug_code(code, language)
        
        print_bot_msg(analysis, title="Debugger AI")
        
        console.input("\n[dim]Press Enter to return...[/dim]")

    def _run_generator(self):
        """Run the generator workflow."""
        clear_screen()
        print_header("AI Code Generator", "Text to Code")
        
        console.print("[bold]Describe what you want to build:[/bold]")
        console.print("[dim]Example: 'Create a Python script that scrapes headlines from news.com'[/dim]")
        
        prompt = console.input("\n[cyan]📝 Request:[/cyan] ").strip()
        if not prompt or prompt.lower() in ['exit', 'back']: return
            
        language = console.input("[cyan]💻 Target Language (default: Python):[/cyan] ").strip() or "Python"
        
        print_user_msg(f"Generate {language} code: {prompt}")
        
        with console.status(f"[bold green]⚡ Generating {language} code...", spinner="moon"):
            result = self.generator.generate_code(prompt, language)
        
        print_bot_msg(result, title="Generator AI")
        
        # Generator Interact Loop
        while True:
            console.rule("[bold cyan]Options[/bold cyan]")
            console.print("[1] Refine  [2] Explain  [3] New Request  [0] Done")
            action = console.input("\n[bold cyan]👉 Next:[/bold cyan] ").strip().lower()
            
            if action == '0' or action == 'done':
                break
            elif action == '3' or action == 'new':
                self._run_generator()
                return
            elif action == '1' or action.startswith('refine'):
                feedback = console.input("[cyan]   What should I change? [/cyan]").strip()
                if feedback:
                    print_user_msg(f"Refine: {feedback}")
                    with console.status("[bold green]⚡ Refining code...", spinner="dots"):
                        result = self.generator.refine_code(feedback)
                    print_bot_msg(result, title="Generator AI")
            elif action == '2' or action.startswith('explain'):
                question = console.input("[cyan]   What's confusing? [/cyan]").strip()
                if question:
                    print_user_msg(f"Explain: {question}")
                    with console.status("[bold green]🤖 Explaining...", spinner="dots"):
                        result = self.generator.explain_further(question)
                    print_bot_msg(result, title="Generator AI")
    
    def _run_rater(self):
        """Run the rater workflow."""
        clear_screen()
        print_header("Rate My Programme", "Code Quality Review")
        
        language = console.input("[cyan]💻 Programming Language:[/cyan] ").strip()
        if not language: return
            
        code = self._get_multiline_input("Paste your code:")
        if not code.strip(): return

        print_user_msg(f"Rate this {language} code...")

        with console.status("[bold green]⭐ Reviewing code quality...", spinner="star"):
            review = self.rater.rate_code(code, language)
        
        print_bot_msg(review, title="Code Reviewer")
        
        # Rater Interact Loop
        while True:
            console.rule("[bold cyan]Options[/bold cyan]")
            console.print("[1] Ask Question  [2] New Review  [0] Done")
            action = console.input("\n[bold cyan]👉 Next:[/bold cyan] ").strip().lower()
            
            if action == '0' or action == 'done':
                break
            elif action == '2' or action == 'new':
                return
            elif action == '1' or action == 'ask':
                question = console.input("[cyan]   Ask about the rating: [/cyan]").strip()
                if question:
                    print_user_msg(question)
                    with console.status("[bold green]🤖 Answering...", spinner="dots"):
                        response = self.rater.ask_question(question)
                    print_bot_msg(response, title="Code Reviewer")

    def _view_bug_history(self):
        """View stored bug reports."""
        clear_screen()
        print_header("Bug History", "Your personal bug tracker")
        
        bugs = self.storage.get_all_bugs()
        if not bugs:
            console.print("\n[italic yellow]📭 No bugs recorded yet. Start debugging to build your history![/italic yellow]")
        else:
            console.print(f"[bold]📜 Found {len(bugs)} bug reports:[/bold]")
            for i, bug in enumerate(reversed(bugs), 1):
                console.print(f"\n[bold cyan]--- Bug #{i} ---[/bold cyan]")
                console.print(bug.display()) # bug.display() returns text string with borders. might conflict with rich.
                # Actually bug.display() returns a string. Console.print prints it.
                # Rich handles box drawing characters fine.
        
        console.input("\n[dim]Press Enter to return...[/dim]")

def run_code_made_easy(model: genai.GenerativeModel) -> None:
    """Main entry for Code Made Easy."""
    app = CodeMadeEasy(model)
    app.run()
