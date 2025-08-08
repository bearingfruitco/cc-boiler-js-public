#!/usr/bin/env python3
"""
Sub-Agent Coordination Hook - Manages parallel agent execution
Tracks progress, handles handoffs, and prevents conflicts
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # Extract sub-agent information
        agent_id = input_data.get('agent_id', 'unknown')
        agent_task = input_data.get('task', '')
        agent_result = input_data.get('result', {})
        
        # Coordination directory
        coord_dir = Path('.claude/coordination')
        coord_dir.mkdir(parents=True, exist_ok=True)
        
        # Record agent completion
        completion_file = coord_dir / f"agent-{agent_id}-complete.json"
        completion_data = {
            'agent_id': agent_id,
            'task': agent_task,
            'completed_at': datetime.now().isoformat(),
            'result_summary': agent_result.get('summary', 'No summary'),
            'files_modified': agent_result.get('files', []),
            'next_steps': agent_result.get('next_steps', [])
        }
        
        with open(completion_file, 'w') as f:
            json.dump(completion_data, f, indent=2)
        
        # Check for coordination needs
        if agent_result.get('needs_coordination'):
            # Create coordination request
            coord_request = coord_dir / 'coordination-needed.json'
            requests = []
            
            if coord_request.exists():
                with open(coord_request, 'r') as f:
                    requests = json.load(f)
            
            requests.append({
                'agent_id': agent_id,
                'reason': agent_result.get('coordination_reason', 'Unspecified'),
                'timestamp': datetime.now().isoformat()
            })
            
            with open(coord_request, 'w') as f:
                json.dump(requests, f, indent=2)
            
            # Notify about coordination need
            message = f"🤝 Agent {agent_id} needs coordination: {agent_result.get('coordination_reason', 'Check details')}"
            print(message, file=sys.stderr)
        
        # Check for handoff requirements
        if agent_result.get('handoff_to'):
            handoff_file = coord_dir / f"handoff-to-{agent_result['handoff_to']}.json"
            handoff_data = {
                'from_agent': agent_id,
                'to_agent': agent_result['handoff_to'],
                'context': agent_result.get('handoff_context', {}),
                'created_at': datetime.now().isoformat()
            }
            
            with open(handoff_file, 'w') as f:
                json.dump(handoff_data, f, indent=2)
        
        # SubagentStop hooks just exit normally
        sys.exit(1)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Coordinate error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
