import json
import os
import re
from pathlib import Path

class KBRepository:
    def __init__(self, kb_path: str = None):
        if kb_path is None:
            # Default to data/knowledge_base.json in project root
            # src/knowledge_base/repository.py -> parent -> parent -> data
            project_root = Path(__file__).resolve().parent.parent.parent
            self.kb_path = project_root / "data" / "knowledge_base.json"
        else:
            self.kb_path = Path(kb_path)
            
        self.patterns = []
        self._load_kb()

    def _load_kb(self):
        try:
            if self.kb_path.exists():
                with open(self.kb_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.patterns = data.get('patterns', [])
            else:
                print(f"Warning: Knowledge base not found at {self.kb_path}")
        except Exception as e:
            print(f"Error loading Knowledge base: {e}")

    def find_match(self, text: str):
        """
        Check the offline knowledge base for a matching resolution.
        Returns the match dictionary if found, else None.
        """
        text_lower = text.lower()
        for entry in self.patterns:
            if re.search(entry['match'], text_lower):
                return {
                    'type': entry['type'],
                    'resolution': entry['resolution'],
                    'confidence': entry.get('confidence', 'MEDIUM'),
                    'source': 'KNOWLEDGE_BASE'
                }
        return None
