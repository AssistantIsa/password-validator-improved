# Project Architecture

## Overview

Password Validator Pro is a Flask web application that follows the MVC pattern.

## Components

### Backend (Python/Flask)

- **app.py**: Main application, routes, and API endpoints
- **validator.py**: Business logic for password validation

### Frontend

- **templates/index.html**: User interface
- **static/**: Static resources (CSS, JS, images)

### Data Flow
```
User → Frontend (HTML/JS) → REST API (Flask) → Validator → JSON Response → Frontend
```

## Class Structure

### PasswordValidator

Main methods:
- `min_length(length)`: Defines minimum length
- `max_length(length)`: Defines maximum length
- `has_uppercase(count)`: Requires uppercase letters
- `has_lowercase(count)`: Requires lowercase letters
- `has_digits(count)`: Requires numbers
- `has_symbols(count)`: Requires symbols
- `no_spaces()`: Prohibits spaces
- `validate(password)`: Performs validation
- `generate_password(length)`: Generates a password

## API Design

RESTful API with JSON endpoints

### Security

- Passwords are not stored
- Server-side validation
- Rate limiting (future)
