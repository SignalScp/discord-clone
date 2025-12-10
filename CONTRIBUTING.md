# Contributing to Discord Clone

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/discord-clone.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

See [docs/SETUP.md](docs/SETUP.md) for complete setup instructions.

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use docstrings for all public functions
- Run `black` for formatting (optional)

Example:
```python
def create_user(username: str, email: str) -> User:
    """Create a new user account.
    
    Args:
        username: Unique username
        email: User email address
        
    Returns:
        Created user object
    """
    # Implementation
```

### GDScript (Frontend)

- Follow Godot style guide
- Use type hints
- Use tabs for indentation
- Document public functions

Example:
```gdscript
func send_message(content: String) -> void:
	"""Send a message to current channel.
	
	Args:
		content: Message text
	"""
	# Implementation
```

## Testing

### Backend Tests

- Write tests for all new features
- Place tests in `backend/tests/`
- Use pytest
- Aim for 80%+ code coverage

```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests

- Manually test all UI changes
- Test on different resolutions
- Verify WebSocket functionality

## Commit Messages

Use clear, descriptive commit messages:

- `Add: New feature description`
- `Fix: Bug description`
- `Update: What was updated`
- `Refactor: What was refactored`
- `Docs: Documentation changes`

Examples:
- `Add: User avatar upload functionality`
- `Fix: WebSocket reconnection bug`
- `Update: Improve message loading performance`

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** (if applicable)
5. **Fill out PR template**

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manually tested

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
```

## Feature Requests

To request a feature:

1. Check existing issues
2. Open new issue with "Feature Request" label
3. Describe the feature and use case
4. Wait for discussion and approval
5. Start implementation after approval

## Bug Reports

To report a bug:

1. Check existing issues
2. Open new issue with "Bug" label
3. Include:
   - Description
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Environment (OS, versions)

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows 10 / Ubuntu 22.04 / macOS 13
- Python: 3.10.5
- Godot: 4.2
- Backend version: 1.0.0
```

## Code Review

All PRs require review before merging:

- At least one approval
- All tests passing
- No merge conflicts
- Follows code style guidelines

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue with the "Question" label.

Thank you for contributing! 🎉
