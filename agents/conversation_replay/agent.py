"""
Conversation Replay - Chat History Viewer
"""
import google.generativeai as genai
from core.logger import ChatLogger
from core.rich_ui import console, print_header, print_user_msg, print_bot_msg, print_error, print_success, clear_screen
from rich.table import Table
from rich import box

def run_conversation_replay(model: genai.GenerativeModel = None) -> None:
    """Main entry for conversation replay."""
    
    while True:
        clear_screen()
        print_header("Conversation Replay", "Review Your Past Chats")
        
        history = ChatLogger.load_history()
        
        if not history:
            console.print("\n[italic yellow]📭 No conversation history found.[/italic yellow]")
            console.print("   Chat with other bots first to save conversations!")
            console.input("\n[dim]Press Enter to return...[/dim]")
            break
        
        # Display List
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=4)
        table.add_column("Date", style="cyan")
        table.add_column("Agent", style="green")
        table.add_column("Title", style="white")
        
        # Reverse to show newest first
        reversed_history = list(reversed(history))
        for i, session in enumerate(reversed_history, 1):
            table.add_row(str(i), session['timestamp'], session['module'], session['title'])
            
        console.print(table)
        
        console.rule("[bold cyan]Options[/bold cyan]")
        console.print("[dim]Enter number to view • 'clear' to delete all • 'exit' to go back[/dim]")
        
        choice = console.input("\n[bold cyan]👉 Choice:[/bold cyan] ").strip().lower()
        
        if choice in ['exit', 'quit', 'back', '0']:
            break
            
        if choice == 'clear':
            confirm = console.input("[bold red]⚠️  Delete ALL history? (yes/no): [/bold red]").lower()
            if confirm == 'yes':
                ChatLogger.clear_history()
                print_success("History cleared!")
            continue
            
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(reversed_history):
                session = reversed_history[idx]
                
                # Display Chat Detail
                clear_screen()
                print_header(f"Replay: {session['module']}", f"{session['title']} ({session['timestamp']})")
                
                for msg in session['messages']:
                    if msg['role'] == 'user':
                        print_user_msg(msg['text'])
                    else:
                        print_bot_msg(msg['text'], title=session['module'])
                
                console.input("\n[dim]End of chat. Press Enter to go back...[/dim]")
            else:
                print_error("Invalid number.")
                time.sleep(1)
        except ValueError:
            print_error("Invalid input.")
            time.sleep(1)

# For standalone testing
if __name__ == "__main__":
    run_conversation_replay()
