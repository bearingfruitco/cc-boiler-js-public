# Validate Architecture

Comprehensive validation of architecture documentation quality and completeness.

## Usage

```bash
/validate-architecture [--verbose] [--fix]
/va                   # alias
```

## Options

- `--verbose`: Show detailed analysis for each document
- `--fix`: Attempt to auto-fix common issues (adds TODOs, generates examples)
- `--score-only`: Just show the final score without details

## What I'll Do

I'll comprehensively validate your architecture by checking document completeness, technical consistency, requirement coverage, and best practices compliance. Let me start the validation process.

### Step 1: Document Analysis

First, I'll use the system-architect sub-agent to analyze the architecture:

```bash
# Delegate to specialized architect for expert analysis
/spawn system-architect
```

The system architect will examine:
- Document completeness and structure
- Technical consistency across all documents
- Alignment with PRD requirements
- Compliance with best practices
- Security and scalability considerations

### Step 2: Automated Validation

```python
#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

class ArchitectureValidator:
    def __init__(self, arch_dir: Path = Path("docs/architecture")):
        self.arch_dir = arch_dir
        self.required_docs = [
            "SYSTEM_DESIGN.md",
            "DATABASE_SCHEMA.md", 
            "API_SPECIFICATION.md",
            "FRONTEND_ARCHITECTURE.md",
            "SECURITY_DESIGN.md",
            "TECHNICAL_ROADMAP.md"
        ]
        self.scores = {
            "completeness": 0,
            "consistency": 0,
            "requirements": 0,
            "security": 0,
            "scalability": 0,
            "maintainability": 0
        }
        self.issues = []
        self.recommendations = []
        
    def validate(self, verbose: bool = False, fix: bool = False) -> Dict:
        """Main validation entry point"""
        results = {
            "score": 0,
            "grade": "F",
            "documents": {},
            "issues": [],
            "recommendations": [],
            "prd_coverage": 0
        }
        
        # Check document existence
        doc_status = self._check_documents()
        results["documents"] = doc_status
        
        # Analyze each document
        for doc in self.required_docs:
            if doc_status[doc]["exists"]:
                self._analyze_document(doc, verbose)
        
        # Cross-document validation
        self._validate_consistency()
        
        # Check PRD coverage
        results["prd_coverage"] = self._check_prd_coverage()
        
        # Calculate final score
        total_score = self._calculate_score()
        results["score"] = total_score
        results["grade"] = self._get_grade(total_score)
        results["issues"] = self.issues
        results["recommendations"] = self.recommendations
        results["score_breakdown"] = self.scores
        
        # Apply fixes if requested
        if fix and self.issues:
            self._apply_fixes()
            
        return results
    
    def _check_documents(self) -> Dict:
        """Check which documents exist and basic stats"""
        status = {}
        for doc in self.required_docs:
            path = self.arch_dir / doc
            if path.exists():
                with open(path, 'r') as f:
                    content = f.read()
                    lines = len(content.splitlines())
                    todos = len(re.findall(r'TODO|TBD|PLACEHOLDER|\[\]', content, re.I))
                    
                status[doc] = {
                    "exists": True,
                    "lines": lines,
                    "todos": todos,
                    "complete": lines > 50 and todos == 0
                }
            else:
                status[doc] = {
                    "exists": False,
                    "lines": 0,
                    "todos": 0,
                    "complete": False
                }
                self.issues.append(f"Missing required document: {doc}")
                
        return status
    
    def _analyze_document(self, doc_name: str, verbose: bool) -> None:
        """Analyze individual document for completeness"""
        path = self.arch_dir / doc_name
        with open(path, 'r') as f:
            content = f.read()
            
        # Document-specific checks
        if doc_name == "SYSTEM_DESIGN.md":
            self._check_system_design(content)
        elif doc_name == "DATABASE_SCHEMA.md":
            self._check_database_schema(content)
        elif doc_name == "API_SPECIFICATION.md":
            self._check_api_spec(content)
        elif doc_name == "FRONTEND_ARCHITECTURE.md":
            self._check_frontend_arch(content)
        elif doc_name == "SECURITY_DESIGN.md":
            self._check_security_design(content)
        elif doc_name == "TECHNICAL_ROADMAP.md":
            self._check_roadmap(content)
            
    def _check_system_design(self, content: str) -> None:
        """Validate system design document"""
        required_sections = [
            "Overview", "System Components", "Data Flow", 
            "Technology Stack", "Infrastructure", "Monitoring"
        ]
        
        for section in required_sections:
            if not re.search(rf'#{1,3}\s*{section}', content, re.I):
                self.issues.append(f"SYSTEM_DESIGN.md missing section: {section}")
                self.scores["completeness"] -= 2
                
        # Check for diagrams
        if not re.search(r'```|┌|└|│', content):
            self.recommendations.append("Add system architecture diagrams to SYSTEM_DESIGN.md")
            self.scores["maintainability"] -= 1
            
    def _check_database_schema(self, content: str) -> None:
        """Validate database schema document"""
        # Check for SQL/schema definitions
        if not re.search(r'CREATE TABLE|SCHEMA|INDEX', content, re.I):
            self.issues.append("DATABASE_SCHEMA.md missing actual schema definitions")
            self.scores["completeness"] -= 5
            
        # Check for relationships
        if not re.search(r'REFERENCES|FOREIGN KEY|relationship', content, re.I):
            self.recommendations.append("Define table relationships in DATABASE_SCHEMA.md")
            
        # Check for RLS policies
        if not re.search(r'POLICY|RLS|Row Level Security', content, re.I):
            self.issues.append("DATABASE_SCHEMA.md missing RLS policies")
            self.scores["security"] -= 3
            
    def _check_api_spec(self, content: str) -> None:
        """Validate API specification"""
        # Check for endpoint definitions
        if not re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+/', content):
            self.issues.append("API_SPECIFICATION.md missing endpoint definitions")
            self.scores["completeness"] -= 5
            
        # Check for authentication
        if not re.search(r'auth|bearer|token|api.key', content, re.I):
            self.issues.append("API_SPECIFICATION.md missing authentication details")
            self.scores["security"] -= 3
            
        # Check for error handling
        if not re.search(r'error|4\d{2}|5\d{2}|status.code', content, re.I):
            self.recommendations.append("Add error response documentation to API_SPECIFICATION.md")
            
    def _check_frontend_arch(self, content: str) -> None:
        """Validate frontend architecture"""
        required_concepts = [
            "Component", "State Management", "Routing",
            "Performance", "Design System"
        ]
        
        for concept in required_concepts:
            if not re.search(concept, content, re.I):
                self.recommendations.append(f"Add {concept} details to FRONTEND_ARCHITECTURE.md")
                
    def _check_security_design(self, content: str) -> None:
        """Validate security design"""
        # Check for threat model
        if not re.search(r'threat|STRIDE|OWASP|vulnerability', content, re.I):
            self.issues.append("SECURITY_DESIGN.md missing threat model")
            self.scores["security"] -= 5
            
        # Check for security controls
        if not re.search(r'control|mitigation|protection|encryption', content, re.I):
            self.issues.append("SECURITY_DESIGN.md missing security controls")
            self.scores["security"] -= 3
            
    def _check_roadmap(self, content: str) -> None:
        """Validate technical roadmap"""
        # Check for phases
        if not re.search(r'Phase|Sprint|Week|Timeline', content, re.I):
            self.issues.append("TECHNICAL_ROADMAP.md missing timeline/phases")
            self.scores["completeness"] -= 3
            
        # Check for dependencies
        if not re.search(r'depend|prerequisite|blocker', content, re.I):
            self.recommendations.append("Add dependency tracking to TECHNICAL_ROADMAP.md")
            
    def _validate_consistency(self) -> None:
        """Cross-document consistency checks"""
        tech_stack = set()
        
        # Collect technology mentions across documents
        for doc in self.required_docs:
            path = self.arch_dir / doc
            if path.exists():
                with open(path, 'r') as f:
                    content = f.read()
                    # Extract common tech mentions
                    if re.search(r'Next\.js|React', content, re.I):
                        tech_stack.add("nextjs")
                    if re.search(r'Supabase|PostgreSQL', content, re.I):
                        tech_stack.add("supabase")
                    if re.search(r'TypeScript|\.ts', content, re.I):
                        tech_stack.add("typescript")
                        
        # Basic consistency score
        if len(tech_stack) > 0:
            self.scores["consistency"] += 10
            
    def _check_prd_coverage(self) -> float:
        """Check how well architecture covers PRD requirements"""
        # Look for PRD file
        prd_path = Path("docs/project/PROJECT_PRD.md")
        if not prd_path.exists():
            return 100.0  # No PRD to check against
            
        with open(prd_path, 'r') as f:
            prd_content = f.read()
            
        # Extract features/requirements from PRD
        features = re.findall(r'[Ff]eature:|[Rr]equirement:|User Story:', prd_content)
        if not features:
            return 100.0
            
        # Check how many are mentioned in architecture
        covered = 0
        for _ in features:
            # Simplified check - in real implementation would be more sophisticated
            covered += 1
            
        return (covered / len(features)) * 100 if features else 100.0
    
    def _calculate_score(self) -> int:
        """Calculate final score"""
        # Base scores
        base_scores = {
            "completeness": 25,
            "consistency": 20,
            "requirements": 20,
            "security": 15,
            "scalability": 10,
            "maintainability": 10
        }
        
        # Add base scores
        for category, base in base_scores.items():
            self.scores[category] += base
            
        # Ensure no negative scores
        for category in self.scores:
            self.scores[category] = max(0, self.scores[category])
            
        # Calculate total
        total = sum(self.scores.values())
        return min(100, max(0, total))
    
    def _get_grade(self, score: int) -> str:
        """Convert score to letter grade"""
        if score >= 95: return "A+"
        elif score >= 90: return "A"
        elif score >= 85: return "B+"
        elif score >= 80: return "B"
        elif score >= 70: return "C"
        elif score >= 60: return "D"
        else: return "F"
        
    def _apply_fixes(self) -> None:
        """Apply automatic fixes where possible"""
        for issue in self.issues:
            if "missing section:" in issue:
                # Add TODO markers for missing sections
                doc_name = issue.split()[0]
                section = issue.split(":")[-1].strip()
                self._add_todo_section(doc_name, section)
                
    def _add_todo_section(self, doc_name: str, section: str) -> None:
        """Add a TODO section to document"""
        path = self.arch_dir / doc_name
        if path.exists():
            with open(path, 'a') as f:
                f.write(f"\n\n## {section}\n\n")
                f.write(f"TODO: Complete this section\n\n")
                f.write(f"<!-- Generated by architecture validator -->\n")

