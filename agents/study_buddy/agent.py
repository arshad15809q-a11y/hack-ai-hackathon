"""
Study Buddy - Academic & Career Guidance Chatbot Module
"""
import google.generativeai as genai
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from core.logger import ChatLogger
from core.rich_ui import console, print_header, print_user_msg, print_bot_msg, print_error, print_success, clear_screen, print_menu
import time

class StudyBuddyFeature(Enum):
    """Features available in Study Buddy."""
    SUBJECT_GUIDE = auto()
    CAREER_PATH = auto()
    INTERNSHIP_FINDER = auto()
    INTERVIEW_PREP = auto()
    GENERAL_CHAT = auto()

@dataclass
class SessionContext:
    """Maintains conversation context throughout the session."""
    branch: Optional[str] = None
    semester: Optional[int] = None
    year: Optional[int] = None
    target_role: Optional[str] = None
    experience_level: str = "fresher"
    conversation_history: list = field(default_factory=list)
    current_feature: Optional[StudyBuddyFeature] = None
    
    def to_context_string(self) -> str:
        parts = []
        if self.branch: parts.append(f"Branch/Department: {self.branch}")
        if self.semester: parts.append(f"Semester: {self.semester}")
        if self.year: parts.append(f"Year: {self.year}")
        if self.target_role: parts.append(f"Target Role: {self.target_role}")
        if self.experience_level: parts.append(f"Experience Level: {self.experience_level}")
        return "\n".join(parts) if parts else "No context set yet."
    
    def reset(self):
        self.branch = None
        self.semester = None
        self.year = None
        self.target_role = None
        self.experience_level = "fresher"
        self.conversation_history = []
        self.current_feature = None

class StudyBuddy:
    # System prompt that defines the chatbot's personality and behavior
    SYSTEM_PROMPT = """You are a senior college mentor.
Your job is to guide students clearly and concisely.
Do NOT write essays.
Do NOT overexplain.
Structure every answer using headings and bullet points.
Be practical, not theoretical.

All Study Buddy responses MUST follow these global rules:
🔒 Global Output Rules
❌ No essays
❌ No paragraphs longer than 3 lines
❌ No generic motivational talk
✅ Max response length: 250–300 words
✅ Use headings + bullet points
✅ Every answer must feel like actionable guidance

📐 RESPONSE FORMAT (STRICT)
Every response must follow THIS TEMPLATE ONLY:

🎯 Summary (1–2 lines)

📚 Key Points
- Bullet 1
- Bullet 2
- Bullet 3

🛠️ What You Should Do Next
1. Step one
2. Step two
3. Step three

⚠️ Common Mistakes (optional, max 2 bullets)

❌ You must NOT invent new sections
❌ You must NOT add explanations outside this structure
"""

    def __init__(self, model: genai.GenerativeModel):
        self.model = model
        self.context = SessionContext()
        self.chat = None
        self._initialize_chat()
    
    def _initialize_chat(self):
        self.chat = self.model.start_chat(history=[])
    
    def _detect_feature(self, user_input: str) -> StudyBuddyFeature:
        input_lower = user_input.lower()
        subject_keywords = ['subject', 'syllabus', 'semester', 'sem', 'study', 'course', 'curriculum', 'book', 'resource', 'learn', 'topic']
        career_keywords = ['career', 'job', 'future', 'role', 'position', 'path', 'higher studies', 'mba', 'mtech', 'masters', 'phd', 'startup', 'freelance', 'what can i do', 'after graduation', 'scope']
        internship_keywords = ['internship', 'intern', 'opportunity', 'apply', 'platform', 'experience', 'where to apply', 'hiring', 'openings']
        interview_keywords = ['interview', 'prepare', 'question', 'hr', 'technical', 'placement', 'selection', 'hiring process', 'crack']
        
        if any(kw in input_lower for kw in interview_keywords): return StudyBuddyFeature.INTERVIEW_PREP
        elif any(kw in input_lower for kw in internship_keywords): return StudyBuddyFeature.INTERNSHIP_FINDER
        elif any(kw in input_lower for kw in career_keywords): return StudyBuddyFeature.CAREER_PATH
        elif any(kw in input_lower for kw in subject_keywords): return StudyBuddyFeature.SUBJECT_GUIDE
        else: return StudyBuddyFeature.GENERAL_CHAT
    
    def _build_prompt(self, user_input: str, feature: StudyBuddyFeature) -> str:
        context_str = self.context.to_context_string()
        base_prompt = f"STUDENT CONTEXT:\n{context_str}\n\nSTUDENT'S QUESTION/REQUEST:\n{user_input}\n"
        feature_instructions = {
            StudyBuddyFeature.SUBJECT_GUIDE: "\nTASK: Provide subject/syllabus guidance.\n🧩 FEATURE-SPECIFIC CONTROLS:\n- Only subject names\n- 1-line description per subject\n- Max 6 subjects\n",
            StudyBuddyFeature.CAREER_PATH: "\nTASK: Provide career guidance.\n🧩 FEATURE-SPECIFIC CONTROLS:\n- Max 4 career roles\n- Each role: Skills (comma-separated), One-line description\n",
            StudyBuddyFeature.INTERNSHIP_FINDER: "\nTASK: Guide on internships and opportunities.\n🧩 FEATURE-SPECIFIC CONTROLS:\n- Platform names ONLY (no links)\n- Skills list\n- 1-line eligibility hint\n",
            StudyBuddyFeature.INTERVIEW_PREP: "\nTASK: Help with interview preparation.\n🧩 FEATURE-SPECIFIC CONTROLS:\n- Max 5 questions\n- Categorized: HR, Technical\n- No long answers, only what interviewer expects\n",
            StudyBuddyFeature.GENERAL_CHAT: "\nTASK: General academic/career guidance.\n- Be helpful and conversational\n- Keep it structured using the standard template\n"
        }
        return base_prompt + feature_instructions.get(feature, "")
    
    def _extract_context_from_input(self, user_input: str):
        input_lower = user_input.lower()
        branches = {
            'cse': 'Computer Science Engineering (CSE)', 'cs': 'Computer Science Engineering (CSE)', 'computer science': 'Computer Science Engineering (CSE)',
            'it': 'Information Technology (IT)', 'information technology': 'Information Technology (IT)',
            'ece': 'Electronics & Communication Engineering (ECE)', 'electronics': 'Electronics & Communication Engineering (ECE)',
            'eee': 'Electrical & Electronics Engineering (EEE)', 'electrical': 'Electrical & Electronics Engineering (EEE)',
            'me': 'Mechanical Engineering (ME)', 'mechanical': 'Mechanical Engineering (ME)',
            'civil': 'Civil Engineering', 'ce': 'Civil Engineering',
            'data science': 'Data Science', 'ds': 'Data Science', 'aiml': 'AI & Machine Learning', 'ai': 'Artificial Intelligence',
            'machine learning': 'AI & Machine Learning', 'biotech': 'Biotechnology', 'chemical': 'Chemical Engineering',
        }
        for key, value in branches.items():
            if key in input_lower:
                self.context.branch = value
                break
        
        import re
        sem_match = re.search(r'(\d+)(?:st|nd|rd|th)?\s*(?:sem|semester)', input_lower)
        if sem_match: self.context.semester = int(sem_match.group(1))
        
        year_match = re.search(r'(\d+)(?:st|nd|rd|th)?\s*year', input_lower)
        if year_match:
            self.context.year = int(year_match.group(1))
            if not self.context.semester: self.context.semester = (self.context.year - 1) * 2 + 1
    
    def _format_response(self, text: str) -> str:
        text = text.strip()
        import re
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text

    def get_response(self, user_input: str) -> str:
        self._extract_context_from_input(user_input)
        feature = self._detect_feature(user_input)
        self.context.current_feature = feature
        prompt = self._build_prompt(user_input, feature)
        
        try:
            full_prompt = f"{self.SYSTEM_PROMPT}\n\n{prompt}"
            response = self.chat.send_message(full_prompt)
            formatted_response = self._format_response(response.text)
            self.context.conversation_history.append({'user': user_input, 'assistant': formatted_response, 'feature': feature.name})
            return formatted_response
        except Exception as e:
            return f"⚠️ Sorry, I encountered an error: {str(e)}\nPlease try again."
    
    def get_status(self) -> str:
        return f"Branch: {self.context.branch or 'Not set'}\nSemester: {self.context.semester or 'Not set'}\nTarget Role: {self.context.target_role or 'Not set'}"
    
    def reset_session(self) -> str:
        self.context.reset()
        self._initialize_chat()
        return "Session reset! Let's start fresh."

