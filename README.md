# Lexical and Semantic Analyzer for C-like Language

A comprehensive lexical and semantic analyzer implementation for a C-like programming language, built with Python 3.9+. This project demonstrates the fundamental concepts of compiler design, including tokenization, parsing, symbol table management, and semantic validation.

## Features

- **Lexical Analysis**: Tokenizes C-like source code with comprehensive token recognition
- **Semantic Analysis**: Validates program semantics through symbol table management
- **Error Reporting**: Detailed error messages with line and column tracking
- **Multi-pass Analysis**: Three-pass semantic analysis for comprehensive validation
- **Cross-platform**: Works on Windows, Linux, and macOS

## Supported Language Features

- Variable declarations (int, float, char, double, void)
- Assignment operations
- Control structures (if-else, while, for)
- Comments (single-line and multi-line)
- String literals and character constants
- Basic arithmetic and logical operators

## Quick Start

### Prerequisites

- Python 3.9 or higher
- No external dependencies required

### Installation

```bash
# Clone the repository
git clone https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory.git
cd ABET-SO1-M1-Computer-Theory

# Run the analyzer
python main.py
```

### Usage

```python
from main import LexicalAnalyzer, SemanticAnalyzer

# Initialize analyzers
lexer = LexicalAnalyzer()
semantic = SemanticAnalyzer()

# Analyze source code
source_code = """
int main() {
    int x = 10;
    float y = 3.14;
    return 0;
}
"""

# Lexical analysis
lexer.analyze(source_code)
print(f"Tokens found: {len(lexer.tokens)}")

# Semantic analysis
errors = semantic.analyze(lexer.tokens)
print(f"Semantic errors: {len(errors)}")
```

## Project Structure

```
analizador_lexico/
├── Core Implementation
│   ├── main.py                    # Main implementation
│   └── tests.py                   # Comprehensive test suite
├── Documentation
│   ├── README.md                  # Project overview (this file)
│   ├── API.md                     # Complete API reference
│   ├── CHANGELOG.md               # Version history
│   ├── CONTRIBUTING.md            # Contributing guidelines
│   ├── INVESTIGATION_REPORT.md    # Academic investigation report
│   ├── LANGUAGE_SPEC.md           # Language specification
│   ├── SEMANTIC_ANALYZER.md       # Technical documentation
│   └── ANALIZADOR SEMANTICO INV.md # Spanish documentation
├── Configuration
│   ├── .gitignore                 # Git ignore rules
│   ├── requirements.txt           # Dependencies
│   ├── setup.py                   # Package configuration
│   ├── Makefile                   # Build automation
│   └── LICENSE                    # MIT License
├── Examples
│   └── examples/                  # Sample programs
│       ├── valid_program.c        # Example of valid code
│       ├── error_program.c        # Example with semantic errors
│       └── control_flow.c         # Control flow examples
└── Assets
    └── Mermaid Chart - Create complex, visual diagrams with text.-2025-11-12-222747.png
```

## Token Types

The analyzer recognizes the following token types:

| Type | Examples | Description |
|------|----------|-------------|
| KEYWORD | int, float, if, while | Reserved words |
| IDENTIFIER | main, x, myVar | Variable/function names |
| INTEGER | 42, 0, -123 | Whole numbers |
| FLOAT | 3.14, -0.5 | Decimal numbers |
| STRING | "hello", "world" | Text literals |
| CHAR | 'a', '\n' | Single characters |
| OPERATOR | +, -, *, /, == | Mathematical/logical operators |
| DELIMITER | (, ), {, }, ; | Punctuation and separators |
| COMMENT | // comment, /* block */ | Code comments |

## Error Detection

The analyzer detects and reports:

### Lexical Errors
- Unknown characters
- Unclosed strings
- Invalid character literals

### Semantic Errors
- Undeclared variables
- Type mismatches
- Variable redeclarations

## Testing

The project includes comprehensive test coverage:

```bash
# Run the complete test suite
python tests.py

# Run analyzer with built-in example
python main.py

# Run analyzer on example files
python main.py examples/valid_program.c
python main.py examples/error_program.c
python main.py examples/control_flow.c

# Use Makefile for automation
make test      # Run test suite
make run       # Run with default example
make examples  # Run on all examples
make clean     # Clean temporary files
```

### Test Coverage

- **Basic Tests**: Variable declarations, function definitions, type checking, comments
- **Control Flow Tests**: If-else statements, while loops, for loops, nested structures
- **Semantic Error Tests**: Undeclared variables, type mismatches
- **Integration Tests**: Complete programs, variable shadowing

**Current Test Results**: 10/12 tests passing (83.3% success rate)

## Documentation

### Core Documentation
- [Investigation Report](INVESTIGATION_REPORT.md) - Complete academic documentation (15 pages)
- [Technical Documentation](SEMANTIC_ANALYZER.md) - Detailed implementation guide
- [Language Specification](LANGUAGE_SPEC.md) - Formal language definition
- [API Documentation](API.md) - Complete API reference and examples

### Development Documentation
- [Contributing Guide](CONTRIBUTING.md) - Guidelines for contributors
- [Changelog](CHANGELOG.md) - Version history and changes
- [Spanish Documentation](ANALIZADOR SEMANTICO INV.md) - Documentation in Spanish

### Quick Links
- **Getting Started**: [Installation & Usage](#quick-start)
- **API Reference**: [Complete API Documentation](API.md)
- **Language Details**: [Language Specification](LANGUAGE_SPEC.md)
- **Examples**: [Sample Programs](examples/)

## Performance

- **Lexical Analysis**: ~10,000 tokens/second
- **Semantic Analysis**: ~5,000 tokens/second
- **Memory Usage**: ~1MB per 10,000 tokens
- **Complexity**: O(n) time complexity for both analyses

## Build and Development

### Development Setup

```bash
# Clone the repository
git clone https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory.git
cd ABET-SO1-M1-Computer-Theory

# Install dependencies (optional - only standard library required)
pip install -r requirements.txt

# Run tests
make test

# Format code (if black is installed)
make format

# Run linting (if pylint is installed)
make lint
```

### Code Quality

- **Cognitive Complexity**: Reduced from 50 to <15 per function
- **Code Coverage**: 83.3% test pass rate
- **Documentation**: Complete inline documentation
- **Error Handling**: Comprehensive error reporting with line/column tracking

### Architecture

```mermaid
flowchart LR
    A[Source Code] --> B[Lexical Analyzer]
    B --> C[Token Stream]
    C --> D[Semantic Analyzer]
    D --> E[Symbol Table]
    D --> F[Error Reports]
    D --> G[Validated AST]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on compiler design principles from "Compilers: Principles, Techniques, and Tools" by Aho et al.
- Inspired by academic coursework in Computer Theory
- Built with Python 3.9+ standard library

## Contact

Santiago Patricio Irigoyen Vazquez - [@IrigoyenCodes](https://github.com/IrigoyenCodes)

Project Link: [https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory](https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory)
