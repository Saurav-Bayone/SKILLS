---
name: "django-codebase-analyzer"
description: "Analyzes Django codebases to generate comprehensive technical documentation"
---

# Django Codebase Analyzer

## Purpose
Guide Claude to analyze existing Django codebases and create comprehensive technical documentation including architecture overview, system design, data flow diagrams, user stories, and code quality metrics extracted from the actual implementation.

## When to Use This Skill
- User uploads or provides path to a Django project
- User requests documentation for their Django codebase  
- User needs architecture diagrams or technical documentation
- User wants to understand an unfamiliar Django codebase

## Environment Context
- Assumes WSL Ubuntu 22.04 environment
- Works with Python 3.8+ Django projects
- Handles both monolithic and microservice Django architectures

## Required Inputs
- Path to Django project root (where manage.py is located)
- Optional: Documentation focus areas (architecture, security, performance)
- Optional: Specific apps to focus on (for large projects)

## Pre-Analysis Commands

```bash
# For WSL Ubuntu environment, ensure proper line endings
dos2unix /path/to/project/**/*.py 2>/dev/null || true

# Check Python version used
python3 --version

# Install analysis tools if needed
pip install pipreqs pylint-django radon --break-system-packages 2>/dev/null || true
```

## Analysis Process

### Phase 1: Initial Project Discovery

1. **Verify Django Project**
   ```bash
   # Check for Django project markers
   ls -la /path/to/project/manage.py
   cat /path/to/project/requirements*.txt | grep -i django
   find /path/to/project -name "settings*.py" | head -5
   ```

2. **Detect Project Configuration Style**
   - Check for settings module (settings/ directory vs settings.py)
   - Identify environment-specific settings (development, staging, production)
   - Check for .env files and environment variable usage
   - Detect use of django-environ or python-decouple

3. **Read Project Configuration**
   - **Core Settings to Document**:
     - INSTALLED_APPS (categorize as Django core, third-party, custom)
     - DATABASES (type, connection pooling)
     - MIDDLEWARE (custom vs third-party)
     - Authentication backends (custom, social, LDAP)
     - REST_FRAMEWORK settings (if using DRF)
     - CELERY settings (if using Celery)
     - CACHES configuration
     - Email backend
     - Storage backend (S3, local, etc.)
     - ALLOWED_HOSTS and CORS settings
     - Logging configuration

4. **Map Complete Project Structure**
   ```bash
   # Get detailed project structure
   tree -L 3 -I '__pycache__|*.pyc|.git|node_modules|venv|env' /path/to/project

   # Alternative if tree not available
   find /path/to/project -type f -name "*.py" | grep -v "__pycache__" | sort | head -50
   
   # Count lines of code
   find /path/to/project -name "*.py" -type f -exec wc -l {} + | sort -rn | head -20
   ```

5. **Identify Django Version and Dependencies**
   ```bash
   # Get Django version
   grep -E "^Django|^django" /path/to/project/requirements*.txt
   
   # List all dependencies
   cat /path/to/project/requirements*.txt | grep -v "^#" | sort
   
   # Check for common Django packages
   grep -E "djangorestframework|celery|redis|channels|django-cors|django-debug-toolbar" requirements*.txt
   ```

### Phase 2: Detailed Component Analysis

#### For each Django app found in INSTALLED_APPS:

1. **Analyze Models (models.py or models/)**
   - Document all model classes
   - Field types and validation rules
   - Relationships with cardinality (1:1, 1:N, M:N)
   - Model inheritance (abstract, proxy, multi-table)
   - Custom model managers and querysets
   - Model methods and properties
   - Signals connected to models
   - Database indexes and constraints
   - Custom validators
   - Model Meta options:
     - db_table (custom table names)
     - ordering
     - unique_together / constraints
     - permissions
     - indexes

