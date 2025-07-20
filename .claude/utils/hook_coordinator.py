#!/usr/bin/env python3
"""
Coordinate hook execution to prevent conflicts
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any

class HookCoordinator:
    """Manages hook execution order and prevents conflicts"""
    
    def __init__(self):
        self.execution_log = []
        self.active_hooks = set()
        self.hook_priorities = {
            # Pre-tool-use priorities (lower = higher priority)
            '00-auto-approve-safe-ops.py': 0,
            '01-collab-sync.py': 10,
            '02-design-check.py': 20,
            '05b-prp-context-loader.py': 25,
            '06-requirement-drift-detector.py': 30,
            '14a-creation-guard.py': 40,
            '16a-prp-validator.py': 50,
            
            # Post-tool-use priorities
            'auto-save-gists.py': 100,
            'pattern-extraction.py': 110,
            '10-prp-progress-tracker.py': 120,
        }
    
    def should_run_hook(self, hook_name: str, params: Dict[str, Any]) -> bool:
        """Determine if hook should run based on context"""
        
        # Prevent duplicate runs
        if hook_name in self.active_hooks:
            return False
        
        # Check for conflicts
        if self.has_conflicts(hook_name, params):
            return False
        
        # Special rules for PRP hooks
        if 'prp' in hook_name.lower():
            return self.should_run_prp_hook(hook_name, params)
        
        return True
    
    def has_conflicts(self, hook_name: str, params: Dict[str, Any]) -> bool:
        """Check if hook conflicts with currently running hooks"""
        
        # Design check conflicts with PRP validator
        if hook_name == '02-design-check.py' and '16a-prp-validator.py' in self.active_hooks:
            return True
        
        # Requirement drift conflicts with PRP context loader
        if hook_name == '06-requirement-drift-detector.py' and '05b-prp-context-loader.py' in self.active_hooks:
            # Unless we're working on a PRP
            if not self.is_prp_context(params):
                return True
        
        return False
    
    def should_run_prp_hook(self, hook_name: str, params: Dict[str, Any]) -> bool:
        """Special logic for PRP-related hooks"""
        
        # Only run PRP hooks when working with PRPs
        if not self.is_prp_context(params):
            return False
        
        # Don't run PRP validator on non-code files
        if hook_name == '16a-prp-validator.py':
            path = params.get('path', '')
            if not any(ext in path for ext in ['.py', '.ts', '.tsx', '.js', '.jsx']):
                return False
        
        return True
    
    def is_prp_context(self, params: Dict[str, Any]) -> bool:
        """Check if current context involves PRPs"""
        
        indicators = [
            'PRPs/' in params.get('path', ''),
            'prp' in params.get('command', '').lower(),
            any('prp' in str(v).lower() for v in params.values() if v)
        ]
        
        return any(indicators)
    
    def register_hook_start(self, hook_name: str):
        """Register that a hook is starting"""
        self.active_hooks.add(hook_name)
        self.execution_log.append({
            'hook': hook_name,
            'action': 'start',
            'timestamp': time.time()
        })
    
    def register_hook_end(self, hook_name: str):
        """Register that a hook has completed"""
        self.active_hooks.discard(hook_name)
        self.execution_log.append({
            'hook': hook_name,
            'action': 'end',
            'timestamp': time.time()
        })
    
    def get_execution_order(self, hooks: List[str]) -> List[str]:
        """Get optimal execution order for hooks"""
        
        return sorted(hooks, key=lambda h: self.hook_priorities.get(h, 999))

# Global coordinator instance
coordinator = HookCoordinator()