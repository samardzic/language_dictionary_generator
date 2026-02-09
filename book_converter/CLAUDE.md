# Development Guide - General Guidelines & Best Practices

This document contains general development guidelines, architectural patterns, and best practices for software development. For project-specific implementations, see [Project Design Document](docs/project_design.md).

## Table of Contents

1. [Architecture Guidelines](#architecture-guidelines)
2. [Clean Code Principles](#clean-code-principles)
3. [SOLID Principles](#solid-principles)
4. [Design Patterns](#design-patterns)
5. [Database Best Practices](#database-best-practices)
6. [UI/UX Guidelines](#uiux-guidelines)
7. [Testing Strategy](#testing-strategy)
8. [Security Guidelines](#security-guidelines)
9. [Performance Optimization](#performance-optimization)
10. [Documentation Standards](#documentation-standards)

---

## Architecture Guidelines

### Model-View-Controller (MVC) Pattern

**Purpose:** Separate concerns between data, UI, and business logic.

**Structure:**
```
Application/
├── models/          # Data models and business entities
├── views/           # UI components and presentation logic
├── controllers/     # Application logic and flow control
├── services/        # Business logic and external integrations
└── utils/           # Helper functions and utilities
```

**Benefits:**
- Clear separation of concerns
- Easier testing and maintenance
- Reusable components
- Independent development of UI and logic

### Service Layer Pattern

**Purpose:** Encapsulate business logic in reusable services.

**Guidelines:**
- One service per domain concept
- Services should be stateless when possible
- Use dependency injection
- Implement as singletons for shared state

**Example:**
```python
class UserService:
    """Handle all user-related operations."""

    def __init__(self, database_service):
        self.db = database_service

    def create_user(self, username: str, email: str) -> User:
        """Create a new user."""
        pass

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID."""
        pass
```

### Repository Pattern

**Purpose:** Abstract data access logic from business logic.

**Benefits:**
- Database-agnostic business logic
- Easier to test (mock repositories)
- Centralized data access logic
- Easier database migration

---

## Clean Code Principles

### 1. Naming Conventions

**Classes:** PascalCase
```python
class DownloadManager:
    pass
```

**Functions/Methods:** snake_case
```python
def download_video(url: str) -> bool:
    pass
```

**Constants:** UPPER_SNAKE_CASE
```python
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
```

**Private Members:** Prefix with underscore
```python
def _validate_input(self, data):
    pass
```

### 2. Function Guidelines

**Single Responsibility:**
```python
# Good: One clear purpose
def calculate_total_price(items: List[Item]) -> float:
    return sum(item.price for item in items)

# Bad: Multiple responsibilities
def process_order(order):
    # Validates, calculates, saves, and sends email
    pass
```

**Maximum Length:** 20-40 lines per function

**Clear Names:**
```python
# Good
def send_confirmation_email(user: User, order: Order):
    pass

# Bad
def send_email(u, o):
    pass
```

**Type Hints:**
```python
def download_file(url: str, destination: Path) -> bool:
    """
    Download file from URL to destination.

    Args:
        url: The file URL
        destination: Local file path

    Returns:
        True if successful, False otherwise
    """
    pass
```

### 3. Error Handling

**Use Specific Exceptions:**
```python
# Good
class InvalidUrlError(ValueError):
    pass

def download(url: str):
    if not is_valid_url(url):
        raise InvalidUrlError(f"Invalid URL: {url}")

# Bad
def download(url: str):
    if not is_valid_url(url):
        raise Exception("Bad URL")
```

**Proper Error Context:**
```python
try:
    result = download_file(url)
except NetworkError as e:
    logger.error(f"Network error downloading {url}: {e}")
    raise DownloadError(f"Failed to download: {url}") from e
```

### 4. Code Organization

**One Class Per File:** (unless tightly coupled)

**Import Organization:**
```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import requests
from sqlalchemy import create_engine

# Local imports
from .models import User
from .services import DatabaseService
```

**Module Docstrings:**
```python
"""
User authentication module.

Handles user login, logout, and session management.
Integrates with OAuth2 providers.
"""
```

---

## SOLID Principles

### Single Responsibility Principle (SRP)

**Definition:** A class should have one, and only one, reason to change.

```python
# Good: Single responsibility
class UserValidator:
    def validate_email(self, email: str) -> bool:
        pass

    def validate_password(self, password: str) -> bool:
        pass

class UserRepository:
    def save(self, user: User) -> None:
        pass

    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

# Bad: Multiple responsibilities
class UserManager:
    def validate_email(self, email: str) -> bool:
        pass

    def save_to_database(self, user: User) -> None:
        pass

    def send_welcome_email(self, user: User) -> None:
        pass
```

### Open/Closed Principle (OCP)

**Definition:** Open for extension, closed for modification.

```python
# Good: Use abstract base classes
from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class EmailNotification(NotificationStrategy):
    def send(self, message: str) -> None:
        # Send email
        pass

class SMSNotification(NotificationStrategy):
    def send(self, message: str) -> None:
        # Send SMS
        pass

# Adding new notification type doesn't modify existing code
class PushNotification(NotificationStrategy):
    def send(self, message: str) -> None:
        # Send push notification
        pass
```

### Liskov Substitution Principle (LSP)

**Definition:** Subtypes must be substitutable for their base types.

```python
# Good: Proper inheritance
class Rectangle:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def area(self) -> int:
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side: int):
        super().__init__(side, side)

    def area(self) -> int:
        return self.width * self.width
```

### Interface Segregation Principle (ISP)

**Definition:** Many specific interfaces over one general interface.

```python
# Good: Segregated interfaces
class Readable(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

class Writable(ABC):
    @abstractmethod
    def write(self, data: str) -> None:
        pass

class File(Readable, Writable):
    def read(self) -> str:
        pass

    def write(self, data: str) -> None:
        pass

# Bad: Fat interface
class DataHandler(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, data: str) -> None:
        pass

    @abstractmethod
    def delete(self) -> None:
        pass

    # Forces read-only implementations to define write()
```

### Dependency Inversion Principle (DIP)

**Definition:** Depend on abstractions, not concretions.

```python
# Good: Depend on abstraction
class EmailService(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None:
        pass

class UserController:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def register_user(self, user: User):
        # Use abstraction
        self.email_service.send(user.email, "Welcome", "...")

# Bad: Depend on concrete implementation
class UserController:
    def __init__(self):
        self.email_service = GmailService()  # Tight coupling
```

---

## Design Patterns

### Singleton Pattern

**Use Case:** Ensure only one instance exists (e.g., database connection, configuration).

```python
class DatabaseService:
    _instance: Optional['DatabaseService'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._setup_connection()
```

### Factory Pattern

**Use Case:** Create objects without specifying exact class.

```python
class NotificationFactory:
    @staticmethod
    def create(notification_type: str) -> Notification:
        if notification_type == 'email':
            return EmailNotification()
        elif notification_type == 'sms':
            return SMSNotification()
        else:
            raise ValueError(f"Unknown type: {notification_type}")
```

### Observer Pattern

**Use Case:** Notify multiple objects of state changes.

```python
class Observable:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, event: Event):
        for observer in self._observers:
            observer.update(event)

class Observer(ABC):
    @abstractmethod
    def update(self, event: Event):
        pass
```

### Strategy Pattern

**Use Case:** Select algorithm at runtime.

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List) -> List:
        pass

class QuickSort(SortStrategy):
    def sort(self, data: List) -> List:
        # Quick sort implementation
        pass

class MergeSort(SortStrategy):
    def sort(self, data: List) -> List:
        # Merge sort implementation
        pass

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort_data(self, data: List) -> List:
        return self.strategy.sort(data)
```

---

## Database Best Practices

### Connection Management

**Use Context Managers:**
```python
@contextmanager
def get_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()
```

### Parameterized Queries

**Always Use Parameters:**
```python
# Good: Safe from SQL injection
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

# Bad: Vulnerable to SQL injection
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### Indexing Strategy

**Create Indexes on:**
- Foreign keys
- Frequently queried columns
- Columns used in WHERE, JOIN, ORDER BY

```sql
-- Index on frequently queried column
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Composite index for common query patterns
CREATE INDEX IF NOT EXISTS idx_orders_user_date
    ON orders(user_id, created_at DESC);
```

### Database Migrations

**Version Control Schema Changes:**
```python
class MigrationManager:
    def apply_migration(self, migration_file: Path) -> None:
        version = migration_file.stem

        with self.db._get_connection() as conn:
            # Execute migration
            with open(migration_file, 'r') as f:
                conn.executescript(f.read())

            # Record migration
            conn.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (version,)
            )
```

---

## UI/UX Guidelines

### Responsive Design

**Principles:**
- Adapt to window size changes
- Minimum supported resolution: 1024x768
- Use relative sizing (percentages, fill/expand)
- Test on different screen sizes

### Accessibility

**Requirements:**
- Keyboard navigation support
- Screen reader compatible
- Sufficient color contrast (WCAG 2.1 AA)
- Focus indicators
- Alt text for images

### User Feedback

**Loading States:**
```python
# Show progress for long operations
def download_large_file(url):
    self.show_progress_bar()
    try:
        result = perform_download(url)
        self.show_success_message("Download complete")
    except Error as e:
        self.show_error_message(f"Download failed: {e}")
    finally:
        self.hide_progress_bar()
```

**Error Messages:**
- User-friendly language
- Actionable suggestions
- Technical details in logs only

---

## Testing Strategy

### Unit Tests

**Test Structure:**
```python
class TestUserService:
    @pytest.fixture
    def user_service(self, mock_db):
        return UserService(mock_db)

    def test_create_user_success(self, user_service):
        user = user_service.create_user("john", "john@example.com")
        assert user.username == "john"
        assert user.email == "john@example.com"

    def test_create_user_duplicate_email(self, user_service):
        user_service.create_user("john", "john@example.com")

        with pytest.raises(DuplicateEmailError):
            user_service.create_user("jane", "john@example.com")
```

### Integration Tests

**Test Complete Workflows:**
```python
def test_user_registration_workflow(app):
    # Register user
    response = app.post('/register', data={
        'username': 'john',
        'email': 'john@example.com',
        'password': 'secure123'
    })
    assert response.status_code == 201

    # Verify user in database
    user = User.query.filter_by(email='john@example.com').first()
    assert user is not None

    # Verify welcome email sent
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Welcome'
```

### Test Coverage

**Targets:**
- Minimum 80% code coverage
- 100% coverage for critical paths
- Test edge cases and error conditions

---

## Security Guidelines

### Input Validation

**Validate All Inputs:**
```python
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_filename(filename: str) -> str:
    # Remove path traversal attempts
    filename = os.path.basename(filename)
    # Remove special characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename
```

### Secure File Operations

**Prevent Path Traversal:**
```python
def save_file(filename: str, content: bytes, base_dir: Path):
    # Sanitize filename
    safe_filename = sanitize_filename(filename)

    # Construct path
    file_path = (base_dir / safe_filename).resolve()

    # Ensure path is within base_dir
    if not file_path.is_relative_to(base_dir):
        raise SecurityError("Path traversal detected")

    # Save file
    file_path.write_bytes(content)
```

### Secure Authentication

**Password Handling:**
```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

---

## Performance Optimization

### Database Optimization

**Use Indexes:**
```sql
-- Before: Slow query
SELECT * FROM users WHERE email = 'john@example.com';

-- Add index
CREATE INDEX idx_users_email ON users(email);

-- After: Fast query
```

**Pagination:**
```python
def get_users(page: int = 1, page_size: int = 100):
    offset = (page - 1) * page_size
    return db.query(User).limit(page_size).offset(offset).all()
```

### Memory Management

**Use Generators for Large Datasets:**
```python
# Good: Memory efficient
def read_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield process_line(line)

# Bad: Loads entire file into memory
def read_large_file(file_path):
    with open(file_path) as f:
        return [process_line(line) for line in f]
```

### Async Operations

**Use Threading for I/O:**
```python
from concurrent.futures import ThreadPoolExecutor

def download_files(urls: List[str]):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download, url) for url in urls]
        results = [future.result() for future in futures]
    return results
```

---

## Documentation Standards

### Module Docstrings

```python
"""
User authentication module.

This module provides user authentication functionality including
login, logout, session management, and password reset.

Example:
    >>> auth = AuthService()
    >>> user = auth.login('username', 'password')
    >>> auth.logout(user)

See Also:
    - UserService: User management
    - SessionManager: Session handling
"""
```

### Function Docstrings

**Google Style:**
```python
def download_file(url: str, destination: Path, timeout: int = 30) -> bool:
    """
    Download file from URL to local destination.

    Args:
        url: The source URL
        destination: Local file path
        timeout: Request timeout in seconds (default: 30)

    Returns:
        True if download successful, False otherwise

    Raises:
        NetworkError: If network connection fails
        TimeoutError: If request times out
        ValueError: If URL is invalid

    Example:
        >>> download_file('https://example.com/file.pdf', Path('file.pdf'))
        True
    """
    pass
```

### README Structure

**Essential Sections:**
1. Project Title & Description
2. Features
3. Installation Instructions
4. Quick Start Guide
5. Configuration Options
6. Examples
7. API Reference (link)
8. Contributing Guidelines
9. License
10. Contact/Support

---

## Logging Guidelines

### Log Levels

**Usage:**
- **DEBUG:** Detailed diagnostic information
- **INFO:** General informational messages
- **WARNING:** Warning messages for potential issues
- **ERROR:** Error messages for failures
- **CRITICAL:** Critical errors causing system failure

**Example:**
```python
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Processing data: {data}")

    try:
        result = perform_operation(data)
        logger.info(f"Operation completed: {result}")
        return result
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
```

### Logging Configuration

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## Version Control Best Practices

### Commit Messages

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

**Examples:**
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow for Google and GitHub.
Includes token refresh and revocation.

Closes #123
```

### Branch Strategy

**Git Flow:**
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `release/*` - Release preparation
- `hotfix/*` - Emergency fixes

---

## Code Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] No obvious bugs

### Code Quality
- [ ] Follows naming conventions
- [ ] Functions have single responsibility
- [ ] No code duplication
- [ ] Comments explain "why" not "what"

### Testing
- [ ] Unit tests included
- [ ] Tests pass
- [ ] Adequate code coverage

### Security
- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] No hardcoded secrets
- [ ] Secure file operations

### Performance
- [ ] No obvious performance issues
- [ ] Efficient database queries
- [ ] Appropriate data structures used

### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic explained
- [ ] API documentation updated
- [ ] README updated if needed

---

## Resources

### Books
- Clean Code (Robert C. Martin)
- Design Patterns (Gang of Four)
- The Pragmatic Programmer (Hunt & Thomas)
- Refactoring (Martin Fowler)

### Online Resources
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Clean Code Principles](https://www.cleancode.com/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Design Patterns](https://refactoring.guru/design-patterns)

### Tools
- **Linting:** flake8, pylint, black
- **Type Checking:** mypy
- **Testing:** pytest, unittest
- **Coverage:** pytest-cov, coverage.py
- **Documentation:** Sphinx, MkDocs

---

*This document contains general development guidelines applicable to most software projects. For project-specific details, implementations, and configurations, refer to the Project Design Document.*

*Last Updated: 2026-01-23*
