# Common Django Patterns - Talent AI Platform

This document provides detailed code examples for common patterns used in the Talent AI platform based on existing infrastructure.

## Service Layer Pattern

### Basic Service with Module-Level Instance

Based on `intelligence/extraction/services/extraction_orchestrator.py`:

```python
# domain/app_name/services.py
from core.diagnostics.logging import get_logger

logger = get_logger('domain.app_name.service_name')

class MyService:
    """
    Service for [business capability].

    Business Logic:
    - [What this service does]
    - [Key responsibilities]

    Example:
        from domain.app_name.services import my_service
        result = my_service.do_something(param1, param2)
    """

    def do_something(self, param1, param2):
        """
        [What this method does]

        Args:
            param1: Description
            param2: Description

        Returns:
            Description of return value

        Raises:
            ValueError: When validation fails
        """
        logger.info("Starting operation", param1=param1)

        # Business logic here
        result = self._process(param1, param2)

        logger.info("Operation completed", result=result)
        return result

    def _process(self, param1, param2):
        """Private helper method."""
        # Implementation
        pass

# Module-level instance for easy import
my_service = MyService()
```

### Usage in Views

```python
# domain/app_name/views.py
from django.http import JsonResponse
from domain.app_name.services import my_service
from core.diagnostics.logging import get_logger

logger = get_logger('domain.app_name.views')

def my_view(request):
    try:
        result = my_service.do_something(
            param1=request.GET.get('param1'),
            param2=request.GET.get('param2')
        )
        return JsonResponse({"status": "success", "result": result})
    except ValueError as e:
        logger.error("Operation failed", error=str(e), user_id=request.user.id)
        # Generic error to user, detailed in logs
        return JsonResponse(
            {"error": "Operation failed. Please check your input."},
            status=400
        )
```

## File Validation Integration

### Using Magika Content Validation

Based on `intelligence/extraction/validators.py` and `core/validation`:

```python
# In a service or view
from django.core.files.uploadedfile import UploadedFile
from core.validation import validate_file
from core.validation.exceptions import FileValidationError
from core.diagnostics.logging import get_logger

logger = get_logger('myapp.file_upload')

def handle_file_upload(uploaded_file: UploadedFile, user):
    """
    Process uploaded file with Magika validation.

    Args:
        uploaded_file: Django UploadedFile instance
        user: User uploading the file

    Returns:
        Success status

    Raises:
        ValueError: If file validation fails (generic message for user)
    """
    try:
        # Magika detects actual content type (~5ms, 99% accurate)
        validate_file(
            uploaded_file,
            allowed_types=['pdf', 'docx', 'txt', 'jpg', 'png'],
            max_size_mb=10
        )
        logger.info(
            "File validation passed",
            filename=uploaded_file.name,
            size=uploaded_file.size,
            user_id=user.id
        )
    except FileValidationError as e:
        # Log detailed error
        logger.error(
            "File validation failed",
            filename=uploaded_file.name,
            error=str(e),
            detected_type=getattr(e, 'detected_type', 'unknown'),
            user_id=user.id
        )
        # Generic error to user (SOC2 requirement: don't expose internals)
        raise ValueError("File validation failed. Please check file type and size.")

    # Validation passed, proceed with processing
    return True
```

### Wrapper for Backward Compatibility

Pattern used in `intelligence/extraction/validators.py`:

```python
# domain/app_name/validators.py
from core.validation import validate_file
from core.validation.exceptions import FileValidationError

def validate_uploaded_file(uploaded_file, max_size_mb=None):
    """
    Validates uploaded files using Magika AI content detection.

    Wrapper around core.validation for backward compatibility.

    Args:
        uploaded_file: Django UploadedFile instance
        max_size_mb: Maximum file size in MB (defaults to settings)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    allowed_types = ['pdf', 'doc', 'docx', 'txt']

    try:
        validate_file(
            uploaded_file,
            allowed_types=allowed_types,
            max_size_mb=max_size_mb
        )
        return True, None
    except FileValidationError as e:
        return False, str(e)
```

## API Endpoint Patterns

### DRF ViewSet with Proper Error Handling

Based on `api/extraction/views.py`:

```python
# api/domain/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from core.diagnostics.logging import get_logger
from domain.app.services import my_service

logger = get_logger('api.domain.resource')

class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Resource management.

    Authentication: Token-based
    Rate Limiting: Configured in settings
    Pagination: Limit/Offset, 50 per page
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """
        Custom action to process a resource.

        POST /api/resources/{id}/process/
        """
        logger.info("Processing resource", resource_id=pk, user_id=request.user.id)

        try:
            result = my_service.process_resource(resource_id=pk, user=request.user)

            logger.audit(
                'resource_processed',
                user_id=request.user.id,
                resource_id=pk
            )

            return Response({"status": "success", "result": result})

        except ValueError as e:
            logger.error(
                "Resource processing failed",
                user_id=request.user.id,
                resource_id=pk,
                error=str(e)
            )
            # Generic error message (don't expose internal details)
            return Response(
                {"error": "Processing failed. Please try again or contact support."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(
                "Unexpected error processing resource",
                user_id=request.user.id,
                resource_id=pk
            )
            # Very generic error for unexpected issues
            return Response(
                {"error": "An unexpected error occurred. Please contact support."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

## Management Command Structure

### Command with Logging and Testing

```python
# domain/app_name/management/commands/test_feature.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.diagnostics.logging import get_logger
from domain.app_name.services import my_service

