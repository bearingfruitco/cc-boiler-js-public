#!/usr/bin/env python3
"""
Integration Test for Agent OS + Boilerplate System
Tests all new features and ensures existing functionality is preserved
"""

import os
import json
import subprocess
import sys

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def test_result(name, passed, details=""):
    if passed:
        print(f"{Colors.GREEN}✅ {name}{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ {name}{Colors.RESET}")
        if details:
            print(f"   {Colors.YELLOW}Details: {details}{Colors.RESET}")
    return passed

def run_tests():
    print(f"\n{Colors.BLUE}=== Agent OS Integration Tests ==={Colors.RESET}\n")
    
    all_passed = True
    
    # Test 1: Check standards directory exists
    standards_exist = os.path.exists(".agent-os/standards")
    all_passed &= test_result("Standards directory exists", standards_exist)
    
    if standards_exist:
        # Test 2: Check all standard files exist
        standard_files = ["design-system.md", "tech-stack.md", "best-practices.md"]
        for file in standard_files:
            path = f".agent-os/standards/{file}"
            exists = os.path.exists(path)
            all_passed &= test_result(f"Standard file: {file}", exists)
    
    # Test 3: Check new commands exist
    command_path = ".claude/commands"
    new_commands = ["analyze-existing.md", "migrate-to-strict-design.md", "smart-resume-standards.md"]
    for cmd in new_commands:
        path = f"{command_path}/{cmd}"
        exists = os.path.exists(path)
        all_passed &= test_result(f"New command: {cmd}", exists)
    
    # Test 4: Check aliases
    try:
        with open(".claude/aliases.json", 'r') as f:
            aliases = json.load(f)
        
        new_aliases = {
            "ae": "analyze-existing",
            "mds": "migrate-to-strict-design",
            "analyze": "analyze-existing",
            "drop-in": "analyze-existing"
        }
        
        for alias, command in new_aliases.items():
            has_alias = aliases.get(alias) == command
            all_passed &= test_result(f"Alias '{alias}' → '{command}'", has_alias)
    except Exception as e:
        all_passed &= test_result("Aliases file", False, str(e))
    
    # Test 5: Check chains
    try:
        with open(".claude/chains.json", 'r') as f:
            chains_data = json.load(f)
            chains = chains_data.get("chains", {})
        
        new_chains = [
            "analyze-existing-project",
            "migrate-design-system",
            "onboard-existing",
            "standards-sync"
        ]
        
        for chain in new_chains:
            has_chain = chain in chains
            all_passed &= test_result(f"Chain: {chain}", has_chain)
    except Exception as e:
        all_passed &= test_result("Chains file", False, str(e))
    
    # Test 6: Check hook exists
    hook_path = ".claude/hooks/pre-tool-use/02-design-check-standards.py"
    hook_exists = os.path.exists(hook_path)
    all_passed &= test_result("Enhanced design check hook", hook_exists)
    
    # Test 7: Verify existing commands still exist
    print(f"\n{Colors.BLUE}--- Existing System Integrity ---{Colors.RESET}\n")
    
    core_commands = [
        "smart-resume.md",
        "create-component.md",
        "validate-design.md",
        "create-prd.md",
        "create-prp.md",
        "task-ledger.md"
    ]
    
    for cmd in core_commands:
        path = f"{command_path}/{cmd}"
        exists = os.path.exists(path)
        all_passed &= test_result(f"Core command preserved: {cmd}", exists)
    
    # Test 8: Check hook system integrity
    core_hooks = [
        "00-auto-approve-safe-ops.py",
        "02-design-check-simple.py",
        "11-truth-enforcer.py",
        "14a-creation-guard.py"
    ]
    
    for hook in core_hooks:
        path = f".claude/hooks/pre-tool-use/{hook}"
        exists = os.path.exists(path)
        all_passed &= test_result(f"Core hook preserved: {hook}", exists)
    
    # Test 9: Integration points
    print(f"\n{Colors.BLUE}--- Integration Points ---{Colors.RESET}\n")
    
    # Check if smart-resume-standards references .agent-os
    if os.path.exists(".claude/commands/smart-resume-standards.md"):
        with open(".claude/commands/smart-resume-standards.md", 'r') as f:
            content = f.read()
            references_standards = ".agent-os/standards" in content
            all_passed &= test_result("Smart resume loads standards", references_standards)
    
    # Check if design hook can read standards
    if hook_exists:
        with open(hook_path, 'r') as f:
            content = f.read()
            reads_standards = "load_design_standards" in content
            all_passed &= test_result("Design hook reads from standards", reads_standards)
    
    # Summary
    print(f"\n{Colors.BLUE}=== Test Summary ==={Colors.RESET}\n")
    
    if all_passed:
        print(f"{Colors.GREEN}🎉 All tests passed! Integration successful.{Colors.RESET}")
    else:
        print(f"{Colors.RED}⚠️  Some tests failed. Please check the issues above.{Colors.RESET}")
    
    return all_passed

def check_workflow_integration():
    """Check if workflows properly integrate new commands"""
    print(f"\n{Colors.BLUE}=== Workflow Integration Test ==={Colors.RESET}\n")
    
    # Simulate workflow scenarios
    scenarios = [
        {
            "name": "Existing Project Onboarding",
            "chain": "onboard-existing",
            "expected_commands": ["analyze-existing", "migrate-to-strict-design", "task-ledger"]
        },
        {
            "name": "Design Migration",
            "chain": "migrate-design-system", 
            "expected_commands": ["migrate-to-strict-design", "validate-design", "test-runner"]
        }
    ]
    
    try:
        with open(".claude/chains.json", 'r') as f:
            chains_data = json.load(f)
            chains = chains_data.get("chains", {})
        
        for scenario in scenarios:
            chain = chains.get(scenario["chain"], {})
            commands = chain.get("commands", [])
            
            print(f"\n{scenario['name']}:")
            for expected in scenario["expected_commands"]:
                found = any(expected in cmd for cmd in commands)
                test_result(f"  Contains {expected}", found)
    
    except Exception as e:
        print(f"{Colors.RED}Could not test workflows: {e}{Colors.RESET}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")  # Go to project root
    
    passed = run_tests()
    check_workflow_integration()
    
    sys.exit(0 if passed else 1)
