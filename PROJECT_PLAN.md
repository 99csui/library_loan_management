# Project Plan — Library Loan Management System

## 1. Project Overview

### Project Name

Library Loan Management System

### Description

Library Loan Management System is a command-line application developed in Python for managing books, library members, and book loans.

The application is designed for a community library that currently manages loans manually and needs a reliable way to prevent duplicate loans, track active loans, register returns, and identify which members are responsible for borrowed books.

The project introduces a Service Layer to coordinate use cases involving multiple entities and repositories.

---

## 2. Problem Statement

The library currently records loans manually, which creates several problems:

* The same book may be loaned to more than one member at the same time.
* It is difficult to identify who currently has a book.
* Returns may not be registered correctly.
* The library cannot easily identify active loans.
* Members may exceed the permitted number of active loans.
* There is no consistent loan history.

The system must centralize this information and enforce the library's business rules.

---

## 3. Learning Objectives

This project is designed to practice and reinforce:

* Object-Oriented Programming.
* Domain modeling.
* Domain validation.
* Repository Pattern.
* Service Layer.
* Application use cases.
* Manual dependency injection.
* Separation of concerns.
* Business rules involving multiple entities.
* Python dataclasses.
* Python enumerations.
* Type hints.
* Exception handling.
* Unit testing with `unittest`.
* Professional Git workflow.
* Pull Requests and code review.
* Technical documentation.

---

## 4. Business Requirements

The application must allow a librarian to:

* Register books.
* Register members.
* Remove books when they have no active loans.
* Remove members when they have no active loans.
* Search for books by ID.
* Search for members by ID.
* List all books.
* List available books.
* Create book loans.
* Register book returns.
* List active loans.
* Search loan history by member.
* Prevent invalid operations.

---

## 5. Functional Requirements

### Books

Each book must contain:

* A unique ID.
* A title.
* An author.

Rules:

* The ID must be an integer greater than zero.
* The title must be a non-empty string.
* The author must be a non-empty string.
* Two books cannot share the same ID.
* A book with an active loan cannot be removed.
* Book availability is derived from active loans and is not stored as a separate attribute.

### Members

Each member must contain:

* A unique ID.
* A name.

Rules:

* The ID must be an integer greater than zero.
* The name must be a non-empty string.
* Two members cannot share the same ID.
* A member with active loans cannot be removed.
* A member may have a maximum of three active loans.

### Loans

Each loan must contain:

* A unique ID.
* A book ID.
* A member ID.
* A borrowing date.
* An optional return date.
* A loan status.

Valid statuses:

* `ACTIVE`
* `RETURNED`

Rules:

* Loan, book, and member IDs must be integers greater than zero.
* A new loan must begin with status `ACTIVE`.
* A new loan must begin with no return date.
* A book may have only one active loan.
* A loan cannot be created for an unregistered book.
* A loan cannot be created for an unregistered member.
* A returned loan cannot be returned again.
* The return date cannot be earlier than the borrowing date.
* Returning a loan changes its status to `RETURNED`.

---

## 6. Domain Model

### Book

Responsibilities:

* Represent a registered library book.
* Validate its own attributes.
* Provide a readable text representation.

Attributes:

```text
id: int
title: str
author: str
```

### Member

Responsibilities:

* Represent a registered library member.
* Validate its own attributes.
* Provide a readable text representation.

Attributes:

```text
id: int
name: str
```

### Loan

Responsibilities:

* Represent the relationship between a book and a member during a loan.
* Protect its own lifecycle and invariants.
* Determine whether it is active.
* Register a valid return.

Attributes:

```text
id: int
book_id: int
member_id: int
borrowed_at: date
returned_at: date | None
status: LoanStatus
```

Methods:

```text
return_loan(returned_at)
is_active()
```

---

## 7. Architecture

```text
ConsoleMenu
      │
      ▼
LibraryService / LoanService
      │
      ├── BookRepository
      ├── MemberRepository
      └── LoanRepository
              │
              ▼
       Book / Member / Loan
```

### Presentation Layer

The presentation layer is responsible for:

* Displaying menus.
* Reading user input.
* Showing operation results.
* Calling application services.

It must not contain business rules.

### Service Layer

The Service Layer represents application use cases.

#### LibraryService

Responsibilities:

* Register books.
* Register members.
* Remove books.
* Remove members.
* Coordinate removal rules involving active loans.

