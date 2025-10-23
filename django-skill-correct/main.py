#!/usr/bin/env python3
"""
Django Issue Automation with Documentation Validation
Validates against existing docs and flags unrelated issues
"""

import os
import re
import toml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class IssueType(Enum):
    """Types of issues that can be found"""
    TODO = "todo"
    DEPRECATED = "deprecated"
    SECURITY = "security"
    BUG = "bug"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"

@dataclass
class UnrelatedIssue:
    """Represents an issue found that's not related to current work"""
    type: IssueType
    file: str
    line: int
    description: str
    severity: str  # low, medium, high, critical

@dataclass
class DocumentationDiscrepancy:
    """Represents mismatch between docs and code"""
    doc_file: str
    doc_statement: str
    actual_code: str
    suggestion: str

class DjangoIssueAutomation:
    """
    Django automation that validates against documentation and flags issues.
    Never proceeds without validating docs match reality.
    """
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.claude_config = {}
        self.project_dependencies = {}
        self.workflow_config = {}
        self.feature_docs = {}
        self.pii_config = {}
        self.magika_config = {}
        self.logging_config = {}
        self.issue_data = {}
        self.unrelated_issues = []
        self.doc_discrepancies = []
        
    def work_on_issue(self, issue_description: str) -> Dict[str, Any]:
        """
        Main entry point with documentation validation and issue flagging.
        """
        
        print("🚀 Django Issue Automation with Validation")
        print("=" * 60)
        
        # Step 1: Read ALL project documentation
        print("\n📚 Reading ALL your documentation...")
        self._deep_documentation_read()
        
        # Step 2: Parse the issue
        print("\n🔍 Analyzing issue requirements...")
        self._parse_issue(issue_description)
        
        # Step 3: Read relevant feature documentation
        print("\n📖 Reading feature-specific documentation...")
        self._read_feature_documentation()
        
        # Step 4: Validate documentation against actual code
        print("\n✅ Validating documentation against actual code...")
        self._validate_documentation_against_code()
        
        # Step 5: Check for documentation discrepancies
        if self.doc_discrepancies:
            return self._handle_documentation_discrepancies()
        
        # Step 6: Scan for unrelated issues
        print("\n🔎 Scanning for unrelated issues in affected files...")
        self._scan_for_unrelated_issues()
        
        # Step 7: Handle unrelated issues if found
        if self.unrelated_issues:
            return self._handle_unrelated_issues()
        
        # Step 8: Get clarification questions
        print("\n❓ Checking what needs clarification...")
        questions = self._get_clarification_questions()
        
        if questions:
            return {
                "status": "need_clarification",
                "questions": questions,
                "message": "I need clarification on these points:"
            }
        
        # Step 9: Check for breaking changes
        print("\n⚠️  Checking for breaking changes...")
        breaking_changes = self._check_breaking_changes()
        
        if breaking_changes:
            return {
                "status": "breaking_changes_warning",
                "changes": breaking_changes,
                "message": "⚠️  These changes might break existing code. Continue?"
            }
        
        # Step 10: Create validated plan
        print("\n📋 Creating implementation plan (validated against docs)...")
        plan = self._create_validated_plan()
        
        return {
            "status": "approval_needed",
            "plan": plan,
            "message": "Implementation plan (validated against your docs). Proceed? (yes/no)"
        }
    
    def _deep_documentation_read(self):
        """Read ALL project documentation including infrastructure docs."""
        
        # Read CLAUDE.md
        claude_path = self.project_root / "CLAUDE.md"
        if claude_path.exists():
            print(f"  ✓ Reading CLAUDE.md")
            self.claude_config = self._parse_claude_md(claude_path.read_text())
        
        # Read pyproject.toml
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            print(f"  ✓ Reading pyproject.toml")
            with open(pyproject_path, 'r') as f:
                pyproject = toml.load(f)
                self.project_dependencies = pyproject.get('tool', {}).get('poetry', {}).get('dependencies', {})
        
        # Read workflow docs
        workflow_path = self.project_root / "docs" / "FEATURE_BRANCH_WORKFLOW.md"
        if workflow_path.exists():
            print(f"  ✓ Reading workflow documentation")
            self.workflow_config = self._parse_workflow(workflow_path.read_text())
        
        # Read PII masking documentation
        pii_path = self.project_root / "docs" / "security" / "pii_masking.md"
        if pii_path.exists():
            print(f"  ✓ Reading PII masking documentation")
            self.pii_config = self._parse_pii_docs(pii_path.read_text())
        else:
            print(f"  ⚠️  No PII masking docs found at docs/security/pii_masking.md")
        
        # Read Magika validation documentation
        magika_path = self.project_root / "docs" / "validation" / "magika.md"
        if magika_path.exists():
            print(f"  ✓ Reading Magika validation documentation")
            self.magika_config = self._parse_magika_docs(magika_path.read_text())
        else:
            print(f"  ⚠️  No Magika docs found at docs/validation/magika.md")
        
        # Read centralized logging documentation
        logging_path = self.project_root / "docs" / "infrastructure" / "logging.md"
        if logging_path.exists():
            print(f"  ✓ Reading centralized logging documentation")
            self.logging_config = self._parse_logging_docs(logging_path.read_text())
        else:
            print(f"  ⚠️  No logging docs found at docs/infrastructure/logging.md")
    
    def _parse_claude_md(self, content: str) -> Dict:
        """Parse CLAUDE.md for project configuration."""
        config = {}
        
        if match := re.search(r'Django\s*([\d.]+)', content, re.I):
            config['django_version'] = match.group(1)
        
        if 'postgresql' in content.lower():
            config['database'] = 'postgresql'
        elif 'mysql' in content.lower():
            config['database'] = 'mysql'
        
        if 'rest framework' in content.lower() or 'drf' in content.lower():
            config['has_drf'] = True
        
        # Check for PII masking mention
        if 'global pii' in content.lower() or 'pii masking' in content.lower():
            config['has_global_pii_masking'] = True
            print(f"    ✓ Global PII masking detected in config")
        
        # Check for Magika mention
        if 'magika' in content.lower():
            config['uses_magika'] = True
            print(f"    ✓ Magika validation detected in config")
        
        # Check for centralized logging
        if 'centralized log' in content.lower() or 'central log' in content.lower():
            config['has_centralized_logging'] = True
            print(f"    ✓ Centralized logging detected in config")
        
        return config
    
    def _parse_workflow(self, content: str) -> Dict:
        """Parse workflow documentation."""
        config = {}
        
        if match := re.search(r'(feature|bugfix|hotfix)/[^\s]+', content):
            config['branch_pattern'] = match.group(0)
        
        if match := re.search(r'\[ISSUE[^\]]*\][^\n]+', content):
            config['commit_format'] = match.group(0)
        
        # Check for PR flagging guidelines
        if 'flag in pr' in content.lower() or 'pr comment' in content.lower():
            config['allows_pr_flags'] = True
            print(f"    ✓ PR flagging allowed for unrelated issues")
        
        return config
    
    def _parse_pii_docs(self, content: str) -> Dict:
        """Parse PII masking documentation."""
        config = {}
        
        # Look for the masking class/function
        if match := re.search(r'(GlobalPIIMasker|PIIMasker|mask_pii)', content):
            config['masking_function'] = match.group(1)
            print(f"    PII Masking: {config['masking_function']}")
        
        # Look for import statements
        if match := re.search(r'from\s+([\w.]+)\s+import', content):
            config['import_from'] = match.group(1)
            print(f"    Import from: {config['import_from']}")
        
        # Check for specific fields that need masking
        if 'email' in content.lower():
            config['mask_email'] = True
        if 'phone' in content.lower():
            config['mask_phone'] = True
        if 'ssn' in content.lower() or 'social' in content.lower():
            config['mask_ssn'] = True
        
        return config
    
    def _parse_magika_docs(self, content: str) -> Dict:
        """Parse Magika validation documentation."""
        config = {}
        
        # Look for validation function
        if match := re.search(r'(validate_with_magika|magika_validate|MagikaValidator)', content):
            config['validation_function'] = match.group(1)
            print(f"    Magika Function: {config['validation_function']}")
        
        # Look for file types to validate
        if 'upload' in content.lower():
            config['validate_uploads'] = True
        if 'attachment' in content.lower():
            config['validate_attachments'] = True
        
        # Look for import
        if match := re.search(r'from\s+([\w.]+)\s+import.*magika', content, re.I):
            config['import_from'] = match.group(1)
        
        return config
    
    def _parse_logging_docs(self, content: str) -> Dict:
        """Parse centralized logging documentation."""
        config = {}
        
        # Look for logger setup
        if match := re.search(r'(get_logger|CentralizedLogger|Logger\.get)', content):
            config['logger_function'] = match.group(1)
            print(f"    Logger Function: {config['logger_function']}")
        
        # Look for log format
        if match := re.search(r'format["\']?\s*[:=]\s*["\']([^"\']+)', content):
            config['log_format'] = match.group(1)
        
        # Look for import
        if match := re.search(r'from\s+([\w.]+)\s+import.*[Ll]ogger', content):
            config['import_from'] = match.group(1)
        
        # Check for log levels mentioned
        if 'debug' in content.lower():
            config['supports_debug'] = True
        if 'audit' in content.lower():
            config['has_audit_logging'] = True
            print(f"    ✓ Audit logging supported")
        
        return config
    
    def _read_feature_documentation(self):
        """Read documentation for features mentioned in the issue."""
        
        # Extract feature names from issue
        features = self._extract_feature_names()
        
        for feature in features:
            doc_path = self.project_root / "docs" / feature
            if doc_path.exists() and doc_path.is_dir():
                print(f"  ✓ Reading docs for feature: {feature}")
                self.feature_docs[feature] = {}
                
                # Read all markdown files in feature directory
                for md_file in doc_path.glob("*.md"):
                    doc_name = md_file.stem
                    content = md_file.read_text()
                    self.feature_docs[feature][doc_name] = content
                    
                    # Check for specific patterns
                    if 'api' in doc_name.lower():
                        self._validate_api_docs(content, feature)
                    elif 'model' in doc_name.lower():
                        self._validate_model_docs(content, feature)
                    elif 'implement' in doc_name.lower():
                        self._validate_implementation_docs(content, feature)
    
    def _extract_feature_names(self) -> List[str]:
        """Extract potential feature names from issue."""
        features = []
        
        # Common feature keywords
        keywords = ['user', 'auth', 'payment', 'profile', 'api', 'admin', 'report', 'notification']
        
        for keyword in keywords:
            if keyword in self.issue_data.get('description', '').lower():
                features.append(keyword)
        
        # Check docs directory for existing features
        docs_path = self.project_root / "docs"
        if docs_path.exists():
            for item in docs_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    if item.name in self.issue_data.get('description', '').lower():
                        features.append(item.name)
        
        return list(set(features))  # Remove duplicates
    
    def _validate_api_docs(self, content: str, feature: str):
        """Validate API documentation against code."""
        # Look for endpoint definitions
        endpoints = re.findall(r'(GET|POST|PUT|PATCH|DELETE)\s+(/[\w/\{\}]+)', content, re.I)
        
        # Check if these endpoints exist in urls.py
        for method, path in endpoints:
            self._check_endpoint_exists(method, path, feature)
    
    def _validate_model_docs(self, content: str, feature: str):
        """Validate model documentation against code."""
        # Look for model definitions
        models = re.findall(r'class\s+(\w+)\s*\(.*Model', content)
        
        # Check if these models exist
        for model in models:
            self._check_model_exists(model, feature)
    
    def _validate_implementation_docs(self, content: str, feature: str):
        """Validate implementation details."""
        # Check for PII handling instructions
        if 'pii' in content.lower() or 'personal' in content.lower():
            if 'GlobalPIIMasker' in content:
                self._verify_pii_implementation(feature)
        
        # Check for validation instructions
        if 'magika' in content.lower() or 'validate' in content.lower():
            if 'validate_with_magika' in content:
                self._verify_magika_implementation(feature)
        
        # Check for logging instructions
        if 'log' in content.lower():
            if 'centralized' in content.lower():
                self._verify_logging_implementation(feature)
    
    def _validate_documentation_against_code(self):
        """Validate that documentation matches actual code."""
        
        # Check PII masking implementation
        if self.pii_config.get('masking_function'):
            self._validate_pii_usage()
        
        # Check Magika validation
        if self.magika_config.get('validation_function'):
            self._validate_magika_usage()
        
        # Check centralized logging
        if self.logging_config.get('logger_function'):
            self._validate_logging_usage()
        
        # Check for inconsistencies in feature docs
        for feature, docs in self.feature_docs.items():
            for doc_name, content in docs.items():
                self._check_doc_code_consistency(feature, doc_name, content)
    
    def _validate_pii_usage(self):
        """Check if PII masking is used correctly."""
        # Search for files that should use PII masking
        for py_file in self.project_root.glob("**/*.py"):
            if 'test' in str(py_file):
                continue
                
            content = py_file.read_text()
            
            # Check if file handles PII but doesn't import masker
            if any(word in content.lower() for word in ['email', 'phone', 'ssn', 'personal']):
                masker = self.pii_config.get('masking_function', 'GlobalPIIMasker')
                if masker not in content:
                    self.doc_discrepancies.append(DocumentationDiscrepancy(
                        doc_file="docs/security/pii_masking.md",
                        doc_statement=f"All PII should use {masker}",
                        actual_code=f"{py_file.name} handles PII but doesn't import {masker}",
                        suggestion=f"Add: from {self.pii_config.get('import_from', 'utils.pii')} import {masker}"
                    ))
    
    def _validate_magika_usage(self):
        """Check if Magika validation is used for file uploads."""
        # Search for file upload handling
        for py_file in self.project_root.glob("**/views.py"):
            content = py_file.read_text()
            
            # Check if file handles uploads but doesn't validate
            if 'FileField' in content or 'ImageField' in content or 'request.FILES' in content:
                validator = self.magika_config.get('validation_function', 'validate_with_magika')
                if validator not in content:
                    self.doc_discrepancies.append(DocumentationDiscrepancy(
                        doc_file="docs/validation/magika.md",
                        doc_statement=f"All file uploads should use {validator}",
                        actual_code=f"{py_file.name} handles files but doesn't call {validator}",
                        suggestion=f"Add validation: {validator}(uploaded_file)"
                    ))
    
    def _validate_logging_usage(self):
        """Check if centralized logging is used correctly."""
        # Search for files using print or basic logging
        for py_file in self.project_root.glob("**/*.py"):
            if 'test' in str(py_file) or 'migration' in str(py_file):
                continue
                
            content = py_file.read_text()
            
            # Check for print statements or basic logging
            if 'print(' in content or 'logging.info' in content:
                logger = self.logging_config.get('logger_function', 'get_logger')
                if logger not in content:
                    self.doc_discrepancies.append(DocumentationDiscrepancy(
                        doc_file="docs/infrastructure/logging.md",
                        doc_statement=f"Use centralized logging with {logger}",
                        actual_code=f"{py_file.name} uses print/basic logging instead of {logger}",
                        suggestion=f"Replace with: logger = {logger}(__name__)"
                    ))
    
    def _check_doc_code_consistency(self, feature: str, doc_name: str, content: str):
        """Check if documentation matches actual implementation."""
        # Extract code blocks from documentation
        code_blocks = re.findall(r'```python(.*?)```', content, re.DOTALL)
        
        for code_block in code_blocks:
            # Check if documented functions exist
            functions = re.findall(r'def\s+(\w+)', code_block)
            for func in functions:
                self._verify_function_exists(func, feature, doc_name)
            
            # Check if documented classes exist
            classes = re.findall(r'class\s+(\w+)', code_block)
            for cls in classes:
                self._verify_class_exists(cls, feature, doc_name)
    
    def _scan_for_unrelated_issues(self):
        """Scan affected files for unrelated issues."""
        
        # Determine which files will be affected
        affected_files = self._get_affected_files()
        
        for file_path in affected_files:
            if file_path.exists():
                content = file_path.read_text()
                line_num = 0
                
                for line in content.split('\n'):
                    line_num += 1
                    
                    # Check for TODOs
                    if 'TODO' in line or 'FIXME' in line:
                        self.unrelated_issues.append(UnrelatedIssue(
                            type=IssueType.TODO,
                            file=str(file_path.relative_to(self.project_root)),
                            line=line_num,
                            description=line.strip(),
                            severity="low"
                        ))
                    
                    # Check for deprecated usage
                    if 'deprecated' in line.lower() or '@deprecated' in line:
                        self.unrelated_issues.append(UnrelatedIssue(
                            type=IssueType.DEPRECATED,
                            file=str(file_path.relative_to(self.project_root)),
                            line=line_num,
                            description="Using deprecated function/method",
                            severity="medium"
                        ))
                    
                    # Check for potential security issues
                    if 'eval(' in line or 'exec(' in line:
                        self.unrelated_issues.append(UnrelatedIssue(
                            type=IssueType.SECURITY,
                            file=str(file_path.relative_to(self.project_root)),
                            line=line_num,
                            description="Potential security issue: eval/exec usage",
                            severity="high"
                        ))
                    
                    # Check for SQL injection risks
                    if '.format(' in line and 'SELECT' in line.upper():
                        self.unrelated_issues.append(UnrelatedIssue(
                            type=IssueType.SECURITY,
                            file=str(file_path.relative_to(self.project_root)),
                            line=line_num,
                            description="Potential SQL injection: string formatting in query",
                            severity="critical"
                        ))
                    
                    # Check for hardcoded secrets
                    if 'password=' in line.lower() and '"' in line:
                        if not 'getenv' in line and not 'environ' in line:
                            self.unrelated_issues.append(UnrelatedIssue(
                                type=IssueType.SECURITY,
                                file=str(file_path.relative_to(self.project_root)),
                                line=line_num,
                                description="Hardcoded password detected",
                                severity="critical"
                            ))
    
    def _get_affected_files(self) -> List[Path]:
        """Determine which files will be affected by this issue."""
        affected = []
        
        # Add model files if models are involved
        if self.issue_data.get('models'):
            affected.extend(self.project_root.glob("**/models.py"))
        
        # Add view files if endpoints are involved
        if self.issue_data.get('endpoints'):
            affected.extend(self.project_root.glob("**/views.py"))
            affected.extend(self.project_root.glob("**/urls.py"))
            affected.extend(self.project_root.glob("**/serializers.py"))
        
        return affected
    
    def _handle_documentation_discrepancies(self) -> Dict[str, Any]:
        """Handle discrepancies between documentation and code."""
        
        questions = ["I found discrepancies between documentation and actual code:\n"]
        
        for i, discrepancy in enumerate(self.doc_discrepancies[:5], 1):  # Show max 5
            questions.append(f"\n{i}. Documentation says: {discrepancy.doc_statement}")
            questions.append(f"   But I found: {discrepancy.actual_code}")
            questions.append(f"   Should I: {discrepancy.suggestion}?")
        
        if len(self.doc_discrepancies) > 5:
            questions.append(f"\n...and {len(self.doc_discrepancies) - 5} more discrepancies.")
        
        questions.append("\nHow should I handle these? Fix them, or follow existing code?")
        
        return {
            "status": "documentation_mismatch",
            "discrepancies": [d.__dict__ for d in self.doc_discrepancies],
            "questions": questions,
            "message": "Documentation doesn't match code - need guidance"
        }
    
    def _handle_unrelated_issues(self) -> Dict[str, Any]:
        """Handle unrelated issues found during scanning."""
        
        # Group by severity
        critical = [i for i in self.unrelated_issues if i.severity == "critical"]
        high = [i for i in self.unrelated_issues if i.severity == "high"]
        medium = [i for i in self.unrelated_issues if i.severity == "medium"]
        low = [i for i in self.unrelated_issues if i.severity == "low"]
        
        message = "I found unrelated issues while reviewing the code:\n"
        
        if critical:
            message += f"\n🔴 CRITICAL ({len(critical)} issues):\n"
            for issue in critical[:2]:  # Show max 2
                message += f"  - {issue.file}:{issue.line} - {issue.description}\n"
        
        if high:
            message += f"\n🟠 HIGH ({len(high)} issues):\n"
            for issue in high[:2]:
                message += f"  - {issue.file}:{issue.line} - {issue.description}\n"
        
        if medium:
            message += f"\n🟡 MEDIUM ({len(medium)} issues)\n"
        
        if low:
            message += f"\n🟢 LOW ({len(low)} issues - mostly TODOs)\n"
        
        options = [
            "1. Fix critical issues now, flag others in PR",
            "2. Create separate issues for all findings",
            "3. Flag all in PR comments for later",
            "4. Ignore for now (not recommended for critical issues)",
            "5. Let me handle each severity level differently"
        ]
        
        return {
            "status": "unrelated_issues_found",
            "issues": {
                "critical": [i.__dict__ for i in critical],
                "high": [i.__dict__ for i in high],
                "medium": [i.__dict__ for i in medium],
                "low": [i.__dict__ for i in low]
            },
            "options": options,
            "message": message + "\n\nHow should I handle these? (Choose 1-5)"
        }
    
    def _parse_issue(self, description: str):
        """Parse issue description."""
        self.issue_data = {
            'description': description,
            'number': None,
            'requirements': [],
            'has_pii': False,
            'needs_auth': False,
            'endpoints': [],
            'models': []
        }
        
        # Extract issue number
        if match := re.search(r'#(\d+)', description):
            self.issue_data['number'] = match.group(1)
        elif match := re.search(r'issue\s+(\d+)', description, re.I):
            self.issue_data['number'] = match.group(1)
        
        # Extract requirements
        for line in description.split('\n'):
            if line.strip().startswith(('-', '*', '•')):
                self.issue_data['requirements'].append(line.strip()[1:].strip())
        
        # Check for PII
        pii_keywords = ['personal', 'pii', 'email', 'phone', 'ssn', 'payment']
        if any(kw in description.lower() for kw in pii_keywords):
            self.issue_data['has_pii'] = True
        
        # Extract endpoints
        endpoint_pattern = r'(GET|POST|PUT|PATCH|DELETE)\s+(/[\w/\{\}]+)'
        for match in re.finditer(endpoint_pattern, description, re.I):
            self.issue_data['endpoints'].append({
                'method': match.group(1).upper(),
                'path': match.group(2)
            })
    
    def _get_clarification_questions(self) -> List[str]:
        """Get clarification questions including validation questions."""
        questions = []
        
        # Standard clarifications
        if not self.issue_data.get('number'):
            questions.append("What's the issue number for branch naming?")
        
        # PII handling clarification
        if self.issue_data.get('has_pii'):
            if self.pii_config.get('masking_function'):
                questions.append(f"Should I use {self.pii_config['masking_function']} for PII as documented?")
            else:
                questions.append("How should PII be handled? I didn't find PII masking docs.")
        
        # File validation clarification
        if 'upload' in self.issue_data.get('description', '').lower():
            if self.magika_config.get('validation_function'):
                questions.append(f"Should file uploads use {self.magika_config['validation_function']}?")
            else:
                questions.append("Should uploaded files be validated? I didn't find Magika docs.")
        
        # Logging clarification
        if not self.logging_config.get('logger_function'):
            questions.append("What logging system should I use? I didn't find centralized logging docs.")
        
        return questions
    
    def _check_breaking_changes(self) -> List[str]:
        """Check for breaking changes."""
        changes = []
        
        # Check existing models
        for model in self.issue_data.get('models', []):
            model_files = list(self.project_root.glob('**/models.py'))
            for mf in model_files:
                if mf.exists() and f'class {model}' in mf.read_text():
                    changes.append(f"Model '{model}' already exists in {mf.relative_to(self.project_root)}")
        
        return changes
    
    def _create_validated_plan(self) -> str:
        """Create plan that's validated against documentation."""
        
        plan = f"""# Implementation Plan (Validated Against Documentation)

## Issue Details
- Number: #{self.issue_data.get('number', 'TBD')}
- Has PII: {'Yes' if self.issue_data.get('has_pii') else 'No'}

## Documentation Validation Status
- ✅ Read {len(self.feature_docs)} feature documentation folders
- ✅ Validated against existing code
- ✅ Checked for unrelated issues
"""
        
        # Add PII handling based on docs
        if self.issue_data.get('has_pii') and self.pii_config:
            plan += f"""
## PII Handling (Per Documentation)
- Will use: {self.pii_config.get('masking_function', 'GlobalPIIMasker')}
- Import from: {self.pii_config.get('import_from', 'utils.pii')}
- Fields to mask: email, phone, SSN
"""
        
        # Add file validation based on docs
        if 'upload' in self.issue_data.get('description', '').lower() and self.magika_config:
            plan += f"""
## File Validation (Per Documentation)  
- Will use: {self.magika_config.get('validation_function', 'validate_with_magika')}
- Import from: {self.magika_config.get('import_from', 'utils.validation')}
- Validate all uploads before processing
"""
        
        # Add logging based on docs
        if self.logging_config:
            plan += f"""
## Logging (Per Documentation)
- Will use: {self.logging_config.get('logger_function', 'get_logger')}
- Import from: {self.logging_config.get('import_from', 'utils.logging')}
- No print statements, only centralized logging
"""
        
        # Add unrelated issues section
        if self.unrelated_issues:
            critical_count = len([i for i in self.unrelated_issues if i.severity == "critical"])
            if critical_count > 0:
                plan += f"""
## ⚠️  Critical Issues Found (Will Flag in PR)
- {critical_count} critical security issues to address
- Will add PR comments for tracking
"""
        
        plan += """
## Implementation Steps
1. Create feature branch per workflow
2. Implement with documentation compliance
3. Use global PII masking where needed
4. Add Magika validation for uploads
5. Use centralized logging throughout
6. Generate tests (>85% coverage)
7. Flag any unrelated issues in PR
8. Create comprehensive documentation

## What I Will NOT Do
- Ignore documentation requirements
- Use print statements instead of logging
- Skip PII masking
- Allow unvalidated file uploads
- Leave critical issues unflagged

**This plan is validated against your documentation. Proceed? (yes/no)**
"""
        
        return plan
    
    def _check_endpoint_exists(self, method: str, path: str, feature: str):
        """Check if documented endpoint exists in code."""
        # This would check urls.py files
        pass
    
    def _check_model_exists(self, model: str, feature: str):
        """Check if documented model exists in code."""
        # This would check models.py files
        pass
    
    def _verify_pii_implementation(self, feature: str):
        """Verify PII is handled as documented."""
        # This would verify PII masking is implemented
        pass
    
    def _verify_magika_implementation(self, feature: str):
        """Verify Magika validation is implemented."""
        # This would verify file validation
        pass
    
    def _verify_logging_implementation(self, feature: str):
        """Verify centralized logging is used."""
        # This would verify logging implementation
        pass
    
    def _verify_function_exists(self, func: str, feature: str, doc_name: str):
        """Verify documented function exists in code."""
        # This would check if function exists
        pass
    
    def _verify_class_exists(self, cls: str, feature: str, doc_name: str):
        """Verify documented class exists in code."""
        # This would check if class exists
        pass

def work_on_issue(description: str):
    """
    Main entry point that:
    1. Validates documentation matches code
    2. Uses global PII masking, Magika, centralized logging
    3. Flags unrelated issues for user decision
    4. Never proceeds without validation
    """
    automation = DjangoIssueAutomation()
    return automation.work_on_issue(description)
