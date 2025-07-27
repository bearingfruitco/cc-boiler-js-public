#!/usr/bin/env python3
"""
Snapshot Manager Hook - Creates automatic snapshots before risky operations
Provides instant rollback capability for AI-assisted development
"""

import json
import sys
import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import subprocess
import tarfile
import tempfile

class SnapshotManager:
    def __init__(self):
        self.snapshot_dir = Path('.claude/snapshots')
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.snapshot_dir / 'manifest.json'
        self.load_manifest()
        
    def load_manifest(self):
        """Load or create manifest file"""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {
                'snapshots': [],
                'version': '1.0.0',
                'created': datetime.now().isoformat(),
                'settings': {
                    'max_snapshots': 20,
                    'auto_snapshot': True,
                    'min_files_for_auto': 5,
                    'exclude_patterns': ['node_modules', '.next', 'dist', 'build', '*.log']
                }
            }
            self.save_manifest()
    
    def save_manifest(self):
        """Save manifest file"""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def should_snapshot(self, tool_name, tool_input):
        """Determine if operation needs snapshot"""
        
        # Check if auto-snapshot is enabled
        if not self.manifest['settings'].get('auto_snapshot', True):
            return False
            
        # Always snapshot for certain tools
        if tool_name in ['MultiEdit', 'Bash']:
            return True
            
        # Check for risky operations
        if tool_name in ['Write', 'Edit']:
            file_path = tool_input.get('file_path', '')
            
            # Critical files - always snapshot
            critical_files = [
                'package.json', '.env', '.env.local', 'tsconfig.json', 
                'next.config.js', 'drizzle.config.ts', 'tailwind.config.js',
                'vite.config.ts', '.claude/settings.json'
            ]
            
            if any(critical in file_path for critical in critical_files):
                return True
                
            # Check recent edit count
            recent_edits = self.get_recent_edit_count()
            if recent_edits >= self.manifest['settings'].get('min_files_for_auto', 5):
                return True
                
        return False
        
    def get_recent_edit_count(self):
        """Count recent edits in last 10 minutes"""
        try:
            # Use git to check recent modifications
            result = subprocess.run(
                ['git', 'diff', '--name-only'],
                capture_output=True,
                text=True
            )
            return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            return 0
            
    def get_changed_files(self):
        """Get list of changed files from git"""
        changed_files = []
        
        try:
            # Get modified files
            result = subprocess.run(
                ['git', 'diff', '--name-only'],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                changed_files.extend(result.stdout.strip().split('\n'))
            
            # Get untracked files
            result = subprocess.run(
                ['git', 'ls-files', '--others', '--exclude-standard'],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                changed_files.extend(result.stdout.strip().split('\n'))
                
        except Exception as e:
            print(f"Error getting changed files: {e}", file=sys.stderr)
            
        # Filter out excluded patterns
        filtered_files = []
        for file in changed_files:
            skip = False
            for pattern in self.manifest['settings']['exclude_patterns']:
                if pattern in file:
                    skip = True
                    break
            if not skip and Path(file).exists():
                filtered_files.append(file)
                
        return filtered_files
        
    def get_git_info(self):
        """Get current git branch and commit"""
        try:
            branch = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            commit = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True
            ).stdout.strip()[:8]
            
            return branch, commit
        except:
            return 'unknown', 'unknown'
    
    def create_snapshot(self, description="auto", reason="", changed_files=None):
        """Create a new snapshot"""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
        # Get changed files if not provided
        if changed_files is None:
            changed_files = self.get_changed_files()
            
        if not changed_files:
            return None
            
        # Create snapshot directory
        snapshot_name = f"{timestamp}-{description.replace(' ', '-')}"
        snapshot_path = self.snapshot_dir / snapshot_name
        
        # Get git info
        branch, commit = self.get_git_info()
        
        # Create snapshot metadata
        metadata = {
            'id': len(self.manifest['snapshots']) + 1,
            'name': snapshot_name,
            'timestamp': timestamp,
            'description': description,
            'reason': reason,
            'files': changed_files,
            'file_count': len(changed_files),
            'git_branch': branch,
            'git_commit': commit,
            'size_bytes': 0
        }
        
        # Create compressed archive
        archive_path = snapshot_path.with_suffix('.tar.gz')
        
        try:
            with tarfile.open(archive_path, 'w:gz') as tar:
                # Add metadata
                metadata_info = tarfile.TarInfo(name='manifest.json')
                metadata_bytes = json.dumps(metadata, indent=2).encode()
                metadata_info.size = len(metadata_bytes)
                tar.addfile(metadata_info, fileobj=tempfile.SpooledTemporaryFile().write(metadata_bytes))
                
                # Add changed files
                for file_path in changed_files:
                    if Path(file_path).exists():
                        # Store with relative path
                        tar.add(file_path, arcname=f"files/{file_path}")
                        
            # Update metadata with size
            metadata['size_bytes'] = archive_path.stat().st_size
            metadata['archive_path'] = str(archive_path)
            
            # Add to manifest
            self.manifest['snapshots'].insert(0, metadata)
            
            # Cleanup old snapshots
            self.cleanup_old_snapshots()
            
            # Save manifest
            self.save_manifest()
            
            return snapshot_name
            
        except Exception as e:
            print(f"Error creating snapshot: {e}", file=sys.stderr)
            if archive_path.exists():
                archive_path.unlink()
            return None
            
    def cleanup_old_snapshots(self):
        """Remove old snapshots keeping only max_snapshots"""
        max_count = self.manifest['settings']['max_snapshots']
        
        if len(self.manifest['snapshots']) > max_count:
            # Keep newest snapshots
            to_remove = self.manifest['snapshots'][max_count:]
            self.manifest['snapshots'] = self.manifest['snapshots'][:max_count]
            
            # Remove old snapshot files
            for snapshot in to_remove:
                if not snapshot.get('important', False):
                    archive_path = Path(snapshot.get('archive_path', ''))
                    if archive_path.exists():
                        try:
                            archive_path.unlink()
                        except:
                            pass
                            
    def get_context_for_claude(self):
        """Get formatted context about snapshots for Claude"""
        if not self.manifest['snapshots']:
            return None
            
        latest = self.manifest['snapshots'][0]
        
        context = f"""🔄 Snapshot Created: {latest['name']}
Files: {latest['file_count']} | Branch: {latest['git_branch']} | Size: {latest['size_bytes'] // 1024}KB

To rollback: /snapshot rollback 1
To view snapshots: /snapshot list"""
        
        return context

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        hook_input = json.loads(sys.stdin.read())
        
        # Extract tool info
        tool_name = hook_input.get('tool_name', '')
        tool_input = hook_input.get('tool_input', {})
        
        # Initialize snapshot manager
        manager = SnapshotManager()
        
        # Check if we should create a snapshot
        if manager.should_snapshot(tool_name, tool_input):
            # Determine reason for snapshot
            reason = ""
            if tool_name == 'MultiEdit':
                reason = "Multiple file edit operation"
            elif tool_name == 'Bash':
                reason = f"Shell command: {tool_input.get('command', '')[:50]}"
            else:
                file_path = tool_input.get('file_path', '')
                if 'package.json' in file_path:
                    reason = "Package.json modification"
                elif '.env' in file_path:
                    reason = "Environment file change"
                else:
                    reason = f"Editing {file_path}"
                    
            # Create snapshot
            snapshot_name = manager.create_snapshot(description="auto", reason=reason)
            
            if snapshot_name:
                # Get context for Claude
                context = manager.get_context_for_claude()
                
                # Output context (will show in Claude's response)
                if context:
                    print(context, file=sys.stderr)
                    
        # PreToolUse hook: Exit normally to continue with permission flow
        # No JSON output needed - hook just creates snapshots as a side effect
        sys.exit(0)
        
    except Exception as e:
        # Don't block on errors - log to stderr and continue
        print(f"Snapshot manager error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Exit with error code 1 for hook errors

if __name__ == '__main__':
    main()
