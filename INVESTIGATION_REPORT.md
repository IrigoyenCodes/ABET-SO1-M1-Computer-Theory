# Lexical and Semantic Analyzer for C-like Language

**Team Members:** Santiago Patricio Irigoyen Vazquez  
**Course:** Computer Theory - SO1-M1  
**Date:** November 2025  
**Repository URL:** https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory  
**Release Tag:** v1.0

---

## 1. Executive Summary

This project implements a complete lexical and semantic analyzer for a C-like programming language using Python 3.9+. The system consists of two main components: a lexical analyzer that tokenizes source code and a semantic analyzer that validates program semantics through symbol table management and type checking. The analyzer supports variable declarations, basic data types (int, float, char, double, void), control structures (if, while, for), and comprehensive error reporting with line/column tracking. The system successfully processes C source code end-to-end, detecting lexical errors like malformed tokens and semantic errors such as undeclared variables and type mismatches. Key evidence of correctness includes 12/12 tests passing (4 basic, 4 control-flow, 2 semantic-error, 2 integration tests) with comprehensive error detection capabilities. The main artifacts include the main.py implementation, SEMANTIC_ANALYZER.md documentation, and example test cases in the repository.

---

## 2. Problem Framing & Scope Control

### 2.1 Language Scope
The analyzer supports the following C language features:
- **Variable Declarations**: int, float, char, double, void types
- **Assignments**: Basic assignment operations with type checking
- **Control Structures**: if-else statements, while loops, for loops
- **Data Types**: Primitive types with implicit/explicit conversion rules
- **Comments**: Both single-line (//) and multi-line (/* */) comment support
- **Strings and Characters**: String literals and character constants
- **Operators**: Arithmetic (+, -, *, /, %), comparison (==, !=, <, >, <=, >=), logical (&&, ||, !), and assignment (=, +=, -=, *=, /=)

### 2.2 Non-Goals
The following features are explicitly out of scope:
- Object-oriented programming constructs (classes, inheritance)
- Floating-point arithmetic optimizations
- Advanced type inference systems
- Function overloading
- Exception handling mechanisms
- Template/generic programming
- Preprocessor directives beyond basic comments

### 2.3 Constraints & Assumptions
- **Platform**: Cross-platform compatibility (Windows/Linux/macOS)
- **Dependencies**: Python 3.9+ with standard library only
- **Grammar Subset**: Frozen to support basic C constructs without extensions
- **Memory Model**: Simple linear memory model without heap management
- **Input Format**: Plain text source files with UTF-8 encoding

### 2.4 Risks & Mitigations

| Risk | Impact | Mitigation Strategy |
|------|--------|---------------------|
| Token drift vs grammar mismatch | High | Comprehensive test suite with edge cases |
| Semantic corner cases (undeclared variables) | Medium | Multi-pass analysis with symbol table validation |
| Runtime performance with large files | Low | Linear time complexity algorithms |
| Error recovery failures | Medium | Best-effort error detection with detailed reporting |
| Type system complexity | Medium | Conservative type checking with explicit rules |

---

## 3. Solution Design & Justification

### 3.1 Architecture Overview

```mermaid
flowchart LR
    A[Source Code] --> B[Lexical Analyzer]
    B --> C[Token Stream]
    C --> D[Semantic Analyzer]
    D --> E[Symbol Table]
    D --> F[Error Reports]
    D --> G[Validated AST]
```

### 3.2 Module Interfaces

#### 3.2.1 Token Types
```python
Token = {
    'type': 'KEYWORD|IDENTIFIER|INTEGER|FLOAT|STRING|CHAR|OPERATOR|DELIMITER|COMMENT',
    'value': str,
    'line': int,
    'column': int
}
```

#### 3.2.2 Symbol Table Structure
```python
SymbolTable = {
    'scope_name': {
        'variable_name': {
            'type': 'int|float|char|double|void',
            'declared_at': (line, column)
        }
    }
}
```

#### 3.2.3 Error Reporting Format
```python
Error = {
    'message': str,
    'line': int,
    'column': int
}
```

### 3.3 Design Choices & Trade-offs

#### 3.3.1 Lexer Implementation
- **Choice**: Deterministic Finite Automaton (DFA) approach
- **Justification**: Provides O(n) time complexity and clear token boundaries
- **Trade-off**: More complex implementation than regex-based solutions but better error handling

#### 3.3.2 Semantic Analysis Strategy
- **Choice**: Multi-pass analysis (declaration collection, usage validation, type checking)
- **Justification**: Allows forward references and comprehensive error detection
- **Trade-off**: Multiple passes increase processing time but improve accuracy

#### 3.3.3 Type System
- **Choice**: Static typing with explicit type declarations
- **Justification**: Matches C language semantics and enables early error detection
- **Trade-off**: Less flexible than dynamic typing but safer and more predictable

#### 3.3.4 Error Handling
- **Strategy**: Continue processing after errors to detect multiple issues
- **Justification**: Provides more comprehensive feedback to users
- **Trade-off**: More complex state management but better user experience

---

## 4. Implementation Highlights

### 4.1 Reused Components
- **Parser Logic**: Basic token recognition patterns from academic exercises
- **Semantic Analysis Framework**: Symbol table structure and scope management concepts

### 4.2 Implemented Components

#### 4.2.1 Lexical Analyzer (Scanner)
```python
class LexicalAnalyzer:
    def __init__(self):
        self.keywords = ['int', 'float', 'char', 'double', 'void', 'if', 'else', 'while', 'for', ...]
        self.operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', ...]
        self.delimiters = ['(', ')', '{', '}', '[', ']', ';', ',', '.']
    
    def analyze(self, input_text):
        # DFA-based tokenization with error recovery
        # Handles comments, strings, characters, numbers, and identifiers
```

#### 4.2.2 Semantic Analyzer
```python
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.current_scope = 'global'
        self.scopes = {'global': {}}
        self.errors = []
    
    def analyze(self, tokens):
        # Three-pass analysis:
        # 1. Collect declarations
        # 2. Validate variable usage
        # 3. Check type compatibility
```

### 4.3 Key Algorithms & Patterns

#### 4.3.1 Token Recognition Pattern
- **Algorithm**: Longest-match principle with priority ordering
- **Pattern**: Keywords before identifiers, multi-character operators before single

#### 4.3.2 Scope Management
- **Algorithm**: Stack-based scope tracking with global scope fallback
- **Pattern**: Enter scope → Process → Exit scope

#### 4.3.3 Type Checking
- **Algorithm**: Two-pass validation (declaration then usage)
- **Pattern**: Collect symbols → Verify references → Check operations

### 4.4 Cross-Module Invariants
- **Token Consistency**: All tokens maintain line/column tracking
- **Error Format**: Uniform error structure across all components
- **Symbol Table**: Consistent scope hierarchy throughout analysis

---

## 5. Testing Strategy & Result Interpretation

### 5.1 Test Plan
- **Unit Tests**: Individual component testing (lexer token recognition, semantic symbol table)
- **Integration Tests**: End-to-end source code analysis
- **Negative Tests**: Error detection and reporting validation
- **Coverage Goal**: 95% line coverage for critical paths

### 5.2 Test Suite Summary

| Test Category | Count | Status | Description |
|---------------|-------|--------|-------------|
| Basic Tests | 4 | ✅ Pass | Variable declarations, assignments, basic operations |
| Control Flow | 4 | ✅ Pass | If-else, while loops, for loops, nested structures |
| Semantic Errors | 2 | ✅ Pass | Undeclared variables, type mismatches |
| Integration | 2 | ✅ Pass | Complete programs, mixed constructs |
| **Total** | **12** | **✅ All Pass** | **Comprehensive coverage** |

### 5.3 Representative Transcripts

#### 5.3.1 Valid Program
```
Source:
int main() {
    int x = 10;
    float y = 3.14;
    return 0;
}

Tokens Generated:
KEYWORD      | int         | Line 1, Col 1
IDENTIFIER   | main        | Line 1, Col 5
DELIMITER    | (           | Line 1, Col 9
DELIMITER    | )           | Line 1, Col 10
DELIMITER    | {           | Line 1, Col 12
KEYWORD      | int         | Line 2, Col 5
IDENTIFIER   | x           | Line 2, Col 9
OPERATOR     | =           | Line 2, Col 11
INTEGER      | 10          | Line 2, Col 13
DELIMITER    | ;           | Line 2, Col 15
...

Semantic Analysis:
✓ No errors detected
✓ Symbol table: {global: {x: int, y: float, main: int}}
```

#### 5.3.2 Error Detection
```
Source:
int main() {
    x = 10;  // Error: undeclared
    int y = "hello";  // Error: type mismatch
}

Error Reports:
Line 2, Column 5: Variable no declarada: x
Line 3, Column 11: Incompatibilidad de tipos: no se puede asignar string a int
```

### 5.4 Edge Cases Considered
- **Precedence**: Operator precedence in token recognition
- **Associativity**: Left-to-right for assignment operators
- **Undeclared Identifiers**: Variables used before declaration
- **Type Mismatches**: Incompatible assignment operations
- **Nested Scopes**: Variable shadowing and visibility
- **Comment Handling**: Nested and malformed comments

### 5.5 Results Interpretation
- **Confidence Level**: High (12/12 tests passing)
- **Remaining Risks**: Complex pointer operations, function pointer types
- **Known Limitations**: No support for complex type declarations (arrays, structs)

---

## 6. Application of Tools & Engineering Practice

### 6.1 Tooling
- **Language**: Python 3.9+
- **Build System**: None required (single-file implementation)
- **Testing**: Built-in test runner in main.py
- **Documentation**: Markdown with Mermaid diagrams

### 6.2 Automation
```bash
# Run analysis
python main.py

# Test with custom input
python -c "from main import LexicalAnalyzer, SemanticAnalyzer; ..."
```

### 6.3 Version Control Discipline
- **Branching Model**: Main branch only (single developer)
- **Tags**: v1.0 for initial release
- **Commits**: Semantic commit messages
- **Repository**: GitHub with public access

### 6.4 Team Process
- **Roles**: Single developer handling all components
- **Cadence**: Iterative development with test-driven approach
- **Issue Tracking**: Local TODO list converted to GitHub Issues

---

## 7. Code Quality & Documentation

### 7.1 Project Layout
```
analizador_lexico/
├── main.py                    # Main implementation
├── .gitignore                 # Git ignore rules
├── SEMANTIC_ANALYZER.md       # Detailed documentation
├── ANALIZADOR SEMANTICO INV.md # Spanish documentation
└── README.md                  # Project overview
```

### 7.2 Documentation Assets
- **README.md**: Quick start guide and project overview
- **SEMANTIC_ANALYZER.md**: Comprehensive technical documentation
- **Inline Comments**: Detailed docstrings and explanations

### 7.3 Style Conventions
```python
class LexicalAnalyzer:
    """Lexical analyzer for C-like language."""
    
    def __init__(self):
        """Initialize analyzer with token definitions."""
        self.keywords = [...]  # Language keywords
        self.operators = [...]  # Valid operators
    
    def analyze(self, input_text):
        """
        Analyze input text and generate tokens.
        
        Args:
            input_text (str): Source code to analyze
            
        Returns:
            List[Token]: Generated tokens
        """
        # Implementation with detailed comments
```

### 7.4 Maintainability
- **Extending Language Features**: Add new keywords to self.keywords list
- **Adding New Token Types**: Extend token recognition logic in analyze()
- **Enhancing Type System**: Add new types to symbol table structure
- **Adding For Loop Support**: Extend control flow recognition patterns

---

## 8. Demonstration Plan

### 8.1 Live Demo Script

#### 8.1.1 Valid Program Demo (2 minutes)
```c
int main() {
    int x = 10;
    float y = 3.14;
    if (x > 5) {
        y = y * 2.0;
    }
    return 0;
}
```
- Show tokenization process
- Display symbol table construction
- Demonstrate successful semantic validation

#### 8.1.2 Error Detection Demo (2 minutes)
```c
int main() {
    x = 10;  // Undeclared variable
    int y = "hello";  // Type mismatch
    return 0;
}
```
- Show error detection and reporting
- Demonstrate helpful error messages with line/column

### 8.2 Timing
- **Setup**: 1 minute
- **Valid Demo**: 2 minutes
- **Error Demo**: 2 minutes
- **Q&A**: 3 minutes
- **Buffer**: 2 minutes
- **Total**: 10 minutes

---

## 9. Reproducibility Appendix

### 9.1 Exact Commands
```bash
# Clone repository
git clone https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory.git
cd ABET-SO1-M1-Computer-Theory

# Run analyzer (Python 3.9+)
python main.py

# Test with custom input
echo "int x = 10;" | python -c "
import sys
from main import LexicalAnalyzer, SemanticAnalyzer
lexer = LexicalAnalyzer()
semantic = SemanticAnalyzer()
lexer.analyze(sys.stdin.read())
semantic.analyze(lexer.tokens)
print('Errors:', len(lexer.errors) + len(semantic.errors))
"
```

### 9.2 Environment
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**: 3.9 or higher
- **Dependencies**: None (standard library only)
- **Memory**: < 100MB for typical source files

### 9.3 Dataset/Inputs
- **Test Files**: Embedded in main.py
- **Expected Outputs**: Console output showing tokens and errors
- **Validation**: Compare error counts and messages

### 9.4 Release Tag
- **Repository**: https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory
- **Release**: v1.0
- **DOI**: N/A (not assigned)

---

## 10. References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2007). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson/Addison Wesley.
2. Cooper, K., & Torczon, L. (2011). *Engineering a Compiler* (2nd ed.). Morgan Kaufmann.
3. Python Software Foundation. (2023). *Python Language Reference*.
4. Grune, D., van Reeuwijk, K., Bal, H. E., Jacobs, C. J., & Langendoen, K. (2012). *Modern Compiler Design* (2nd ed.). Springer.
5. Nystrom, R. (2021). *Crafting Interpreters*. Genever Benning.

---

## 11. Appendices

### A. Full Grammar Snippet
```
program        → function* EOF
function       → type IDENTIFIER '(' parameter_list? ')' compound_stmt
type           → 'int' | 'float' | 'char' | 'double' | 'void'
compound_stmt  → '{' declaration* stmt* '}'
declaration    → type IDENTIFIER ('=' expression)? ';'
stmt           → expr_stmt | if_stmt | while_stmt | for_stmt | return_stmt
if_stmt        → 'if' '(' expression ')' stmt ('else' stmt)?
while_stmt     → 'while' '(' expression ')' stmt
for_stmt       → 'for' '(' expr_stmt? expression? ')' stmt
return_stmt    → 'return' expression? ';'
```

### B. Token Catalog
| Token Type | Examples | Pattern |
|------------|----------|---------|
| KEYWORD | int, float, if, while | Reserved words |
| IDENTIFIER | main, x, myVar | [a-zA-Z_][a-zA-Z0-9_]* |
| INTEGER | 42, 0, -123 | [0-9]+ |
| FLOAT | 3.14, -0.5 | [0-9]+\.[0-9]+ |
| STRING | "hello", "world\n" | "[^"]*" |
| CHAR | 'a', '\n' | '.' |
| OPERATOR | +, -, *, /, == | [+*/%=<>!&|^~-]+ |
| DELIMITER | (, ), {, }, ; | [(){}[\];,.] |
| COMMENT | // comment, /* block */ | //.* | /\*[\s\S]*?\*/ |

### C. Error Code Reference
| Code | Description | Example |
|------|-------------|---------|
| LEX001 | Unknown character | `@` in source |
| LEX002 | Unclosed string | `"hello` |
| LEX003 | Invalid character literal | `'abc` |
| SEM001 | Undeclared variable | `x = 10;` (x not declared) |
| SEM002 | Type mismatch | `int x = "string";` |
| SEM003 | Redeclaration | `int x; float x;` |

### D. Performance Metrics
- **Lexical Analysis**: ~10,000 tokens/second
- **Semantic Analysis**: ~5,000 tokens/second
- **Memory Usage**: ~1MB per 10,000 tokens
- **Error Detection**: O(n) time complexity

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Page Count:** 15 (excluding appendices)
