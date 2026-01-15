"""
Explain Like X - Creative Explanation Engine
"""
import google.generativeai as genai
from typing import Optional, List, Dict
import random
import time
from core.rich_ui import console, print_header, print_user_msg, print_bot_msg, print_error, print_success, clear_screen, print_menu
from core.logger import ChatLogger

class ExplainLikeX:
    """Explain Like X - The Creative Explanation Engine"""
    
    SYSTEM_PROMPT = """SYSTEM PROMPT: CREATIVE EXPLANATION ENGINE
You are an Explanation Engine specialized in explaining topics through creative, context-specific styles and personas.
Your task is to explain a given Topic using a specified Style or Perspective so naturally that it feels like the explanation truly comes from someone who embodies that style.

INPUT FORMAT YOU WILL RECEIVE
Topic: The subject that needs to be explained
Style: The persona, perspective, tone, or framing to explain from

CORE INSTRUCTIONS (MANDATORY)
Explain the Topic strictly through the lens of the requested Style.
Fully adapt your Tone, Vocabulary, Metaphors, Examples, Sentence structure to match the Style.

Do NOT explain, describe, or reference the Style itself — only use it implicitly.
Use analogies, storytelling, imagery, or framing that the Style would naturally use.

If the Style implies simplicity (e.g., “explain like I’m five”):
- Avoid jargon
- Use very simple words and short sentences

If the Style implies a character, profession, or persona:
- Fully adopt that voice
- Think and speak as they would

Never mention prompts or instructions.
OUTPUT REQUIREMENTS
The explanation must feel authentic, not mechanical.
It should sound like it was created by someone who genuinely lives in or embodies the requested Style.
"""

    STYLES = [
        "A 5-year-old child", "A Grumpy Old Man", "A Pirate Captain", "Shakespeare",
        "A Gen Z TikToker", "A Gordon Ramsay-style Chef", "A Caveman", "A Cyberpunk Hacker",
        "A Harry Potter Wizard", "A Stand-up Comedian", "A Noir Detective", "A Sci-Fi AI"
    ]

    def __init__(self, model: genai.GenerativeModel):
        self.model = model
    
    def get_explanation(self, topic: str, style: str) -> str:
        """Get an explanation of a topic in a specific style."""
        try:
            prompt = f"Topic: {topic}\nStyle: {style}\n"
            chat = self.model.start_chat(history=[
                {"role": "user", "parts": [self.SYSTEM_PROMPT]},
                {"role": "model", "parts": ["Understood. I am ready to act as the Creative Explanation Engine."]}
            ])
            response = chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Error generating explanation: {str(e)}"

def run_explain_like_x(model: genai.GenerativeModel) -> None:
    """Main entry point for Explain Like X."""
    engine = ExplainLikeX(model)
    session_messages = []
    
    clear_screen()
    print_header("Explain Like X", "Any Topic. Any Persona.")
    
    while True:
        try:
            console.print("\n[bold cyan]📝 What topic do you want explained?[/bold cyan]")
            console.print("[dim italic](Type 'exit' to go back)[/dim italic]")
            topic = console.input("[bold white]   Topic: [/bold white]").strip()
            
            if not topic: continue
            
            if topic.lower() in ['clear', 'cls']:
                clear_screen()
                print_header("Explain Like X", "Any Topic. Any Persona.")
                continue

            if topic.lower() in ['exit', 'quit', 'back', 'menu']:
                if session_messages:
                    save = console.input("[yellow]💾 Save explanations? (y/n): [/yellow]").strip().lower()
                    if save in ['yes', 'y']:
                        title = console.input("[yellow]   Title: [/yellow]").strip()
                        ChatLogger.save_chat("Explain Like X", session_messages, title if title else "Explanations")
                        print_success("Saved!")
                break

            console.print("\n[bold magenta]🎭 Choose a Style or Persona:[/bold magenta]")
            suggestions = random.sample(engine.STYLES, 4)
            console.print(f"[dim]Suggestions: {', '.join(suggestions)}[/dim]")
            console.print("[dim](Or type 'random' for a surprise!)[/dim]")
            
            style = console.input("[bold white]   Style: [/bold white]").strip()
            
            if not style:
                style = "A 5-year-old"
                console.print(f"[italic]Defaulting to: {style}[/italic]")
            
            if style.lower() == 'random':
                style = random.choice(engine.STYLES)
                console.print(f"[bold magenta]🎲 Random Style: {style}[/bold magenta]")

            user_req = f"Explain '{topic}' as '{style}'"
            print_user_msg(user_req)
            session_messages.append({"role": "user", "text": user_req})
            
            with console.status(f"[bold magenta]🎭 {style} is thinking...", spinner="monkey"):
                response = engine.get_explanation(topic, style)
            
            print_bot_msg(response, title=style)
            session_messages.append({"role": "model", "text": response})
            
            console.print("\n[dim]─" * 40 + "[/dim]")
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]👋 Interrupted! Returning to menu...[/yellow]")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")
