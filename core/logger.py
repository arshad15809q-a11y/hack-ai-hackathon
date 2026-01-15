"""
Chat Logger - Utility for saving and loading chat history
"""
import json
import os
import datetime
from typing import List, Dict, Optional
from core.rich_ui import print_success, print_error

class ChatLogger:
    """Handles logging and retrieval of chat sessions."""
    
    HISTORY_FILE = "chat_history.json"
    
    @staticmethod
    def save_chat(module_name: str, messages: List[Dict[str, str]], title: str = None):
        """Save a chat session to the history file."""
        if not messages:
            return

        history = ChatLogger.load_history()
        
        timestamp = datetime.datetime.now().isoformat()
        display_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if not title:
            first_msg = next((m['text'] for m in messages if m['role'] == 'user'), "No Title")
            title = first_msg[:30] + "..." if len(first_msg) > 30 else first_msg
            
        session = {
            "id": timestamp,
            "timestamp": display_time,
            "module": module_name,
            "title": title,
            "messages": messages
        }
        
        history.append(session)
        
        try:
            with open(ChatLogger.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            # print_success(f"Chat saved: '{title}'") # Let the agent confirm
        except Exception as e:
            print_error(f"Error saving chat history: {e}")

    @staticmethod
    def load_history() -> List[Dict]:
        """Load all chat history."""
        if not os.path.exists(ChatLogger.HISTORY_FILE):
            return []
        
        try:
            with open(ChatLogger.HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def clear_history():
        """Clear all chat history."""
        if os.path.exists(ChatLogger.HISTORY_FILE):
            os.remove(ChatLogger.HISTORY_FILE)
            # print_success("Chat history cleared.")
