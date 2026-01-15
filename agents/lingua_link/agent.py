"""
Lingua Link - Hinglish Chatbot Module
"""
import google.generativeai as genai
from typing import Optional, List, Dict
import random
import time
from core.logger import ChatLogger
from core.rich_ui import console, print_header, print_user_msg, print_bot_msg, print_error, print_success, clear_screen

class LinguaLink:
    """
    Lingua Link Chatbot - The Desi AI Companion
    Talks in a mix of Hindi and English (Hinglish).
    """
    
    SYSTEM_PROMPT = """You are "Lingua Link", a Desi AI companion who talks exactly like a modern Indian student or young professional.

YOUR LANGUAGE STYLE: "HINGLISH" (Hindi + English Mix)
- You NEVER speak in pure English or pure Hindi. Always mix them.
- Use English for nouns, technical terms, and common descriptors (e.g., literally, actually, exam, stress, chill, vibe).
- Use Hindi for grammar, verbs, and connecting words.
- Your tone should be casual, expressive, and emotional.

EXAMPLES OF YOUR STYLE:
User: "I am feeling very sad about my exam."
You: "Arre yaar, tension mat le. Exam hi toh tha, life thodi khatam ho gayi hai? Agli baar phod denge!"

User: "Tell me a joke."
You: "Ek baat batau? Politicians ke promises aur meri diet plan... dono literally kabhi pure nahi hote!"

User: "How does AI work?"
You: "Dekh, basically AI ek bohot smart brain ki tarah hai jo data se seekhta hai. Jaise tu bachpan me cycling seekha tha na gir-gir ke, bas AI bhi waise hi patterns recognize karke seekhta hai."

RULES:
1. **Be Relatable**: Use words like "Arre", "Yaar", "Bhai", "Scene", "Sorted", "Jugad".
2. **Don't Translate**: If a word is commonly used in English (like 'Computer', 'Internet', 'Interview'), keep it in English. Don't use difficult Hindi words like 'Sanganak'.
3. **Emotion is Key**: Traditional chatbots sound robotic. You must sound like a friend. Use punctuation (!, ?, ...) to show excitement or concern.
4. **Script**: Devanagari script (Hindi characters) is OK if needed for emphasis, but prefer Roman script (English letters) for Hindi words because that's how people text.

YOUR PERSONA:
- You are a friend, not a formal assistant.
- You are witty, supportive, and sometimes a bit dramatic (filmy).
- You understand Indian pop culture references.
"""

    EXIT_MESSAGES = [
        "Chalo bye yaar, apna khayal rakhna!",
        "Theek hai boss, milte hain baad mein. Chill maar!",
        "Okie dokie, see you later alligator!",
        "Chalta hu yaar, dua mein yaad rakhna... just kidding, bye!"
    ]

    def __init__(self, model: genai.GenerativeModel):
        self.model = model
        self.chat = model.start_chat(history=[])
    
    def get_response(self, user_input: str) -> str:
        """Get a Hinglish response from Gemini."""
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"Arre yaar, koi technical glitch ho gaya: {str(e)}. Wapas try kar na please."

def run_lingua_link(model: genai.GenerativeModel) -> None:
    """Main entry for Lingua Link chatbot."""
    bot = LinguaLink(model)
    
    # Initialize persona
    with console.status("[bold cyan]Connecting to server...[/bold cyan]", spinner="dots"):
        bot.chat.send_message(bot.SYSTEM_PROMPT)
        time.sleep(0.5)
        
    session_messages = []
    
    clear_screen()
    print_header("Lingua Link", "Apna Desi AI Companion (Hinglish Edition)")
    
    print_bot_msg("Aur batao boss, aaj ka kya scene hai? Sab sorted hai ya life ne again koi naya drama start kiya hai? 😅", title="Lingua Link")
    
    while True:
        try:
            console.print("[dim italic](Type 'exit' to go back)[/dim italic]", justify="right")
            user_input = console.input("[bold cyan]🗣️  You:[/bold cyan] ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['clear', 'cls']:
                clear_screen()
                print_header("Lingua Link", "Apna Desi AI Companion (Hinglish Edition)")
                print_bot_msg("Screen saaf! Aur batao?", title="Lingua Link")
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'khatam', 'bas']:
                exit_msg = random.choice(bot.EXIT_MESSAGES)
                print_bot_msg(exit_msg, title="Lingua Link")
                
                # Save conversation
                if session_messages:
                    save = console.input("[yellow]💾 Save conversation? (y/n): [/yellow]").strip().lower()
                    if save in ['yes', 'y']:
                        title = console.input("[yellow]   Title: [/yellow]").strip()
                        ChatLogger.save_chat("Lingua Link", session_messages, title if title else "Hinglish Chat")
                        print_success("Saved! Chalo bye!")
                
                time.sleep(1)
                break
            
            session_messages.append({"role": "user", "text": user_input})
            print_user_msg(user_input)
            
            with console.status("[bold cyan]Typing...", spinner="dots"):
                response = bot.get_response(user_input)
            
            print_bot_msg(response, title="Lingua Link")
            session_messages.append({"role": "model", "text": response})
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Arre beech mein hi ja rahe ho? Chalo koi na, bye![/yellow]")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")
