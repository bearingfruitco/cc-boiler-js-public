"""
PRP Merge Strategy
Strategies for merging old and new PRP content
"""

import re
from typing import Dict, List, Optional


class PRPMergeStrategy:
    """Handles merging of old and new PRP content"""
    
    def __init__(self):
        self.strategies = {
            'preserve_progress': self.merge_preserve_progress,
            'architecture_priority': self.merge_architecture_priority,
            'interactive': self.merge_interactive
        }
        
    def merge_preserve_progress(self, old_prp: str, new_prp: str, 
                                progress: Dict) -> str:
        """Merge strategy that preserves all progress"""
        merged = new_prp
        
        # Restore checkbox states
        merged = self._restore_checkboxes(merged, progress)
        
        # Restore implementation notes
        merged = self._restore_implementation_notes(merged, progress)
        
        # Restore custom sections
        merged = self._restore_custom_sections(merged, progress)
        
        # Add progress preservation marker
        if '**Progress Preserved**' not in merged:
            merged = self._add_preservation_marker(merged, progress)
        
        return merged
    
    def merge_architecture_priority(self, old_prp: str, new_prp: str,
                                  progress: Dict) -> str:
        """Merge strategy that prioritizes architecture updates"""
        # Start with new PRP
        merged = new_prp
        
        # Only restore completed checkboxes
        completed_only_progress = {
            'checkboxes': [cb for cb in progress['checkboxes'] 
                          if cb['state'] == 'completed']
        }
        merged = self._restore_checkboxes(merged, completed_only_progress)
        
        # Add notes about what was not preserved
        deprecation_notes = self._identify_deprecated_tasks(old_prp, new_prp, progress)
        if deprecation_notes:
            merged = self._add_deprecation_section(merged, deprecation_notes)
        
        return merged
    
    def merge_interactive(self, old_prp: str, new_prp: str,
                         progress: Dict) -> str:
        """Interactive merge strategy (placeholder for future implementation)"""
        # For now, default to preserve_progress
        return self.merge_preserve_progress(old_prp, new_prp, progress)
    
    def _restore_checkboxes(self, content: str, progress: Dict) -> str:
        """Restore checkbox states from progress"""
        if 'checkboxes' not in progress:
            return content
            
        lines = content.split('\n')
        modified = False
        
        for checkbox in progress['checkboxes']:
            if checkbox['state'] == 'completed':
                task_text = checkbox['task']
                
                # Find and update the checkbox
                for i, line in enumerate(lines):
                    # Match unchecked checkbox with same task text
                    if re.match(r'^\s*- \[ \]', line) and task_text in line:
                        # Replace with checked version
                        lines[i] = line.replace('- [ ]', '- [x]', 1)
                        modified = True
                        break
        
        return '\n'.join(lines) if modified else content
    
    def _restore_implementation_notes(self, content: str, progress: Dict) -> str:
        """Restore implementation notes sections"""
        if 'implementation_notes' not in progress or not progress['implementation_notes']:
            return content
            
        # Find implementation notes section
        impl_pattern = r'(###?\s*Implementation Notes)\s*\n(.*?)(?=\n##|\n###|\Z)'
        
        for note_data in progress['implementation_notes']:
            note_content = note_data['content']
            
            # Check if section exists
            match = re.search(impl_pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                # Replace with preserved content
                replacement = f"{match.group(1)}\n\n{note_content}\n"
                content = content[:match.start()] + replacement + content[match.end():]
            else:
                # Add section if it doesn't exist
                # Find a good place to insert (before validation loops or at end)
                insert_pattern = r'(\n##\s*Validation Loops)'
                insert_match = re.search(insert_pattern, content)
                
                if insert_match:
                    insert_pos = insert_match.start()
                    new_section = f"\n\n### Implementation Notes\n\n{note_content}\n"
                    content = content[:insert_pos] + new_section + content[insert_pos:]
                else:
                    # Append at end
                    content += f"\n\n### Implementation Notes\n\n{note_content}\n"
        
        return content
    
    def _restore_custom_sections(self, content: str, progress: Dict) -> str:
        """Restore custom sections"""
        if 'custom_sections' not in progress:
            return content
            
        for section in progress['custom_sections']:
            section_name = section['name']
            section_content = section['content']
            
            if section.get('auto_preserved'):
                # These are sections like "Lessons Learned" that should be preserved
                # Check if section exists in new content
                section_pattern = rf'##?\s*{re.escape(section_name)}(.*?)(?=\n##|\Z)'
                if not re.search(section_pattern, content, re.DOTALL | re.IGNORECASE):
                    # Add it back
                    content += f"\n\n## {section_name}\n\n{section_content}\n"
            else:
                # Explicitly marked custom sections
                marker = f"<!-- CUSTOM: {section_name} -->"
                end_marker = "<!-- END CUSTOM -->"
                
                if marker not in content:
                    # Add at end of document
                    content += f"\n\n{marker}\n{section_content}\n{end_marker}\n"
        
        return content
    
    def _add_preservation_marker(self, content: str, progress: Dict) -> str:
        """Add marker showing progress was preserved"""
        completion = progress.get('completion', {})
        
        # Find the change header
        header_match = re.search(r'(> ⚠️ .*?)\n\n', content, re.DOTALL)
        if header_match:
            # Add preservation info to header
            header = header_match.group(1)
            if '**Progress Preserved**' not in header:
                header += f"\n> **Progress Preserved**: ✅ {completion.get('completed_tasks', 0)} completed tasks retained"
                content = content.replace(header_match.group(0), header + '\n\n')
        
        return content
    
    def _identify_deprecated_tasks(self, old_prp: str, new_prp: str,
                                  progress: Dict) -> List[Dict]:
        """Identify tasks that were removed in new PRP"""
        deprecated = []
        
        # Extract all tasks from old PRP
        old_tasks = self._extract_all_tasks(old_prp)
        new_tasks = self._extract_all_tasks(new_prp)
        
        # Find tasks that were in old but not in new
        for old_task in old_tasks:
            if not any(self._tasks_match(old_task, new_task) for new_task in new_tasks):
                # This task was removed
                # Check if it was completed
                was_completed = any(
                    cb['task'] == old_task['task'] and cb['state'] == 'completed'
                    for cb in progress.get('checkboxes', [])
                )
                
                deprecated.append({
                    'task': old_task['task'],
                    'was_completed': was_completed,
                    'phase': old_task.get('phase', 'Unknown')
                })
        
        return deprecated
    
    def _extract_all_tasks(self, content: str) -> List[Dict]:
        """Extract all checkbox tasks from PRP content"""
        tasks = []
        lines = content.split('\n')
        current_phase = None
        
        for i, line in enumerate(lines):
            # Track current phase
            if 'Phase' in line and line.startswith('#'):
                phase_match = re.search(r'Phase\s+(\d+)', line)
                if phase_match:
                    current_phase = f"Phase {phase_match.group(1)}"
            
            # Extract checkbox
            checkbox_match = re.match(r'^\s*- \[([ x])\] (.+?)$', line)
            if checkbox_match:
                tasks.append({
                    'state': checkbox_match.group(1),
                    'task': checkbox_match.group(2),
                    'phase': current_phase,
                    'line': i
                })
        
        return tasks
    
    def _tasks_match(self, task1: Dict, task2: Dict) -> bool:
        """Check if two tasks are the same"""
        # Simple text matching for now
        # Could be enhanced with fuzzy matching
        return task1['task'].strip().lower() == task2['task'].strip().lower()
    
    def _add_deprecation_section(self, content: str, deprecated_tasks: List[Dict]) -> str:
        """Add section documenting deprecated tasks"""
        if not deprecated_tasks:
            return content
            
        deprecation_section = "\n\n## Deprecated Tasks\n\n"
        deprecation_section += "The following tasks were removed in the architecture update:\n\n"
        
        for task in deprecated_tasks:
            status = "✅ Completed" if task['was_completed'] else "❌ Not completed"
            deprecation_section += f"- {status} - {task['task']} (from {task['phase']})\n"
        
        # Insert before validation loops or at end
        insert_pattern = r'(\n##\s*Validation Loops)'
        match = re.search(insert_pattern, content)
        
        if match:
            insert_pos = match.start()
            content = content[:insert_pos] + deprecation_section + content[insert_pos:]
        else:
            content += deprecation_section
        
        return content
