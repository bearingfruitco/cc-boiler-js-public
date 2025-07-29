#!/usr/bin/env python3
"""
Architecture Visualization Generator
Creates ASCII and Mermaid diagrams from architecture documents
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ArchitectureVisualizer:
    def __init__(self, arch_dir: Path = Path("docs/architecture")):
        self.arch_dir = arch_dir
        self.components = {
            "frontend": [],
            "backend": [],
            "database": [],
            "external": []
        }
        self.tables = []
        self.apis = []
        self.data_flows = []
        self.security_layers = []
        
    def analyze_architecture(self):
        """Parse architecture documents to extract components"""
        # Analyze each document
        docs = {
            "system": self.arch_dir / "SYSTEM_DESIGN.md",
            "database": self.arch_dir / "DATABASE_SCHEMA.md",
            "api": self.arch_dir / "API_SPECIFICATION.md",
            "frontend": self.arch_dir / "FRONTEND_ARCHITECTURE.md",
            "security": self.arch_dir / "SECURITY_DESIGN.md"
        }
        
        for doc_type, path in docs.items():
            if path.exists():
                with open(path, 'r') as f:
                    content = f.read()
                    if doc_type == "system":
                        self._parse_system_components(content)
                    elif doc_type == "database":
                        self._parse_database_schema(content)
                    elif doc_type == "api":
                        self._parse_api_spec(content)
                    elif doc_type == "frontend":
                        self._parse_frontend_components(content)
                    elif doc_type == "security":
                        self._parse_security_architecture(content)
                        
    def _parse_system_components(self, content: str):
        """Extract system components from SYSTEM_DESIGN.md"""
        # Look for component definitions
        component_patterns = [
            r'(?:Frontend|Client):\s*(.+?)(?:\n|$)',
            r'(?:Backend|Server):\s*(.+?)(?:\n|$)',
            r'(?:Database|Storage):\s*(.+?)(?:\n|$)',
            r'(?:External|Third-party):\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in component_patterns:
            matches = re.findall(pattern, content, re.I | re.M)
            for match in matches:
                if 'frontend' in pattern.lower():
                    self.components["frontend"].extend(match.split(','))
                elif 'backend' in pattern.lower():
                    self.components["backend"].extend(match.split(','))
                elif 'database' in pattern.lower():
                    self.components["database"].extend(match.split(','))
                elif 'external' in pattern.lower():
                    self.components["external"].extend(match.split(','))
                    
        # Look for technology mentions
        if re.search(r'Next\.js|React', content, re.I):
            self.components["frontend"].append("Next.js")
        if re.search(r'Supabase', content, re.I):
            self.components["backend"].append("Supabase")
        if re.search(r'PostgreSQL|Postgres', content, re.I):
            self.components["database"].append("PostgreSQL")
            
    def _parse_database_schema(self, content: str):
        """Extract database tables and relationships"""
        # Find CREATE TABLE statements
        table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:public\.)?(\w+)\s*\((.*?)\);'
        matches = re.findall(table_pattern, content, re.I | re.S)
        
        for table_name, columns in matches:
            table = {
                "name": table_name,
                "columns": [],
                "relationships": []
            }
            
            # Parse columns
            column_lines = columns.strip().split('\n')
            for line in column_lines:
                line = line.strip()
                if line and not line.startswith('--'):
                    # Extract column name and type
                    col_match = re.match(r'(\w+)\s+(\w+(?:\([^)]+\))?)', line)
                    if col_match:
                        col_name, col_type = col_match.groups()
                        is_pk = 'PRIMARY KEY' in line or 'PK' in line
                        is_fk = 'REFERENCES' in line or 'FK' in line
                        
                        column = {
                            "name": col_name,
                            "type": col_type,
                            "pk": is_pk,
                            "fk": is_fk
                        }
                        
                        # Extract foreign key reference
                        fk_match = re.search(r'REFERENCES\s+(\w+)(?:\((\w+)\))?', line)
                        if fk_match:
                            ref_table = fk_match.group(1)
                            table["relationships"].append({
                                "from": col_name,
                                "to_table": ref_table,
                                "to_column": fk_match.group(2) or "id"
                            })
                            
                        table["columns"].append(column)
                        
            self.tables.append(table)
            
    def _parse_api_spec(self, content: str):
        """Extract API endpoints"""
        # Look for endpoint definitions
        endpoint_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+(/[\w/:\-{}]+)(?:\s*[→-]\s*(.+?))?(?:\n|$)'
        matches = re.findall(endpoint_pattern, content, re.I | re.M)
        
        for method, path, description in matches:
            self.apis.append({
                "method": method.upper(),
                "path": path,
                "description": description.strip() if description else ""
            })
            
    def _parse_frontend_components(self, content: str):
        """Extract frontend component hierarchy"""
        # Look for component definitions
        comp_pattern = r'(?:components?/|├──\s*)(\w+)(?:\.tsx?)?'
        matches = re.findall(comp_pattern, content, re.I)
        
        for comp in matches:
            if comp not in ["components", "src", "pages", "app"]:
                self.components["frontend"].append(comp)
                
    def _parse_security_architecture(self, content: str):
        """Extract security layers and controls"""
        # Look for security layer definitions
        if "Network" in content:
            self.security_layers.append(("Network", ["WAF", "DDoS Protection", "SSL/TLS"]))
        if "Application" in content:
            self.security_layers.append(("Application", ["Authentication", "Authorization", "Input Validation"]))
        if "Database" in content or "Data" in content:
            self.security_layers.append(("Data", ["Encryption", "RLS", "Backup"]))
        if "Monitoring" in content:
            self.security_layers.append(("Monitoring", ["Audit Logs", "Alerts", "SIEM"]))
            
    def generate_system_diagram(self, format: str = "both") -> Dict[str, str]:
        """Generate system architecture diagram"""
        diagrams = {}
        
        if format in ["ascii", "both"]:
            diagrams["ascii"] = self._generate_ascii_system()
            
        if format in ["mermaid", "both"]:
            diagrams["mermaid"] = self._generate_mermaid_system()
            
        return diagrams
        
    def _generate_ascii_system(self) -> str:
        """Generate ASCII art system diagram"""
        # Default to common architecture if no components found
        if not any(self.components.values()):
            return self._default_ascii_system()
            
        # Build custom diagram based on found components
        lines = []
        lines.append("┌" + "─" * 73 + "┐")
        lines.append("│" + "System Architecture".center(73) + "│")
        lines.append("└" + "─" * 73 + "┘")
        lines.append("")
        
        # Add components by layer
        if self.components["frontend"]:
            lines.append("Frontend Layer:")
            for comp in self.components["frontend"][:3]:  # Limit to 3
                lines.append(f"  ┌─────────────┐")
                lines.append(f"  │ {comp[:11].center(11)} │")
                lines.append(f"  └──────┬──────┘")
                lines.append("         │")
                
        if self.components["backend"]:
            lines.append("Backend Layer:")
            for comp in self.components["backend"][:3]:
                lines.append(f"  ┌─────────────┐")
                lines.append(f"  │ {comp[:11].center(11)} │")
                lines.append(f"  └──────┬──────┘")
                lines.append("         │")
                
        if self.components["database"]:
            lines.append("Data Layer:")
            for comp in self.components["database"][:2]:
                lines.append(f"  ┌─────────────┐")
                lines.append(f"  │ {comp[:11].center(11)} │")
                lines.append(f"  └─────────────┘")
                
        return "\n".join(lines)
        
    def _default_ascii_system(self) -> str:
        """Default system architecture diagram"""
        return '''
┌─────────────────────────────────────────────────────────────────────────┐
│                           System Architecture                            │
└─────────────────────────────────────────────────────────────────────────┘

     ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
     │   Browser    │         │ Mobile App   │         │   API Client │
     │   (Users)    │         │   (Users)    │         │  (External)  │
     └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
            │                        │                         │
            └────────────┬───────────┴─────────────┬──────────┘
                         ▼                         ▼
                 ┌───────────────────────────────────────┐
                 │          Cloudflare CDN               │
                 │    (Static Assets & DDoS Protection)  │
                 └───────────────┬───────────────────────┘
                                 ▼
                 ┌───────────────────────────────────────┐
                 │           Vercel Edge                 │
                 │      (Next.js Application)            │
                 └───────────────┬───────────────────────┘
                                 ▼
                 ┌───────────────────────────────────────┐
                 │         Supabase Backend              │
                 │     (Auth, Storage, Database)         │
                 └───────────────────────────────────────┘

Legend: ─── Data Flow  │ Connection  ▼ Direction
'''
        
    def _generate_mermaid_system(self) -> str:
        """Generate Mermaid diagram for system"""
        lines = ["graph TB"]
        
        # Add subgraphs for layers
        if self.components["frontend"] or True:  # Always show structure
            lines.append('    subgraph "Client Layer"')
            lines.append('        Browser[Browser Users]')
            lines.append('        Mobile[Mobile App]')
            lines.append('    end')
            lines.append('')
            
        if self.components["backend"] or True:
            lines.append('    subgraph "Application Layer"')
            lines.append('        API[API Server]')
            lines.append('        Auth[Authentication]')
            lines.append('        BL[Business Logic]')
            lines.append('    end')
            lines.append('')
            
        if self.components["database"] or True:
            lines.append('    subgraph "Data Layer"')
            lines.append('        DB[(Database)]')
            lines.append('        Cache[(Cache)]')
            lines.append('    end')
            lines.append('')
            
        # Add connections
        lines.append('    Browser --> API')
        lines.append('    Mobile --> API')
        lines.append('    API --> Auth')
        lines.append('    API --> BL')
        lines.append('    BL --> DB')
        lines.append('    BL --> Cache')
        
        return "\n".join(lines)
        
    def generate_database_diagram(self, format: str = "both") -> Dict[str, str]:
        """Generate database schema diagram"""
        diagrams = {}
        
        if format in ["ascii", "both"]:
            diagrams["ascii"] = self._generate_ascii_database()
            
        if format in ["mermaid", "both"]:
            diagrams["mermaid"] = self._generate_mermaid_database()
            
        return diagrams
        
    def _generate_ascii_database(self) -> str:
        """Generate ASCII database diagram"""
        if not self.tables:
            return self._default_ascii_database()
            
        lines = []
        lines.append("┌" + "─" * 73 + "┐")
        lines.append("│" + "Database Schema".center(73) + "│")
        lines.append("└" + "─" * 73 + "┘")
        lines.append("")
        
        # Add each table
        for table in self.tables[:4]:  # Limit to 4 tables for space
            lines.append(f"┌─────────────────────┐")
            lines.append(f"│ {table['name'][:19].center(19)} │")
            lines.append(f"├─────────────────────┤")
            
            # Add columns (limit to 5)
            for col in table["columns"][:5]:
                col_str = f"{col['name']} {col['type']}"
                if col["pk"]:
                    col_str += " PK"
                elif col["fk"]:
                    col_str += " FK"
                lines.append(f"│ {col_str[:19].ljust(19)} │")
                
            lines.append(f"└─────────────────────┘")
            lines.append("")
            
        return "\n".join(lines)
        
    def _default_ascii_database(self) -> str:
        """Default database schema"""
        return '''
┌─────────────────────────────────────────────────────────────────────────┐
│                          Database Schema                                 │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐       ┌─────────────────────┐
│      users          │       │      projects       │
├─────────────────────┤       ├─────────────────────┤
│ id (uuid) PK        │       │ id (uuid) PK        │
│ email               │       │ name                │
│ created_at          │◄──────┤ user_id FK          │
└─────────────────────┘       │ created_at          │
                              └─────────────────────┘
'''
        
    def _generate_mermaid_database(self) -> str:
        """Generate Mermaid ER diagram"""
        if not self.tables:
            return self._default_mermaid_database()
            
        lines = ["erDiagram"]
        
        # Add relationships
        relationships = []
        for table in self.tables:
            for rel in table.get("relationships", []):
                relationships.append(f"    {table['name']} ||--o{{ {rel['to_table']} : has")
                
        # Add unique relationships
        seen = set()
        for rel in relationships:
            if rel not in seen:
                lines.append(rel)
                seen.add(rel)
                
        lines.append("")
        
        # Add table definitions
        for table in self.tables:
            lines.append(f"    {table['name']} {{")
            for col in table["columns"][:8]:  # Limit columns
                type_str = "string" if "char" in col["type"].lower() else "number"
                key_str = " PK" if col["pk"] else " FK" if col["fk"] else ""
                lines.append(f"        {type_str} {col['name']}{key_str}")
            lines.append("    }")
            lines.append("")
            
        return "\n".join(lines)
        
    def _default_mermaid_database(self) -> str:
        """Default Mermaid database diagram"""
        return '''erDiagram
    users ||--o{ projects : owns
    
    users {
        string id PK
        string email
        datetime created_at
    }
    
    projects {
        string id PK
        string name
        string user_id FK
        datetime created_at
    }
'''
        
    def generate_api_diagram(self, format: str = "both") -> Dict[str, str]:
        """Generate API structure diagram"""
        diagrams = {}
        
        if format in ["ascii", "both"]:
            diagrams["ascii"] = self._generate_ascii_api()
            
        if format in ["mermaid", "both"]:
            diagrams["mermaid"] = self._generate_mermaid_api()
            
        return diagrams
        
    def _generate_ascii_api(self) -> str:
        """Generate ASCII API structure"""
        lines = []
        lines.append("┌" + "─" * 73 + "┐")
        lines.append("│" + "API Structure".center(73) + "│")
        lines.append("└" + "─" * 73 + "┘")
        lines.append("")
        lines.append("/api")
        
        if not self.apis:
            # Default structure
            lines.append("├── /auth")
            lines.append("│   ├── POST   /login")
            lines.append("│   └── POST   /logout")
            lines.append("├── /users")
            lines.append("│   ├── GET    /")
            lines.append("│   └── GET    /:id")
            lines.append("└── /health")
            lines.append("    └── GET    /")
        else:
            # Group APIs by path
            api_tree = {}
            for api in self.apis:
                parts = api["path"].split('/')
                current = api_tree
                for part in parts[1:]:  # Skip empty first part
                    if part and not part.startswith(':'):
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                        
            # Render tree
            self._render_api_tree(lines, api_tree, "", True)
            
        return "\n".join(lines)
        
    def _render_api_tree(self, lines: List[str], tree: Dict, prefix: str, is_last: bool):
        """Recursively render API tree"""
        items = list(tree.items())
        for i, (key, subtree) in enumerate(items):
            is_last_item = i == len(items) - 1
            connector = "└── " if is_last_item else "├── "
            lines.append(f"{prefix}{connector}/{key}")
            
            if subtree:
                extension = "    " if is_last_item else "│   "
                self._render_api_tree(lines, subtree, prefix + extension, is_last_item)
                
    def _generate_mermaid_api(self) -> str:
        """Generate Mermaid API diagram"""
        return '''sequenceDiagram
    participant Client
    participant API
    participant Auth
    participant DB
    
    Client->>API: Request
    API->>Auth: Verify Token
    Auth-->>API: Authorized
    API->>DB: Query Data
    DB-->>API: Results
    API-->>Client: Response
'''
        
    def generate_component_diagram(self, format: str = "both") -> Dict[str, str]:
        """Generate component hierarchy diagram"""
        diagrams = {}
        
        if format in ["ascii", "both"]:
            diagrams["ascii"] = self._generate_ascii_components()
            
        if format in ["mermaid", "both"]:
            diagrams["mermaid"] = self._generate_mermaid_components()
            
        return diagrams
        
    def _generate_ascii_components(self) -> str:
        """Generate ASCII component tree"""
        return '''
┌─────────────────────────────────────────────────────────────────────────┐
│                        Component Structure                               │
└─────────────────────────────────────────────────────────────────────────┘

src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Container.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Modal.tsx
│   └── features/
│       ├── UserProfile.tsx
│       └── Dashboard.tsx
├── hooks/
│   ├── useAuth.ts
│   └── useData.ts
└── utils/
    ├── api.ts
    └── helpers.ts
'''
        
    def _generate_mermaid_components(self) -> str:
        """Generate Mermaid component diagram"""
        return '''graph TD
    App[App]
    App --> Layout[Layout]
    App --> Router[Router]
    
    Layout --> Header[Header]
    Layout --> Main[Main Content]
    Layout --> Footer[Footer]
    
    Router --> Pages[Pages]
    Pages --> Home[Home]
    Pages --> Dashboard[Dashboard]
    Pages --> Profile[Profile]
    
    Dashboard --> Charts[Charts]
    Dashboard --> Stats[Stats]
'''
        
    def generate_flow_diagram(self, format: str = "both") -> Dict[str, str]:
        """Generate data flow diagram"""
        diagrams = {}
        
        if format in ["ascii", "both"]:
            diagrams["ascii"] = self._generate_ascii_flow()
            
        if format in ["mermaid", "both"]:
            diagrams["mermaid"] = self._generate_mermaid_flow()
            
        return diagrams
        
    def _generate_ascii_flow(self) -> str:
        """Generate ASCII data flow"""
        return '''
┌─────────────────────────────────────────────────────────────────────────┐
│                           Data Flow                                      │
└─────────────────────────────────────────────────────────────────────────┘

User Input ──► Validation ──► API Request ──► Business Logic
                                                    │
                                                    ▼
Response ◄──── Transform ◄──── Database ◄──── Process
'''
        
    def _generate_mermaid_flow(self) -> str:
        """Generate Mermaid flow diagram"""
        return '''flowchart LR
    UI[User Input] --> V{Validation}
    V -->|Valid| API[API Layer]
    V -->|Invalid| E[Error]
    API --> BL[Business Logic]
    BL --> DB[(Database)]
    DB --> T[Transform]
    T --> R[Response]
    R --> UI
    E --> UI
'''
        
    def generate_security_diagram(self, format: str = "both") -> Dict[str, str]:
        """Generate security architecture diagram"""
        diagrams = {}
        
        if format in ["ascii", "both"]:
            diagrams["ascii"] = self._generate_ascii_security()
            
        if format in ["mermaid", "both"]:
            diagrams["mermaid"] = self._generate_mermaid_security()
            
        return diagrams
        
    def _generate_ascii_security(self) -> str:
        """Generate ASCII security diagram"""
        lines = []
        lines.append("┌" + "─" * 73 + "┐")
        lines.append("│" + "Security Architecture".center(73) + "│")
        lines.append("└" + "─" * 73 + "┘")
        lines.append("")
        
        if self.security_layers:
            for layer, controls in self.security_layers:
                lines.append(f"Layer: {layer}")
                for control in controls[:3]:  # Limit to 3
                    lines.append(f"  • {control}")
                lines.append("")
        else:
            # Default security layers
            lines.append("Layer 1: Network")
            lines.append("  • Firewall")
            lines.append("  • DDoS Protection")
            lines.append("")
            lines.append("Layer 2: Application")
            lines.append("  • Authentication")
            lines.append("  • Authorization")
            lines.append("")
            lines.append("Layer 3: Data")
            lines.append("  • Encryption")
            lines.append("  • Access Control")
            
        return "\n".join(lines)
        
    def _generate_mermaid_security(self) -> str:
        """Generate Mermaid security diagram"""
        return '''graph TB
    subgraph "Threats"
        T1[SQL Injection]
        T2[XSS]
        T3[CSRF]
        T4[DDoS]
    end
    
    subgraph "Controls"
        C1[Input Validation]
        C2[Output Encoding]
        C3[CSRF Tokens]
        C4[Rate Limiting]
    end
    
    T1 --> C1
    T2 --> C2
    T3 --> C3
    T4 --> C4
'''
        
    def generate_all_diagrams(self, format: str = "both") -> Dict[str, Dict[str, str]]:
        """Generate all diagram types"""
        return {
            "system": self.generate_system_diagram(format),
            "database": self.generate_database_diagram(format),
            "api": self.generate_api_diagram(format),
            "components": self.generate_component_diagram(format),
            "flow": self.generate_flow_diagram(format),
            "security": self.generate_security_diagram(format)
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate architecture visualizations")
    parser.add_argument("type", nargs="?", default="all",
                       choices=["all", "system", "database", "api", "components", "flow", "security"],
                       help="Type of diagram to generate")
    parser.add_argument("--format", "-f", default="both",
                       choices=["ascii", "mermaid", "both"],
                       help="Output format")
    parser.add_argument("--arch-dir", default="docs/architecture",
                       help="Architecture directory path")
    parser.add_argument("--output", "-o", help="Output file (optional)")
    
    args = parser.parse_args()
    
    # Create visualizer and analyze
    viz = ArchitectureVisualizer(Path(args.arch_dir))
    viz.analyze_architecture()
    
    # Generate diagrams
    if args.type == "all":
        diagrams = viz.generate_all_diagrams(args.format)
    else:
        method = f"generate_{args.type}_diagram"
        diagrams = {args.type: getattr(viz, method)(args.format)}
    
    # Output results
    output_lines = []
    
    for diagram_type, formats in diagrams.items():
        output_lines.append(f"\n{'=' * 75}")
        output_lines.append(f"{diagram_type.upper()} DIAGRAM")
        output_lines.append('=' * 75)
        
        for format_type, content in formats.items():
            output_lines.append(f"\n--- {format_type.upper()} ---")
            output_lines.append(content)
            
            if format_type == "mermaid":
                output_lines.append("\n<!-- Copy above into Mermaid viewer: https://mermaid.live -->")
    
    output = "\n".join(output_lines)
    
    # Save or print
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✅ Visualizations saved to {args.output}")
    else:
        print(output)
        
    # Also save individual files if generating all
    if args.type == "all" and not args.output:
        save_dir = Path(args.arch_dir) / "visualizations"
        save_dir.mkdir(exist_ok=True)
        
        for diagram_type, formats in diagrams.items():
            for format_type, content in formats.items():
                filename = save_dir / f"{diagram_type}_{format_type}.txt"
                with open(filename, 'w') as f:
                    f.write(content)
                    
        print(f"\n✅ Individual diagrams saved to {save_dir}/")


if __name__ == "__main__":
    main()
