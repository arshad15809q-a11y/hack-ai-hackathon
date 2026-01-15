"""
Code Debugger - AI-powered debugging agent
"""
import google.generativeai as genai
from .storage import BugStorage

class CodeDebugger:
    """AI Code Debugger - Find and fix bugs in beginner-friendly language."""
    
    SYSTEM_PROMPT = """You are a strict senior code reviewer.
You do not write essays.
You follow output formats exactly.
If the task is code-related, code comes first.

🔹 MODE 1: DEBUG CODE
🎯 Output Goal
Help the user fix code fast, not teach theory.

✅ FORMAT (STRICT)
❌ Errors Found
1. Error type – short reason
2. Error type – short reason

🛠️ Fixes
- Fix 1
- Fix 2

✅ Corrected Code
```language
<ONLY CODE HERE>
```

❌ No long explanations
❌ No theory
❌ No motivational text
"""

    def __init__(self, model: genai.GenerativeModel, storage: BugStorage):
        """Initialize the debugger."""
        self.model = model
        self.storage = storage
        self.chat = model.start_chat(history=[])
    
    def debug_code(self, code: str, language: str) -> str:
        """
        Debug the provided code and return analysis.
        
        Args:
            code: The code to debug
            language: Programming language
            
        Returns:
            Analysis and fixes as formatted string
        """
        prompt = f"""
{self.SYSTEM_PROMPT}

LANGUAGE: {language}

USER'S CODE TO DEBUG:
```{language}
{code}
```

Please analyze this code thoroughly and help the user understand and fix any issues.
"""
        
        try:
            response = self.chat.send_message(prompt)
            analysis = response.text
            
            # Save to bug history
            self.storage.add_bugs_from_analysis(language, analysis)
            
            return analysis
        except Exception as e:
            return f"⚠️ Error analyzing code: {str(e)}\nPlease try again."
