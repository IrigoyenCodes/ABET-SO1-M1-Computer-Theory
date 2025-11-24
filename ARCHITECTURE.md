# Architecture Overview

## System Pipeline

```
Source Code → Lexical Analyzer → Parser → Semantic Analyzer → Code Generator → Virtual Machine
     ↓              ↓              ↓                    ↓                  ↓              ↓
  .c files     Tokens      AST Nodes      Symbol Table      Bytecode      Execution
```

## Module Interfaces

### 1. Lexical Analyzer → Parser
**Token Format**:
```python
{
    'type': 'KEYWORD|IDENTIFIER|INTEGER|FLOAT|OPERATOR|DELIMITER',
    'value': 'token_value',
    'line': line_number,
    'column': column_number
}
```

**Supported Token Types**:
- Keywords: `int, float, char, void, if, while, return`
- Operators: `+, -, *, /, =, ==, !=, <, >, <=, >=`
- Delimiters: `(, ), {, }, ;, ,`
- Literals: integers, floats, strings, characters

### 2. Parser → Semantic Analyzer
**AST Node Structure**:
```python
class ASTNode:
    type: NodeType  # PROGRAM, FUNCTION, DECLARATION, ASSIGNMENT, etc.
    value: Any      # Node-specific data
    children: List[ASTNode]
    line: int
    column: int
```

**Key Node Types**:
- `PROGRAM`: Root node containing functions
- `FUNCTION`: Function definitions with body
- `DECLARATION`: Variable declarations with types
- `ASSIGNMENT`: Variable assignment statements
- `BINARY_EXPRESSION`: Arithmetic and comparison operations
- `IF_STATEMENT`: Conditional branching
- `WHILE_STATEMENT`: Loop constructs

### 3. Semantic Analyzer → Code Generator
**Symbol Table Format**:
```python
{
    'scope_name': {
        'variable_name': {
            'type': 'int|float|char|void',
            'declared_at': (line, column)
        }
    }
}
```

**Error Reporting**:
```python
{
    'message': 'error_description',
    'line': line_number,
    'column': column_number
}
```

### 4. Code Generator → Virtual Machine
**Bytecode Instruction Format**:
```python
class Instruction:
    opcode: OpCode  # LOAD_CONST, STORE_VAR, BINARY_ADD, etc.
    operand: Any    # Optional operand data
    line: int       # Source line for debugging
```

**Supported Operations**:
- Stack operations: `LOAD_CONST, LOAD_VAR, STORE_VAR`
- Arithmetic: `BINARY_ADD, BINARY_SUB, BINARY_MUL, BINARY_DIV`
- Comparison: `BINARY_CMP`
- Control flow: `JUMP_IF_FALSE, JUMP`
- System: `RETURN, PRINT`

## Design Choices & Trade-offs

### Bytecode vs Three-Address Code (TAC)
**Choice**: Bytecode instruction set
**Rationale**:
- Simpler implementation for educational scope
- Direct mapping to virtual machine operations
- Efficient stack-based execution model
- Easier debugging with instruction pointers

### Control Flow Representation
**Choice**: Label-based jumps with conditional branching
**Implementation**:
- `JUMP_IF_FALSE label` for conditional execution
- `JUMP label` for unconditional branching
- Labels are instruction indices in bytecode array
- Supports nested control structures

### Type System Design
**Hierarchy**: `int → float` (implicit conversion allowed)
**Rules**:
- Strict type checking for assignments
- Implicit widening conversions (int to float)
- No implicit narrowing conversions
- Type compatibility validation in semantic analysis

### Error Handling Strategy
**Multi-Phase Error Detection**:
1. **Lexical**: Invalid characters, unclosed strings
2. **Parsing**: Syntax errors, unexpected tokens
3. **Semantic**: Undeclared variables, type mismatches
4. **Runtime**: Stack underflow, division by zero

**Error Reporting**:
- Phase identification (lexical/semantic/runtime)
- Line and column precision
- Human-readable error messages
- Error recovery when possible

## Cross-Module Contracts

### Token Stream Contract
- Lexical analyzer produces complete token stream
- Parser consumes tokens sequentially
- Error positions preserved across phases

### AST Structure Contract
- Parser produces well-formed hierarchical tree
- Semantic analyzer traverses tree for validation
- Code generator walks tree for instruction generation

### Symbol Table Contract
- Semantic analyzer builds and maintains scopes
- Code generator uses symbol table for variable references
- Virtual machine uses symbol information for memory layout

### Bytecode Contract
- Code generator produces valid instruction sequence
- Virtual machine executes instructions deterministically
- Error conditions handled gracefully

## Component Integration

### Data Flow
1. **Source** → **Tokens**: Character-level lexical analysis
2. **Tokens** → **AST**: Grammar-based parsing with error recovery
3. **AST** → **Symbols**: Semantic validation and scope management
4. **Symbols + AST** → **Bytecode**: Target-independent code generation
5. **Bytecode** → **Execution**: Stack-based virtual machine

### Error Propagation
- Early phases detect and report errors
- Later phases validate assumptions from earlier phases
- Comprehensive error collection and reporting
- Graceful degradation for debugging

### Performance Considerations
- Linear time lexical analysis (O(n))
- Single-pass parsing where possible
- Efficient symbol table lookup (hash-based)
- Stack-based VM execution (O(instructions))

## Extensibility Points

### Language Extensions
- New token types in lexical analyzer
- Additional AST node types in parser
- Extended type system in semantic analyzer
- New bytecode operations in code generator

### Optimization Opportunities
- Constant folding in code generation
- Peephole optimization on bytecode
- Register allocation improvements
- Dead code elimination

### Tool Integration
- AST visualization tools
- Bytecode disassemblers
- Performance profilers
- Interactive debuggers
