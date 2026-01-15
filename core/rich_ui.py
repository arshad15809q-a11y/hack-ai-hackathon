"""
Rich UI Utilities for CLI Chatbot
Provides a unified theme and helper functions for a premium terminal experience.
"""
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.align import Align
from rich.table import Table
from rich import box
import time

# Define a custom color theme
THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "user_panel": "blue",
    "bot_panel": "green",
    "header": "bold white on blue",
    "menu_border": "cyan",
    "highlight": "bold magenta",
})

# Global console instance
console = Console(theme=THEME)

def print_header(title: str, subtitle: str = ""):
    """Print a styled header."""
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_row(f"[bold white]{title}[/bold white]")
    if subtitle:
        grid.add_row(f"[italic cyan]{subtitle}[/italic cyan]")
    
    panel = Panel(
        grid,
        style="white",
        border_style="blue",
        padding=(1, 2),
        box=box.HEAVY
    )
    console.print(panel)
    console.print()

def print_user_msg(text: str):
    """Print a user message (right-aligned)."""
    # Note: Rich aligns the panel content, but we want the panel itself to look right-aligned.
    # Align.right() works for the whole renderable.
    
    content = Text(text, style="white")
    panel = Panel(
        content,
        title="[bold blue]You[/bold blue]",
        title_align="right",
        border_style="blue",
        subtitle_align="right",
        box=box.ROUNDED,
        padding=(0, 1),
        expand=False
    )
    console.print(Align.right(panel))
    # console.print() # spacer

def print_bot_msg(text: str, title: str = "Bot", style: str = "white"):
    """Print a bot message (left-aligned)."""
    try:
        content = Markdown(text)
    except:
        content = Text(text)
        
    panel = Panel(
        content,
        title=f"[bold green]{title}[/bold green]",
        title_align="left",
        border_style="green",
        box=box.ROUNDED,
        padding=(0, 1),
        expand=False,
        width=100 # Good width for readability
    )
    console.print(Align.left(panel))
    console.print()

def print_menu(options: dict, title: str = "MAIN MENU"):
    """Print a nice menu table."""
    table = Table(box=box.SIMPLE, show_header=False, expand=True, border_style="cyan", padding=(0, 2))
    table.add_column("Key", justify="right", style="bold cyan", width=4)
    table.add_column("Content", justify="left")
    
    # Sort keys if they are numeric strings
    sorted_keys = sorted(options.keys(), key=lambda x: int(x) if x.isdigit() else 99)
    
    for key in sorted_keys:
        info = options[key]
        if info.get('available', True):
            icon = info.get('icon', '🔹')
            name = info.get('name', 'Unknown')
            desc = info.get('description', '')
            
            # Create a little grid for name + desc
            text_grid = Table.grid()
            text_grid.add_row(f"[bold white]{icon} {name}[/bold white]")
            if desc:
                text_grid.add_row(f"[dim]{desc}[/dim]")
                
            table.add_row(f"[{key}]", text_grid)
            table.add_section()
        
    panel = Panel(
        table,
        title=f"[bold]{title}[/bold]",
        border_style="cyan",
        padding=(1, 1),
        box=box.ROUNDED
    )
    console.print(panel)

def print_error(msg: str):
    """Print an error message."""
    console.print(f"[bold red]❌ {msg}[/bold red]")

def print_success(msg: str):
    """Print a success message."""
    console.print(f"[bold green]✅ {msg}[/bold green]")

def clear_screen():
    """Clear the terminal screen."""
    console.clear()

def stream_thinking(text="Thinking..."):
    """Show a spinner."""
    pass # Use 'with console.status("Thinking..."):' in the code instead