2. **Analyze Views (views.py or views/)**
   - **Function-Based Views (FBVs)**:
     - HTTP methods handled
     - Decorators used (@login_required, @csrf_exempt, etc.)
     - Template rendered or JSON response
   
   - **Class-Based Views (CBVs)**:
     - Base classes used (ListView, DetailView, CreateView, etc.)
     - Mixins employed
     - Method overrides (get_queryset, get_context_data)
     - Permission classes
   
   - **Django REST Framework ViewSets**:
     - ViewSet type (ModelViewSet, ReadOnlyModelViewSet, etc.)
     - Queryset definition
     - Serializer classes
     - Permission classes
     - Authentication classes
     - Filter backends and ordering
     - Custom actions (@action decorator)
     - Pagination configuration

3. **Analyze URL Configuration (urls.py)**
   - Main project URL configuration
   - App-level URL patterns
   - URL namespacing
   - URL parameters and converters
   - Include patterns
   - Static/Media file serving (development)
   - API versioning strategy (if applicable)
   - Router configuration (for DRF)

4. **Analyze Serializers (serializers.py - if using DRF)**
   - Serializer types (ModelSerializer, Serializer)
   - Field configuration (read_only, write_only, required)
   - Nested serializers
   - SerializerMethodFields
   - Custom validation methods
   - Custom create/update methods
   - Meta options (fields, exclude, depth)

5. **Analyze Forms (forms.py)**
   - Form types (Form, ModelForm)
   - Field definitions and widgets
   - Validation methods (clean_*, clean)
   - Formsets usage
   - Crispy forms configuration (if used)

6. **Analyze Admin Configuration (admin.py)**
   - Registered models
   - Custom admin classes
   - List display configuration
   - Search fields and filters
   - Inline models
   - Custom admin actions
   - Admin site customization

