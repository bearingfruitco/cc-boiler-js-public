#!/usr/bin/env python3
"""Test chains.json configuration"""

import json
from pathlib import Path

def test_chains():
    chains_file = Path('/Users/shawnsmith/dev/bfc/boilerplate/.claude/config/chains.json')
    
    if not chains_file.exists():
        print("❌ chains.json not found in expected location")
        return False
    
    try:
        with open(chains_file, 'r') as f:
            chains = json.load(f)
        
        print(f"✅ chains.json is valid JSON")
        
        # Count chains
        if 'chains' in chains:
            chain_count = len(chains['chains'])
            print(f"✅ Found {chain_count} chains")
            
            # List chains
            print("\nAvailable chains:")
            for chain_name in chains['chains'].keys():
                print(f"  • {chain_name}")
            
            # Check for parallel support
            has_parallel = False
            for chain_name, chain_data in chains['chains'].items():
                if 'parallel' in str(chain_data):
                    has_parallel = True
                    break
            
            if has_parallel:
                print("\n✅ Some chains support parallel execution")
            else:
                print("\n⚠️  No chains currently use parallel execution")
                print("   Consider adding 'parallel': true to phases for better performance")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in chains.json: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading chains.json: {e}")
        return False

if __name__ == '__main__':
    success = test_chains()
    exit(0 if success else 1)
