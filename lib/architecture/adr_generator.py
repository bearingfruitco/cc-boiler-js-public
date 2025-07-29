"""
Architecture Decision Record (ADR) Generator
Generates ADRs from significant architecture changes
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ADRGenerator:
    """Generates Architecture Decision Records from changes"""
    
    def __init__(self, base_path: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.base_path = Path(base_path)
        self.adr_dir = self.base_path / "docs" / "architecture" / "decisions"
        self.adr_dir.mkdir(parents=True, exist_ok=True)
        
    def get_next_adr_number(self) -> int:
        """Get the next ADR number in sequence"""
        existing_adrs = list(self.adr_dir.glob("*.md"))
        if not existing_adrs:
            return 1
            
        # Extract numbers from filenames
        numbers = []
        for adr_file in existing_adrs:
            match = re.match(r'^(\d+)-', adr_file.name)
            if match:
                numbers.append(int(match.group(1)))
                
        return max(numbers) + 1 if numbers else 1
    
    def should_generate_adr(self, change_record: Dict) -> bool:
        """Determine if a change warrants an ADR"""
        # Major change indicators
        major_indicators = [
            "component_added",
            "component_removed",
            "technology_change",
            "security_policy_change",
            "architecture_pattern_change"
        ]
        
        # Check change type
        if change_record["type"] in major_indicators:
            return True
            
        # Check impact severity
        if change_record["impact"].get("severity") in ["high", "critical"]:
            return True
            
        # Check for breaking changes
        if change_record["impact"].get("breaking_change"):
            return True
            
        # Check for explicit ADR tag
        if "architectural_decision" in change_record.get("tags", []):
            return True
            
        # Check for multiple component impacts
        if len(change_record["impact"].get("components_affected", [])) >= 3:
            return True
            
        return False
    
    def generate_adr(self, change_record: Dict) -> str:
        """Generate an ADR from a change record"""
        adr_number = self.get_next_adr_number()
        title = self.generate_adr_title(change_record)
        filename = f"{adr_number:04d}-{self.slugify(title)}.md"
        
        # Generate ADR content
        content = self.generate_adr_content(adr_number, title, change_record)
        
        # Write ADR file
        adr_path = self.adr_dir / filename
        adr_path.write_text(content)
        
        return str(adr_path.relative_to(self.base_path))
    
    def generate_adr_title(self, change_record: Dict) -> str:
        """Generate a meaningful title for the ADR"""
        change_type = change_record["type"]
        
        if change_type == "component_added":
            components = [c["name"] for c in change_record["changes"]["components"]["added"]]
            return f"Add {', '.join(components)} Component{'s' if len(components) > 1 else ''}"
            
        elif change_type == "component_removed":
            components = [c["name"] for c in change_record["changes"]["components"]["removed"]]
            return f"Remove {', '.join(components)} Component{'s' if len(components) > 1 else ''}"
            
        elif change_type == "api_modified":
            return "Modify API Endpoints"
            
        elif change_type == "schema_changed":
            return "Update Database Schema"
            
        elif change_type == "security_updated":
            return "Update Security Policies"
            
        else:
            # Use description as title
            desc = change_record["description"]
            # Limit length and clean up
            if len(desc) > 50:
                desc = desc[:47] + "..."
            return desc
    
    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        # Convert to lowercase
        text = text.lower()
        # Replace spaces and special characters with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        # Remove leading/trailing hyphens
        text = text.strip('-')
        return text
    
    def generate_adr_content(self, number: int, title: str, 
                           change_record: Dict) -> str:
        """Generate the full ADR content"""
        timestamp = datetime.fromisoformat(change_record["timestamp"])
        
        content = f"""# {number}. {title}

Date: {timestamp.strftime("%Y-%m-%d")}

## Status

Accepted

## Context

{self.expand_context(change_record)}

## Decision

{self.expand_decision(change_record)}

## Consequences

{self.expand_consequences(change_record)}

## Implementation

{self.expand_implementation(change_record)}

## Related

