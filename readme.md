# Calculator Application

## Overview

This project is a professional command-line calculator application built
using Python. It demonstrates clean architecture, object-oriented
programming principles, SOLID principles, design patterns, structured
exception handling, automated testing, and version control best
practices.

The application is designed not only to perform arithmetic operations
but also to showcase real-world software engineering standards.

------------------------------------------------------------------------

# Features

-   Command-Line REPL Interface (Read--Eval--Print Loop)
-   Advanced arithmetic operations:
    -   add
    -   subtract
    -   multiply
    -   divide
    -   power
    -   root
    -   modulus
    -   int_divide
    -   percent
    -   abs_diff
-   Undo / Redo functionality (Memento Pattern)
-   Calculation history tracking
-   CSV-based history persistence using pandas
-   Environment-based configuration using dotenv
-   Structured logging
-   Full unit testing with positive and negative test cases

------------------------------------------------------------------------

# Architecture

The application follows a modular architecture:
```
project_root/
│
├── .github/
│   └── workflows/                 # CI/CD configuration (GitHub Actions)
│
├── app/                           # Main application package
│   ├── __init__.py
│   ├── calculation.py             # Calculation data model
│   ├── calculator.py              # Core calculator logic
│   ├── calculator_config.py       # Environment configuration loader
│   ├── calculator_memento.py      # Memento pattern (undo/redo)
│   ├── calculator_repl.py         # REPL interface (CLI)
│   ├── exceptions.py              # Custom exception classes
│   ├── history.py                 # Observer pattern implementation
│   ├── input_validators.py        # Input validation utilities
│   ├── logger.py                  # Logging configuration
│   └── operations.py              # Factory pattern & operations
│
├── tests/                         # Unit tests (pytest)
│   ├── __init__.py
│   ├── test_calculation_model.py
│   ├── test_calculator_config.py
│   ├── test_calculator_positive.py
│   ├── test_calculator_negative.py
│   ├── test_calculator_repl.py
│   ├── test_config.py
│   ├── test_input_validators.py
│   ├── test_logger_and_observers.py
│   ├── test_memento.py
│   └── test_operations_factory.py
│
├── .env                           # Environment variables
├── .gitignore
├── pytest.ini                     # Pytest configuration
├── main.py                        # Entry point (optional)
├── requirements.txt               # Project dependencies
├── LICENSE
└── README.md
```
Each module has a single responsibility, ensuring maintainability and
scalability.

------------------------------------------------------------------------

# Environment Variables

This project uses **python-dotenv** to load configuration from a `.env`
file.

## Step 1: Create a `.env` file in the project root

Example:

CALCULATOR_BASE_DIR=. CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_FILE=calculator_history.csv
CALCULATOR_MAX_HISTORY_SIZE=100 CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10 CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8

## Variable Explanation

-   CALCULATOR_BASE_DIR → Base directory for logs and history
-   CALCULATOR_LOG_DIR → Folder for log files
-   CALCULATOR_HISTORY_DIR → Folder for CSV history files
-   CALCULATOR_LOG_FILE → Log filename
-   CALCULATOR_HISTORY_FILE → CSV filename
-   CALCULATOR_MAX_HISTORY_SIZE → Maximum number of calculations stored
-   CALCULATOR_AUTO_SAVE → Auto-save history after each operation
    (true/false)
-   CALCULATOR_PRECISION → Decimal rounding precision (0--50
    recommended)
-   CALCULATOR_MAX_INPUT_VALUE → Maximum allowed numeric input
-   CALCULATOR_DEFAULT_ENCODING → File encoding

------------------------------------------------------------------------

# Setup Instructions

## 1. Clone Repository

git clone `<your-repo-url>`{=html} cd `<project-folder>`{=html}

## 2. Create Virtual Environment

### Windows (PowerShell)

python -m venv .venv .venv`\Scripts`{=tex}`\Activate`{=tex}.ps1

### macOS / Linux

python3 -m venv .venv source .venv/bin/activate

## 3. Install Dependencies

pip install -r requirements.txt

------------------------------------------------------------------------

# Running the Application

Start the calculator REPL:

python -m app.calculator_repl

You should see:

Calculator started. Type 'help' for commands.

------------------------------------------------------------------------

# Running Tests

## Run all tests

pytest -q

## Run tests with coverage

pytest -q --cov=app --cov-report=term-missing

## Generate HTML coverage report

pytest --cov=app --cov-report=html

Then open:

htmlcov/index.html

------------------------------------------------------------------------

# Object-Oriented Programming (OOP)

## Encapsulation

Classes bundle related data and methods together while protecting
internal state.

## Abstraction

Abstract base classes define interfaces while hiding implementation
details.

## Inheritance

Concrete operation classes inherit from a common base class.

## Polymorphism

All operations share a common interface, allowing uniform execution.

------------------------------------------------------------------------

# SOLID Principles

## Single Responsibility Principle

Each class handles one responsibility.

## Open/Closed Principle

New operations can be added without modifying existing logic.

## Liskov Substitution Principle

Subclasses can replace their base class without breaking behavior.

## Interface Segregation Principle

Interfaces are small and focused.

## Dependency Inversion Principle

High-level modules depend on abstractions rather than concrete
implementations.

------------------------------------------------------------------------

# Design Patterns

## Factory Pattern

Centralizes object creation of operations.

## Observer Pattern

Handles logging and auto-save behavior on calculation events.

## Memento Pattern

Enables undo and redo functionality by saving object state.

------------------------------------------------------------------------

# Python Concepts Used

-   Abstract Base Classes (abc module)
-   Dataclasses
-   Type hints
-   Decorators
-   Lambda functions
-   Context managers
-   Decimal module for precise arithmetic
-   Environment variable management

------------------------------------------------------------------------

# Exception Handling

Custom exceptions: - ValidationError - OperationError - PersistenceError

Low-level errors are converted into meaningful domain-level errors for
clean output.

------------------------------------------------------------------------

# Testing

The project uses pytest with full positive and negative test coverage.

Run tests: pytest -q

With coverage: pytest --cov=app

Testing ensures reliability, correctness, and regression safety.

------------------------------------------------------------------------

# Git Workflow

Professional Git practices followed: 
- Feature branching 
- Meaningful commit messages 
- Pull requests for merging 
- .gitignore usage 
- Version control tracking

------------------------------------------------------------------------

# Software Engineering Concepts

-   Modular architecture
-   Loose coupling
-   High cohesion
-   Maintainability
-   Scalability
-   Clean code principles

------------------------------------------------------------------------

# How to Run

Install dependencies: pip install -r requirements.txt

Run the application: python -m app.calculator_repl

------------------------------------------------------------------------

# Conclusion

This calculator application demonstrates strong backend development
skills including OOP, SOLID principles, design patterns, testing, Git
workflow, and maintainable architecture.
