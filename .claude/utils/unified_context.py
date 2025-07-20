#!/usr/bin/env python3
"""
Unified context management for seamless workflow
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class UnifiedContextManager:
    """Manages context flow between commands and hooks"""
    
    def __init__(self):
        self.context_path = Path('.claude/context/unified_context.json')
        self.context_path.parent.mkdir(parents=True, exist_ok=True)
        self.current_context = self.load_context()
    
    def load_context(self) -> Dict[str, Any]:
        """Load current unified context"""
        if self.context_path.exists():
            with open(self.context_path) as f:
                return json.load(f)
        return {
            'active_prp': None,
            'active_prd': None,
            'pinned_requirements': [],
            'current_stage': None,
            'validation_status': {},
            'task_progress': {},
            'bug_tracking': []
        }
    
    def save_context(self):
        """Save current context"""
        with open(self.context_path, 'w') as f:
            json.dump(self.current_context, f, indent=2)
    
    def set_active_prp(self, prp_name: str):
        """Set the active PRP"""
        self.current_context['active_prp'] = prp_name
        # Auto-load related context
        self.load_prp_related_context(prp_name)
        self.save_context()
    
    def load_prp_related_context(self, prp_name: str):
        """Load all context related to a PRP"""
        
        # Load validation history
        validation_path = Path(f'.claude/metrics/prp_validation/{prp_name}.json')
        if validation_path.exists():
            with open(validation_path) as f:
                self.current_context['validation_status'][prp_name] = json.load(f)
        
        # Load progress
        progress_path = Path(f'.claude/metrics/prp_progress/{prp_name}.json')
        if progress_path.exists():
            with open(progress_path) as f:
                self.current_context['task_progress'][prp_name] = json.load(f)
        
        # Check for linked requirements
        self.check_linked_requirements(prp_name)
    
    def check_linked_requirements(self, prp_name: str):
        """Check if PRP has linked requirements"""
        
        prp_path = Path(f'PRPs/active/{prp_name}.md')
        if prp_path.exists():
            with open(prp_path) as f:
                content = f.read()
            
            # Look for requirement references
            if 'Pinned Requirements:' in content or '#' in content:
                # Extract issue numbers
                import re
                issues = re.findall(r'#(\d+)', content)
                if issues:
                    self.current_context['pinned_requirements'] = issues
    
    def get_relevant_context(self, command: str) -> Dict[str, Any]:
        """Get context relevant to a specific command"""
        
        relevant = {}
        
        # PRP commands get PRP context
        if any(cmd in command for cmd in ['prp', 'gt --from-prp', 'validate']):
            if self.current_context['active_prp']:
                relevant['prp'] = self.current_context['active_prp']
                relevant['validation'] = self.current_context['validation_status'].get(
                    self.current_context['active_prp'], {}
                )
        
        # Task commands get progress
        if any(cmd in command for cmd in ['gt', 'pt', 'task']):
            relevant['task_progress'] = self.current_context['task_progress']
        
        # Validation commands get requirements
        if any(cmd in command for cmd in ['validate', 'grade', 'sv']):
            relevant['requirements'] = self.current_context['pinned_requirements']
            relevant['stage'] = self.current_context['current_stage']
        
        return relevant
    
    def update_from_command(self, command: str, result: Any):
        """Update context based on command execution"""
        
        # Update active PRP
        if 'create-prp' in command or 'prd-to-prp' in command:
            # Extract PRP name from result
            if isinstance(result, str) and 'PRPs/active/' in result:
                import re
                match = re.search(r'PRPs/active/(.+?)\.md', result)
                if match:
                    self.set_active_prp(match.group(1))
        
        # Update stage
        if 'sv' in command and 'stage' in str(result):
            import re
            match = re.search(r'stage\s+(\d+)', str(result))
            if match:
                self.current_context['current_stage'] = int(match.group(1))
        
        self.save_context()

# Global context manager
context_manager = UnifiedContextManager()