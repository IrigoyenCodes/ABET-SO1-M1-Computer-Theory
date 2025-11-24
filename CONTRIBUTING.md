# Contributing to Lexical and Semantic Analyzer

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of compiler design concepts
- Familiarity with C programming language

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/ABET-SO1-M1-Computer-Theory.git
   cd ABET-SO1-M1-Computer-Theory
   ```

2. **Set Up Development Environment**
   ```bash
   # Create a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies (optional)
   pip install pytest black pylint mypy
   ```

3. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   python tests.py
   
   # Run the analyzer
   python main.py
   ```

## Project Structure

```
analizador_lexico/
├── main.py                    # Core implementation
├── tests.py                   # Test suite
├── examples/                  # Example programs
├── docs/                      # Documentation (if created)
├── README.md                  # Project overview
├── CONTRIBUTING.md            # This file
├── LICENSE                    # MIT License
└── .github/                   # GitHub configuration (if created)
    ├── workflows/             # CI/CD workflows
    └── ISSUE_TEMPLATE/        # Issue templates
```

## Development Guidelines

### Code Style

This project follows Python best practices:

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Add type hints where appropriate
- **Docstrings**: Include comprehensive docstrings
- **Comments**: Add comments for complex logic

#### Example Code Style

```python
class ExampleClass:
    """Example class demonstrating coding standards.
    
    Attributes:
        attribute: Description of the attribute
    """
    
    def __init__(self, attribute: str) -> None:
        """Initialize the ExampleClass.
        
        Args:
            attribute: Description of the parameter
        """
        self.attribute = attribute
    
    def example_method(self, param: int) -> bool:
        """Example method with proper documentation.
        
        Args:
            param: Description of the parameter
            
        Returns:
            True if successful, False otherwise
        """
        return param > 0
```

### Testing Guidelines

#### Writing Tests

1. **Test Structure**: Follow the existing test structure in `tests.py`
2. **Test Naming**: Use descriptive test names
3. **Test Coverage**: Aim for high test coverage
4. **Edge Cases**: Test edge cases and error conditions

#### Example Test

```python
def test_example_feature(self):
    """Test example feature with valid input."""
    source_code = """
    int main() {
        int x = 10;
        return x;
    }
    """
    
    lexer = LexicalAnalyzer()
    semantic = SemanticAnalyzer()
    
    lexer.analyze(source_code)
    errors = semantic.analyze(lexer.tokens)
    
    self.assertEqual(len(errors), 0, "Should have no semantic errors")
    self.assertGreater(len(lexer.tokens), 0, "Should generate tokens")
```

#### Running Tests

```bash
# Run all tests
python tests.py

# Run specific test category
python -m pytest tests.py::TestSuite::test_category

# Run with coverage (if pytest is installed)
pytest --cov=main tests.py
```

### Submitting Changes

#### Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. **Make Changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Ensure all tests pass
   - Update documentation if needed

3. **Test Your Changes**
   ```bash
   # Run the test suite
   python tests.py
   
   # Check code style (if black is installed)
   black --check main.py tests.py
   
   # Run linting (if pylint is installed)
   pylint main.py tests.py
   
   # Type checking (if mypy is installed)
   mypy main.py
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # Then create a pull request on GitHub
   ```

#### Commit Message Format

Use conventional commit messages:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add support for float type checking
fix: resolve variable shadowing issue
docs: update API documentation
test: add tests for error handling
```

## Types of Contributions

### 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear Description**: What the bug is
2. **Steps to Reproduce**: How to reproduce the issue
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, etc.
6. **Sample Code**: Minimal example that reproduces the issue

### ✨ Feature Requests

When requesting features, please include:

1. **Use Case**: Why this feature is needed
2. **Proposed Solution**: How you envision the feature
3. **Alternatives**: Other approaches you've considered
4. **Implementation Ideas** (optional): How you might implement it

### 📝 Documentation

Documentation improvements are always welcome:

- Fix typos and grammatical errors
- Improve clarity of existing documentation
- Add examples and tutorials
- Translate documentation to other languages

### 🧪 Testing

Help improve test coverage:

- Add tests for uncovered edge cases
- Improve existing test quality
- Add integration tests
- Add performance tests

## Code Review Process

### Review Guidelines

When reviewing pull requests:

1. **Code Quality**: Check for clean, maintainable code
2. **Functionality**: Ensure the feature works as intended
3. **Tests**: Verify adequate test coverage
4. **Documentation**: Check that documentation is updated
5. **Performance**: Consider performance implications

### Review Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass and provide good coverage
- [ ] Documentation is updated if needed
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages are clear and descriptive

## Community Guidelines

### Code of Conduct

This project follows a simple code of conduct:

1. **Be Respectful**: Treat all contributors with respect
2. **Be Constructive**: Provide helpful, constructive feedback
3. **Be Inclusive**: Welcome contributors of all backgrounds
4. **Be Patient**: Remember that everyone is learning

### Getting Help

If you need help:

1. **Check Documentation**: Review existing documentation first
2. **Search Issues**: Look for similar issues in the repository
3. **Ask Questions**: Create an issue with the "question" label
4. **Join Discussions**: Participate in GitHub discussions (if enabled)

## Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

### Contributor Types

- **Code Contributors**: Submit code changes
- **Documentation Contributors**: Improve documentation
- **Test Contributors**: Write and improve tests
- **Community Contributors**: Help others and provide feedback

## Release Process

### Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version number is updated
- [ ] Git tag is created
- [ ] Release is published on GitHub

## Resources

### Learning Resources

- [Compiler Design Principles](https://www.amazon.com/Compilers-Principles-Techniques-Tools-2nd/dp/0321486811)
- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Testing Best Practices](https://docs.pytest.org/en/stable/)

### Tools

- **IDE**: VS Code, PyCharm, or your preferred Python IDE
- **Linting**: pylint, flake8
- **Formatting**: black, autopep8
- **Testing**: pytest, unittest
- **Type Checking**: mypy

## Questions?

If you have questions about contributing:

1. Check this document first
2. Search existing issues and discussions
3. Create a new issue with the "question" label
4. Contact the project maintainer

---

Thank you for contributing to this project! Your contributions help make this project better for everyone.