- Change ID: `{change_record["id"]}`
- Architecture File: [{change_record["file"]}](../../{change_record["file"]})
"""

        # Add optional related items
        if change_record.get("related_prp"):
            content += f"- Related PRP: [{change_record['related_prp']}](../../../PRPs/active/{change_record['related_prp']}.md)\n"
            
        if change_record.get("related_issue"):
            content += f"- Related Issue: #{change_record['related_issue']}\n"
            
        if change_record.get("commit"):
            content += f"- Commit: `{change_record['commit']}`\n"
        
        return content
    
    def expand_context(self, change_record: Dict) -> str:
        """Expand the context section of the ADR"""
        context_parts = []
        
        # Add rationale if provided
        if change_record.get("rationale"):
            context_parts.append(change_record["rationale"])
        
        # Describe the current situation
        change_type = change_record["type"]
        if change_type == "component_added":
            context_parts.append(
                "The system requires new functionality that warrants "
                "the addition of new architectural components."
            )
        elif change_type == "component_removed":
            context_parts.append(
                "Existing components are no longer needed or have been "
                "replaced by better alternatives."
            )
        elif change_type == "api_modified":
            context_parts.append(
                "API endpoints need modification to better serve client needs "
                "or to align with new requirements."
            )
        elif change_type == "schema_changed":
            context_parts.append(
                "The database schema requires updates to support new features "
                "or to improve data organization."
            )
        elif change_type == "security_updated":
            context_parts.append(
                "Security policies need updating to address new threats "
                "or to comply with updated requirements."
            )
        
        # Add impact information
        impact = change_record["impact"]
        if impact.get("breaking_change"):
            context_parts.append(
                "This change will break existing functionality and requires "
                "careful migration planning."
            )
        
        return "\n\n".join(context_parts) if context_parts else \
               "Architecture changes were needed to improve the system."
    
    def expand_decision(self, change_record: Dict) -> str:
        """Expand the decision section of the ADR"""
        decisions = []
        
        # Describe what was decided
        decisions.append(f"We will {change_record['description'].lower()}.")
        
        # Add specific changes
        changes = change_record["changes"]
        
        if changes["components"]["added"]:
            components = [c["name"] for c in changes["components"]["added"]]
            decisions.append(f"The following components will be added: {', '.join(components)}")
            
        if changes["components"]["removed"]:
            components = [c["name"] for c in changes["components"]["removed"]]
            decisions.append(f"The following components will be removed: {', '.join(components)}")
        
        if changes["apis"]["added"] or changes["apis"]["removed"]:
            decisions.append("API endpoints will be modified as specified in the architecture documents.")
            
        if changes["database_tables"]["added"] or changes["database_tables"]["removed"]:
            decisions.append("Database schema will be updated with appropriate migrations.")
        
        return "\n\n".join(decisions)
    
    def expand_consequences(self, change_record: Dict) -> str:
        """Expand the consequences section of the ADR"""
        positive = []
        negative = []
        neutral = []
        
        impact = change_record["impact"]
        changes = change_record["changes"]
        
        # Positive consequences
        if changes["components"]["added"]:
            positive.append("New functionality will be cleanly separated into dedicated components")
            positive.append("System modularity and maintainability will improve")
            
        if changes["apis"]["added"]:
            positive.append("New API endpoints will provide better client functionality")
            
        if changes["security_policies"]["added"]:
            positive.append("Security posture will be strengthened")
        
        # Negative consequences
        if impact.get("breaking_change"):
            negative.append("Existing integrations will need to be updated")
            negative.append("Downtime may be required during migration")
            
        if impact.get("requires_migration"):
            negative.append("Database migrations will be needed")
            negative.append("Data migration risks must be managed")
            
        if changes["components"]["removed"]:
            negative.append("Functionality dependent on removed components must be refactored")
        
        # Neutral consequences
        if impact.get("requires_code_changes"):
            neutral.append("Implementation code will need to be updated")
            
        if impact.get("components_affected"):
            affected = impact["components_affected"]
            neutral.append(f"The following components will be affected: {', '.join(affected)}")
        
        # Format consequences
        consequences = "### Positive\n\n"
        if positive:
            consequences += "\n".join(f"- {c}" for c in positive)
        else:
            consequences += "- Better system organization"
            
        consequences += "\n\n### Negative\n\n"
        if negative:
            consequences += "\n".join(f"- {c}" for c in negative)
        else:
            consequences += "- Additional implementation effort required"
            
        consequences += "\n\n### Neutral\n\n"
        if neutral:
            consequences += "\n".join(f"- {c}" for c in neutral)
        else:
            consequences += "- Documentation will need updating"
        
        return consequences
    
    def expand_implementation(self, change_record: Dict) -> str:
        """Expand the implementation section of the ADR"""
        impl_steps = []
        
        impact = change_record["impact"]
        
        # Add implementation steps based on impact
        if impact.get("requires_code_changes"):
            impl_steps.append("1. Update implementation code to match new architecture")
            
        if impact.get("requires_migration"):
            impl_steps.append("2. Create and test database migrations")
            
        if impact.get("breaking_change"):
            impl_steps.append("3. Update all dependent systems")
            impl_steps.append("4. Coordinate deployment with stakeholders")
        
        # Add PRP reference if available
        if change_record.get("related_prp"):
            impl_steps.append(
                f"5. Follow implementation plan in PRP: {change_record['related_prp']}"
            )
        
        # Default steps if none specified
        if not impl_steps:
            impl_steps = [
                "1. Update architecture documentation",
                "2. Generate/update PRPs for affected components",
                "3. Implement changes following PRPs",
                "4. Update tests and documentation"
            ]
        
        return "\n".join(impl_steps)
    
    def generate_adr_index(self):
        """Generate or update the ADR index file"""
        index_path = self.adr_dir / "README.md"
        
        # Get all ADR files
        adr_files = sorted(self.adr_dir.glob("[0-9]*.md"))
        
        # Build index content
        content = """# Architecture Decision Records

This directory contains all Architecture Decision Records (ADRs) for the project.

## What is an ADR?

An Architecture Decision Record captures an important architectural decision made along with its context and consequences.

## ADR Index

"""
        
        # Add each ADR to the index
        for adr_file in adr_files:
            # Extract number and title from filename
            match = re.match(r'^(\d+)-(.*?)\.md$', adr_file.name)
            if match:
                number = match.group(1)
                slug = match.group(2)
                
                # Read the title from the file
                first_line = adr_file.read_text().split('\n')[0]
                if first_line.startswith('#'):
                    title = first_line.strip('# ').strip()
                else:
                    title = slug.replace('-', ' ').title()
                
                # Add to index
                content += f"- [{title}](./{adr_file.name})\n"
        
        # Write index
        index_path.write_text(content)
