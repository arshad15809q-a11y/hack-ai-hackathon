"""
Code Generator - AI-powered code generation agent
"""
import google.generativeai as genai

class CodeGenerator:
    """AI Code Generator - Generate code from plain English descriptions."""
    
    SYSTEM_PROMPT = """You are a strict senior code reviewer.
You do not write essays.
You follow output formats exactly.
Code comes first.

🔹 MODE 2: GENERATE CODE

### 🎯 Output Goal
**CODE FIRST. EVERYTHING ELSE OPTIONAL.**

### ✅ FORMAT (ULTRA STRICT)

```python
<CODE ONLY – 80% of response>
```

🧪 Want changes?
Say: "modify"
Say: "optimize"
Say: "add comments"

❌ No explanation unless user asks
❌ Code must dominate response
"""

    TEMPLATES = {
        'web_scraper': 'Create a web scraper that...',
        'file_handler': 'Create a program that reads/writes files...',
        'api_consumer': 'Create code that calls an API...',
        'data_processor': 'Create a program that processes data...',
        'game': 'Create a simple game...',
        'automation': 'Create a script that automates...',
        'calculator': 'Create a calculator that...',
        'converter': 'Create a converter that...',
    }

    def __init__(self, model: genai.GenerativeModel):
        """Initialize the code generator."""
        self.model = model
        self.chat = model.start_chat(history=[])
        self.last_code = None
        self.last_language = None
    
    def _validate_and_format(self, text: str) -> str:
        """Validate and format the generated code output."""
        # Check for code block
        if "```" not in text:
            return "⚠️ Error: The AI failed to generate a code block. Please try again."
        
        # Strip text before first code block (Scenario: Code First)
        # Find index of first ```
        first_block_idx = text.find("```")
        if first_block_idx != -1:
            # Keep the header if it exists, otherwise strip pre-text
            # But the requirement says "Strip any text before code blocks"
            # We'll allow a small buffer or strictly strip.
            # Let's strictly strip to comply with "Code must dominate response"
            return text[first_block_idx:]
            
        return text

    def generate_code(self, description: str, language: str) -> str:
        """
        Generate code from a plain English description.
        
        Args:
            description: What the user wants the code to do
            language: Target programming language
            
        Returns:
            Generated code with explanation
        """
        prompt = f"""
{self.SYSTEM_PROMPT}

TARGET LANGUAGE: {language}

USER'S REQUEST:
{description}

Please generate complete, working code that fulfills this request.
"""
        
        try:
            response = self.chat.send_message(prompt)
            formatted_text = self._validate_and_format(response.text)
            self.last_code = formatted_text
            self.last_language = language
            return formatted_text
        except Exception as e:
            return f"⚠️ Error generating code: {str(e)}\nPlease try again."
    
    def refine_code(self, feedback: str) -> str:
        """
        Refine the last generated code based on user feedback.
        
        Args:
            feedback: User's feedback or additional requirements
            
        Returns:
            Refined code with explanation
        """
        if not self.last_code:
            return "⚠️ No previous code to refine. Please generate code first."
        
        prompt = f"""
The user wants to modify the previously generated code.

USER'S FEEDBACK/REQUEST:
{feedback}

Please update the code based on this feedback.
"""
        
        try:
            response = self.chat.send_message(prompt)
            self.last_code = response.text
            return response.text
        except Exception as e:
            return f"⚠️ Error refining code: {str(e)}\nPlease try again."
    
    def explain_further(self, question: str) -> str:
        """
        Answer questions about the generated code.
        
        Args:
            question: User's question about the code
            
        Returns:
            Explanation
        """
        if not self.last_code:
            return "⚠️ No code to explain. Please generate code first."
        
        prompt = f"""
The user has a question about the code you just generated.

USER'S QUESTION:
{question}

Please answer in a beginner-friendly way with examples if helpful.
"""
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}\nPlease try again."
    
    def reset(self):
        """Reset the generator state."""
        self.chat = self.model.start_chat(history=[])
        self.last_code = None
        self.last_language = None