def run_study_buddy(model: genai.GenerativeModel) -> None:
    buddy = StudyBuddy(model)
    session_messages = []
    
    clear_screen()
    print_header("Study Buddy", "Your AI Senior Mentor")
    console.print("[dim]Subject Guide • Career Path • Internships • Interview Prep[/dim]\n", justify="center")
    
    print_bot_msg("Hey! I'm your Study Buddy. Think of me as that helpful senior who's been through it all.\n\nTell me: **What's your branch and semester?**", title="Senior Mentor")
    
    while True:
        try:
            user_input = console.input("\n[bold cyan]🎓 You:[/bold cyan] ").strip()
            
            if not user_input:
                continue
            
            command = user_input.lower()
            
            if command in ['clear', 'cls']:
                clear_screen()
                print_header("Study Buddy", "Your AI Senior Mentor")
                print_bot_msg(buddy.get_status(), title="Profile Status")
                continue

            if command == 'exit':
                console.print("\n")
                console.rule("[bold blue]Session Ended[/bold blue]")
                
                chat_msgs = [m for m in session_messages if m['text'] not in ['help', 'status', 'reset', 'exit']]
                if chat_msgs:
                    save = console.input("[yellow]💾 Save conversation? (y/n): [/yellow]").strip().lower()
                    if save in ['yes', 'y']:
                        title = console.input("[yellow]   Title: [/yellow]").strip()
                        ChatLogger.save_chat("Study Buddy", chat_msgs, title if title else "Study Session")
                        print_success("Conversation saved!")
                
                break
            
            elif command == 'status':
                print_bot_msg(buddy.get_status(), title="Profile Status")
                continue
            
            elif command == 'reset':
                print_success(buddy.reset_session())
                continue
            
            if command not in ['help', 'status', 'reset']:
                session_messages.append({"role": "user", "text": user_input})
            
            print_user_msg(user_input)
            
            with console.status("[bold green]Thinking...", spinner="dots"):
                response = buddy.get_response(user_input)
            
            print_bot_msg(response, title="Senior Mentor")
            
            if command not in ['help', 'status', 'reset']:
                session_messages.append({"role": "model", "text": response})
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠️ Interrupted! Returning to menu...[/yellow]")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")