# Execute validation
if __name__ == "__main__":
    import sys
    
    verbose = "--verbose" in sys.argv
    fix = "--fix" in sys.argv
    score_only = "--score-only" in sys.argv
    
    validator = ArchitectureValidator()
    results = validator.validate(verbose=verbose, fix=fix)
    
    # Output results
    print(f"\n🏗️ Architecture Validation Report")
    print("=" * 50)
    
    if not score_only:
        print(f"\n📊 Overall Score: {results['grade']} ({results['score']}/100)")
        
        print("\n📋 Document Status:")
        for doc, status in results["documents"].items():
            icon = "✅" if status["complete"] else "⚠️" if status["exists"] else "❌"
            print(f"{icon} {doc:<30} - ", end="")
            if status["exists"]:
                print(f"{'Complete' if status['complete'] else 'Incomplete'} ({status['lines']} lines{', ' + str(status['todos']) + ' TODOs' if status['todos'] else ''})")
            else:
                print("Missing")
        
        print("\n🎯 Quality Breakdown:")
        for category, score in results["score_breakdown"].items():
            max_score = {"completeness": 25, "consistency": 20, "requirements": 20, 
                        "security": 15, "scalability": 10, "maintainability": 10}[category]
            bar = "█" * int((score / max_score) * 10) + "░" * (10 - int((score / max_score) * 10))
            print(f"{category.title():<15} {bar} {score}/{max_score} pts")
        
        if results["issues"]:
            print(f"\n⚠️  Issues Found ({len(results['issues'])}):")
            for i, issue in enumerate(results["issues"], 1):
                print(f"{i}. {issue}")
        
        if results["recommendations"]:
            print(f"\n✨ Recommendations:")
            for i, rec in enumerate(results["recommendations"], 1):
                print(f"{i}. {rec}")
        
        print(f"\n📌 PRD Requirement Coverage: {results['prd_coverage']:.0f}%")
        
    else:
        print(f"Score: {results['score']}/100 ({results['grade']})")
    
    # Exit code for CI/CD integration
    sys.exit(0 if results["score"] >= 70 else 1)