#### LoanService

Responsibilities:

* Create loans.
* Register returns.
* List available books.
* List active loans.
* Find loans by member.
* Coordinate books, members, and loans.

### Repository Layer

Repositories manage in-memory collections.

They are responsible for:

* Adding entities.
* Finding entities.
* Removing entities.
* Listing entities.
* Preventing duplicated IDs.

Repositories must not:

* Print messages.
* Read user input.
* Coordinate complete business use cases.
* Contain presentation logic.

### Domain Layer

Domain entities are responsible for:

* Validating their own data.
* Protecting their invariants.
* Managing their own state transitions.

---

## 8. Repository Contracts

### BookRepository

```text
add(book)
find_by_id(book_id)
remove(book_id)
list_all()
```

### MemberRepository

```text
add(member)
find_by_id(member_id)
remove(member_id)
list_all()
```

### LoanRepository

```text
add(loan)
find_by_id(loan_id)
list_all()
list_active()
find_active_by_book_id(book_id)
find_active_by_member_id(member_id)
list_by_member_id(member_id)
```

Repository results:

* `True` for a successful modification.
* `False` for a failed storage operation.
* An entity when a search succeeds.
* `None` when an entity is not found.
* A list for collection queries.

---

## 9. Service Contracts

### LibraryService

```text
register_book(book_id, title, author)
register_member(member_id, name)
remove_book(book_id)
remove_member(member_id)
```

### LoanService

```text
borrow_book(loan_id, book_id, member_id)
return_book(loan_id)
list_available_books()
list_active_loans()
find_loans_by_member(member_id)
```

Service methods may raise `ValueError` when an expected business rule prevents an operation.

Examples:

```text
book ID already exists
member ID already exists
book does not exist
member does not exist
book already has an active loan
member has reached the active loan limit
cannot remove a book with an active loan
cannot remove a member with active loans
loan does not exist
loan has already been returned
```

---

## 10. Dependency Injection

Repositories must be created outside the services and passed through their constructors.

```text
main.py
   │
   ├── creates BookRepository
   ├── creates MemberRepository
   ├── creates LoanRepository
   │
   ├── injects repositories into LibraryService
   ├── injects repositories into LoanService
   │
   └── injects services into ConsoleMenu
```

Services must not instantiate their own repositories.

This keeps dependencies explicit and allows services to be tested independently.

---

## 11. Project Structure

```text
library_loan_management/
│
├── cli/
│   ├── __init__.py
│   └── menu.py
│
├── models/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   ├── loan.py
│   └── enums.py
│
├── repositories/
│   ├── __init__.py
│   ├── book_repository.py
│   ├── member_repository.py
│   └── loan_repository.py
│
├── services/
│   ├── __init__.py
│   ├── library_service.py
│   └── loan_service.py
│
├── tests/
│   ├── __init__.py
│   ├── test_book.py
│   ├── test_member.py
│   ├── test_loan.py
│   ├── test_book_repository.py
│   ├── test_member_repository.py
│   ├── test_loan_repository.py
│   ├── test_library_service.py
│   └── test_loan_service.py
│
├── main.py
├── PROJECT_PLAN.md
├── README.md
└── .gitignore
```

---

## 12. Coding Standards

The project must follow:

* PEP 8.
* Type hints in all new functions and methods.
* Clear and descriptive names.
* Small methods with one responsibility.
* Fail Fast.
* DRY where it improves clarity.
* Domain validation inside entities.
* Business use-case coordination inside services.
* Storage operations inside repositories.
* Presentation logic inside the CLI.

Type and value validation convention:

* Incorrect type → `TypeError`.
* Correct type with invalid value → `ValueError`.

---

## 13. Testing Strategy

The project uses Python's `unittest` framework.

### Domain Tests

Must cover:

* Valid entity creation.
* Invalid IDs.
* Invalid text fields.
* Initial loan state.
* Valid loan return.
* Duplicate return attempt.
* Invalid return dates.
* Active loan behavior.

### Repository Tests

Must cover:

* Empty initial repositories.
* Adding valid entities.
* Rejecting invalid objects.
* Rejecting duplicated IDs.
* Successful searches.
* Missing searches.
* Successful removals.
* Failed removals.
* Loan-specific collection queries.

### Service Tests

Must cover:

