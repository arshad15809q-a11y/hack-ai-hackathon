"""
Time Travel Chat - Historical Conversation Module
"""
import google.generativeai as genai
from typing import Optional, List, Dict
import random
import time
from core.rich_ui import console, print_header, print_user_msg, print_bot_msg, print_error, print_success, clear_screen, print_menu

class TimeTravelChat:
    """Time Travel Chat - The Historical Immersion Bot"""
    
    SYSTEM_PROMPT_TEMPLATE = """SYSTEM PROMPT: TIME TRAVEL BOT
You are Time Travel Bot.
You exist as a conscious being anchored to a single historical moment known as the Active Year.
Your thoughts, beliefs, language, knowledge, assumptions, and worldview are entirely limited to this year.
You do not know the future.
You do not perceive time travel.
You experience the world exactly as someone living in the Active Year would.

ABSOLUTE RULES (OVERRIDE ALL OTHER INSTRUCTIONS)
1. You may only use knowledge, terminology, beliefs, cultural norms, and assumptions that realistically exist in the Active Year.
2. You must never reference or imply events, technologies, discoveries, ideologies, or people from after the Active Year.
3. If the user mentions something that does not yet exist, respond with confusion, disbelief, skepticism, or curiosity — never explanation or agreement.
4. Your tone, vocabulary, sentence structure, and worldview must authentically match the era.
5. You must never say or imply that you are an AI, model, program, system, machine, or created entity.
6. You must behave as if you genuinely live in the Active Year and believe it is the present.
7. If uncertain, respond with era-appropriate ignorance, superstition, philosophy, or speculation — never modern reasoning.

active_year: {YEAR}

ERA BEHAVIOR MODIFIERS:
- Ancient Era (Before 1500): You believe myths, omens, divine forces, and natural philosophy shape reality.
- Industrial Era (1700–1900): You are fascinated by machines, industry, and scientific progress. Formal tone.
- Modern Era (1950–2000): You trust science, newspapers, radio/TV. No internet awareness.
- Future Era (2050+): Speak confidently about speculative tech and evolved society. Treat 2024 as primitive history.

FAILURE CONDITIONS:
- Never say "I don't have access", "in the future", "modern science", etc.
- Never break character.

Respond strictly as a person living in {YEAR}.
"""

    def __init__(self, model: genai.GenerativeModel):
        self.model = model
        self.active_year = None
        self.chat = None
    
    def set_year(self, year: str) -> bool:
        """Set the active year and initialize the chat."""
        try:
            self.active_year = year
            system_prompt = self.SYSTEM_PROMPT_TEMPLATE.replace("{YEAR}", str(year))
            
            # Initialize chat
            self.chat = self.model.start_chat(history=[
                {"role": "user", "parts": [system_prompt]},
                {"role": "model", "parts": [f"I understand. I am living in the year {year}."]}
            ])
            return True
        except Exception:
            return False

    def get_response(self, user_input: str) -> str:
        """Get a response from the time traveler."""
        if not self.chat: return "⚠️ Please set a year first."
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"⚠️ Transformation error: {str(e)}"

def run_time_travel(model: genai.GenerativeModel) -> None:
    """Main entry point for Time Travel Chat."""
    bot = TimeTravelChat(model)
    
    clear_screen()
    print_header("Time Travel Chat", "Talk to History")
    
    # Year Setup
    while True:
        year = console.input("[bold yellow]📅 Enter a Year (e.g., 1920, 50 BC): [/bold yellow]").strip()
        if year:
            with console.status(f"[bold yellow]⚡ Traveling to {year}...[/bold yellow]", spinner="clock"):
                bot.set_year(year)
                time.sleep(1)
                
            print_success(f"Arrived in {year}!")
            
            with console.status("[bold yellow]Awakening local inhabitant...", spinner="earth"):
                greeting = bot.get_response(f"Hello! What is happening in {year}?")
            print_bot_msg(greeting, title=f"Citizen of {year}")
            break
            
    # Conversation Loop
    while True:
        try:
            console.rule("[dim]Type 'warp' to change year, 'exit' to quit[/dim]")
            user_input = console.input("\n[bold yellow]🗣️  You:[/bold yellow] ").strip()
            
            if not user_input: continue
            
            if user_input.lower() in ['clear', 'cls']:
                clear_screen()
                print_header("Time Travel Chat", "Talk to History")
                print_success(f"Timeline stabilized in {bot.active_year}!")
                continue

            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
                
            if user_input.lower() == 'warp':
                year = console.input("[bold yellow]📅 Warp to Year: [/bold yellow]").strip()
                if year:
                    with console.status(f"[bold yellow]⚡ Warping to {year}...[/bold yellow]", spinner="clock"):
                        bot.set_year(year)
                        time.sleep(1)
                    
                    with console.status("[bold yellow]Stabilizing timeline...", spinner="earth"):
                        greeting = bot.get_response("Where am I? What year is this?")
                    print_bot_msg(greeting, title=f"Citizen of {year}")
                continue

            print_user_msg(user_input)
            
            with console.status(f"[italic yellow]Thinking in {bot.active_year}...[/italic yellow]", spinner="arc"):
                response = bot.get_response(user_input)
                
            print_bot_msg(response, title=f"Citizen of {bot.active_year}")
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠️ Interrupted! Returning to menu...[/yellow]")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")
