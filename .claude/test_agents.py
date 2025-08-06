#!/usr/bin/env python3
"""Test all agent files for proper configuration"""

import os
import yaml
from pathlib import Path

def test_agents():
    agents_dir = Path('/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents')
    
    results = {
        'valid': [],
        'invalid': []
    }
    
    for agent_file in agents_dir.glob('*.md'):
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            # Check for YAML frontmatter
            if content.startswith('---'):
                # Extract frontmatter
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    config = yaml.safe_load(frontmatter)
                    
                    # Check required fields
                    if 'name' in config and 'description' in config:
                        results['valid'].append(agent_file.name)
                    else:
                        results['invalid'].append(f"{agent_file.name}: Missing required fields")
                else:
                    results['invalid'].append(f"{agent_file.name}: Invalid format")
            else:
                results['invalid'].append(f"{agent_file.name}: No frontmatter")
                
        except Exception as e:
            results['invalid'].append(f"{agent_file.name}: {str(e)}")
    
    print(f"✅ Valid agents: {len(results['valid'])}")
    print(f"❌ Invalid agents: {len(results['invalid'])}")
    
    if results['invalid']:
        print("\nInvalid agents:")
        for issue in results['invalid']:
            print(f"  - {issue}")
    
    if results['valid']:
        print("\nValid agents:")
        for agent in results['valid']:
            print(f"  ✓ {agent}")
    
    return len(results['invalid']) == 0

if __name__ == '__main__':
    success = test_agents()
    exit(0 if success else 1)
