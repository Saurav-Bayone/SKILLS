# Issue Flagging Guide

This guide explains how to classify and present issues discovered during implementation.

## Severity Levels

### Critical

**Definition**: Security vulnerabilities that could lead to data breaches, system compromise, or immediate harm.

**Examples**:
- Hardcoded secrets (passwords, API keys, tokens)
- SQL injection vulnerabilities (raw SQL without parameterization)
- eval() or exec() on user input
- Missing authentication on sensitive endpoints
- Exposed PII in logs or error messages

**Action**: Must be fixed immediately or create blocking issue

**Example Finding**:
```
File: api/users/views.py:45
Severity: CRITICAL
Issue: Hardcoded API key in source code
Code: `api_key = "sk-1234567890abcdef"`
Fix: Move to environment variable and rotate the exposed key immediately
```

### High

**Definition**: Serious issues that could lead to security problems, data loss, or compliance violations.

**Examples**:
- Using deprecated security functions
- Missing input validation on user data
- Inconsistent PII masking (using `logging.getLogger` instead of `get_logger`)
- Missing authentication checks
- Broad exception handling that swallows errors

**Action**: Should be fixed soon (in current PR or separate high-priority issue)

**Example Finding**:
```
File: core/utils/helpers.py:23
Severity: HIGH
Issue: Using standard logging instead of centralized PII-masking logger
Code: `logger = logging.getLogger(__name__)`
Fix: Replace with `from core.diagnostics.logging import get_logger` and `logger = get_logger('core.utils.helpers')`
Impact: User emails, IPs, and other PII may leak into logs
```

### Medium

**Definition**: Code quality issues, performance problems, or deprecated patterns that should be addressed.

**Examples**:
- Deprecated Django functions
- N+1 database query problems
- Missing database indexes
- Code duplication
- Using extension-based validation instead of Magika
- Inconsistent error handling patterns

**Action**: Fix when convenient or document for later

**Example Finding**:
```
File: recruitment/candidates/views.py:112-125
Severity: MEDIUM
Issue: N+1 query problem - loading related objects in loop
Code:
    for candidate in candidates:
        candidate.applications.all()  # Executes query for each candidate
Fix: Use select_related or prefetch_related:
    candidates = Candidate.objects.all().prefetch_related('applications')
Impact: Performance degrades with large datasets (100+ candidates)
```

### Low

**Definition**: Minor issues that don't affect functionality but reduce code quality or maintainability.

**Examples**:
- TODO/FIXME comments without context
- Unused imports
- Code style inconsistencies
- Dead code
- Missing docstrings
- Suboptimal variable names

**Action**: Fix if easy, otherwise document for cleanup sprint

**Example Finding**:
```
File: intelligence/extraction/utils.py:8
Severity: LOW
Issue: TODO comment without context or issue number
Code: `# TODO: Fix this later`
Fix: Either fix now, or add issue number: `# TODO (#193): Implement caching for extracted entities`
Impact: None, but makes tracking technical debt harder
```

## How to Present Issues to Users

### Format

```
📋 Issue Found During Implementation

File: [file path]:[line number]
Severity: [Critical/High/Medium/Low]

Description:
[What the issue is]

Current Code:
```
[code snippet]
```

Recommended Fix:
[how to fix it]

Impact:
[what could happen if not fixed]

Options:
1. Fix now - Stop current work and fix immediately
2. Document in PR - Add to PR description for reviewer awareness
3. Create separate issue - File GitHub issue for future work
4. Document in commit - Note in commit message
5. Ignore - Skip (please provide reason)

What would you like to do?
```

### Example Presentation

```
📋 Issue Found During Implementation

File: api/extraction/views.py:156
Severity: HIGH

Description:
Using standard Python logging instead of centralized PII-masking logger.
This means user emails, IP addresses, and other PII may leak into log files,
violating SOC2 basic requirements.

Current Code:
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"User {user.email} uploaded file from {request.META['REMOTE_ADDR']}")
```

Recommended Fix:
```python
from core.diagnostics.logging import get_logger
logger = get_logger('api.extraction.views')

logger.info("User uploaded file", user_id=user.id, file_size=file.size)
# Email and IP are automatically masked by centralized logger
```

Impact:
- PII leakage in logs (SOC2 violation)
- Potential GDPR compliance issues
- Security team can't search logs without seeing sensitive data

Options:
1. Fix now - Takes ~5 minutes, straightforward find/replace
2. Document in PR - Reviewer can decide priority
3. Create separate issue - Label as "security", "high priority"
4. Document in commit - Include in commit message
5. Ignore - Not recommended for HIGH severity

What would you like to do?
```

## Grouping Related Issues

When multiple instances of the same issue are found, group them:

```
📋 Multiple Related Issues Found

Issue Type: Using standard logging instead of centralized logger
Severity: HIGH
Instances: 7 files

Files affected:
- api/extraction/views.py:156, 178, 203
- intelligence/extraction/services.py:45, 89
- core/storage/services.py:123
- api/users/views.py:67

Recommended Fix:
Replace all instances of:
  `import logging; logger = logging.getLogger(__name__)`
With:
  `from core.diagnostics.logging import get_logger; logger = get_logger('module.path')`

Estimated Time: 15 minutes for all 7 files

Options:
1. Fix all now
2. Fix critical files now (api/), document rest
3. Create single issue for all instances
4. Ignore

What would you like to do?
```

## Tracking Decisions

Maintain a list of user decisions for Phase 5:

```
Issues Found and Resolved:
1. [FIXED] api/extraction/views.py:156 - Replaced standard logging with centralized logger (HIGH)
2. [PR_DOCS] N+1 queries in recruitment/candidates (MEDIUM) - Added to PR description
3. [ISSUE_#xyz] TODO comments cleanup (LOW) - Created issue #xyz
4. [IGNORED] Old comment style in legacy code (LOW) - User decision: cleanup in separate sprint
```

## Common Issues by Category

### Security
- Hardcoded secrets → CRITICAL
- SQL injection → CRITICAL
- Missing authentication → HIGH
- PII in logs → HIGH
- Weak password validation → MEDIUM

### Performance
- N+1 queries → MEDIUM
- Missing indexes → MEDIUM
- Loading entire table into memory → HIGH
- Inefficient file I/O → MEDIUM

### Code Quality
- Code duplication → MEDIUM
- Missing error handling → MEDIUM to HIGH
- Inconsistent patterns → MEDIUM
- TODO without context → LOW
- Missing docstrings → LOW

### Django Patterns
- Not using service layer → MEDIUM
- Business logic in views/models → MEDIUM
- Not using `DJANGO_ENVIRONMENT=local` → HIGH
- Extension-based validation → MEDIUM
- Deprecated Django functions → MEDIUM
