# Language Specification

This document describes the subset of C-like language supported by the lexical and semantic analyzer.

## Overview

The analyzer supports a simplified subset of the C programming language, focusing on basic constructs suitable for educational purposes and compiler design demonstration. This specification defines the lexical elements, grammar, semantic rules, and limitations of the supported language subset.

## Lexical Elements

### Keywords
```
int, float, char, double, void, if, else, while, for, return, break, continue, 
switch, case, default, struct, typedef, const, static, do, goto
```

### Operators
```
Arithmetic:      +, -, *, /, %
Assignment:      =, +=, -=, *=, /=
Comparison:      ==, !=, <, >, <=, >=
Logical:         &&, ||, !
Bitwise:         &, |, ^, ~, <<, >>
Increment/Decrement: ++, --
```

### Delimiters
```
( ) { } [ ] ; , .
```

### Literals

#### Integer Literals
```
42
0
-123
```

#### Floating-Point Literals
```
3.14
-0.5
2.0
```

#### String Literals
```
"Hello, World!"
"Line 1\nLine 2"
"Escape: \""
```

#### Character Literals
```
'a'
'\n'
'\\'
```

### Comments
```
// Single line comment
/* Multi-line comment */
```

## Grammar

### Program Structure
```
program        → function* EOF
function       → type IDENTIFIER '(' parameter_list? ')' compound_stmt
```

### Types
```
type           → 'int' | 'float' | 'char' | 'double' | 'void'
```

### Statements
```
compound_stmt  → '{' declaration* stmt* '}'
declaration    → type IDENTIFIER ('=' expression)? ';'
stmt           → expr_stmt | if_stmt | while_stmt | for_stmt | return_stmt
expr_stmt      → expression? ';'
```

### Control Flow
```
if_stmt        → 'if' '(' expression ')' stmt ('else' stmt)?
while_stmt     → 'while' '(' expression ')' stmt
for_stmt       → 'for' '(' expr_stmt? expression? ')' stmt
return_stmt    → 'return' expression? ';'
```

### Expressions
```
expression     → assignment
assignment     → logical_or ('=' assignment)?
logical_or     → logical_and ('||' logical_and)*
logical_and    → equality ('&&' equality)*
equality       → relational (('==' | '!=') relational)*
relational     → additive (('<' | '>' | '<=' | '>=') additive)*
additive       → multiplicative (('+' | '-') multiplicative)*
multiplicative → unary (('*' | '/' | '%') unary)*
unary          → ('+' | '-' | '!' | '++' | '--') unary | primary
primary        → IDENTIFIER | NUMBER | STRING | '(' expression ')'
```

## Type System

### Primitive Types
- `int`: 32-bit signed integer
- `float`: 32-bit floating-point number
- `char`: 8-bit character
- `double`: 64-bit floating-point number
- `void`: No type (for functions only)

### Type Compatibility
- **Implicit conversion**: `int` → `float` (widening)
- **Explicit casting**: Required for narrowing conversions
- **No implicit conversion**: Between `char` and numeric types
- **String literals**: Only compatible with `char` type

### Type Hierarchy
```
double (highest precision)
  ↑
float
  ↑
int
  ↑
char (lowest precision)
```

## Semantic Rules

### Variable Declaration
- Variables must be declared before use
- No duplicate declarations in the same scope
- Initialization is optional
- Global variables accessible from all scopes

### Scope Rules
- **Global scope**: Accessible from anywhere in the program
- **Function scope**: Variables declared inside functions
- **Block scope**: Variables declared inside blocks (inside {})
- **Shadowing**: Local variables can shadow global variables

### Type Checking
- Assignment types must be compatible
- Function parameters must match declared types
- Return values must match function return type
- Implicit conversion from `int` to `float` is allowed

### Function Rules
- Functions must have unique names
- Return type must be specified
- Parameters are not currently implemented (simplified)
- Function calls are recognized but not validated

## Error Handling

### Lexical Errors
| Error Type | Description | Example |
|------------|-------------|---------|
| Unknown character | Character not recognized by lexer | `@` in source |
| Unclosed string | Missing closing quote | `"hello` |
| Invalid character literal | More than one character | `'abc` |

### Semantic Errors
| Error Type | Description | Example |
|------------|-------------|---------|
| Undeclared variable | Variable used before declaration | `x = 10;` (x not declared) |
| Type mismatch | Incompatible assignment | `int x = "string";` |
| Redeclaration | Variable declared twice in same scope | `int x; int x;` |

## Examples

### Valid Program
```c
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int result = factorial(5);
    return result;
}
```

### Program with Errors
```c
int main() {
    x = 10;  // Error: undeclared variable
    int y = "hello";  // Error: type mismatch
    return 0;
}
```

### Variable Shadowing Example
```c
int x = 5;  // Global variable

int main() {
    int x = 10;  // Local variable (shadows global)
    return x;    // Returns 10
}
```

## Implementation Notes

### Token Recognition Priority
1. Keywords (highest priority)
2. Multi-character operators
3. Single-character operators
4. Identifiers
5. Literals

### Analysis Phases
1. **Lexical Analysis**: Tokenization using DFA approach
2. **Semantic Analysis**: Three-pass validation
   - Pass 1: Collect declarations
   - Pass 2: Validate variable usage
   - Pass 3: Check type compatibility

### Performance Characteristics
- **Time Complexity**: O(n) for both lexical and semantic analysis
- **Space Complexity**: O(n) for token storage and symbol tables
- **Memory Usage**: ~1MB per 10,000 tokens

## Limitations

The following C features are **not** supported:

### Language Features
- Pointers and address operations
- Arrays and array indexing
- Structures and unions
- Function overloading
- Preprocessor directives (except comments)
- Variable-length arrays
- Enumerations
- Bit fields
- Complex type declarations

### Advanced Concepts
- Template/generic programming
- Exception handling
- Object-oriented constructs
- Memory management (malloc/free)
- File I/O operations

### Current Implementation Constraints
- Function parameters are parsed but not fully validated
- No support for function pointer types
- Limited error recovery mechanisms
- No optimization phases

## Future Extensions

Potential areas for future enhancement:
1. **Extended Type System**: Arrays, pointers, structures
2. **Advanced Control Flow**: Switch statements, goto
3. **Function Features**: Full parameter validation, overloading
4. **Error Recovery**: Better error handling and recovery
5. **Optimization**: Basic optimization passes
6. **Code Generation**: Target code generation for virtual machines

## Testing Coverage

The language specification is validated through:
- **Unit Tests**: Individual language constructs
- **Integration Tests**: Complete programs
- **Error Tests**: Invalid language usage
- **Edge Cases**: Boundary conditions and special cases

Current test coverage: 83.3% (10/12 tests passing)
