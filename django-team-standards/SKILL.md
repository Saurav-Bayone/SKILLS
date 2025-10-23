---
name: django-team-standards
description: This skill should be used when implementing Django issues for the Talent AI recruitment platform. It validates against existing documentation, enforces team coding standards, flags unrelated issues discovered during development, and ensures consistent Django patterns across the team. Use when working on GitHub issues, adding Django apps, creating services, or making changes affecting multiple files.
---

# Django Team Standards - Talent AI Platform

## Overview

This skill automates Django implementation for the Talent AI recruitment platform while validating against existing documentation, enforcing team standards, and flagging unrelated issues discovered during development. It ensures consistent code quality across the team by leveraging existing infrastructure and catching problems before they become technical debt.

## When to Use This Skill

Use this skill when:
- Implementing features from GitHub issues
- Adding new Django apps or models
- Working with extraction, storage, validation, or logging modules
- Creating APIs or service layers
- Making changes that affect multiple files (3+)

## Workflow Overview

This skill follows a 7-phase process:

1. **Documentation Discovery** - Read docs, validate against codebase, note gaps
2. **Issue Discovery** - Scan for unrelated problems, let user decide how to handle
3. **Planning & Approval** - Create detailed plan, get user approval BEFORE coding
4. **Implementation** - Write code following standards
5. **Testing & Validation** - Comprehensive tests (not superficial)
6. **Final Checklist** - Verify all requirements met
7. **Documentation** - Update docs, track issue resolutions

**Key Principle**: No code is written until the user approves the plan in Phase 3.

## Detailed Workflow

### Phase 1: Documentation Discovery and Validation

Before implementing any issue, discover and validate existing documentation:

1. **Read Core Documentation** (Always check these):
   - `CLAUDE.md` - Project structure, workflows, development principles
   - `pyproject.toml` - Dependencies, Python version, package constraints
   - `talent_ai_project/settings/base.py` - Configuration, installed apps

2. **Search for Feature-Specific Documentation** (`docs/` folder):
   - Check if `docs/<domain>/` exists for the feature area (e.g., `docs/extraction/`, `docs/logging/`, `docs/validation/`, `docs/storage/`)
   - Read relevant markdown files if found
   - Note what documentation exists vs. what's missing

3. **Cross-Validate Documentation Against Codebase**:
   - Verify imports mentioned in docs actually exist in the codebase
   - Check if patterns described in docs match current implementation
   - Identify documentation drift (docs say X, code does Y)
   - Example: Docs mention `get_extraction_logger()` but code now uses `get_logger()` from centralized logging

