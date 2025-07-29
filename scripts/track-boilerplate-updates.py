#!/usr/bin/env python3
"""
Boilerplate Update Tracker
Generates a report of what needs to be updated in projects using the boilerplate
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

class BoilerplateUpdateTracker:
    def __init__(self, boilerplate_path: Path = Path(".")):
        self.boilerplate_path = boilerplate_path
        self.tracking_file = boilerplate_path / ".claude" / "boilerplate-version.json"
        
    def get_current_version(self) -> Dict:
        """Get current boilerplate version info"""
        try:
            # Get latest commit
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=self.boilerplate_path,
                text=True
            ).strip()
            
            # Get commit date
            date = subprocess.check_output(
                ["git", "show", "-s", "--format=%ai", commit],
                cwd=self.boilerplate_path,
                text=True
            ).strip()
            
            return {
                "version": commit[:8],
                "commit": commit,
                "date": date,
                "commands": self._get_command_list(),
                "agents": self._get_agent_list(),
                "hooks": self._get_hook_list()
            }
        except Exception as e:
            print(f"Error getting version: {e}")
            return {}
    
    def _get_command_list(self) -> List[str]:
        """Get list of all commands"""
        registry_path = self.boilerplate_path / ".claude" / "command-registry.json"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                return list(json.load(f).keys())
        return []
    
    def _get_agent_list(self) -> List[str]:
        """Get list of all agents"""
        agents_dir = self.boilerplate_path / ".claude" / "agents"
        if agents_dir.exists():
            return [f.stem for f in agents_dir.glob("*.md") 
                   if f.stem not in ["QUICK_REFERENCE", "archive"]]
        return []
    
    def _get_hook_list(self) -> List[str]:
        """Get list of all hooks"""
        hooks_dir = self.boilerplate_path / ".claude" / "hooks"
        hooks = []
        for hook_type in ["pre-tool-use", "post-tool-use", "user-prompt-submit"]:
            type_dir = hooks_dir / hook_type
            if type_dir.exists():
                hooks.extend([f"{hook_type}/{f.name}" for f in type_dir.glob("*.py")
                            if not f.name.startswith("_")])
        return hooks
    
    def generate_update_report(self, since_commit: str = None) -> str:
        """Generate report of changes since a commit"""
        report = ["# Boilerplate Update Report\n"]
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        current = self.get_current_version()
        report.append(f"Current Version: {current['version']}\n")
        
        if since_commit:
            # Get changes since commit
            try:
                changes = subprocess.check_output(
                    ["git", "diff", "--name-only", f"{since_commit}..HEAD"],
                    cwd=self.boilerplate_path,
                    text=True
                ).strip().split('\n')
                
                # Categorize changes
                categorized = self._categorize_changes(changes)
                
                # Add to report
                report.append(f"## Changes since {since_commit[:8]}\n")
                
                if categorized["commands"]:
                    report.append("### New/Modified Commands")
                    for cmd in categorized["commands"]:
                        report.append(f"- {cmd}")
                    report.append("")
                
                if categorized["agents"]:
                    report.append("### New/Modified Agents")
                    for agent in categorized["agents"]:
                        report.append(f"- {agent}")
                    report.append("")
                
                if categorized["hooks"]:
                    report.append("### New/Modified Hooks")
                    for hook in categorized["hooks"]:
                        report.append(f"- {hook}")
                    report.append("")
                
                if categorized["scripts"]:
                    report.append("### New/Modified Scripts")
                    for script in categorized["scripts"]:
                        report.append(f"- {script}")
                    report.append("")
                
                # Git log summary
                report.append("### Commit Summary")
                log = subprocess.check_output(
                    ["git", "log", "--oneline", f"{since_commit}..HEAD"],
                    cwd=self.boilerplate_path,
                    text=True
                )
                report.append("```")
                report.append(log)
                report.append("```")
                
            except Exception as e:
                report.append(f"Error getting changes: {e}")
        
        # Migration instructions
        report.append("\n## Migration Instructions\n")
        report.append("### Option 1: Cherry-pick specific commits")
        report.append("```bash")
        report.append("# In your project directory")
        report.append("git remote add boilerplate [boilerplate-repo-url]")
        report.append("git fetch boilerplate")
        report.append("git cherry-pick [commit-hash]  # For specific updates")
        report.append("```\n")
        
        report.append("### Option 2: Copy specific files")
        report.append("```bash")
        report.append("# Copy updated commands")
        report.append("cp -r /path/to/boilerplate/.claude/commands/* .claude/commands/")
        report.append("# Copy updated hooks")
        report.append("cp -r /path/to/boilerplate/.claude/hooks/* .claude/hooks/")
        report.append("```\n")
        
        report.append("### Option 3: Full sync (careful!)")
        report.append("```bash")
        report.append("# This will overwrite your .claude directory")
        report.append("rsync -av --delete /path/to/boilerplate/.claude/ .claude/")
        report.append("```")
        
        return "\n".join(report)
    
    def _categorize_changes(self, files: List[str]) -> Dict[str, List[str]]:
        """Categorize changed files"""
        categorized = {
            "commands": [],
            "agents": [],
            "hooks": [],
            "scripts": [],
            "other": []
        }
        
        for file in files:
            if not file:
                continue
                
            if ".claude/commands/" in file:
                categorized["commands"].append(file)
            elif ".claude/agents/" in file:
                categorized["agents"].append(file)
            elif ".claude/hooks/" in file:
                categorized["hooks"].append(file)
            elif "scripts/" in file:
                categorized["scripts"].append(file)
            else:
                categorized["other"].append(file)
                
        return categorized
    
    def save_version_snapshot(self):
        """Save current version snapshot"""
        version_info = self.get_current_version()
        with open(self.tracking_file, 'w') as f:
            json.dump(version_info, f, indent=2)
        print(f"Version snapshot saved to {self.tracking_file}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Track boilerplate updates")
    parser.add_argument("--since", help="Generate report since this commit")
    parser.add_argument("--save-snapshot", action="store_true", 
                       help="Save current version snapshot")
    
    args = parser.parse_args()
    
    tracker = BoilerplateUpdateTracker()
    
    if args.save_snapshot:
        tracker.save_version_snapshot()
    else:
        report = tracker.generate_update_report(args.since)
        print(report)
        
        # Also save to file
        report_path = Path("BOILERPLATE_UPDATE_REPORT.md")
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {report_path}")


if __name__ == "__main__":
    main()
