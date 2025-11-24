# Executive Summary

## Project Information
- **Project Title**: Lexical and Semantic Analyzer for C-like Language
- **Team Members**: Santiago Patricio Irigoyen Vazquez
- **Course**: Computer Theory - SO1-M1
- **Date**: November 2025
- **Repository URL**: https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory
- **Release Tag**: v1.0.0

## What We Built

We implemented a complete compiler pipeline for a C-like programming language, including lexical analysis, parsing, semantic analysis, code generation, and virtual machine execution. The system supports variable declarations, assignments, arithmetic expressions, and control flow constructs (if/while statements), with comprehensive error reporting and type checking.

## End-to-End Functionality

The compiler successfully transforms source code through the complete pipeline: `source → lexer → parser → semantic analyzer → code generator → virtual machine`. All components work together to validate syntax and semantics, generate bytecode, and execute programs with proper variable management and arithmetic operations.

## Key Evidence of Correctness

- **Test Results**: 10/12 tests passing (83.3% success rate)
- **Pipeline Verification**: Complete compilation from source to execution
- **Error Handling**: Comprehensive error detection with line/column tracking
- **Type System**: Working type checking with implicit conversions
- **Memory Management**: Proper variable storage and retrieval in VM

## Most Important Artifacts

- **[README.md](README.md)** - Project overview and quick start
- **[LANGUAGE_SPEC.md](LANGUAGE_SPEC.md)** - Complete language specification
- **[main.py](main.py)** - Full compiler implementation
- **[tests.py](tests.py)** - Comprehensive test suite
- **[Makefile](Makefile)** - Build automation and run scripts

## How to Run

```bash
# Clone repository
git clone https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory.git
cd ABET-SO1-M1-Computer-Theory

# Run with built-in example
python main.py

# Run test suite
python tests.py

# Run on specific file
python main.py examples/valid_program.c
```

## Technical Achievements

- **Complete AST Generation**: Proper parsing of function definitions and statements
- **Bytecode Generation**: Working instruction set for arithmetic and control flow
- **Virtual Machine**: Stack-based execution with memory management
- **Error Recovery**: Robust error handling across all compilation phases
- **Type Safety**: Semantic validation with type compatibility checking
