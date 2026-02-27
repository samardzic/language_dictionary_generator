# Aliases

## Aliases

| Alias                  | Path                                                        |
|------------------------|-------------------------------------------------------------|
| db, database           | /db/dictionary.db                                           |
| sources                | /language_sources                                           |
| app requirements       | /docs/app_requirements.md                                   |


## Files
| Alias                  | Path                                                |
|:-----------------------|:----------------------------------------------------|
| `prompts file`         | docs/prompts_used.md                                |
| `action logs`          | docs/action_logs/                                   |


# Project

- Architecture: MVC pattern (models/, views/, controllers/, services/, utils/)
- Python conventions: PascalCase classes, snake_case functions, UPPER_SNAKE_CASE constants
- Use type hints and Google-style docstrings
- Use specific exceptions, not generic `Exception`
- For details see [Project Requirements](docs/app_requirements.md)
- Store documentation in `docs/` (keep `README.md` and `CLAUDE.md` in project root)

# Development Guide - General Guidelines & Best Practices

This document contains general development guidelines, architectural patterns, and best practices for software development. For project-specific implementations, see [Project Design Document](docs/project_design.md).

# Session Rules

- Append each user prompt to `prompts file` (whole prompt, prefixed with timestamp)
- After each code change, if any summary is generated move it to the folder `action logs`

