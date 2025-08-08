#!/usr/bin/env python3
"""
PRP Regeneration Hook
Detects architecture changes and regenerates affected PRPs
"""

import sys
import json
import os
from pathlib import Path
from typing import List, Dict

# Add project root to path
sys.path.insert(0, os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate'))

from lib.prp.architecture_mapper import ArchitecturePRPMapper
from lib.prp.prp_regenerator import PRPRegenerator
from lib.architecture.change_detector import ArchitectureChangeDetector


def main():
    """Main hook entry point"""
    try:
        # Get hook input
        input_data = json.loads(sys.stdin.read())
        
        # Check if this is a command execution
        tool_name = input_data.get('tool_name')
        if tool_name != 'RunCommand':
            return 0
            
        # Get command
        tool_input = input_data.get('tool_input', {})
        command = tool_input.get('command', '')
        
        # Trigger on architecture validation or explicit sync
        if not ('/validate-architecture' in command or '/prp-sync' in command):
            return 0
        
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate')
        
        # Detect architecture changes
        detector = ArchitectureChangeDetector(project_dir)
        arch_changes = detector.get_recent_changes()
        
        if not arch_changes:
            # No architecture changes detected
            if '/prp-sync' in command:
                print(json.dumps({
                    "continue": True,
                    "feedback": "✅ No architecture changes detected. PRPs are up to date."
                }))
            return 0
        
        # Map changes to affected PRPs
        mapper = ArchitecturePRPMapper(project_dir)
        affected_prps = []
        
        for change in arch_changes:
            affected = mapper.analyze_architecture_change(
                change['file'],
                change
            )
            affected_prps.extend(affected)
        
        if not affected_prps:
            if '/prp-sync' in command:
                print(json.dumps({
                    "continue": True,
                    "feedback": "✅ Architecture changes don't affect any PRPs."
                }))
            return 0
        
        # Handle based on command
        if '/prp-sync' in command:
            # Explicit sync requested
            output = handle_prp_sync(affected_prps, command)
        else:
            # Architecture validation - just suggest
            output = suggest_prp_sync(affected_prps)
        
        print(json.dumps(output))
        
    except Exception as e:
        print(f"PRP regeneration hook error: {e}", file=sys.stderr)
        return 1
    
    return 0


def handle_prp_sync(affected_prps: List[Dict], command: str) -> Dict:
    """Handle explicit PRP sync command"""
    # Check for preview flag
    if '--preview' in command:
        return preview_changes(affected_prps)
    
    # Check for force flag
    preserve_progress = '--force' not in command
    
    # Perform regeneration
    regenerator = PRPRegenerator()
    results = []
    errors = []
    
    for prp_info in affected_prps:
        if prp_info['regeneration_needed']:
            result = regenerator.regenerate_prp(
                Path(prp_info['prp_file']),
                prp_info['impact']['changes'],
                preserve_progress=preserve_progress
            )
            
            if result['success']:
                results.append(result)
            else:
                errors.append(result)
    
    # Format feedback
    feedback_lines = []
    
    if results:
        feedback_lines.append(f"✅ Regenerated {len(results)} PRPs:")
        for result in results:
            prp_name = Path(result['file']).name
            feedback_lines.append(f"  - {prp_name} (progress preserved: {result['progress_preserved']})")
    
    if errors:
        feedback_lines.append(f"\n❌ Failed to regenerate {len(errors)} PRPs:")
        for error in errors:
            prp_name = Path(error['file']).name
            feedback_lines.append(f"  - {prp_name}: {error['error']}")
    
    # Suggest next actions
    suggestions = []
    
    if results:
        suggestions.append({
            "command": "/prp-status",
            "description": "Review regenerated PRPs"
        })
        suggestions.append({
            "command": "git add PRPs/active/ && git commit -m 'chore: sync PRPs with architecture changes'",
            "description": "Commit PRP updates"
        })
    
    return {
        "continue": True,
        "feedback": "\n".join(feedback_lines),
        "nextSuggestions": suggestions
    }


def preview_changes(affected_prps: List[Dict]) -> Dict:
    """Preview what would be changed"""
    feedback_lines = ["🔍 PRP Sync Preview\n"]
    
    # Group by severity
    critical = [p for p in affected_prps if p['impact']['severity'] == 'critical']
    high = [p for p in affected_prps if p['impact']['severity'] == 'high']
    medium = [p for p in affected_prps if p['impact']['severity'] == 'medium']
    low = [p for p in affected_prps if p['impact']['severity'] == 'low']
    
    if critical:
        feedback_lines.append(f"🚨 Critical ({len(critical)} PRPs):")
        for prp in critical:
            feedback_lines.append(format_prp_preview(prp))
    
    if high:
        feedback_lines.append(f"\n🔴 High Impact ({len(high)} PRPs):")
        for prp in high:
            feedback_lines.append(format_prp_preview(prp))
    
    if medium:
        feedback_lines.append(f"\n🟡 Medium Impact ({len(medium)} PRPs):")
        for prp in medium:
            feedback_lines.append(format_prp_preview(prp))
    
    if low:
        feedback_lines.append(f"\n🟢 Low Impact ({len(low)} PRPs):")
        for prp in low:
            feedback_lines.append(format_prp_preview(prp))
    
    # Add summary
    total = len(affected_prps)
    need_regen = len([p for p in affected_prps if p['regeneration_needed']])
    
    feedback_lines.append(f"\n📊 Summary:")
    feedback_lines.append(f"  - Total affected PRPs: {total}")
    feedback_lines.append(f"  - Need regeneration: {need_regen}")
    feedback_lines.append(f"  - Optional updates: {total - need_regen}")
    
    return {
        "continue": True,
        "feedback": "\n".join(feedback_lines),
        "nextSuggestions": [
            {
                "command": "/prp-sync",
                "description": f"Sync {need_regen} PRPs that need regeneration"
            },
            {
                "command": "/prp-sync --force",
                "description": "Sync without preserving progress (clean regeneration)"
            }
        ]
    }


def format_prp_preview(prp_info: Dict) -> str:
    """Format preview for a single PRP"""
    prp_name = Path(prp_info['prp_file']).name
    impact = prp_info['impact']
    
    preview = f"\n  📄 {prp_name}"
    preview += f"\n     Severity: {impact['severity']}"
    
    if impact['reasons']:
        preview += f"\n     Reasons: {'; '.join(impact['reasons'][:2])}"
    
    if impact['changes_needed']:
        preview += f"\n     Changes: {impact['changes_needed'][0]}"
    
    if prp_info['regeneration_needed']:
        preview += "\n     ⚡ Regeneration required"
    
    return preview


def suggest_prp_sync(affected_prps: List[Dict]) -> Dict:
    """Suggest PRP sync after architecture validation"""
    # Count by severity
    severity_counts = {}
    for prp in affected_prps:
        severity = prp['impact']['severity']
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    # Format feedback
    feedback = f"🔄 Architecture changes affect {len(affected_prps)} PRPs\n"
    
    if severity_counts:
        feedback += "\nImpact breakdown:"
        for severity in ['critical', 'high', 'medium', 'low']:
            if severity in severity_counts:
                emoji = {'critical': '🚨', 'high': '🔴', 'medium': '🟡', 'low': '🟢'}[severity]
                feedback += f"\n  {emoji} {severity.title()}: {severity_counts[severity]} PRPs"
    
    # Check if any need immediate attention
    urgent = any(p['impact']['severity'] in ['critical', 'high'] for p in affected_prps)
    
    if urgent:
        feedback += "\n\n⚠️  Critical or high-impact changes detected!"
    
    return {
        "continue": True,
        "feedback": feedback,
        "nextSuggestions": [
            {
                "command": "/prp-sync --preview",
                "description": "Preview which PRPs need updating"
            },
            {
                "command": "/prp-sync",
                "description": f"Sync {len(affected_prps)} affected PRPs"
            }
        ]
    }


if __name__ == "__main__":
    sys.exit(main())