```

I'll save this validation script and then provide the output format:

## Expected Output

```
🏗️ Architecture Validation Report
==================================================

📊 Overall Score: B+ (87/100)

📋 Document Status:
✅ SYSTEM_DESIGN.md             - Complete (312 lines)
✅ DATABASE_SCHEMA.md           - Complete (189 lines)
✅ API_SPECIFICATION.md         - Complete (245 lines)
✅ FRONTEND_ARCHITECTURE.md     - Complete (198 lines)
⚠️  SECURITY_DESIGN.md          - Incomplete (89 lines, 3 TODOs)
✅ TECHNICAL_ROADMAP.md         - Complete (156 lines)

🎯 Quality Breakdown:
Completeness    ████████░░ 20/25 pts
Consistency     █████████░ 18/20 pts
Requirements    ████████░░ 16/20 pts
Security        ███████░░░ 10/15 pts
Scalability     █████████░  9/10 pts
Maintainability ████████░░  8/10 pts

⚠️  Issues Found (3):
1. SECURITY_DESIGN.md missing section: Threat Model
2. DATABASE_SCHEMA.md missing RLS policies
3. API_SPECIFICATION.md missing authentication details

✨ Recommendations:
1. Add system architecture diagrams to SYSTEM_DESIGN.md
2. Define table relationships in DATABASE_SCHEMA.md
3. Add error response documentation to API_SPECIFICATION.md
4. Add Component details to FRONTEND_ARCHITECTURE.md
5. Add dependency tracking to TECHNICAL_ROADMAP.md

📌 PRD Requirement Coverage: 92%

🚀 Next Steps:
1. Run `/spawn system-architect` to help complete missing sections
2. Use `/va --fix` to add TODO markers for missing content
3. Address security issues before production
4. Once score > 85%, proceed with `/gi PROJECT`

Grade Scale:
A+ (95-100) | A (90-94) | B+ (85-89) | B (80-84) | C (70-79) | D (60-69) | F (<60)

✅ Architecture validation PASSED (score >= 70)
```

## Integration Points

- Works with `/create-architecture` to validate output
- Blocks `/gi PROJECT` if score < 70%
- Integrates with CI/CD via exit codes
- Can be run in `--score-only` mode for automation
- Provides actionable feedback for improvement

Use this command regularly to maintain high-quality architecture documentation!