User = get_user_model()
logger = get_logger('management.test_feature')

class Command(BaseCommand):
    help = 'Test the feature functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show verbose output'
        )

    def handle(self, *args, **options):
        """Run feature tests."""
        verbose = options.get('verbose', False)

        self.stdout.write(self.style.WARNING('Testing Feature'))
        self.stdout.write('')

        # Test 1
        self.stdout.write('Test 1: Basic functionality...')
        try:
            result = my_service.do_something('param1', 'param2')
            if verbose:
                self.stdout.write(f'  Result: {result}')
            self.stdout.write(self.style.SUCCESS('✓ PASS'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ FAIL: {e}'))

        # Test 2
        self.stdout.write('Test 2: Error handling...')
        try:
            my_service.do_something(None, None)  # Should fail
            self.stdout.write(self.style.ERROR('✗ FAIL: Should have raised error'))
        except ValueError:
            self.stdout.write(self.style.SUCCESS('✓ PASS: Error properly raised'))

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Tests completed'))
```

## Testing Patterns

### Service Layer Tests

```python
# domain/app_name/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from domain.app_name.services import my_service

User = get_user_model()

class MyServiceTestCase(TestCase):
    def setUp(self):
        """Create test data before each test."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_do_something_success(self):
        """Test successful operation."""
        result = my_service.do_something('param1', 'param2')

        self.assertIsNotNone(result)
        # Add more specific assertions

    def test_do_something_with_invalid_input(self):
        """Test that invalid input raises ValueError."""
        with self.assertRaises(ValueError):
            my_service.do_something(None, None)

    def tearDown(self):
        """Clean up after tests."""
        User.objects.all().delete()
```

### Integration Tests with File Upload

```python
# domain/app_name/tests.py
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from domain.app_name.services import my_service

class FileUploadTestCase(TestCase):
    def test_valid_file_upload(self):
        """Test uploading a valid PDF file."""
        # Create a simple PDF file for testing
        pdf_content = b'%PDF-1.4\n...'  # Minimal valid PDF
        uploaded_file = SimpleUploadedFile(
            "test.pdf",
            pdf_content,
            content_type="application/pdf"
        )

        result = my_service.handle_upload(uploaded_file)

        self.assertTrue(result)

    def test_invalid_file_type(self):
        """Test that invalid file types are rejected."""
        exe_content = b'MZ\x90\x00...'  # Executable header
        uploaded_file = SimpleUploadedFile(
            "malware.pdf",  # Renamed to .pdf but actually exe
            exe_content,
            content_type="application/pdf"
        )

        with self.assertRaises(ValueError) as context:
            my_service.handle_upload(uploaded_file)

        self.assertIn('validation failed', str(context.exception).lower())
```

## Error Handling Patterns

### SOC2 Basic Requirement: Generic Errors to Users

**ALWAYS**:
- Show generic, user-friendly error messages to users
- Log detailed error information internally
- Never expose stack traces, file paths, or internal details to users

```python
# ✓ GOOD: Generic message to user, detailed in logs
try:
    result = process_data(user_input)
except ValueError as e:
    logger.error("Data processing failed", error=str(e), user_input=user_input, user_id=user.id)
    return JsonResponse(
        {"error": "Invalid input. Please check your data and try again."},
        status=400
    )
except DatabaseError as e:
    logger.exception("Database error during processing", user_id=user.id)
    return JsonResponse(
        {"error": "A system error occurred. Please contact support."},
        status=500
    )

# ✗ BAD: Exposes internal details to user
try:
    result = process_data(user_input)
except ValueError as e:
    return JsonResponse(
        {"error": f"ValueError in process_data: {str(e)}", "traceback": traceback.format_exc()},
        status=400
    )
```

### Logging with Context

```python
# ✓ GOOD: Rich context in logs, generic to user
logger.error(
    "File upload failed",
    filename=uploaded_file.name,
    file_size=uploaded_file.size,
    detected_type='exe',
    expected_types=['pdf', 'docx'],
    user_id=user.id,
    ip_address=request.META.get('REMOTE_ADDR')
)
return {"error": "File upload failed. Please check file type."}

# ✗ BAD: No context, not helpful for debugging
logger.error("Upload failed")
return {"error": "Error"}
```
