"""
PRP Progress Tracker
Tracks and preserves PRP implementation progress
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRPProgressTracker:
    """Tracks and saves PRP implementation progress"""
    
    def __init__(self, tracking_file: str = ".claude/prp-progress.json",
                 project_root: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.project_root = Path(project_root)
        self.tracking_file = self.project_root / tracking_file
        self.progress_data = self.load_progress()
        
    def load_progress(self) -> Dict:
        """Load existing progress data"""
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_progress_data(self):
        """Save progress data to file"""
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tracking_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)
    
    def extract_progress(self, prp_file: Path) -> Dict:
        """Extract completion progress from PRP"""
        if not prp_file.exists():
            return {}
            
        with open(prp_file, 'r') as f:
            content = f.read()
            
        progress = {
            'file': str(prp_file),
            'timestamp': datetime.now().isoformat(),
            'completion': {
                'total_tasks': 0,
                'completed_tasks': 0,
                'in_progress_tasks': 0,
                'percentage': 0
            },
            'checkboxes': [],
            'implementation_notes': [],
            'custom_sections': [],
            'phases': {}
        }
        
        # Extract checkbox states with context
        checkbox_pattern = r'^(\s*)- \[([ x])\] (.+?)$'
        current_phase = None
        phase_indent = 0
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Check for phase headers
            if line.startswith('### Phase') or line.startswith('## Phase'):
                phase_match = re.search(r'Phase\s+(\d+)', line)
                if phase_match:
                    current_phase = f"Phase {phase_match.group(1)}"
                    phase_indent = 0
                    if current_phase not in progress['phases']:
                        progress['phases'][current_phase] = {
                            'total': 0,
                            'completed': 0,
                            'tasks': []
                        }
            
            # Extract checkboxes
            match = re.match(checkbox_pattern, line)
            if match:
                indent = len(match.group(1))
                state = match.group(2)
                task = match.group(3)
                
                checkbox_info = {
                    'state': 'completed' if state == 'x' else 'pending',
                    'task': task,
                    'line_number': i + 1,
                    'indent': indent,
                    'phase': current_phase,
                    'context': self._get_context(lines, i)
                }
                
                progress['checkboxes'].append(checkbox_info)
                progress['completion']['total_tasks'] += 1
                
                if state == 'x':
                    progress['completion']['completed_tasks'] += 1
                    
                # Track phase progress
                if current_phase and current_phase in progress['phases']:
                    progress['phases'][current_phase]['total'] += 1
                    progress['phases'][current_phase]['tasks'].append(checkbox_info)
                    if state == 'x':
                        progress['phases'][current_phase]['completed'] += 1
        
        # Calculate completion percentage
        if progress['completion']['total_tasks'] > 0:
            progress['completion']['percentage'] = round(
                (progress['completion']['completed_tasks'] / 
                 progress['completion']['total_tasks']) * 100, 1
            )
        
        # Extract implementation notes
        progress['implementation_notes'] = self._extract_implementation_notes(content)
        
        # Extract custom sections
        progress['custom_sections'] = self._extract_custom_sections(content)
        
        return progress
    
    def _get_context(self, lines: List[str], index: int) -> str:
        """Get the context (parent heading) for a checkbox"""
        # Look backwards for the nearest heading
        for i in range(index - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith('#') and not line.startswith('####'):
                # Found a heading
                return line.lstrip('#').strip()
        return ""
    
    def _extract_implementation_notes(self, content: str) -> List[Dict]:
        """Extract implementation notes sections"""
        notes = []
        
        # Pattern for implementation notes sections
        impl_pattern = r'###?\s*Implementation Notes(.*?)(?=\n##|\n###|\Z)'
        matches = re.finditer(impl_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            note_content = match.group(1).strip()
            if note_content:
                notes.append({
                    'content': note_content,
                    'position': match.start()
                })
        
        # Also look for inline notes marked with NOTE: or TODO:
        inline_pattern = r'(?:NOTE|TODO):\s*(.+?)(?:\n|$)'
        for match in re.finditer(inline_pattern, content):
            notes.append({
                'content': match.group(1),
                'type': 'inline',
                'position': match.start()
            })
        
        return notes
    
    def _extract_custom_sections(self, content: str) -> List[Dict]:
        """Extract custom sections marked for preservation"""
        custom_sections = []
        
        # Look for explicitly marked custom sections
        custom_pattern = r'<!-- CUSTOM:\s*(.*?)\s*-->(.*?)<!-- END CUSTOM -->'
        matches = re.finditer(custom_pattern, content, re.DOTALL)
        
        for match in matches:
            custom_sections.append({
                'name': match.group(1).strip(),
                'content': match.group(2).strip(),
                'position': match.start()
            })
        
        # Also preserve certain sections by default
        preserve_patterns = [
            (r'##?\s*Lessons Learned(.*?)(?=\n##|\Z)', 'Lessons Learned'),
            (r'##?\s*Known Issues(.*?)(?=\n##|\Z)', 'Known Issues'),
            (r'##?\s*Gotchas(.*?)(?=\n##|\Z)', 'Gotchas'),
            (r'##?\s*Performance Notes(.*?)(?=\n##|\Z)', 'Performance Notes')
        ]
        
        for pattern, name in preserve_patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                custom_sections.append({
                    'name': name,
                    'content': match.group(1).strip(),
                    'position': match.start(),
                    'auto_preserved': True
                })
        
        return custom_sections
    
    def save_progress(self, prp_file: Path) -> Dict:
        """Save current progress before regeneration"""
        progress = self.extract_progress(prp_file)
        
        # Create backup of current state
        backup_key = f"{str(prp_file)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        progress['backup_key'] = backup_key
        
        # Store in tracking file
        self.progress_data[str(prp_file)] = progress
        self.progress_data[f"backups/{backup_key}"] = progress
        
        self.save_progress_data()
        
        return progress
    
    def restore_progress(self, prp_file: Path, backup_key: Optional[str] = None) -> Optional[Dict]:
        """Restore progress from a backup"""
        if backup_key:
            return self.progress_data.get(f"backups/{backup_key}")
        else:
            return self.progress_data.get(str(prp_file))
    
    def get_progress_summary(self, prp_file: Path) -> Dict:
        """Get a summary of progress for a PRP"""
        progress = self.extract_progress(prp_file)
        
        summary = {
            'file': str(prp_file.name),
            'completion_percentage': progress['completion']['percentage'],
            'tasks': f"{progress['completion']['completed_tasks']}/{progress['completion']['total_tasks']}",
            'has_notes': len(progress['implementation_notes']) > 0,
            'has_custom_sections': len(progress['custom_sections']) > 0,
            'phases': {}
        }
        
        # Add phase summaries
        for phase, data in progress['phases'].items():
            if data['total'] > 0:
                summary['phases'][phase] = {
                    'completion': f"{data['completed']}/{data['total']}",
                    'percentage': round((data['completed'] / data['total']) * 100, 1)
                }
        
        return summary
    
    def get_all_prp_progress(self) -> List[Dict]:
        """Get progress summary for all tracked PRPs"""
        summaries = []
        prp_dir = self.project_root / "PRPs" / "active"
        
        if prp_dir.exists():
            for prp_file in prp_dir.glob("*.md"):
                if not prp_file.stem.startswith('_'):
                    summary = self.get_progress_summary(prp_file)
                    summaries.append(summary)
        
        # Sort by completion percentage
        summaries.sort(key=lambda x: x['completion_percentage'], reverse=True)
        
        return summaries
