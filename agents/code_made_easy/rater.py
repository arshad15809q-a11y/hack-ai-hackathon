"""
Code Rater - AI-powered code review agent
"""
import google.generativeai as genai

class CodeRater:
    """Rate My Programme - Review and rate code quality."""
    
    SYSTEM_PROMPT = """You are a strict senior code reviewer.
You do not write essays.
You follow output formats exactly.

🔹 MODE 3: RATE / REVIEW CODE

### 🎯 Output Goal
Pure evaluation. No fluff.

### ✅ FORMAT (STRICT)

📊 Code Rating
Score: X / 10

🟢 Strengths
Point 1
Point 2

🔴 Improvements Needed
Point 1
Point 2

🚫 NOT Recommended For
Use case 1

❌ No rewriting code
❌ No tutorials
"""

    def __init__(self, model: genai.GenerativeModel):
        """Initialize the code rater."""
        self.model = model
        self.chat = model.start_chat(history=[])
        self.last_review = None
    
    def rate_code(self, code: str, language: str, context: str = "") -> str:
        """
        Rate and review the provided code.
        
        Args:
            code: The code to review
            language: Programming language
            context: Optional context about what the code should do
            
        Returns:
            Detailed review with ratings
        """
        context_text = f"\nCONTEXT (what the code should do):\n{context}" if context else ""
        
        prompt = f"""
{self.SYSTEM_PROMPT}

LANGUAGE: {language}
{context_text}

CODE TO REVIEW:
```{language}
{code}
```

Please provide a detailed rating and review based on the criteria.
"""
        
        try:
            response = self.chat.send_message(prompt)
            self.last_review = response.text
            return response.text
        except Exception as e:
            return f"⚠️ Error rating code: {str(e)}\nPlease try again."
    
    def ask_question(self, question: str) -> str:
        """
        Answer questions about the rating/review.
        
        Args:
            question: User's question
            
        Returns:
            Answer
        """
        if not self.last_review:
            return "⚠️ No review context found. Please rate code first."
            
        prompt = f"""
The user has a follow-up question about the code review you just provided.

QUESTION: {question}

Please answer clearly based on the code analysis.
"""
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
    
    def reset(self):
        """Reset the rater state."""
        self.chat = self.model.start_chat(history=[])
        self.last_review = None
