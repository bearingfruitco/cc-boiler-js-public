#!/usr/bin/env python3
"""
Save Transcript Hook - Saves conversation transcript when session ends
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def save_transcript():
    """Save the current session transcript"""
    try:
        # Create transcripts directory
        transcript_dir = Path(".claude/transcripts")
        transcript_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{timestamp}.txt"
        filepath = transcript_dir / filename
        
        # Note: In a real implementation, we would capture the actual transcript
        # For now, we just create a marker file
        with open(filepath, 'w') as f:
            f.write(f"Session ended at {datetime.now().isoformat()}\n")
            f.write(f"Session ID: {os.getenv('CLAUDE_SESSION_ID', 'unknown')}\n")
        
        return True
    except Exception as e:
        print(f"Failed to save transcript: {str(e)}", file=sys.stderr)
        return False

def main():
    """Main hook logic"""
    try:
        # Read input if provided
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # Save the transcript
        save_transcript()
        
        # Allow Claude to stop normally - exit with code 0
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr but still allow stop
        print(f"Save transcript hook error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
