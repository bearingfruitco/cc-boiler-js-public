#!/usr/bin/env python3
"""
Architecture Validation Script
Validates architecture documentation for completeness, consistency, and quality
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

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
        self.prd_coverage_details = {}
        
    def validate(self, verbose: bool = False, fix: bool = False) -> Dict:
        """Main validation entry point"""
        results = {
            "score": 0,
            "grade": "F",
            "documents": {},
            "issues": [],
            "recommendations": [],
            "prd_coverage": 0,
            "prd_details": {}
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
        results["prd_coverage"], results["prd_details"] = self._check_prd_coverage()
        
        # Calculate final score
        total_score = self._calculate_score()
        results["score"] = total_score
        results["grade"] = self._get_grade(total_score)
        results["issues"] = self.issues
        results["recommendations"] = self.recommendations
        results["score_breakdown"] = self.scores
        
        # Apply fixes if requested
        if fix and self.issues:
            fixes_applied = self._apply_fixes()
            results["fixes_applied"] = fixes_applied
            
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
                    todos = len(re.findall(r'TODO|TBD|PLACEHOLDER|\[\]|XXX', content, re.I))
                    
                    # Check for actual content (not just template)
                    has_content = len(content.strip()) > 500  # More than just headers
                    
                status[doc] = {
                    "exists": True,
                    "lines": lines,
                    "todos": todos,
                    "complete": lines > 50 and todos == 0 and has_content,
                    "has_content": has_content
                }
                
                # Deduct points for incomplete documents
                if todos > 0:
                    self.scores["completeness"] -= 1
                if not has_content:
                    self.scores["completeness"] -= 2
            else:
                status[doc] = {
                    "exists": False,
                    "lines": 0,
                    "todos": 0,
                    "complete": False,
                    "has_content": False
                }
                self.issues.append(f"Missing required document: {doc}")
                self.scores["completeness"] -= 5
                
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
            ("Overview", r"#{1,3}\s*(System\s*)?Overview"),
            ("Components", r"#{1,3}\s*(System\s*)?Components?"),
            ("Data Flow", r"#{1,3}\s*Data\s*Flow"),
            ("Technology Stack", r"#{1,3}\s*(Technology|Tech)\s*Stack"),
            ("Infrastructure", r"#{1,3}\s*Infrastructure"),
            ("Monitoring", r"#{1,3}\s*(Monitoring|Observability)")
        ]
        
        for section_name, pattern in required_sections:
            if not re.search(pattern, content, re.I):
                self.issues.append(f"SYSTEM_DESIGN.md missing section: {section_name}")
                self.scores["completeness"] -= 2
                
        # Check for diagrams
        if not re.search(r'```|┌|└|│|--->', content):
            self.recommendations.append("Add system architecture diagrams to SYSTEM_DESIGN.md")
            self.scores["maintainability"] -= 1
            
        # Check for scalability considerations
        if not re.search(r'scal(e|ability|ing)|growth|load|performance', content, re.I):
            self.recommendations.append("Add scalability planning to SYSTEM_DESIGN.md")
            self.scores["scalability"] -= 2
            
    def _check_database_schema(self, content: str) -> None:
        """Validate database schema document"""
        # Check for SQL/schema definitions
        if not re.search(r'CREATE\s+TABLE|CREATE\s+SCHEMA|CREATE\s+INDEX', content, re.I):
            self.issues.append("DATABASE_SCHEMA.md missing actual schema definitions")
            self.scores["completeness"] -= 5
            
        # Check for relationships
        if not re.search(r'REFERENCES|FOREIGN\s+KEY|relationship|belongs_to|has_many', content, re.I):
            self.recommendations.append("Define table relationships in DATABASE_SCHEMA.md")
            self.scores["consistency"] -= 2
            
        # Check for RLS policies (Supabase specific)
        if not re.search(r'POLICY|RLS|Row\s+Level\s+Security|CREATE\s+POLICY', content, re.I):
            self.issues.append("DATABASE_SCHEMA.md missing RLS policies")
            self.scores["security"] -= 3
            
        # Check for indexes
        if not re.search(r'INDEX|CREATE\s+INDEX|KEY', content, re.I):
            self.recommendations.append("Add database indexes for performance in DATABASE_SCHEMA.md")
            self.scores["scalability"] -= 1
            
        # Check for migrations
        if not re.search(r'migration|migrate|ALTER\s+TABLE', content, re.I):
            self.recommendations.append("Add migration strategy to DATABASE_SCHEMA.md")
            
    def _check_api_spec(self, content: str) -> None:
        """Validate API specification"""
        # Check for endpoint definitions
        if not re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+/api/', content):
            self.issues.append("API_SPECIFICATION.md missing endpoint definitions")
            self.scores["completeness"] -= 5
            
        # Check for authentication
        if not re.search(r'auth(entication|orization)?|bearer|token|api[\s-]?key|JWT', content, re.I):
            self.issues.append("API_SPECIFICATION.md missing authentication details")
            self.scores["security"] -= 3
            
        # Check for error handling
        if not re.search(r'error|4\d{2}|5\d{2}|status[\s-]?code|exception', content, re.I):
            self.recommendations.append("Add error response documentation to API_SPECIFICATION.md")
            self.scores["maintainability"] -= 1
            
        # Check for rate limiting
        if not re.search(r'rate[\s-]?limit|throttl|quota|429', content, re.I):
            self.recommendations.append("Add rate limiting documentation to API_SPECIFICATION.md")
            self.scores["scalability"] -= 1
            
        # Check for versioning
        if not re.search(r'version|v\d|/api/v\d', content, re.I):
            self.recommendations.append("Add API versioning strategy to API_SPECIFICATION.md")
            
    def _check_frontend_arch(self, content: str) -> None:
        """Validate frontend architecture"""
        required_concepts = [
            ("Components", r"component|atomic|molecule|organism"),
            ("State Management", r"state|zustand|redux|context"),
            ("Routing", r"rout(e|ing)|navigation|page"),
            ("Performance", r"performance|optimization|lazy|split|cache"),
            ("Design System", r"design\s*system|theme|styling|tailwind")
        ]
        
        for concept_name, pattern in required_concepts:
            if not re.search(pattern, content, re.I):
                self.recommendations.append(f"Add {concept_name} details to FRONTEND_ARCHITECTURE.md")
                if concept_name in ["Components", "State Management"]:
                    self.scores["completeness"] -= 1
                    
        # Check for accessibility
        if not re.search(r'a11y|accessibility|ARIA|screen\s*reader', content, re.I):
            self.recommendations.append("Add accessibility considerations to FRONTEND_ARCHITECTURE.md")
            
    def _check_security_design(self, content: str) -> None:
        """Validate security design"""
        # Check for threat model
        if not re.search(r'threat(\s+model)?|STRIDE|OWASP|vulnerability|attack', content, re.I):
            self.issues.append("SECURITY_DESIGN.md missing threat model")
            self.scores["security"] -= 5
            
        # Check for security controls
        if not re.search(r'control|mitigation|protection|encryption|sanitiz|validat', content, re.I):
            self.issues.append("SECURITY_DESIGN.md missing security controls")
            self.scores["security"] -= 3
            
        # Check for compliance
        if not re.search(r'complian|GDPR|CCPA|HIPAA|SOC|privacy', content, re.I):
            self.recommendations.append("Add compliance requirements to SECURITY_DESIGN.md")
            
        # Check for authentication/authorization
        if not re.search(r'authenticat|authoriz|RBAC|permission|role', content, re.I):
            self.issues.append("SECURITY_DESIGN.md missing auth details")
            self.scores["security"] -= 2
            
    def _check_roadmap(self, content: str) -> None:
        """Validate technical roadmap"""
        # Check for phases
        if not re.search(r'Phase|Sprint|Week|Milestone|Timeline', content, re.I):
            self.issues.append("TECHNICAL_ROADMAP.md missing timeline/phases")
            self.scores["completeness"] -= 3
            
        # Check for dependencies
        if not re.search(r'depend(enc)?|prerequisite|block(er|ing)|require', content, re.I):
            self.recommendations.append("Add dependency tracking to TECHNICAL_ROADMAP.md")
            
        # Check for deliverables
        if not re.search(r'deliverable|output|result|complete', content, re.I):
            self.recommendations.append("Add clear deliverables to TECHNICAL_ROADMAP.md")
            
        # Check for risk assessment
        if not re.search(r'risk|mitigation|contingency|fallback', content, re.I):
            self.recommendations.append("Add risk assessment to TECHNICAL_ROADMAP.md")
            
    def _validate_consistency(self) -> None:
        """Cross-document consistency checks"""
        tech_mentions = {
            "nextjs": [],
            "supabase": [],
            "typescript": [],
            "tailwind": [],
            "postgres": []
        }
        
        # Collect technology mentions across documents
        for doc in self.required_docs:
            path = self.arch_dir / doc
            if path.exists():
                with open(path, 'r') as f:
                    content = f.read()
                    
                    # Track where each technology is mentioned
                    if re.search(r'Next\.js|NextJS|next\.js', content, re.I):
                        tech_mentions["nextjs"].append(doc)
                    if re.search(r'Supabase', content, re.I):
                        tech_mentions["supabase"].append(doc)
                    if re.search(r'TypeScript|\.ts|\.tsx', content, re.I):
                        tech_mentions["typescript"].append(doc)
                    if re.search(r'Tailwind|tailwindcss', content, re.I):
                        tech_mentions["tailwind"].append(doc)
                    if re.search(r'PostgreSQL|Postgres|psql', content, re.I):
                        tech_mentions["postgres"].append(doc)
        
        # Check consistency
        tech_count = sum(1 for tech, docs in tech_mentions.items() if len(docs) > 0)
        if tech_count >= 3:  # At least 3 technologies mentioned
            self.scores["consistency"] += 5
            
        # Check if core technologies are mentioned in multiple docs
        for tech, docs in tech_mentions.items():
            if len(docs) >= 3:  # Mentioned in at least 3 documents
                self.scores["consistency"] += 1
                
        # Check for contradictions (would need more sophisticated logic)
        # For now, give bonus points if no obvious issues
        self.scores["consistency"] += 5
            
    def _check_prd_coverage(self) -> Tuple[float, Dict]:
        """Check how well architecture covers PRD requirements"""
        prd_paths = [
            Path("docs/project/PROJECT_PRD.md"),
            Path("PROJECT_PRD.md"),
            Path("docs/PROJECT_PRD.md")
        ]
        
        prd_content = None
        for path in prd_paths:
            if path.exists():
                with open(path, 'r') as f:
                    prd_content = f.read()
                break
                
        if not prd_content:
            return 100.0, {"status": "No PRD found"}
            
        # Extract features/requirements from PRD
        feature_patterns = [
            r'(?:^|\n)#+\s*(?:Feature|Requirement|User Story):\s*(.+)',
            r'(?:^|\n)-\s*(?:As a|Feature|Must have):\s*(.+)',
            r'(?:^|\n)\d+\.\s*(.+(?:feature|requirement|functionality))',
        ]
        
        features = []
        for pattern in feature_patterns:
            matches = re.findall(pattern, prd_content, re.I | re.M)
            features.extend(matches)
            
        if not features:
            # Try to extract from sections
            section_pattern = r'(?:^|\n)#+\s*(.+?)(?:\n|$)'
            sections = re.findall(section_pattern, prd_content)
            features = [s for s in sections if any(word in s.lower() for word in 
                       ['feature', 'requirement', 'functionality', 'capability'])]
        
        if not features:
            return 100.0, {"status": "No clear features found in PRD"}
            
        # Check coverage in architecture docs
        coverage_details = {}
        total_features = len(features)
        covered_features = 0
        
        # Combine all architecture content
        arch_content = ""
        for doc in self.required_docs:
            path = self.arch_dir / doc
            if path.exists():
                with open(path, 'r') as f:
                    arch_content += f.read() + "\n"
                    
        for feature in features:
            feature_clean = feature.strip()
            # Simple keyword matching (could be more sophisticated)
            if any(word in arch_content.lower() for word in feature_clean.lower().split()[:3]):
                covered_features += 1
                coverage_details[feature_clean] = "✅ Covered"
            else:
                coverage_details[feature_clean] = "❌ Not found"
                self.recommendations.append(f"Address PRD requirement: {feature_clean[:50]}...")
                
        coverage_percent = (covered_features / total_features * 100) if total_features > 0 else 100.0
        
        # Adjust requirements score based on coverage
        if coverage_percent >= 90:
            self.scores["requirements"] += 5
        elif coverage_percent >= 80:
            self.scores["requirements"] += 3
        elif coverage_percent >= 70:
            self.scores["requirements"] += 1
        else:
            self.scores["requirements"] -= 5
            
        return coverage_percent, coverage_details
    
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
            
        # Ensure no negative scores and cap at max
        for category, max_score in base_scores.items():
            self.scores[category] = max(0, min(self.scores[category], max_score))
            
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
        
    def _apply_fixes(self) -> List[str]:
        """Apply automatic fixes where possible"""
        fixes_applied = []
        
        for issue in self.issues:
            if "missing section:" in issue:
                # Add TODO markers for missing sections
                doc_name = issue.split()[0]
                section = issue.split(":")[-1].strip()
                if self._add_todo_section(doc_name, section):
                    fixes_applied.append(f"Added TODO section '{section}' to {doc_name}")
                    
            elif "Missing required document:" in issue:
                # Create missing document from template
                doc_name = issue.split()[-1]
                if self._create_from_template(doc_name):
                    fixes_applied.append(f"Created {doc_name} from template")
                    
        return fixes_applied
                
    def _add_todo_section(self, doc_name: str, section: str) -> bool:
        """Add a TODO section to document"""
        path = self.arch_dir / doc_name
        if path.exists():
            with open(path, 'a') as f:
                f.write(f"\n\n## {section}\n\n")
                f.write(f"TODO: Complete this section\n\n")
                f.write(f"Key points to cover:\n")
                
                # Add section-specific hints
                if "threat" in section.lower():
                    f.write("- STRIDE analysis\n")
                    f.write("- Attack vectors\n")
                    f.write("- Risk assessment\n")
                elif "component" in section.lower():
                    f.write("- Component hierarchy\n")
                    f.write("- Interfaces and contracts\n")
                    f.write("- Dependencies\n")
                elif "data flow" in section.lower():
                    f.write("- Input sources\n")
                    f.write("- Processing stages\n")
                    f.write("- Output destinations\n")
                else:
                    f.write("- Overview\n")
                    f.write("- Key concepts\n")
                    f.write("- Implementation details\n")
                    
                f.write(f"\n<!-- Generated by architecture validator on {datetime.now().isoformat()} -->\n")
            return True
        return False
        
    def _create_from_template(self, doc_name: str) -> bool:
        """Create missing document from template"""
        template_path = Path(".claude/templates/architecture") / doc_name
        target_path = self.arch_dir / doc_name
        
        # Ensure architecture directory exists
        self.arch_dir.mkdir(parents=True, exist_ok=True)
        
        if template_path.exists():
            # Copy template
            with open(template_path, 'r') as src, open(target_path, 'w') as dst:
                dst.write(src.read())
            return True
        else:
            # Create minimal template
            with open(target_path, 'w') as f:
                f.write(f"# {doc_name.replace('.md', '').replace('_', ' ').title()}\n\n")
                f.write(f"TODO: Complete this document\n\n")
                f.write(f"<!-- Generated by architecture validator on {datetime.now().isoformat()} -->\n")
            return True
            
    def generate_report(self, results: Dict, verbose: bool = False) -> str:
        """Generate formatted validation report"""
        report = []
        report.append("\n🏗️  Architecture Validation Report")
        report.append("=" * 50)
        
        # Overall score
        report.append(f"\n📊 Overall Score: {results['grade']} ({results['score']}/100)")
        
        # Document status
        report.append("\n📋 Document Status:")
        for doc, status in results["documents"].items():
            icon = "✅" if status["complete"] else "⚠️ " if status["exists"] else "❌"
            line = f"{icon} {doc:<30} - "
            if status["exists"]:
                line += f"{'Complete' if status['complete'] else 'Incomplete'}"
                line += f" ({status['lines']} lines"
                if status['todos'] > 0:
                    line += f", {status['todos']} TODOs"
                line += ")"
            else:
                line += "Missing"
            report.append(line)
        
        # Quality breakdown
        report.append("\n🎯 Quality Breakdown:")
        max_scores = {
            "completeness": 25, "consistency": 20, "requirements": 20,
            "security": 15, "scalability": 10, "maintainability": 10
        }
        
        for category, score in results["score_breakdown"].items():
            max_score = max_scores[category]
            percentage = (score / max_score) * 100 if max_score > 0 else 0
            bar_length = int(percentage / 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            report.append(f"{category.title():<15} {bar} {score:>2}/{max_score} pts")
        
        # Issues
        if results["issues"]:
            report.append(f"\n⚠️  Issues Found ({len(results['issues'])}):")
            for i, issue in enumerate(results["issues"], 1):
                report.append(f"{i}. {issue}")
        else:
            report.append("\n✅ No critical issues found!")
        
        # Recommendations
        if results["recommendations"]:
            report.append(f"\n✨ Recommendations:")
            for i, rec in enumerate(results["recommendations"], 1):
                report.append(f"{i}. {rec}")
        
        # PRD Coverage
        report.append(f"\n📌 PRD Requirement Coverage: {results['prd_coverage']:.0f}%")
        
        if verbose and isinstance(results["prd_details"], dict) and "status" not in results["prd_details"]:
            report.append("\nDetailed PRD Coverage:")
            for feature, status in results["prd_details"].items():
                report.append(f"  {status} {feature[:60]}{'...' if len(feature) > 60 else ''}")
        
        # Fixes applied
        if "fixes_applied" in results and results["fixes_applied"]:
            report.append(f"\n🔧 Fixes Applied:")
            for fix in results["fixes_applied"]:
                report.append(f"  ✓ {fix}")
        
        # Next steps
        report.append("\n🚀 Next Steps:")
        if results["score"] < 70:
            report.append("1. Address critical issues listed above")
            report.append("2. Run `/spawn system-architect` for help with missing sections")
            report.append("3. Use `/va --fix` to auto-generate missing content")
            report.append("4. Aim for score > 70 before generating issues")
        elif results["score"] < 85:
            report.append("1. Address remaining issues for better quality")
            report.append("2. Consider recommendations for improvement")
            report.append("3. Target score > 85 for best results")
        else:
            report.append("1. Architecture is ready for implementation!")
            report.append("2. Run `/gi PROJECT` to generate issues")
            report.append("3. Use `/chain architecture-design` for updates")
        
        # Grade scale
        report.append("\nGrade Scale:")
        report.append("A+ (95-100) | A (90-94) | B+ (85-89) | B (80-84) | C (70-79) | D (60-69) | F (<60)")
        
        # Pass/fail
        if results["score"] >= 70:
            report.append("\n✅ Architecture validation PASSED")
        else:
            report.append("\n❌ Architecture validation FAILED (minimum score: 70)")
            
        return "\n".join(report)


def main():
    """Main entry point for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate architecture documentation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed analysis")
    parser.add_argument("--fix", "-f", action="store_true", help="Attempt to fix issues")
    parser.add_argument("--score-only", "-s", action="store_true", help="Only show score")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON format")
    parser.add_argument("--arch-dir", default="docs/architecture", help="Architecture directory")
    
    args = parser.parse_args()
    
    # Run validation
    validator = ArchitectureValidator(Path(args.arch_dir))
    results = validator.validate(verbose=args.verbose, fix=args.fix)
    
    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    elif args.score_only:
        print(f"Score: {results['score']}/100 ({results['grade']})")
    else:
        report = validator.generate_report(results, verbose=args.verbose)
        print(report)
    
    # Exit with appropriate code
    sys.exit(0 if results["score"] >= 70 else 1)


if __name__ == "__main__":
    main()