7. **Analyze Additional Components**
   - **signals.py**: Event handlers and receivers
   - **tasks.py**: Celery/background tasks
   - **middleware.py**: Custom middleware classes
   - **context_processors.py**: Custom context processors
   - **templatetags/**: Custom template tags and filters
   - **management/commands/**: Custom Django commands
   - **consumers.py**: WebSocket consumers (if using Channels)
   - **tests.py or tests/**: Test coverage and test types

8. **Analyze Templates (templates/)**
   - Template structure and inheritance
   - Base templates
   - Include and extend patterns
   - Custom template tags usage
   - Static file references

9. **Analyze Static Files and Frontend**
   - CSS framework (Bootstrap, Tailwind, etc.)
   - JavaScript files and framework (if any)
   - Asset pipeline (webpack, django-compress)

### Phase 3: Cross-Cutting Concerns Analysis

1. **Authentication & Authorization**
   - User model (default or custom)
   - Authentication methods (session, token, JWT)
   - Permission system usage
   - Groups and roles
   - Third-party auth (OAuth, SAML)

2. **Database Analysis**
   - Database backend(s) used
   - Read/write splitting
   - Connection pooling
   - Raw SQL usage
   - Database views and stored procedures
   - Migration history analysis

3. **Caching Strategy**
   - Cache backend (Redis, Memcached)
   - Cache usage patterns
   - Cache keys structure
   - Cache invalidation

4. **API Documentation**
   - API endpoints inventory
   - HTTP methods and status codes
   - Request/Response formats
   - Authentication requirements
   - Rate limiting
   - API versioning

5. **Background Tasks**
   - Task queue (Celery, Django-Q)
   - Scheduled tasks (celery beat)
   - Task priorities and queues
   - Task error handling

6. **Logging and Monitoring**
   - Logging configuration
   - Log levels used
   - Custom loggers
   - Error tracking integration (Sentry, etc.)

### Phase 4: Code Quality Metrics

```bash
# Analyze code complexity
radon cc /path/to/project -a -nb

# Check for code smells
pylint --load-plugins pylint_django /path/to/project/app_name/

# Count TODO/FIXME/HACK comments
grep -r "TODO\|FIXME\|HACK" /path/to/project --include="*.py" | wc -l
```

### Phase 5: Documentation Generation

Create the following documentation files:

#### 1. Architecture Overview (01_architecture_overview.md)

```markdown
# [Project Name] Architecture Documentation

## Executive Summary
[Brief description of what the application does, extracted from code analysis]

## Project Metrics
- **Django Version**: [version]
- **Python Version**: [version]
- **Lines of Code**: [total]
- **Number of Apps**: [count]
- **Number of Models**: [count]
- **Number of API Endpoints**: [count]
- **Test Coverage**: [if available]

## Technology Stack

### Core Framework
- **Django**: [version]
- **Python**: [version]
- **Database**: [PostgreSQL/MySQL/SQLite + version]

### API Layer
- **REST Framework**: Django REST Framework [version] (if used)
- **GraphQL**: Graphene-Django (if used)
- **WebSockets**: Django Channels (if used)

### Infrastructure Components
- **Task Queue**: Celery [version] with [Redis/RabbitMQ]
- **Cache**: [Redis/Memcached]
- **Search**: [Elasticsearch/PostgreSQL Full Text]
- **File Storage**: [Local/S3/Azure Blob]
- **Email**: [SMTP/SendGrid/AWS SES]

### Frontend (if applicable)
- **Template Engine**: Django Templates / Jinja2
- **CSS Framework**: [Bootstrap/Tailwind]
- **JavaScript**: [Vanilla/jQuery/Vue/React]

### Development & Deployment
- **Environment**: WSL Ubuntu 22.04
- **Package Manager**: pip/pipenv/poetry
- **WSGI Server**: [Gunicorn/uWSGI]
- **Web Server**: [Nginx/Apache]
- **Container**: Docker (if dockerized)

## System Architecture

\`\`\`mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser]
        MOBILE[Mobile App]
        API_CLIENT[API Clients]
    end
    
    subgraph "Load Balancer"
        LB[Nginx/HAProxy]
    end
    
    subgraph "Application Layer"
        subgraph "Django Application"
            WSGI[WSGI Server]
            DJANGO[Django Core]
            DRF[REST Framework]
            CHANNELS[Channels/WebSockets]
        end
    end
    
    subgraph "Background Processing"
        CELERY[Celery Workers]
        BEAT[Celery Beat]
    end
    
    subgraph "Data Layer"
        DB[(Primary Database)]
        CACHE[(Redis Cache)]
        QUEUE[(Message Queue)]
        STORAGE[File Storage]
    end
    
    WEB --> LB
    MOBILE --> LB
    API_CLIENT --> LB
    LB --> WSGI
    WSGI --> DJANGO
    DJANGO --> DRF
    DJANGO --> CHANNELS
    DJANGO --> DB
    DJANGO --> CACHE
    DJANGO --> CELERY
    CELERY --> QUEUE
    BEAT --> QUEUE
    CELERY --> DB
    DJANGO --> STORAGE
\`\`\`

## Django Applications

### Core Applications

[For each custom app, create a section like this:]

#### [app_name]
- **Path**: `apps/[app_name]/` or `[app_name]/`
- **Purpose**: [Inferred from models and views]
- **Type**: [Business Logic / API / Admin / Utility]

**Key Components**:
- **Models** ([count]): [List main models]
- **Views** ([count]): [List view types - CBV/FBV/ViewSets]
- **API Endpoints** ([count]): [If applicable]
- **Background Tasks** ([count]): [If applicable]
- **Templates** ([count]): [If applicable]

**Dependencies**:
- Depends on: [List apps this app imports from]
- Used by: [List apps that import from this app]

**Key Features**:
- [Feature 1 based on views/models]
- [Feature 2]
- [Feature 3]

### Third-Party Applications
[List key third-party Django apps and their purpose]
- **django-rest-framework**: RESTful API implementation
- **django-cors-headers**: CORS handling
- **django-filter**: Advanced filtering
- [etc.]

## Security Configuration
- **Authentication**: [Session/Token/JWT/OAuth]
- **CORS**: [Enabled/Disabled, allowed origins]
- **CSRF**: [Enabled/Disabled]
- **SSL**: [Required/Optional]
- **Rate Limiting**: [If configured]
- **Permissions**: [Permission classes used]
```

#### 2. Data Model Documentation (02_data_models.md)

```markdown
# Data Model Documentation

## Database Configuration
- **Engine**: [PostgreSQL/MySQL/SQLite]
- **Name**: [database_name]
- **Host**: [host info if not sensitive]
- **Connection Pooling**: [Yes/No]
- **Read Replicas**: [If configured]

## Entity Relationship Diagram

\`\`\`mermaid
erDiagram
    [Generate comprehensive ER diagram based on all models]
    
    User ||--o{ UserProfile : "has one"
    User ||--o{ Post : "creates"
    Post ||--|{ Comment : "has many"
    User ||--o{ Comment : "writes"
    Post }|--|{ Tag : "tagged with"
    
    User {
        int id PK
        string username UK
        string email UK
        string password
        boolean is_active
        datetime date_joined
    }
    
    Post {
        int id PK
        int author_id FK
        string title
        text content
        string slug UK
        datetime created_at
        datetime updated_at
        boolean is_published
    }
\`\`\`

## Model Specifications

[For each app and model:]

### [App Name]

#### Model: [ModelName]
**File**: `[app_name]/models.py`
**Database Table**: `[table_name]`
**Purpose**: [Detailed description]

**Fields**:
| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | AutoField | PRIMARY KEY | auto | Primary key |
| [field_name] | [Django field type] | [null, blank, unique] | [default] | [purpose] |

**Relationships**:
| Related Model | Relationship Type | Field | Related Name | Description |
|---------------|------------------|-------|--------------|-------------|
| [Model] | ForeignKey | [field_name] | [related_name] | [purpose] |
| [Model] | ManyToMany | [field_name] | [related_name] | [purpose] |

**Indexes**:
- Single: [field_name] - [reason]
- Composite: [field1, field2] - [reason]
- Unique: [field_name] - [constraint description]

**Model Methods**:
| Method | Returns | Description |
|--------|---------|-------------|
| __str__() | string | [String representation] |
| get_absolute_url() | string | [URL pattern] |
| [custom_method]() | [type] | [purpose] |

**Model Properties**:
| Property | Type | Description |
|----------|------|-------------|
| [property_name] | [type] | [computed value description] |

**Signals**:
- pre_save: [handler and purpose]
- post_save: [handler and purpose]
- pre_delete: [handler and purpose]

**Manager Methods**:
| Method | Returns | Description |
|--------|---------|-------------|
| [custom_manager_method]() | QuerySet | [purpose] |

**Meta Options**:
- ordering: [fields]
- unique_together: [field combinations]
- permissions: [custom permissions]
- verbose_name: [name]
```

#### 3. API Documentation (03_api_documentation.md)

```markdown
# API Documentation

## API Overview
- **Base URL**: `/api/` or `/api/v1/`
- **Format**: JSON (REST) / GraphQL
- **Authentication**: [Token/JWT/Session/OAuth]
- **Pagination**: [PageNumberPagination/LimitOffsetPagination]
- **Rate Limiting**: [requests per minute/hour]

## Authentication Endpoints

### POST /api/auth/login/
**Description**: Authenticate user and obtain token
**Authentication Required**: No
**Request Body**:
\`\`\`json
{
    "username": "string",
    "password": "string"
}
\`\`\`
**Response** (200 OK):
\`\`\`json
{
    "token": "string",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string"
    }
}
\`\`\`

[Continue for all endpoints...]

## Resource Endpoints

### [Resource Name] (/api/[resource]/)

#### GET /api/[resource]/
**Description**: List all [resources]
**Authentication Required**: [Yes/No]
**Permissions**: [Permission classes]
**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `search`: Search term
- `ordering`: Field to sort by
- `[filter_field]`: Filter by field value

**Response** (200 OK):
\`\`\`json
{
    "count": "integer",
    "next": "url",
    "previous": "url",
    "results": [
        {
            "id": "integer",
            "field1": "value",
            "field2": "value"
        }
    ]
}
\`\`\`

#### GET /api/[resource]/{id}/
**Description**: Retrieve single [resource]
**Authentication Required**: [Yes/No]
**URL Parameters**:
- `id`: Resource ID

**Response** (200 OK):
\`\`\`json
{
    "id": "integer",
    "field1": "value",
    "field2": "value",
    "created_at": "datetime",
    "updated_at": "datetime"
}
\`\`\`

#### POST /api/[resource]/
**Description**: Create new [resource]
**Authentication Required**: Yes
**Permissions**: [IsAuthenticated/custom]
**Request Body**:
\`\`\`json
{
    "field1": "required|string",
    "field2": "optional|integer",
    "field3": "required|array"
}
\`\`\`

**Validation Rules**:
- field1: Required, max length 255
- field2: Optional, must be positive integer
- field3: Required, must contain valid IDs

**Response** (201 Created):
\`\`\`json
{
    "id": "integer",
    "field1": "value",
    "field2": "value"
}
\`\`\`

#### PUT/PATCH /api/[resource]/{id}/
**Description**: Update [resource]
**Authentication Required**: Yes
**Permissions**: [IsOwner/custom]

#### DELETE /api/[resource]/{id}/
**Description**: Delete [resource]
**Authentication Required**: Yes
**Permissions**: [IsOwner/IsAdmin]
**Response** (204 No Content)

### Custom Actions

#### POST /api/[resource]/{id}/[action]/
**Description**: [Custom action description]
**Authentication Required**: Yes
**Business Logic**: [What this action does]

## Error Responses

### 400 Bad Request
\`\`\`json
{
    "error": "validation_error",
    "details": {
        "field_name": ["Error message"]
    }
}
\`\`\`

### 401 Unauthorized
\`\`\`json
{
    "error": "authentication_required",
    "message": "Authentication credentials were not provided"
}
\`\`\`

### 403 Forbidden
\`\`\`json
{
    "error": "permission_denied",
    "message": "You do not have permission to perform this action"
}
\`\`\`

### 404 Not Found
\`\`\`json
{
    "error": "not_found",
    "message": "Resource not found"
}
\`\`\`

## WebSocket Endpoints (if using Channels)

### WebSocket /ws/[namespace]/
**Description**: [WebSocket purpose]
**Authentication**: [Token in query params/headers]
**Events**:
- `connect`: Initial connection
- `message`: Receive message
- `disconnect`: Connection closed

**Message Format**:
\`\`\`json
{
    "type": "event_type",
    "data": {
        "field": "value"
    }
}
\`\`\`
```

#### 4. Business Logic & Data Flow (04_business_logic.md)

```markdown
# Business Logic & Data Flow

## Core Business Processes

### User Registration Flow

\`\`\`mermaid
sequenceDiagram
    participant Client
    participant API
    participant Serializer
    participant Model
    participant Database
    participant Email
    participant Cache
    
    Client->>API: POST /api/register/
    API->>Serializer: Validate input
    Serializer->>Serializer: Check email uniqueness
    Serializer->>Model: Create User instance
    Model->>Database: Save user
    Database-->>Model: User created
    Model->>Email: Send verification email
    Model->>Cache: Store verification token
    Model-->>API: User object
    API-->>Client: 201 Created + User data
\`\`\`

### Order Processing Flow (Example)

\`\`\`mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted: Submit order
    Submitted --> PaymentPending: Confirm
    PaymentPending --> Paid: Payment success
    PaymentPending --> Cancelled: Payment failed
    Paid --> Processing: Start fulfillment
    Processing --> Shipped: Ship items
    Shipped --> Delivered: Confirm delivery
    Delivered --> [*]
    Cancelled --> [*]
\`\`\`

## Background Task Processing

### Celery Tasks

#### Task: [task_name]
**Module**: `[app_name]/tasks.py`
**Queue**: [queue_name]
**Schedule**: [If periodic - cron expression]
**Purpose**: [What this task does]

**Flow**:
1. [Trigger condition]
2. [Processing steps]
3. [Success handling]
4. [Error handling]

## Caching Strategy

### Cache Keys Structure
- User data: `user:{user_id}:profile`
- List views: `{model}:list:{filter_hash}:page:{page}`
- Detail views: `{model}:detail:{id}`
- API responses: `api:{endpoint}:{params_hash}`

### Cache Invalidation
- Model save: Invalidate detail and list caches
- Model delete: Invalidate all related caches
- Bulk operations: Clear entire cache namespace

## Permission & Authorization Logic

### Permission Classes
| Permission | Description | Used In |
|------------|-------------|---------|
| IsAuthenticated | User must be logged in | Most views |
| IsOwner | User must own the object | Update/Delete |
| IsAdminUser | User must be admin | Admin views |
| [CustomPermission] | [Logic description] | [Views] |

## Validation Rules

### Model Validation
[Document custom validators and clean methods]

### Serializer Validation
[Document serializer validation methods]

### Form Validation
[Document form validation logic]
```

#### 5. User Stories (05_user_stories.md)

```markdown
# User Stories & Features

## User Roles
Based on the permission system, the following user roles exist:
- **Anonymous User**: Non-authenticated visitor
- **Registered User**: Authenticated user
- **Staff User**: Can access admin panel
- **Superuser**: Full system access
- **[Custom Role]**: [Description based on groups/permissions]

## Authentication & User Management

### User Registration
**As a** visitor  
**I want to** create an account  
**So that** I can access protected features

**Acceptance Criteria**:
- [✓] Valid email address required
- [✓] Password must meet security requirements
- [✓] Email verification required
- [✓] Username must be unique

**Technical Implementation**:
- Endpoint: `POST /api/auth/register/`
- View: `accounts.views.RegisterView`
- Serializer: `accounts.serializers.UserRegistrationSerializer`
- Models: `User`, `UserProfile`
- Signals: Creates UserProfile on User creation
- Email: Sends verification email via Celery task

### Password Reset
**As a** registered user  
**I want to** reset my forgotten password  
**So that** I can regain account access

**Acceptance Criteria**:
- [✓] Request reset via email
- [✓] Receive secure reset token
- [✓] Token expires after 24 hours
- [✓] Old password invalidated after reset

[Continue for all major features...]

## [App Name] Features

### [Feature Name based on views]
**As a** [user role from permissions]  
**I want to** [action from view/endpoint]  
**So that** [business value inferred]

**Acceptance Criteria**:
- [✓] [Validation from serializer]
- [✓] [Permission check from view]
- [✓] [Business rule from model]

**Technical Details**:
- URL: `[pattern]`
- View: `[app].[viewfile].[ViewClass]`
- Template: `[template path]` (if applicable)
- API Endpoint: `[endpoint]` (if applicable)
- Permissions: `[permission classes]`
- Cache: `[caching strategy]`
```

#### 6. Deployment & Operations (06_deployment_operations.md)

```markdown
# Deployment & Operations Guide

## Development Environment Setup

### Prerequisites
- Python [version]
- PostgreSQL/MySQL [version]
- Redis [version] (if used)
- Node.js [version] (if needed for frontend)

### Local Setup (WSL Ubuntu 22.04)
\`\`\`bash
# Clone repository
git clone [repository]
cd [project-name]

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists

# Setup database
createdb [database_name]
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (if fixtures exist)
python manage.py loaddata [fixtures]

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
\`\`\`

## Environment Variables
Required environment variables (from settings analysis):
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection (if used)
- `DEBUG`: True/False
- `ALLOWED_HOSTS`: Comma-separated hosts
- [List all found in settings]

## Management Commands

### Custom Commands
| Command | Purpose | Usage |
|---------|---------|-------|
| [command_name] | [purpose] | `python manage.py [command] [args]` |

## Database Operations

### Migrations
\`\`\`bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate [app_name] [migration_number]
\`\`\`

### Database Optimization
- Indexes identified: [List key indexes]
- Query optimization: [select_related, prefetch_related usage]
- Database connections: [connection pooling setup]

## Background Tasks

### Celery Setup
\`\`\`bash
# Start Celery worker
celery -A [project_name] worker -l info

# Start Celery beat (for periodic tasks)
celery -A [project_name] beat -l info

# Monitor with Flower
celery -A [project_name] flower
\`\`\`

### Scheduled Tasks
| Task | Schedule | Purpose |
|------|----------|---------|
| [task_name] | [cron expression] | [purpose] |

## Monitoring & Logging

### Log Files
- Application logs: `[path]`
- Error logs: `[path]`
- Access logs: `[path]`

### Health Checks
- Database connectivity: `/health/db/`
- Cache connectivity: `/health/cache/`
- Celery status: `/health/celery/`

## Performance Considerations

### Identified Bottlenecks
- [N+1 queries in specific views]
- [Missing database indexes]
- [Synchronous operations that could be async]

### Caching Implementation
- Cache backend: [Redis/Memcached]
- Cached views: [List]
- Cache TTL: [Duration]

## Security Checklist
- [ ] DEBUG = False in production
- [ ] SECRET_KEY is secure and not in code
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enforced
- [ ] CSRF protection enabled
- [ ] XSS protection headers
- [ ] SQL injection prevention (using ORM)
- [ ] Rate limiting configured
- [ ] Sensitive data encrypted
```

#### 7. Testing Documentation (07_testing.md)

```markdown
# Testing Documentation

## Test Coverage
- **Overall Coverage**: [percentage if available]
- **Apps with Tests**: [list]
- **Apps without Tests**: [list]

## Test Structure

### Unit Tests
Location: `[app_name]/tests/test_models.py`

#### Model Tests
- Field validation
- Model methods
- Signal handlers
- Model relationships

#### View Tests  
- HTTP response codes
- Template rendering
- Context data
- Authentication/permissions
- Form processing

#### API Tests
- Endpoint accessibility
- Response format
- Authentication
- Permissions
- Data validation
- Pagination

### Integration Tests
- User workflows
- API integration
- Background task execution
- Cache behavior

### Test Data
- Fixtures: `[app_name]/fixtures/`
- Factories: Using factory_boy (if present)
- Test database: SQLite/PostgreSQL

## Running Tests

\`\`\`bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test [app_name]

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run specific test class
python manage.py test [app_name].tests.TestClassName

# Run with verbose output
python manage.py test --verbosity=2
\`\`\`

## Continuous Integration
- CI Tool: [GitHub Actions/GitLab CI/Jenkins]
- Test stages: [Linting, Unit tests, Integration tests]
- Coverage requirements: [minimum percentage]
```

#### 8. README.md (Summary)

```markdown
# [Project Name] Technical Documentation

## 📋 Overview
[Project description extracted from code analysis]

**Documentation Generated**: [Current date]
**Analysis Performed on**: WSL Ubuntu 22.04
**Django Version**: [version]
**Python Version**: [version]

## 📚 Documentation Index

### Architecture & Design
1. **[Architecture Overview](./01_architecture_overview.md)**
   - System architecture diagrams
   - Technology stack
   - Application structure
   - Component interactions

2. **[Data Models](./02_data_models.md)**
   - Complete ER diagrams
   - Model specifications
   - Database schema
   - Relationships mapping

3. **[API Documentation](./03_api_documentation.md)**
   - REST endpoints
   - Request/Response formats
   - Authentication
   - WebSocket events

### Implementation Details
4. **[Business Logic](./04_business_logic.md)**
   - Core workflows
   - State machines
   - Background tasks
   - Caching strategy

5. **[User Stories](./05_user_stories.md)**
   - Feature documentation
   - User roles
   - Acceptance criteria
   - Technical implementation

### Operations
6. **[Deployment & Operations](./06_deployment_operations.md)**
   - Setup instructions
   - Environment configuration
   - Management commands
   - Monitoring

7. **[Testing](./07_testing.md)**
   - Test coverage
   - Test structure
   - Running tests
   - CI/CD pipeline

## 🔑 Key Metrics

| Metric | Value |
|--------|-------|
| Total Lines of Code | [count] |
| Number of Apps | [count] |
| Number of Models | [count] |
| Number of Views | [count] |
| API Endpoints | [count] |
| Test Coverage | [percentage] |
| Background Tasks | [count] |
| Database Tables | [count] |

## 🏗️ Application Structure

\`\`\`
[project_name]/
├── [project_name]/        # Main project directory
│   ├── settings/          # Settings module
│   ├── urls.py           # Root URL config
│   └── wsgi.py           # WSGI application
├── apps/                  # Django applications
│   ├── [app1]/
│   ├── [app2]/
│   └── [app3]/
├── templates/            # HTML templates
├── static/               # Static files
├── media/                # User uploads
├── requirements.txt      # Python dependencies
└── manage.py            # Django CLI
\`\`\`

## 🚀 Quick Start

### Prerequisites
- Python [version]
- PostgreSQL/MySQL
- Redis (if using caching/Celery)

### Basic Setup
\`\`\`bash
# Clone and setup
git clone [repository]
cd [project_name]
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver
\`\`\`

Visit: http://localhost:8000

## 🔗 Important Links
- Admin Panel: `/admin/`
- API Documentation: `/api/docs/` (if configured)
- Health Check: `/health/`

## 📝 Notes & Observations

### Strengths
- [Identified strong points in architecture]
- [Good practices observed]

### Areas for Improvement
- [Identified potential issues]
- [Missing best practices]
- [Technical debt]

### Recommendations
- [Specific suggestions based on analysis]

---
*This documentation was auto-generated by analyzing the Django codebase. For questions or updates, refer to the source code as the source of truth.*
```

### Phase 6: Final Output Organization

Create this structure in `/mnt/user-data/outputs/`:
```
[project-name]-documentation/
├── README.md
├── 01_architecture_overview.md
├── 02_data_models.md
├── 03_api_documentation.md
├── 04_business_logic.md
├── 05_user_stories.md
├── 06_deployment_operations.md
├── 07_testing.md
└── analysis/
    ├── code_metrics.txt
    ├── dependencies.txt
    └── security_notes.txt
```

## Additional Analysis Utilities

### Quick Commands for Common Patterns

```bash
# Find all TODO/FIXME comments
grep -rn "TODO\|FIXME\|HACK\|XXX\|NOTE" --include="*.py" /path/to/project

# Find all model classes
grep -r "class.*Model):" --include="*.py" /path/to/project

# Find all API endpoints
grep -r "@api_view\|ViewSet\|APIView" --include="*.py" /path/to/project

# Find raw SQL queries
grep -r "raw(\|execute(\|cursor" --include="*.py" /path/to/project

# Find hardcoded secrets (basic check)
grep -r "SECRET\|PASSWORD\|API_KEY" --include="*.py" /path/to/project | grep -v "os.environ\|settings"

# Count test files
find /path/to/project -name "test*.py" -o -name "*test.py" | wc -l

# List all URL patterns
grep -r "path(\|url(\|re_path(" --include="urls.py" /path/to/project
```

## Quality Checks Before Delivery

1. **Completeness**
   - [ ] All INSTALLED_APPS documented
   - [ ] All models mapped with relationships
   - [ ] All URL patterns documented
   - [ ] All API endpoints listed
   - [ ] User flows captured

2. **Accuracy**
   - [ ] Django version correct
   - [ ] Dependencies properly listed
   - [ ] Model fields match actual code
   - [ ] API endpoints tested if possible

3. **Diagrams**
   - [ ] Architecture diagram includes all components
   - [ ] ER diagram shows all relationships
   - [ ] Flow diagrams are logically correct
   - [ ] Mermaid syntax is valid

4. **Readability**
   - [ ] Clear section headings
   - [ ] Consistent formatting
   - [ ] Code examples properly formatted
   - [ ] Tables align correctly

## Important Notes

1. **Always base on actual code** - Read the files, don't assume
2. **Note uncertainties** - If something is unclear, document it
3. **WSL considerations** - Be aware of line ending issues (CRLF vs LF)
4. **Version specific** - Note Django version differences
5. **Security awareness** - Don't expose sensitive information in docs
6. **Focus on what exists** - Document current state, not ideal state

## Error Handling

- **Import errors**: Note missing dependencies but continue
- **Complex project structure**: Document as found, note any confusion
- **Missing standard files**: Check for alternative locations
- **Large codebases**: Focus on core functionality first
- **Legacy code**: Note deprecated patterns found

## Final Note

This skill is designed to create comprehensive documentation from Django codebases running on WSL Ubuntu 22.04. The documentation should serve as both a technical reference and an onboarding guide for new developers. Always prioritize accuracy over assumptions, and clearly mark any areas where the code structure or purpose is uncertain.
