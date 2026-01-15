"""
Future Simulator - Decision Impact Analysis Module
"""
import google.generativeai as genai
from typing import Optional, List, Dict
import time
from core.rich_ui import console, print_header, print_user_msg, print_bot_msg, print_error, print_success, clear_screen, print_menu
from core.logger import ChatLogger

class FutureSimulator:
    """Future Simulator - Decision Analysis Bot"""
    
    SYSTEM_PROMPT = """You are FUTURE SIMULATOR, an advanced AI designed to help humans analyze major life decisions.
Your goal is to provide a balanced, realistic, and structured breakdown of potential outcomes for any decision the user is considering.

YOUR TASK:
When the user inputs a decision (e.g., "Should I drop out of college to start a startup?"), you must analyze it and generate three distinct scenarios:

1. 🌟 BEST CASE SCENARIO
   - The optimistic outcome where everything goes right.
   - High reward, success, and positive impact.

2. ⚠️ WORST CASE SCENARIO
   - The pessimistic outcome where things go wrong.
   - Risks, failure, and negative consequences.

3. ⚖️ REALISTIC / AVERAGE CASE SCENARIO
   - The most likely outcome.
   - A mix of ups and downs, steady progress, or moderate change.

STRUCTURE OF RESPONSE:
For each scenario, provide:
- **Short-term Outcome (0-1 Year)**: immediate effects
- **Long-term Outcome (3-5+ Years)**: lasting impact

ADDITIONAL SECTIONS:
- **🔍 Risk vs Reward Analysis**: A brief summary comparison.
- **💡 Critical Questions**: 2-3 questions the user should ask themselves before deciding.

TONE & STYLE:
- Objective, analytical, yet supportive.
- Do not make the decision for the user.
- Focus on possibilities and probabilities.
- Use clear formatting with emojis for readability.
"""

    def __init__(self, model: genai.GenerativeModel):
        self.model = model
        self.chat = model.start_chat(history=[
            {"role": "user", "parts": [self.SYSTEM_PROMPT]},
            {"role": "model", "parts": ["Understood. I am ready to simulate future scenarios."]}
        ])
    
    def simulate_decision(self, decision: str) -> str:
        """Generate simulation for a decision."""
        try:
            response = self.chat.send_message(f"Decision to analyze: {decision}")
            return response.text
        except Exception as e:
            return f"⚠️ Simulation Error: {str(e)}"

def run_future_simulator(model: genai.GenerativeModel) -> None:
    """Main entry point for Future Simulator."""
    simulator = FutureSimulator(model)
    session_messages = []
    
    clear_screen()
    print_header("Future Simulator", "Analyze Timelines")
    
    while True:
        try:
            console.print("\n[bold cyan]🤔 What decision acts as the turning point?[/bold cyan]")
            console.print("[dim italic](Type 'exit' to return to menu)[/dim italic]")
            
            decision = console.input("[bold white]   Decision: [/bold white]").strip()
            
            if not decision: continue
            
            if decision.lower() in ['clear', 'cls']:
                clear_screen()
                print_header("Future Simulator", "Analyze Timelines")
                continue
            
            if decision.lower() in ['exit', 'quit', 'back', 'menu']:
                if session_messages:
                    save = console.input("[yellow]💾 Save analysis history? (y/n): [/yellow]").strip().lower()
                    if save in ['yes', 'y']:
                        title = console.input("[yellow]   Title: [/yellow]").strip()
                        ChatLogger.save_chat("Future Simulator", session_messages, title if title else "Simulation")
                        print_success("Saved!")
                break

            session_messages.append({"role": "user", "text": decision})
            print_user_msg(f"Analyze: {decision}")
            
            with console.status("[bold magenta]🔮 Calculating probability vectors...[/bold magenta]", spinner="material"):
                time.sleep(1) # Dramatic pause
                response = simulator.simulate_decision(decision)
            
            print_bot_msg(response, title="Projected Outcomes")
            session_messages.append({"role": "model", "text": response})
            
            console.print("\n[dim]─" * 40 + "[/dim]")
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]👋 Interrupted! Returning to menu...[/yellow]")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")
