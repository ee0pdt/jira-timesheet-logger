# Contributing to Jira Timesheet Logger

We welcome contributions to this project! Here's how you can help make this tool even better.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Set up the development environment

### Development Setup

```bash
# Install dependencies including development tools
pip install -r requirements.txt

# Or install with development dependencies
pip install -e .[dev]
```

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Keep functions focused and small
- Add docstrings to public functions
- Use meaningful variable and function names

### Running Tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=log-timesheet

# Run linting
flake8 log-timesheet.py

# Format code
black log-timesheet.py
```

### Testing Your Changes

1. Test with dry-run mode first:
   ```bash
   python log-timesheet.py --dry-run --limit 5
   ```

2. Test with a small dataset:
   ```bash
   python log-timesheet.py --limit 3
   ```

3. Verify error handling with invalid data

## Types of Contributions

### Bug Reports

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)
- Sample data (sanitized) if relevant

### Feature Requests

For new features:
- Describe the use case
- Explain why it would be valuable
- Consider backward compatibility
- Be open to discussion about implementation

### Code Contributions

#### Before You Start

- Check existing issues to avoid duplicated work
- Discuss major changes in an issue first
- Ensure your changes maintain backward compatibility

#### Pull Request Process

1. **NEVER push directly to main**: Always create feature branches
   ```bash
   git checkout -b feature/your-feature-name
   # Make changes, test, commit
   git push -u origin feature/your-feature-name
   gh pr create --title "Your change description"
   ```

2. **Branch naming**: Use descriptive names with prefixes:
   - `feature/add-custom-fields` - New functionality
   - `fix/datetime-bug` - Bug fixes
   - `docs/update-readme` - Documentation
   - `refactor/validation` - Code improvements

3. **Commit messages**: Use clear, descriptive commit messages
   ```
   Add validation for ticket format
   
   - Validates PROJECT-123 format using regex
   - Provides helpful error messages
   - Handles uppercase conversion automatically
   ```

3. **Code changes**:
   - Add tests for new functionality
   - Update documentation if needed
   - Ensure all tests pass
   - Follow existing code patterns

4. **Pull request description**:
   - Clearly describe what the PR does
   - Reference any related issues
   - Include testing instructions
   - Note any breaking changes

### Documentation Improvements

- Fix typos or unclear instructions
- Add examples for common use cases  
- Improve setup or troubleshooting guides
- Update API documentation

## Areas Where We Need Help

- **Testing**: More comprehensive test coverage
- **Error handling**: Better error messages and recovery
- **Performance**: Optimization for large datasets
- **Features**: 
  - Custom field support
  - Multiple CSV formats
  - Batch operations
  - Configuration file support
- **Documentation**: More examples and use cases

## Code of Conduct

- Be respectful and constructive
- Help others learn and improve
- Focus on the technical merits of contributions
- Welcome newcomers to the project

## Questions?

- Open an issue for questions about the codebase
- Use discussions for general questions about usage
- Check existing documentation and issues first

## Recognition

Contributors will be recognized in:
- The project README
- Release notes for significant contributions
- GitHub's contributor statistics

Thank you for helping improve this project!