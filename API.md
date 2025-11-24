# API Documentation

This document provides detailed API documentation for the Lexical and Semantic Analyzer.

## Overview

The analyzer consists of two main classes:

- `LexicalAnalyzer`: Converts source code into tokens
- `SemanticAnalyzer`: Validates program semantics and builds symbol tables

## LexicalAnalyzer Class

### Constructor

```python
LexicalAnalyzer() -> LexicalAnalyzer
```

Creates a new lexical analyzer instance.

**Returns:**
- `LexicalAnalyzer`: A new analyzer instance

**Example:**
```python
lexer = LexicalAnalyzer()
```

### Methods

#### analyze()

```python
analyze(input_text: str) -> None
```

Analyzes the input text and generates tokens.

**Parameters:**
- `input_text` (str): The source code to analyze

**Returns:**
- `None`: Results are stored in the `tokens` and `errors` attributes

**Side Effects:**
- Populates `self.tokens` with recognized tokens
- Populates `self.errors` with lexical errors

**Example:**
```python
lexer = LexicalAnalyzer()
lexer.analyze("int x = 10;")
print(lexer.tokens)  # List of tokens
print(lexer.errors)  # List of errors
```

#### Token Format

Each token is a dictionary with the following structure:

```python
{
    'type': str,      # Token type (KEYWORD, IDENTIFIER, INTEGER, etc.)
    'value': str,     # Token value
    'line': int,      # Line number (1-based)
    'column': int     # Column number (1-based)
}
```

#### Error Format

Each lexical error is a dictionary:

```python
{
    'message': str,   # Error description
    'line': int,      # Line number (1-based)
    'column': int     # Column number (1-based)
}
```

#### Supported Token Types

| Type | Description | Examples |
|------|-------------|----------|
| `KEYWORD` | Reserved words | `int`, `float`, `if`, `while` |
| `IDENTIFIER` | Variable/function names | `main`, `x`, `myVar` |
| `INTEGER` | Whole numbers | `42`, `0`, `-123` |
| `FLOAT` | Decimal numbers | `3.14`, `-0.5` |
| `STRING` | Text literals | `"hello"`, `"world"` |
| `CHAR` | Single characters | `'a'`, `'\n'` |
| `OPERATOR` | Mathematical/logical operators | `+`, `-`, `*`, `/`, `==` |
| `DELIMITER` | Punctuation and separators | `(`, `)`, `{`, `}`, `;` |
| `COMMENT` | Code comments | `// comment`, `/* block */` |

## SemanticAnalyzer Class

### Constructor

```python
SemanticAnalyzer() -> SemanticAnalyzer
```

Creates a new semantic analyzer instance.

**Returns:**
- `SemanticAnalyzer`: A new analyzer instance

**Example:**
```python
semantic = SemanticAnalyzer()
```

### Methods

#### analyze()

```python
analyze(tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]
```

Performs semantic analysis on a list of tokens.

**Parameters:**
- `tokens` (List[Dict]): List of tokens from the lexical analyzer

**Returns:**
- `List[Dict]`: List of semantic errors found during analysis

**Side Effects:**
- Populates `self.scopes` with symbol tables
- Populates `self.errors` with semantic errors

**Example:**
```python
lexer = LexicalAnalyzer()
semantic = SemanticAnalyzer()

lexer.analyze("int x = 10;")
errors = semantic.analyze(lexer.tokens)

print(errors)  # Semantic errors
print(semantic.scopes)  # Symbol tables
```

#### Symbol Table Structure

Symbol tables are organized by scope:

```python
{
    'scope_name': {
        'variable_name': {
            'type': str,              # Variable type
            'declared_at': (int, int) # (line, column) of declaration
        }
    }
}
```

#### Error Format

Each semantic error is a dictionary:

```python
{
    'message': str,   # Error description
    'line': int,      # Line number (1-based)
    'column': int     # Column number (1-based)
}
```

#### Semantic Error Types

| Error Type | Description | Example |
|------------|-------------|---------|
| Undeclared variable | Variable used before declaration | `x = 10;` (x not declared) |
| Type mismatch | Incompatible assignment | `int x = "string";` |
| Redeclaration | Variable declared twice in same scope | `int x; int x;` |

### Scope Management

#### enter_scope()

```python
enter_scope(scope_name: str) -> None
```

Creates a new scope for variable declarations.

**Parameters:**
- `scope_name` (str): Name of the new scope

**Example:**
```python
semantic.enter_scope('function_local')
```

#### exit_scope()

```python
exit_scope() -> None
```

Exits the current scope and returns to the parent scope.

**Example:**
```python
semantic.exit_scope()  # Returns to global scope
```

#### add_symbol()

```python
add_symbol(name: str, var_type: str, line: int, column: int) -> Optional[bool]
```

Adds a symbol to the current scope.

**Parameters:**
- `name` (str): Variable name
- `var_type` (str): Variable type
- `line` (int): Declaration line number
- `column` (int): Declaration column number

**Returns:**
- `Optional[bool]`: `True` if added successfully, `None` if error occurred

**Example:**
```python
success = semantic.add_symbol('x', 'int', 1, 5)
```

#### lookup_symbol()

```python
lookup_symbol(name: str) -> Optional[Dict[str, Any]]
```

Looks up a symbol in the symbol tables.

**Parameters:**
- `name` (str): Variable name to look up

**Returns:**
- `Optional[Dict]`: Symbol information if found, `None` otherwise

**Example:**
```python
symbol_info = semantic.lookup_symbol('x')
if symbol_info:
    print(f"Type: {symbol_info['type']}")
```

