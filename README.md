# Library Loan Management System

A console-based library loan management application built with Python.

The project was developed to practice backend software design principles such as layered architecture, dependency injection, separation of concerns, repository abstractions, service-layer business rules, and automated testing.

## Features

The application allows users to:

* Register books.
* Register library members.
* Remove books that do not have active loans.
* Remove members that do not have active loans.
* Borrow books.
* Return borrowed books.
* List all registered books.
* List currently available books.
* List active loans.
* View the loan history of a member.

## Architecture

The application follows a layered architecture:

```text
CLI
 ↓
Services
 ↓
Repositories
 ↓
Models
```

### Models

Contain the domain entities and their invariants:

* `Book`
* `Member`
* `Loan`
* `LoanStatus`

### Repositories

Manage the storage and retrieval of domain objects.

The V1 implementation uses in-memory repositories:

* `BookRepository`
* `MemberRepository`
* `LoanRepository`

### Services

Coordinate application use cases and business rules:

* `LibraryService`
* `LoanService`

Examples of rules enforced by the service layer include:

* A book cannot be borrowed if it already has an active loan.
* A book with an active loan cannot be removed.
* A member with active loans cannot be removed.
* A member cannot exceed the configured active-loan limit.
* A loan cannot be returned more than once.

### CLI

`ConsoleMenu` is responsible only for user interaction:

* Displaying menu options.
* Reading and converting input.
* Calling application services.
* Displaying results.
* Presenting expected errors.

Business rules are intentionally kept outside the CLI.

### Composition Root

`main.py` acts as the application composition root.

It creates the repositories, injects the same repository instances into the services, creates the console interface, and starts the application.

```text
main.py
  ├── BookRepository
  ├── MemberRepository
  ├── LoanRepository
  │
  ├── LibraryService
  ├── LoanService
  │
  └── ConsoleMenu
```

Sharing repository instances between services ensures that all application components operate on the same in-memory state.

## Project Structure

```text
library_loan_management/
├── cli/
│   └── console_menu.py
├── models/
│   ├── book.py
│   ├── enums.py
│   ├── loan.py
│   └── member.py
├── repositories/
│   ├── book_repository.py
│   ├── loan_repository.py
│   └── member_repository.py
├── services/
│   ├── library_service.py
│   └── loan_service.py
├── tests/
│   ├── cli/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── test_main.py
├── main.py
├── PROJECT_PLAN.md
└── README.md
```

## Testing

The project was developed using a test-driven workflow:

```text
RED → GREEN → REFACTOR
```

The automated test suite covers:

* Domain model validation and invariants.
* Repository behavior.
* Service-layer business rules.
* Console interactions.
* Application startup and dependency composition.

The current V1 test suite contains **197 automated tests**.

Run the complete suite from the project root with:

```bash
python -m unittest discover -s tests -t . -p "test_*.py" -v
```

## How to Run

### Requirements

* Python 3
* No third-party dependencies are required for V1.

Clone the repository and move into the project directory.

Optionally create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Run the application:

```bash
python main.py
```

The console menu will then provide access to the available operations.

## Technical Decisions

### Dependency Injection

Repositories are provided to services through constructor injection instead of being created internally.

This keeps dependencies explicit and makes individual layers easier to test.

### Service Layer

Business workflows that involve multiple domain objects or repositories are coordinated by services rather than by the console interface.

### In-Memory Persistence

V1 intentionally stores data in memory.

This keeps persistence concerns separate from the domain and application logic while the architecture is being established.

Data therefore exists only for the duration of the application process.

## Future Improvements

Possible future versions could introduce:

* Persistent storage with SQLite or PostgreSQL.
* Repository interfaces or abstractions for multiple persistence implementations.
* A REST API.
* FastAPI integration.
* Improved CLI presentation.
* Application logging.
* Configuration management.
* Packaging and dependency management.

These features are intentionally outside the scope of V1.

## Project Status

**V1 — Finalization**

The implementation is functionally complete and has passed the automated test suite and manual end-to-end acceptance testing. Final repository review and release integration are in progress.
