"""
Bug Storage - Persistence layer for Code Made Easy
"""
import json
import os
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class BugRecord:
    """Represents a single bug/mistake record."""
    date: str
    language: str
    error_type: str
    mistake: str
    wrong_code: str
    correct_code: str
    explanation: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            'date': self.date,
            'language': self.language,
            'error_type': self.error_type,
            'mistake': self.mistake,
            'wrong_code': self.wrong_code,
            'correct_code': self.correct_code,
            'explanation': self.explanation
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BugRecord':
        """Create from dictionary."""
        return cls(
            date=data.get('date', ''),
            language=data.get('language', ''),
            error_type=data.get('error_type', ''),
            mistake=data.get('mistake', ''),
            wrong_code=data.get('wrong_code', ''),
            correct_code=data.get('correct_code', ''),
            explanation=data.get('explanation', '')
        )
    
    def display(self) -> str:
        """Format bug record for display."""
        return f"""
┌─────────────────────────────────────────────────────────────────┐
│ 📅 Date: {self.date:<54}│
│ 💻 Language: {self.language:<51}│
│ ⚠️ Error Type: {self.error_type:<49}│
├─────────────────────────────────────────────────────────────────┤
│ ❌ Mistake: {self.mistake[:52]:<52}│
├─────────────────────────────────────────────────────────────────┤
│ Wrong Code:                                                     │
│ {self.wrong_code[:60]:<62}│
├─────────────────────────────────────────────────────────────────┤
│ Correct Code:                                                   │
│ {self.correct_code[:60]:<62}│
├─────────────────────────────────────────────────────────────────┤
│ 💡 Explanation:                                                 │
│ {self.explanation[:60]:<62}│
└─────────────────────────────────────────────────────────────────┘
"""

class BugStorage:
    """Handles saving andloading bug records."""
    
    def __init__(self, storage_file: str = "bug_history.json"):
        """Initialize bug storage."""
        self.storage_file = storage_file
        self.bugs: List[BugRecord] = []
        self._load()
    
    def _load(self):
        """Load bugs from storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.bugs = [BugRecord.from_dict(b) for b in data]
            except (json.JSONDecodeError, KeyError):
                self.bugs = []
    
    def _save(self):
        """Save bugs to storage file."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in self.bugs], f, indent=2)
    
    def add_bug(self, bug: BugRecord):
        """Add a new bug record."""
        self.bugs.append(bug)
        self._save()
    
    def add_bugs_from_analysis(self, language: str, analysis_text: str):
        """Parse analysis text and extract bugs to save."""
        # This is a simplified parser - bugs are saved when explicitly parsed
        date = datetime.now().strftime("%d-%m-%Y")
        
        # We'll save a summary record for the debugging session
        bug = BugRecord(
            date=date,
            language=language,
            error_type="Mixed/Multiple",
            mistake="See full analysis",
            wrong_code="See full analysis",
            correct_code="See full analysis", 
            explanation=analysis_text[:500] + "..." if len(analysis_text) > 500 else analysis_text
        )
        self.add_bug(bug)
    
    def get_all_bugs(self) -> List[BugRecord]:
        """Get all bug records."""
        return self.bugs
    
    def get_bugs_by_language(self, language: str) -> List[BugRecord]:
        """Get bugs filtered by language."""
        return [b for b in self.bugs if b.language.lower() == language.lower()]
    
    def get_bugs_by_error_type(self, error_type: str) -> List[BugRecord]:
        """Get bugs filtered by error type."""
        return [b for b in self.bugs if error_type.lower() in b.error_type.lower()]
    
    def get_summary(self) -> Dict[str, int]:
        """Get summary of bugs by language and type."""
        summary = {
            'total': len(self.bugs),
            'by_language': {},
            'by_error_type': {}
        }
        for bug in self.bugs:
            lang = bug.language
            err_type = bug.error_type
            summary['by_language'][lang] = summary['by_language'].get(lang, 0) + 1
            summary['by_error_type'][err_type] = summary['by_error_type'].get(err_type, 0) + 1
        return summary
    
    def clear_history(self):
        """Clear all bug history."""
        self.bugs = []
        self._save()
