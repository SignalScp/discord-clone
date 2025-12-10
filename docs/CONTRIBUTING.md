# Contributing to Discord Clone

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/discord-clone.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all functions
- Format code with `black`

```python
def example_function(param: str) -> dict:
    """Example function with proper documentation.
    
    Args:
        param: Description of parameter
        
    Returns:
        Dictionary with result
    """
    return {"result": param}
```

### GDScript (Frontend)

- Follow Godot style guide
- Use tabs for indentation
- Use type hints where possible
- Document complex functions

```gdscript
func example_function(param: String) -> Dictionary:
	"""Example function with documentation."""
	return {"result": param}
```

## Testing

### Backend

Add tests for new features:

```python
def test_new_feature():
    """Test description."""
    # Arrange
    test_data = {...}
    
    # Act
    result = function_to_test(test_data)
    
    # Assert
    assert result.success
```

Run tests:
```bash
pytest tests/
```

### Frontend

Manually test UI changes:
- Test on different screen sizes
- Verify WebSocket connections
- Check error handling

## Pull Request Guidelines

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `style: Code style improvements`
- `refactor: Code refactoring`
- `test: Add tests`
- `chore: Maintenance tasks`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added tests
- [ ] Tested manually
- [ ] Updated documentation

## Screenshots (if applicable)
[Add screenshots]
```

## Feature Requests

Open an issue with:
- Clear description
- Use cases
- Expected behavior
- Example implementation (optional)

## Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- System information
- Error messages/logs

## Code Review Process

1. Automated checks must pass
2. At least one approval required
3. No merge conflicts
4. Documentation updated
5. Tests passing

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