## Usage Examples

### Basic Usage

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
print(f"Tokens: {len(lexer.tokens)}")
print(f"Lexical errors: {len(lexer.errors)}")

# Semantic analysis
semantic_errors = semantic.analyze(lexer.tokens)
print(f"Semantic errors: {len(semantic_errors)}")
print(f"Symbol tables: {semantic.scopes}")
```

### Error Handling

```python
from main import LexicalAnalyzer, SemanticAnalyzer

lexer = LexicalAnalyzer()
semantic = SemanticAnalyzer()

# Code with errors
source_code = """
int main() {
    x = 10;  // Undeclared variable
    int y = "hello";  // Type mismatch
    return 0;
}
"""

lexer.analyze(source_code)
errors = semantic.analyze(lexer.tokens)

# Handle errors
if lexer.errors:
    print("Lexical errors:")
    for error in lexer.errors:
        print(f"  Line {error['line']}, Column {error['column']}: {error['message']}")

if errors:
    print("Semantic errors:")
    for error in errors:
        print(f"  Line {error['line']}, Column {error['column']}: {error['message']}")
```

### Custom Error Processing

```python
from main import LexicalAnalyzer, SemanticAnalyzer

class CustomAnalyzer:
    def __init__(self):
        self.lexer = LexicalAnalyzer()
        self.semantic = SemanticAnalyzer()
    
    def analyze_file(self, filename: str) -> Dict[str, Any]:
        """Analyze a file and return detailed results."""
        with open(filename, 'r') as f:
            source_code = f.read()
        
        # Perform analysis
        self.lexer.analyze(source_code)
        semantic_errors = self.semantic.analyze(self.lexer.tokens)
        
        # Return comprehensive results
        return {
            'tokens': self.lexer.tokens,
            'lexical_errors': self.lexer.errors,
            'semantic_errors': semantic_errors,
            'symbol_tables': self.semantic.scopes,
            'total_errors': len(self.lexer.errors) + len(semantic_errors),
            'is_valid': len(self.lexer.errors) == 0 and len(semantic_errors) == 0
        }

# Usage
analyzer = CustomAnalyzer()
results = analyzer.analyze_file('example.c')
print(f"Analysis complete. Valid: {results['is_valid']}")
```

## Performance Considerations

### Time Complexity

- **Lexical Analysis**: O(n) where n is the length of input text
- **Semantic Analysis**: O(n) where n is the number of tokens

### Space Complexity

- **Token Storage**: O(n) where n is the number of tokens
- **Symbol Tables**: O(m) where m is the number of declared variables

### Memory Usage

Approximate memory usage:
- ~1MB per 10,000 tokens
- ~100KB per 1000 declared variables

## Error Codes Reference

### Lexical Error Codes

| Code | Description | Example |
|------|-------------|---------|
| LEX001 | Unknown character | `@` in source |
| LEX002 | Unclosed string | `"hello` |
| LEX003 | Invalid character literal | `'abc` |

### Semantic Error Codes

| Code | Description | Example |
|------|-------------|---------|
| SEM001 | Undeclared variable | `x = 10;` (x not declared) |
| SEM002 | Type mismatch | `int x = "string";` |
| SEM003 | Redeclaration | `int x; int x;` |

## Integration Examples

### Command Line Interface

```python
import sys
from main import LexicalAnalyzer, SemanticAnalyzer

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <source_file>")
        return
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return
    
    # Analyze
    lexer = LexicalAnalyzer()
    semantic = SemanticAnalyzer()
    
    lexer.analyze(source_code)
    errors = semantic.analyze(lexer.tokens)
    
    # Report results
    print(f"File: {filename}")
    print(f"Tokens: {len(lexer.tokens)}")
    print(f"Lexical errors: {len(lexer.errors)}")
    print(f"Semantic errors: {len(errors)}")
    
    if lexer.errors or errors:
        print("\nErrors found:")
        for error in lexer.errors + errors:
            print(f"  Line {error['line']}, Column {error['column']}: {error['message']}")
    else:
        print("✅ No errors found")

if __name__ == '__main__':
    main()
```

### Web API Integration

```python
from flask import Flask, request, jsonify
from main import LexicalAnalyzer, SemanticAnalyzer

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_code():
    """API endpoint for code analysis."""
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        # Analyze code
        lexer = LexicalAnalyzer()
        semantic = SemanticAnalyzer()
        
        lexer.analyze(data['code'])
        semantic_errors = semantic.analyze(lexer.tokens)
        
        # Return results
        return jsonify({
            'tokens': lexer.tokens,
            'lexical_errors': lexer.errors,
            'semantic_errors': semantic_errors,
            'symbol_tables': semantic.scopes,
            'is_valid': len(lexer.errors) == 0 and len(semantic_errors) == 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## Troubleshooting

### Common Issues

1. **No tokens generated**
   - Check if input text is empty
   - Verify source code syntax

2. **Unexpected lexical errors**
   - Check for unsupported characters
   - Verify string literals are properly closed

3. **Semantic errors for valid code**
   - Check variable declarations
   - Verify type compatibility

4. **Performance issues**
   - For large files, consider processing in chunks
   - Monitor memory usage

### Debug Mode

Enable debug output for troubleshooting:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Analyze with debug info
lexer = LexicalAnalyzer()
semantic = SemanticAnalyzer()

lexer.analyze(source_code)
print(f"Debug: Generated {len(lexer.tokens)} tokens")
print(f"Debug: Symbol tables: {semantic.scopes}")
```

---

For more examples and advanced usage, see the [examples](examples/) directory and the [test suite](tests.py).