* Successful use cases.
* Missing books and members.
* Duplicated IDs.
* Active loan restrictions.
* Member loan limits.
* Invalid removals.
* Successful returns.
* Duplicate returns.
* Coordination between repositories.

Tests should validate behavior rather than internal implementation details.

The CLI will initially be verified through manual acceptance testing.

---

## 14. Git Workflow

The stable branch is:

```text
main
```

Development occurs in focused feature branches.

Planned branches:

```text
feature/domain-models
feature/repositories
feature/library-service
feature/loan-service
feature/console-interface
docs/project-documentation
```

Each branch must:

* Start from an updated `main`.
* Represent one coherent unit of work.
* Include relevant tests.
* Be reviewed through a Pull Request.
* Be deleted after merging.

Commit examples:

```text
chore: initialize project structure
feat: implement loan domain model
test: add loan domain tests
feat: implement loan repository
feat: add book registration service
refactor: simplify loan service validation
docs: complete project documentation
```

---

## 15. Development Roadmap

### Sprint 0 — Planning and Architecture

* Define the problem.
* Identify entities.
* Define business rules.
* Design repositories.
* Design services.
* Define error contracts.
* Create the project plan.
* Initialize Git and project structure.

### Sprint 1 — Domain Models

* Implement `LoanStatus`.
* Implement `Book`.
* Implement `Member`.
* Implement `Loan`.
* Add domain validation.
* Add domain unit tests.
* Open and merge the domain-model Pull Request.

### Sprint 2 — Repositories

* Implement `BookRepository`.
* Implement `MemberRepository`.
* Implement `LoanRepository`.
* Add repository tests.
* Open and merge the repository Pull Request.

### Sprint 3 — Library Service

* Implement book registration.
* Implement member registration.
* Implement protected book removal.
* Implement protected member removal.
* Add service tests.
* Open and merge the Pull Request.

### Sprint 4 — Loan Service

* Implement book loans.
* Enforce availability rules.
* Enforce member loan limits.
* Implement returns.
* Implement loan queries.
* Add service tests.
* Open and merge the Pull Request.

### Sprint 5 — Console Interface

* Implement the CLI.
* Validate user input.
* Display domain and service results.
* Perform manual acceptance testing.
* Open and merge the Pull Request.

### Sprint 6 — Project Closure

* Complete final code review.
* Address technical findings.
* Complete README.
* Update Project Plan.
* Run all tests.
* Open the final documentation Pull Request.
* Merge the stable release.

---

## 16. Out of Scope

The first version will not include:

* SQL or database persistence.
* REST APIs.
* Authentication.
* User roles.
* Fines.
* Book reservations.
* Notifications.
* Graphical interfaces.
* External dependencies.
* Automated CLI tests.
* Custom business exception classes.
* Operation result objects.

These may be considered in future projects or versions.

---

## 17. Known Technical Decisions

### Book Availability

Book availability is derived from active loans.

The `Book` entity will not contain an `available` attribute.

### Loan Relationships

`Loan` stores `book_id` and `member_id` instead of complete entity references.

### Time Management

The user does not enter loan or return dates.

The Service Layer obtains the current date and passes it to the `Loan` entity.

### Error Communication

* Entities use `TypeError` and `ValueError` to protect invariants.
* Repositories return simple storage results.
* Services use `ValueError` with clear messages for rejected business operations.

### Dependency Management

Services receive repositories through manual dependency injection.

---

## 18. Technical Debt and Future Improvements

Potential improvements include:

* Replace generic `ValueError` service errors with custom business exceptions.
* Introduce an `OperationResult` model.
* Abstract access to the system clock.
* Add automated CLI tests using mocks.
* Add SQLite or PostgreSQL persistence.
* Create repository interfaces using `Protocol` or abstract base classes.
* Add logging.
* Add configuration management.
* Expose the use cases through a REST API.
* Add filtering and reporting functionality.

---

## 19. Definition of Done

The project is complete when:

* All planned entities are implemented.
* All repositories are implemented.
* All planned services are implemented.
* All business rules are enforced.
* All domain, repository, and service tests pass.
* The console interface passes manual acceptance testing.
* Type hints are complete.
* PEP 8 is followed.
* Code review findings are addressed.
* Documentation reflects the final implementation.
* All feature branches have been reviewed and merged.
* `main` represents a stable version.
* The Software Engineering Playbook has been updated with new lessons.
