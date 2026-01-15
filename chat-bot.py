"""
Multi-Bot CLI Chatbot System
=============================
Entry point for the chatbot application.
"""
import sys
from core.ui import ChatbotMenu

def main():
    """Entry point for the chatbot system."""
    try:
        menu = ChatbotMenu()
        menu.run()
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        print("   Please report this issue.")
        sys.exit(1)

if __name__ == "__main__":
    main()
