# Django Team Standards Skill

A comprehensive skill for implementing Django issues with team consistency, documentation validation, and thorough testing.

## What This Skill Does

This skill automates Django implementation while:
- ✅ Validating against existing documentation
- ✅ Enforcing team coding standards
- ✅ Flagging unrelated issues during development
- ✅ Creating detailed plans before coding
- ✅ Ensuring comprehensive testing (not superficial)
- ✅ Maintaining consistency across the team

## When to Use This Skill

Use this skill when:
- Implementing features from GitHub issues
- Adding new Django apps or models
- Working with extraction, storage, validation, or logging modules
- Creating APIs or service layers
- Making changes that affect multiple files (3+)

## 7-Phase Workflow

### 1. Documentation Discovery
- Reads issue, CLAUDE.md, pyproject.toml, docs/
- Validates docs against actual codebase
- Identifies documentation drift
- Notes gaps for later documentation

### 2. Issue Discovery
- Scans for unrelated problems while exploring
- Classifies by severity (Critical/High/Medium/Low)
- **Asks you how to handle each issue** (fix now, create issue, document, or ignore)

### 3. Planning & Approval ⭐
- Analyzes what needs to be built
- Creates detailed implementation plan:
  * All components (models, services, tests)
  * What existing infrastructure to use
  * Testing strategy (comprehensive)
  * Potential risks
- **Presents plan to you**
- **Waits for your approval before writing ANY code**

### 4. Implementation
- Follows approved plan
- Uses existing patterns (logging, validation, storage)
- Service layer for business logic
- Generic errors to users (SOC2 basic requirement)

### 5. Testing & Validation ⭐
- **Comprehensive tests, not superficial!**
- Unit tests (happy path + errors + edge cases)
- Integration tests for full workflows
- Manual testing verification
- Database state checks

### 6. Final Checklist
- All tests pass (0 failures)
- Tests are comprehensive
- Manual testing complete
- Database verified
- Logs checked (no PII exposure)

### 7. Documentation
- Documents implementation
- Updates relevant docs
- Tracks issue resolutions

## Key Features

### Planning Before Coding
No code is written until you approve the detailed plan. The skill will:
1. Show you exactly what will be built
2. Explain all design decisions
3. Wait for your "yes" or "approved"
4. Update plan based on your feedback

### Issue Flagging with Your Control
When the skill finds problems during exploration, it asks YOU:
- Fix now?
- Document in PR?
- Create separate issue?
- Document in commit?
- Ignore?

### Comprehensive Testing
The skill enforces proper testing, not just:
```python
# ❌ BAD
def test_create(self):
    obj = service.create()
    self.assertIsNotNone(obj)  # Too weak!
```

But comprehensive tests like:
```python
# ✅ GOOD
def test_create_with_all_fields(self):
    """Test creation with all required fields."""
    obj = service.create(field1='value1', field2='value2')

    # Verify all fields
    self.assertEqual(obj.field1, 'value1')
    self.assertEqual(obj.field2, 'value2')
    self.assertIsNotNone(obj.created_at)

    # Verify in database
    self.assertTrue(Model.objects.filter(id=obj.id).exists())

    # Test error case
    with self.assertRaises(ValueError):
        service.create(field1=None)  # Should fail
```

## Infrastructure Integration

The skill leverages existing project infrastructure:

### Logging
```python
from core.diagnostics.logging import get_logger
logger = get_logger('domain.app.module')

# Automatic PII masking
logger.info("User action", email="user@example.com")
# Output: "User action | email=<EMAIL_ADDRESS>"
```

### File Validation
```python
from core.validation import validate_file

# Magika AI content detection (~5ms, 99% accurate)
validate_file(uploaded_file, allowed_types=['pdf', 'docx'], max_size_mb=10)
```

### Error Handling (SOC2 Basic Requirement)
```python
# ✅ Generic error to user, detailed in logs
try:
    result = process_data(input)
except ValueError as e:
    logger.error("Processing failed", error=str(e), user_id=user.id)
    return {"error": "Invalid input. Please try again."}
```

## Installation

1. Download `django-team-standards.zip`
2. Upload to Claude.ai as a project skill
3. The skill will automatically activate when working on Django issues

## Team Usage

Share this skill with your team to ensure:
- ✅ Consistent coding patterns across all team members
- ✅ Proper use of existing infrastructure (no reinventing the wheel)
- ✅ Comprehensive testing standards
- ✅ Security best practices (SOC2 compliance)
- ✅ Documentation maintained and accurate

## Example Usage

```
User: "Let's work on issue #193 - Audit Foundation"

Skill (Phase 1):
- Reading issue #193...
- Checking CLAUDE.md...
- Searching docs/compliance/...
- Note: No existing compliance domain docs found

Skill (Phase 2):
- Exploring codebase...
- Found issue: api/extraction/views.py:156 using standard logging (HIGH severity)
  Options: Fix now, Document in PR, Create issue, Ignore?

User: "Document in PR"

Skill (Phase 3):
# Implementation Plan for Issue #193

## Summary
Building SOC2-compliant audit logging system with immutable logs...

## Components to Create
1. Model: compliance/audit/models.py - Immutable AuditLog model
2. Service: compliance/audit/services.py - AuditService with log_action()
3. Tests: compliance/audit/tests.py - Unit + integration tests
...

## Testing Strategy
- Unit test each service method
- Test immutability enforcement
- Integration test full logging workflow
- Edge cases: null user, system actions, validation errors
...

Should I proceed with this plan?

User: "Yes, proceed"

Skill (Phase 4):
- Creating compliance/audit app...
- Building AuditLog model...
- Creating AuditService...
...

Skill (Phase 5):
- Running tests... ✓ 15 tests passed
- Manual testing immutability... ✓ Works
- Checking database state... ✓ Migrations applied

Skill (Phase 6):
✅ All checks passed! Implementation complete.
```

## Project-Specific Configuration

This skill is designed for Django projects following:
- Domain-driven design (core/, intelligence/, compliance/, etc.)
- Service layer pattern for business logic
- Centralized logging with PII masking
- Magika content-based file validation
- PostgreSQL databases (all environments)

Adapt the skill for your specific project by updating:
- Domain structure in Phase 4
- Infrastructure patterns to match your utilities
- Testing standards to match your requirements

## Contributing

Found improvements or project-specific patterns to add?
Submit PRs to: https://github.com/Saurav-Bayone/SKILLS

## License

MIT License - See LICENSE file in repository