4. **Document Gaps** (Track but don't block):
   - Note missing documentation in a list
   - Will create documentation after implementation if needed
   - Example: "No architecture docs for `compliance/` domain - will create after implementing audit system"

5. **Ask User for Clarification** when documentation conflicts with reality:
   - Present the discrepancy clearly
   - Ask which is correct: docs or code
   - Wait for user decision before proceeding

### Phase 2: Issue Discovery and Classification

While exploring the codebase for implementation, actively search for unrelated issues:

1. **Scan for Common Issues**:
   - TODO/FIXME comments without context
   - Deprecated function usage (e.g., old logging patterns)
   - Hardcoded secrets or credentials in code
   - Missing error handling or broad try/except blocks
   - SQL injection vulnerabilities (raw SQL without parameterization)
   - Performance anti-patterns (N+1 queries, missing indexes)
   - Inconsistent logging patterns (using `logging.getLogger` instead of `get_logger`)
   - Missing validation (e.g., extension-based instead of Magika content-based)
   - Code duplication (same logic in multiple places)
   - Unused imports or dead code
   - Missing audit logging for sensitive operations

2. **Classify by Severity**:
   - **Critical**: SQL injection, hardcoded secrets (passwords, API keys), eval/exec on user input, security vulnerabilities
   - **High**: Deprecated security functions, missing authentication checks, PII leakage in logs
   - **Medium**: Deprecated functions, N+1 queries, missing validation, inconsistent patterns
   - **Low**: TODO comments, code duplication, unused imports, style inconsistencies

3. **Present Issues to User** (One at a time or grouped):
   For each flagged issue, provide:
   - File path and line number
   - Severity level
   - Description of the issue
   - Recommended fix
   - Options for handling:
     * **Fix now**: Stop current work, fix immediately, then continue
     * **Document in PR**: Add to PR description for reviewer awareness
     * **Create separate issue**: File GitHub issue for future work
     * **Document in commit**: Note in commit message
     * **Ignore**: Skip this issue (with reason)

4. **Track Decisions**: Maintain a list of user decisions for Phase 5

### Phase 3: Planning and Approval

Before writing any code, create a detailed implementation plan and get user approval:

1. **Analyze the Issue Requirements**:
   - Break down what needs to be built
   - Identify all components needed (models, services, views, APIs, tests, etc.)
   - Map to existing infrastructure (what can be reused vs. what's new)

2. **Create Implementation Plan**:
   - List all files that will be created or modified
   - For each component, describe:
     * What it does (business logic)
     * What existing patterns/utilities it uses
     * Key design decisions
   - Identify dependencies between components
   - Estimate complexity and potential risks

3. **Document Plan in Markdown Format**:
   ```markdown
   # Implementation Plan for Issue #XXX

   ## Summary
   [Brief description of what we're building and why]

   ## Components to Create/Modify

   ### 1. Model: `domain/app/models.py`
   - **Purpose**: [What this model represents]
   - **Key Fields**: [List important fields]
   - **Business Rules**: [Any special logic]
   - **Uses**: Django ORM, UUID primary keys, immutability if needed

   ### 2. Service: `domain/app/services.py`
   - **Purpose**: [Business logic this service handles]
   - **Key Methods**: [List main methods]
   - **Dependencies**: [What it uses - logging, validation, storage, etc.]
   - **Pattern**: Module-level instance for easy import

   ### 3. Tests: `domain/app/tests.py`
   - **Coverage**: [What scenarios will be tested]
   - **Test Types**: Unit tests for service layer, integration tests for full flow
   - **Test Data**: [What test fixtures needed]

   [Continue for all components...]

   ## Existing Infrastructure Usage
   - ✅ Logging: `core.diagnostics.logging.get_logger()`
   - ✅ Validation: `core.validation.validate_file()` (if file handling)
   - ✅ Storage: `core.storage` (if file storage)
   - [ ] New dependency needed: [If any - requires approval]

   ## Testing Strategy
   - Unit tests for each service method
   - Integration tests for full workflow
   - Edge cases: [List important edge cases]
   - Performance considerations: [If relevant]

   ## Potential Risks
   - [List any concerns or unknowns]
   - [Migration complexity if database changes]
   - [Breaking changes to existing code]

   ## Documentation Updates Needed
   - [List what docs to create/update after implementation]
   ```

4. **Present Plan to User**:
   - Show the complete plan
   - Highlight any uncertainties or decisions needed
   - Ask specific questions:
     * "Should component X be in domain A or domain B?"
     * "Should I use pattern Y or Z?"
     * "This will modify existing file F - is that acceptable?"

5. **Incorporate Feedback**:
   - Update plan based on user input
   - Document any design decisions made
   - Get explicit approval: "Is this plan good? Should I proceed with implementation?"

6. **Wait for Approval**:
   - Do NOT start coding until user says "yes", "approved", "go ahead", "implement it"
   - If user has questions, answer them first
   - If user suggests changes, update the plan and present again

### Phase 4: Implementation with Standards Enforcement

After plan is approved, implement the feature following project standards:

#### 1. Environment

Always use `DJANGO_ENVIRONMENT=local` for all commands:
```bash
DJANGO_ENVIRONMENT=local poetry run python manage.py <command>
```

#### 2. Project Structure (Domain-Driven Design)

```
talent_ai/
├── core/                 # Foundation domain
│   ├── accounts/         # Authentication
│   ├── shared/           # Reusable components
│   ├── diagnostics/      # Logging, monitoring
│   ├── storage/          # File storage (Azure + local)
│   └── validation/       # File validation (Magika)
├── intelligence/         # AI/ML domain
│   └── extraction/       # Document extraction pipeline
├── api/                  # REST API endpoints
│   └── extraction/       # Extraction API
├── integrations/         # External services
│   └── microsoft/        # Microsoft Graph, email
└── recruitment/          # Business domain (future)
```

**App Naming**: Use `domain.app_name` format in `apps.py`:
```python
class MyAppConfig(AppConfig):
    name = 'domain.app_name'  # e.g., 'compliance.audit'
```

#### 3. Django App Structure

```
domain/app_name/
├── models.py or models/           # Data models
├── views.py or views/             # View logic
├── urls.py                        # URL routing
├── admin.py                       # Admin interface
├── apps.py                        # App configuration
├── migrations/                    # Database migrations
├── services/ or services.py       # Business logic layer (IMPORTANT!)
├── tests.py or tests/             # Tests
└── management/commands/           # Management commands (if needed)
```

**Rule**: Business logic ALWAYS goes in `services/`, not in views or models.

#### 4. Service Layer Pattern (Required for Business Logic)

Use the service layer pattern for all business logic:

```python
# domain/app_name/services/service_name.py or domain/app_name/services.py
from core.diagnostics.logging import get_logger

logger = get_logger('domain.app_name.service_name')

class ServiceName:
    """
    Service for [business capability].

    Business Logic:
    - [What this service does]
    - [Key responsibilities]

    Example:
        from domain.app_name.services import service_name
        result = service_name.method_name(param1, param2)
    """

    def method_name(self, param1, param2):
        """
        [What this method does]

        Args:
            param1: Description
            param2: Description

        Returns:
            Description of return value

        Raises:
            ExceptionType: When this happens
        """
        logger.info("Starting operation", param1=param1)
        # Implementation
        logger.audit('operation_completed', param1=param1, param2=param2)
        return result

# Module-level instance for easy import
service_name = ServiceName()
```

**Example from codebase**: `intelligence/extraction/services/extraction_orchestrator.py` has `ExtractionOrchestrator` class with module-level instance.

#### 5. Logging (Centralized with Auto PII Masking)

**ALWAYS use centralized logger**, never `import logging` directly:

```python
from core.diagnostics.logging import get_logger

logger = get_logger('domain.app_name.module')

# Standard logging (PII automatically masked - emails, phones, IPs)
logger.info("Processing file", user_id=123, file_size=1024)
# Output: "Processing file | user_id=123 | file_size=1024"

logger.info("User uploaded file", email="john@example.com", ip="192.168.1.1")
# Output: "User uploaded file | email=<EMAIL_ADDRESS> | ip=<IP_ADDRESS>"

# Audit logging (for sensitive operations)
logger.audit('action_name', user_id=user.id, resource_id=resource.id)

# Performance monitoring
import time
start = time.time()
# ... operation ...
duration = time.time() - start
logger.performance('operation_name', duration=duration, custom_metric=value)

# Security events
logger.security_event('event_type', severity='high', details=info)
```

**Documentation**: See `docs/logging/PII_MASKING_GUIDE.md` for complete guide

#### 6. File Validation (Magika Content-Based)

**ALWAYS use Magika content validation**, never extension-based:

```python
from core.validation import validate_file
from core.validation.exceptions import FileValidationError

try:
    # Magika AI detects actual file content (~5ms, 99% accurate)
    validate_file(
        uploaded_file,
        allowed_types=['pdf', 'docx', 'txt'],  # Magika labels, not extensions
        max_size_mb=10
    )
except FileValidationError as e:
    logger.error("File validation failed", error=str(e))
    raise ValueError(f"File validation failed: {e}")
```

**Why Magika**: Detects content type via AI, not filename. A malicious `.exe` renamed to `.pdf` will be correctly identified and blocked.

**Documentation**: See `docs/validation/CENTRALIZED_VALIDATION_INTEGRATION.md`

#### 7. Models (Django Best Practices)

```python
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ModelName(models.Model):
    """
    [What this model represents]

    Business Logic:
    - [Key business rules]
    - [Important constraints]
    """

    # UUID primary key (better for distributed systems, SOC2)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Timestamps (always include)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Foreign keys (use SET_NULL for audit trail preservation)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Preserve record even if user deleted
        null=True,
        blank=True,
        related_name='model_names'
    )

    class Meta:
        db_table = 'table_name'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at', 'user']),
        ]
        verbose_name = 'Model Name'
        verbose_name_plural = 'Model Names'

    def __str__(self):
        return f"ModelName({self.id})"
```

**For Immutable Models** (e.g., audit logs):
```python
def save(self, *args, **kwargs):
    """Prevent updates to existing records (immutability)."""
    if not self._state.adding:
        raise ValidationError("Cannot update existing audit record")
    super().save(*args, **kwargs)

def delete(self, *args, **kwargs):
    """Prevent deletion (immutability)."""
    raise ValidationError("Cannot delete audit records")
```

#### 8. API Endpoints (Django REST Framework)

If creating APIs, follow these patterns:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.diagnostics.logging import get_logger

logger = get_logger('api.domain.endpoint')

class ResourceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def custom_action(self, request, pk=None):
        # Audit logging
        logger.audit('action_performed', user_id=request.user.id, resource_id=pk)

        # Generic error messages to user (SOC2)
        # Detailed errors in logs only
        try:
            # ... implementation ...
            return Response({"status": "success"})
        except Exception as e:
            logger.error("Action failed", error=str(e), user_id=request.user.id)
            return Response(
                {"error": "Operation failed. Please contact support."},
                status=status.HTTP_400_BAD_REQUEST
            )
```

**Required Features**:
- Token authentication
- Rate limiting (configured in settings)
- Pagination (limit/offset, 50 per page)
- Audit logging for sensitive operations
- Generic user error messages (don't expose internals)
- Detailed internal logging

**Example**: See `api/extraction/` for complete REST API implementation

#### 9. Testing

Always write tests for business logic:

```bash
# Run specific app tests
DJANGO_ENVIRONMENT=local poetry run python manage.py test domain.app_name

# Run specific test class
DJANGO_ENVIRONMENT=local poetry run python manage.py test domain.app_name.tests.TestClassName

# Run with coverage
DJANGO_ENVIRONMENT=local poetry run coverage run --source='.' manage.py test domain.app_name
DJANGO_ENVIRONMENT=local poetry run coverage report
```

**Test Structure**:
```python
from django.test import TestCase
from domain.app_name.services import service_name

class ServiceNameTestCase(TestCase):
    def setUp(self):
        # Setup test data
        pass

    def test_method_name(self):
        """Test [what this tests]."""
        result = service_name.method_name(param1, param2)
        self.assertEqual(result, expected)
```

#### 10. Migrations

```bash
# Create migration
DJANGO_ENVIRONMENT=local poetry run python manage.py makemigrations app_name

# Apply migrations
DJANGO_ENVIRONMENT=local poetry run python manage.py migrate

# Check migration status
DJANGO_ENVIRONMENT=local poetry run python manage.py showmigrations
```

**IMPORTANT**: Do NOT apply migrations to dev/prod without user approval. Only apply to local.

#### 11. Management Commands

For administrative tasks or testing:

```python
# domain/app_name/management/commands/command_name.py
from django.core.management.base import BaseCommand
from core.diagnostics.logging import get_logger

logger = get_logger('management.command_name')

class Command(BaseCommand):
    help = 'Description of what this command does'

    def add_arguments(self, parser):
        parser.add_argument('--option', type=str, help='Option description')

    def handle(self, *args, **options):
        logger.audit('command_executed', command='command_name', options=options)
        self.stdout.write(self.style.SUCCESS('Command completed'))
```

Run with:
```bash
DJANGO_ENVIRONMENT=local poetry run python manage.py command_name --option value
```

### Phase 5: Testing and Validation

After implementation is complete, thoroughly test before marking as done:

1. **Write Comprehensive Tests**:
   - **Unit Tests**: Test each service method independently
     * Test happy path (successful operations)
     * Test error cases (invalid input, missing data)
     * Test edge cases (empty strings, null values, boundary conditions)
     * Test business rules enforcement

   - **Integration Tests**: Test full workflows
     * Test complete user journeys
     * Test interaction between components
     * Test database transactions
     * Test API endpoints end-to-end

   - **Example - NOT superficial**:
     ```python
     # ❌ BAD: Superficial test
     def test_create_audit_log(self):
         log = audit_service.log_action('create', user, 'Test')
         self.assertIsNotNone(log)  # Weak assertion

     # ✅ GOOD: Comprehensive test
     def test_create_audit_log_with_all_fields(self):
         """Test that audit log captures all required fields."""
         log = audit_service.log_action(
             action='create',
             user=self.user,
             description='Created test resource',
             ip_address='192.168.1.1',
             user_agent='Test Agent',
             model_name='Resource',
             record_id='123'
         )

         # Verify all fields populated correctly
         self.assertEqual(log.action, 'create')
         self.assertEqual(log.username, self.user.username)
         self.assertEqual(log.user, self.user)
         self.assertEqual(log.description, 'Created test resource')
         self.assertEqual(log.ip_address, '192.168.1.1')
         self.assertEqual(log.user_agent, 'Test Agent')
         self.assertEqual(log.model_name, 'Resource')
         self.assertEqual(log.record_id, '123')
         self.assertIsNotNone(log.created_at)

         # Verify it's actually in database
         self.assertTrue(AuditLog.objects.filter(id=log.id).exists())
     ```

2. **Run Tests and Verify All Pass**:
   ```bash
   DJANGO_ENVIRONMENT=local poetry run python manage.py test domain.app_name
   ```
   - All tests must pass (0 failures, 0 errors)
   - Review test output carefully
   - If any failures, debug and fix before proceeding

3. **Test Edge Cases Manually** (if applicable):
   - Try invalid inputs
   - Test with empty/null data
   - Test with very large files (if file handling)
   - Test concurrent operations (if relevant)
   - Verify error messages are generic to users, detailed in logs

4. **Run Management Command Tests** (if created):
   ```bash
   DJANGO_ENVIRONMENT=local poetry run python manage.py your_test_command
   ```
   - Verify all test scenarios pass
   - Check command output is clear and helpful
   - Verify database changes are correct

5. **Check Database State**:
   ```bash
   DJANGO_ENVIRONMENT=local poetry run python manage.py shell
   ```
   - Verify migrations applied correctly
   - Check data integrity (no orphaned records)
   - Test model constraints work (try to violate them)
   - For immutable models, verify cannot update/delete

6. **Manual Functional Testing**:
   - If UI exists, test in browser
   - If API exists, test with curl or Postman
   - Verify error handling works as expected
   - Check logs show proper detail (without PII)

### Phase 6: Final Validation Checklist

Before marking implementation complete, verify all of these:

- [ ] **Logging**: Uses `get_logger()` from `core.diagnostics.logging`, not `logging.getLogger()`
- [ ] **Validation**: Uses `validate_file()` from `core.validation` (Magika), not extension checks
- [ ] **PII Masking**: Relies on automatic PII masking, no manual masking needed
- [ ] **Structure**: Follows domain-driven structure (correct app location)
- [ ] **Service Layer**: Business logic in `services/`, not in views or models
- [ ] **Error Handling**: Generic errors to users, detailed errors in logs (SOC2 basic requirement)
- [ ] **Tests**: Tests written and passing with `DJANGO_ENVIRONMENT=local`
- [ ] **Migrations**: Created with `makemigrations` (not applied to non-local without approval)
- [ ] **Documentation**: Updated if new patterns introduced
- [ ] **Security**: No hardcoded secrets, SQL injection protection, input validation
- [ ] **Dependencies**: Only uses existing dependencies from `pyproject.toml` (or user approved new ones)
- [ ] **Reusability**: Checked if similar functionality exists before creating new code
- [ ] **Tests Pass**: All unit and integration tests pass with 0 failures
- [ ] **Tests Are Comprehensive**: Tests cover happy path, error cases, edge cases, and business rules
- [ ] **Manual Testing**: Manually tested the functionality works as expected
- [ ] **Database Verified**: Checked database state is correct (migrations applied, data integrity)
- [ ] **Logs Checked**: Verified logs show appropriate detail without exposing PII

### Phase 7: Issue Resolution Tracking and Documentation

For each flagged issue from Phase 2, ensure user decision was implemented:

- **Fix now**: Verify fix was applied and tested
- **Document in PR**: Add to PR description template (provide formatted text)
- **Create issue**: Create GitHub issue with:
  - Clear title
  - Severity label (critical, high, medium, low)
  - Detailed description with file path and line number
  - Recommended fix
  - Link to related PR if applicable
- **Document in commit**: Include in commit message under "Issues Found" section
- **Ignore**: Note reason in internal documentation (not in code)

## Integration with Existing Infrastructure

### Leverage These Utilities (Don't Recreate)

Before creating any new utility, check if it exists:

1. **Logging** → `core.diagnostics.logging`
   - `get_logger()` - Auto PII masking (emails, phones, IPs)
   - `.audit()`, `.performance()`, `.security_event()` methods
   - See: `docs/logging/PII_MASKING_GUIDE.md`

2. **File Validation** → `core.validation`
   - `validate_file()` - Magika AI content detection (~5ms, 99% accurate)
   - See: `docs/validation/CENTRALIZED_VALIDATION_INTEGRATION.md`

3. **File Storage** → `core.storage`
   - `StorageService` - Azure Blob Storage + local filesystem
   - `store_file()`, `store_bytes()`, `retrieve_file()`
   - See: `docs/storage/STORAGE_MODULE_DOCUMENTATION.md`

4. **Extraction Pipeline** → `intelligence.extraction`
   - `ExtractionOrchestrator` - Document processing (PDF, DOCX, etc.)
   - `extract_document()` returns `(StoredFile, ExtractionJob)`
   - See: `docs/extraction/EXTRACTION_PIPELINE_DOCUMENTATION.md`

5. **API Patterns** → `api.extraction`
   - Token authentication
   - Rate limiting
   - Pagination
   - Audit logging
   - See: `docs/extraction/API_DOCUMENTATION.md`

### Check Before Creating

Before creating any new utility, service, or pattern:

1. Search `pyproject.toml` for existing dependencies
   - Example: Don't add `python-magic` when `magika` already exists
2. Grep codebase for similar functionality
   - Example: Search for "logger" to find logging patterns
3. Check `docs/` for existing patterns
   - Example: Check `docs/extraction/` for document processing patterns
4. Ask user if uncertain
   - Example: "I see we have `StorageService` for file storage. Should I use this or create a new utility?"

## Communication Protocol

### Answer First, Implement Only When Approved

- When user asks a question, provide a clear answer first
- Do NOT assume they want implementation unless explicitly requested
- Do NOT jump into coding solutions automatically
- **Exception**: When user explicitly says "fix this", "implement X", "create Y", "work on issue #123" → proceed directly

### Always Discuss Before Major Changes

- Explain what was found and why it needs fixing
- Propose the solution approach clearly
- Wait for explicit approval before implementing
- **"Major changes"** include:
  - Architectural changes (new domains, app structure changes)
  - New features (new models, services, APIs)
  - Refactoring (changing existing patterns)
  - Performance optimizations (database changes, caching)
  - Dependency additions (new packages in `pyproject.toml`)

### Get Explicit Confirmation

- State what you're going to do and why
- Ask for permission: "Should I implement this fix?" or "Would you like me to proceed?"
- Get explicit confirmation before proceeding
- **User says "yes", "implement it", "go ahead", "proceed"** → proceed
- **User asks follow-up questions** → answer first, don't implement
- **Unclear response** → ask for clarification

### Implementation Progress

- Keep user informed of progress during implementation
- Use TodoWrite tool to track tasks
- Report completion of major milestones
- Flag any blockers or issues immediately

## Common Patterns Reference

See `references/common_patterns.md` for detailed examples of:
- Service layer implementation (with module-level instance)
- File validation integration (Magika)
- API endpoint patterns (DRF)
- Management command structure (with logging)
- Testing patterns (Django TestCase)

## Issue Flagging Guide

See `references/issue_flagging_guide.md` for:
- How to classify issues by severity
- Examples of each severity level
- Recommended fixes for common issues
- How to present issues to users

## Troubleshooting

### Documentation Doesn't Match Code

**Symptoms**: Docs mention `function_x()` but code has `function_y()`

**Action**:
1. Verify which is correct (code or docs)
2. Present findings to user: "Docs say X, but code does Y. Which is correct?"
3. Wait for user clarification
4. Update docs after implementation if needed
5. Note documentation drift in findings

### Missing Dependencies

**Symptoms**: Need a package that's not in `pyproject.toml`

**Action**:
1. Check if similar dependency exists
   - Example: Need JSON parsing? `json` is built-in
   - Example: Need file type detection? `magika` already installed
2. Ask user before adding new dependencies
3. If approved, use Poetry:
   ```bash
   poetry add package-name
   ```
4. Update documentation if pattern changes

### Integration Conflicts

**Symptoms**: New code conflicts with existing patterns

**Action**:
1. Review existing integration patterns in relevant domain
2. Check if service or utility already exists
3. Propose integration approach to user with pros/cons
4. Wait for approval before proceeding
5. Update documentation if new pattern established

### Test Failures

**Symptoms**: Tests fail when running `manage.py test`

**Action**:
1. Read error messages carefully (full stack trace)
2. Check if `DJANGO_ENVIRONMENT=local` was used
3. Verify PostgreSQL database is running
4. Check migrations are applied: `python manage.py showmigrations`
5. Check test data setup in `setUp()` method
6. Report issue to user with:
   - Full error message
   - What was tested
   - Expected vs actual behavior
   - Steps already tried

### Migration Conflicts

**Symptoms**: Migration fails or conflicts with existing migrations

**Action**:
1. Check migration sequence: `python manage.py showmigrations`
2. Look for branched migrations (two migrations with same parent)
3. If conflict:
   - Do NOT merge migrations without user approval
   - Report conflict to user with details
   - Suggest resolution approach
   - Wait for approval

### Environment Issues

**Symptoms**: Different behavior in local vs dev/prod

**Action**:
1. Check `.env.local`, `.env.dev`, `.env.prod` files
2. Verify environment-specific settings in `settings/`
3. Check if issue is environment configuration or code
4. Report findings to user
5. Do NOT change dev/prod settings without approval

## References

For detailed code examples and guides:
- `references/common_patterns.md` - Code examples and implementation patterns
- `references/issue_flagging_guide.md` - How to classify and report issues
