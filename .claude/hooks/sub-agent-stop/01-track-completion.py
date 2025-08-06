#!/usr/bin/env python3
"""
Track sub-agent completion for parallel tasks
Useful for monitoring progress of multiple concurrent operations
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
        
        # Track sub-agent completion
        subagent_id = input_data.get('subagent_id', 'unknown')
        subagent_task = input_data.get('task', 'unknown task')
        
        # Log completion to tracking file
        tracking_dir = Path('.claude/state/subagent-tracking')
        tracking_dir.mkdir(parents=True, exist_ok=True)
        
        completion_file = tracking_dir / 'completions.jsonl'
        
        completion_record = {
            'timestamp': datetime.now().isoformat(),
            'subagent_id': subagent_id,
            'task': subagent_task,
            'status': 'completed'
        }
        
        # Append to tracking file
        with open(completion_file, 'a') as f:
            f.write(json.dumps(completion_record) + '\n')
        
        # Check if all subagents completed for batch operations
        if 'batch_id' in input_data:
            batch_file = tracking_dir / f"batch-{input_data['batch_id']}.json"
            if batch_file.exists():
                with open(batch_file, 'r') as f:
                    batch_data = json.load(f)
                    
                completed = batch_data.get('completed', [])
                completed.append(subagent_id)
                batch_data['completed'] = completed
                
                # Check if all done
                if len(completed) == batch_data.get('total', 0):
                    message = f"✅ All {batch_data['total']} sub-agents completed for batch {input_data['batch_id']}"
                    print(message, file=sys.stderr)
                
                # Update batch file
                with open(batch_file, 'w') as f:
                    json.dump(batch_data, f, indent=2)
        
        # SubagentStop hooks just exit normally
        sys.exit(1)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Track completion error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
