# Coding Style Guidelines

This document outlines the coding style guidelines to be followed when contributing to the AI-Based Sorting Robot Arm project. Consistent coding styles enhance code readability and maintainability across the project.

## C++ Coding Style

### Indentation and Spacing

- Use 2 spaces for indentation.
- Limit line length to 80 characters.
- Use spaces around operators, but not immediately inside parentheses.

### Naming Conventions

- Use meaningful and descriptive variable and function names.
- Follow a consistent naming convention (e.g., camelCase or snake_case).

### Pointers

- Prefer smart pointers (`std::shared_ptr`, `std::unique_ptr`) over raw pointers where appropriate.

### Includes

- Organize includes alphabetically and separate them into standard library includes, third-party library includes, and project-specific includes.

### Comments

- Use comments sparingly and ensure they add value to the understanding of the code.
- Follow a consistent commenting style (e.g., `//` for single-line comments, `/* */` for multi-line comments).

## Python Coding Style

### Indentation and Spacing

- Use 4 spaces for indentation.
- Limit all lines to a maximum of 79 characters for code and 72 for docstrings.
- Use spaces around operators.

### Naming Conventions

- Use meaningful and descriptive variable and function names.
- Follow the PEP 8 naming conventions.

### Blank Lines

- Use blank lines to separate functions, classes, and blocks of code inside functions.

### Comments

- Use comments sparingly and ensure they add value to the understanding of the code.
- Follow a consistent commenting style (e.g., `#` for single-line comments).

## General Recommendations

- Consistency is key; maintain a consistent coding style throughout the project.
- Use automated tools (linters and formatters) to catch and fix style issues.
- Perform thorough code reviews to ensure adherence to coding style guidelines.

## Editor Configuration

Consider using an editor configuration file, such as `.clang-format` for C++ and `.editorconfig`, to maintain a consistent coding style across different editors.

By contributing to this project, you agree to adhere to these coding style guidelines.

Thank you for your commitment to maintaining a high standard of code quality in the AI-Based Sorting Robot Arm project.
