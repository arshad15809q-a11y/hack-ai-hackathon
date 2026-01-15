
import os
import sys
import time
import google.generativeai as genai
from typing import Callable, Dict, Optional
from core.rich_ui import console, print_header, print_error, print_success, print_menu, clear_screen

# Import chatbot modules from agents package
from agents.study_buddy import run_study_buddy
from agents.code_made_easy import run_code_made_easy
from agents.lingua_link import run_lingua_link
from agents.explain_like_x import run_explain_like_x
from agents.time_travel import run_time_travel
from agents.future_simulator import run_future_simulator
from agents.conversation_replay import run_conversation_replay


class ChatbotMenu:
    """Main menu system for the multi-bot chatbot framework."""
    
    def __init__(self):
        """Initialize the chatbot menu system."""
        self.model: Optional[genai.GenerativeModel] = None
        self.api_key: Optional[str] = None
        
        # Map of menu options to chatbot functions
        self.chatbots: Dict[str, Dict] = {
            '1': {
                'name': 'Study Buddy',
                'description': 'Academic & Career Guidance for Students',
                'icon': '📚',
                'function': run_study_buddy,
                'available': True
            },
            '2': {
                'name': 'Lingua Link',
                'description': 'Your Desi AI Companion (Hinglish Chat)',
                'icon': '🌐',
                'function': run_lingua_link,
                'available': True
            },
            '3': {
                'name': 'Code Made Easy',
                'description': 'Debug Code, Generate Code, Rate Programs',
                'icon': '💻',
                'function': run_code_made_easy,
                'available': True
            },
            '4': {
                'name': 'Time Travel Chat',
                'description': 'Chat with History (Talk to people from any year)',
                'icon': '⏰',
                'function': run_time_travel,
                'available': True
            },
            '5': {
                'name': 'Future Simulator',
                'description': 'Predict & Analyze Decision Outcomes',
                'icon': '🔮',
                'function': run_future_simulator,
                'available': True
            },
            '6': {
                'name': 'Explain Like X',
                'description': 'Explanations in Creative Styles & Personas',
                'icon': '🎭',
                'function': run_explain_like_x,
                'available': True
            },
            '7': {
                'name': 'Conversation Replay',
                'description': 'Replay & Analyze Past Chats',
                'icon': '🔄',
                'function': run_conversation_replay,
                'available': True
            },
             '0': {
                'name': 'Exit',
                'description': 'Close the application',
                'icon': '❌',
                'function': None,
                'available': True
            },
        }
    
    def setup_gemini(self) -> bool:
        """Setup Gemini API with API key."""
        
        with console.status("[bold cyan]🔧 Setting up Gemini API...", spinner="dots"):
            time.sleep(0.5) # Simulate work
            self.api_key = os.environ.get("GEMINI_API_KEY")
            
            if not self.api_key:
                # Need user input, stop spinner
                pass
        
        if not self.api_key:
            print_error("GEMINI_API_KEY environment variable not found.")
            console.print("   [dim]You can set it using: set GEMINI_API_KEY=your_key_here[/dim]")
            console.print("\n   [bold]Or enter your API key now (it won't be stored):[/bold]")
            
            try:
                self.api_key = console.input("   [bold yellow]API Key: [/bold yellow]").strip()
            except KeyboardInterrupt:
                console.print("\n\n❌ Setup cancelled.")
                return False
            
            if not self.api_key:
                print_error("No API key provided. Cannot continue.")
                return False
        
        try:
            with console.status("[bold green]Connecting to Google Gemini...", spinner="earth"):
                # Configure the Gemini API
                genai.configure(api_key=self.api_key)
                # Initialize the model
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                # Test connection
                self.model.generate_content("Say 'ready' in one word.")
            
            print_success("Connected to Gemini API!")
            time.sleep(0.5)
            return True
                
        except Exception as e:
            print_error(f"Failed to setup Gemini API: {str(e)}")
            console.print("   Please check your API key and internet connection.")
            return False
    
    def run(self):
        """Main loop for the chatbot menu system."""
        clear_screen()
        
        # Startup animation
        with console.status("[bold blue]Booting Handyware AI System...", spinner="aesthetic"):
            time.sleep(1.2)
            
        print_header("🤖 Multi-Purpose AI Chatbot System", "Powered by Google Gemini 2.5 Flash")
        
        # Setup Gemini API
        if not self.setup_gemini():
            console.print("\n[bold red]⚠️  Cannot start without Gemini API access.[/bold red]")
            console.input("\n   Press Enter to exit...")
            return
        
        # Main menu loop
        while True:
            try:
                clear_screen()
                print_header("🤖 Handyware AI Hub", "Select an agent to begin")
                print_menu(self.chatbots)
                
                choice = console.input("\n[bold cyan]👉 Enter your choice:[/bold cyan] ").strip()
                
                if choice == '0':
                    console.print("\n")
                    console.rule("[bold blue]Goodbye![/bold blue]")
                    console.print("[italic]Thanks for using Handyware AI![/italic]", justify="center")
                    break
                
                if choice in self.chatbots:
                    bot = self.chatbots[choice]
                    
                    if not bot['available']:
                        console.print(f"\n[yellow]⏳ Sorry, {bot['name']} is coming soon![/yellow]")
                        console.input("Press Enter to continue...")
                        continue
                    
                    # Launch the selected chatbot
                    clear_screen()
                    with console.status(f"[bold green]🚀 Launching {bot['name']}...", spinner="point"):
                        time.sleep(0.8)
                    
                    try:
                        bot['function'](self.model)
                    except Exception as e:
                        print_error(f"Error in {bot['name']}: {str(e)}")
                        console.input("Press Enter to return to menu...")
                    
                else:
                    console.print("\n[bold red]❓ Invalid choice. Please try again.[/bold red]")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                console.print("\n\n[yellow]⚠️  Interrupted! Returning to menu...[/yellow]")
                time.sleep(1)
                continue
            except Exception as e:
                print_error(f"An unexpected error occurred: {str(e)}")
                console.input("Press Enter to recover...")
                continue
