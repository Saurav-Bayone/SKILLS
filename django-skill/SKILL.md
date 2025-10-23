---
name: django-issue-automation
description: Django automation with documentation validation and issue flagging
---

# Django Issue Automation Skill

Automated Django implementation that validates against existing documentation and flags unrelated issues.

## Key Features

- **Documentation Validation** - Reads existing feature docs and validates implementation matches
- **Global PII Masking** - Uses your existing PII masking infrastructure
- **File Validation** - Integrates with your Magika file validation
- **Centralized Logging** - Uses your existing logging system
- **Issue Flagging** - Identifies and flags unrelated issues found during implementation
- **Never Assumes** - Always asks when documentation doesn't match reality

## How It Works

1. **Reads ALL your documentation** including:
   - `CLAUDE.md` - Project configuration
   - `pyproject.toml` - Your dependencies (Poetry)
   - `docs/<feature>/*.md` - Feature documentation
   - `docs/security/pii_masking.md` - PII handling docs
   - `docs/infrastructure/logging.md` - Logging patterns
   - `docs/validation/magika.md` - File validation docs

2. **Validates implementation plan against docs**:
   - "Your docs say PII uses global masking, but I don't see the import. Should I add it?"
   - "Documentation mentions Magika validation but it's not in this module. Should I integrate it?"
   - "Your logging docs specify format X but I see format Y in code. Which should I use?"

3. **Flags unrelated issues**:
   - "Found TODO comment in authentication module - should I create issue?"
   - "Noticed deprecated function in models.py - flag in PR or new issue?"
   - "Security vulnerability in unrelated code - create urgent issue?"

## Workflow

1. **Deep Documentation Read** - Reads ALL relevant feature docs
2. **Cross-Validation** - Checks if docs match actual code
3. **Clarification Phase** - Asks about any discrepancies
4. **Issue Detection** - Identifies unrelated problems
5. **User Decision** - You decide: fix now, flag in PR, or new issue
6. **Implementation** - Follows validated documentation
7. **Final Check** - Ensures implementation matches docs

## What Makes This Different

- **Never trusts docs blindly** - Always validates against actual code
- **Catches documentation drift** - Identifies when docs are outdated
- **Proactive issue detection** - Finds problems before they become bugs
- **Uses YOUR infrastructure** - PII masking, Magika, centralized logging
- **Maintains code hygiene** - Flags TODOs, deprecations, vulnerabilities
- **Zero configuration** - Reads everything from YOUR files

## Required Project Structure

```
your_project/
├── CLAUDE.md                        # Your project config
├── pyproject.toml                   # Your Poetry dependencies
├── docs/
│   ├── FEATURE_BRANCH_WORKFLOW.md  # Git workflow
│   ├── security/
│   │   └── pii_masking.md         # Global PII masking docs
│   ├── validation/
│   │   └── magika.md              # File validation docs
│   ├── infrastructure/
│   │   └── logging.md             # Centralized logging docs
│   └── <feature>/
│       ├── architecture.md
│       ├── api.md
│       └── implementation.md
```

## Usage Examples

When you say "Work on issue #45", the skill will:

1. Read your CLAUDE.md and all docs
2. Find that your docs say to use `GlobalPIIMasker`
3. Check if code actually uses it
4. Ask you if discrepancies are found
5. Scan for unrelated issues
6. Ask how to handle them (fix/flag/new issue)
7. Create validated implementation plan
8. Wait for your approval

## Issue Flagging

When unrelated issues are found:

**CRITICAL** (immediate attention):
- SQL injection vulnerabilities
- Hardcoded passwords/secrets
- Security vulnerabilities

**HIGH** (should fix soon):
- eval/exec usage
- Deprecated security functions

**MEDIUM** (technical debt):
- Deprecated functions
- Performance issues

**LOW** (cleanup):
- TODO comments
- FIXME notes

You decide for each severity level:
1. Fix now in this implementation
2. Flag in PR for later
3. Create separate issue
4. Ignore (not recommended)

## Environment

Always uses:
```bash
DJANGO_ENVIRONMENT=local
```

## What This Skill Does NOT Do

- Never proceeds without your approval
- Never ignores documentation
- Never assumes when unclear
- Never skips validation
- Never leaves critical issues unflagged
- Never adds dependencies to the skill (uses YOUR pyproject.toml)