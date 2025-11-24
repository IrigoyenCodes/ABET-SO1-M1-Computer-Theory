# Reproducibility Appendix

## Exact Build and Run Commands

### Prerequisites
```bash
# Check Python version (requires 3.9+)
python --version

# Verify dependencies (should be empty - uses only standard library)
pip list
```

### Clone Repository
```bash
git clone https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory.git
cd ABET-SO1-M1-Computer-Theory
git checkout v1.0.0
```

### Run Complete Pipeline
```bash
# Run with built-in example program
python main.py

# Run on specific source file
python main.py examples/valid_program.c
python main.py examples/error_program.c
python main.py examples/control_flow.c

# Run test suite
python tests.py

# Use Makefile for automation
make run      # Run with default example
make examples  # Run on all example files
make test     # Run test suite
make clean    # Clean temporary files
```

### Individual Component Testing
```bash
# Test lexical analysis only
python -c "
from main import LexicalAnalyzer
lexer = LexicalAnalyzer()
lexer.analyze('int x = 10;')
print(f'Tokens: {len(lexer.tokens)}')
"

# Test parsing only
python -c "
from main import LexicalAnalyzer, Parser
lexer = LexicalAnalyzer()
lexer.analyze('int main() { return 0; }')
parser = Parser(lexer.tokens)
ast = parser.parse()
print(f'AST: {ast}')
"

# Test complete compilation
python -c "
from main import LexicalAnalyzer, SemanticAnalyzer, Parser, CodeGenerator, VirtualMachine
lexer = LexicalAnalyzer()
lexer.analyze('int x = 10; int y = 20; int result = x + y;')
semantic = SemanticAnalyzer()
semantic.analyze(lexer.tokens)
parser = Parser(lexer.tokens)
ast = parser.parse()
codegen = CodeGenerator()
instructions = codegen.generate(ast)
vm = VirtualMachine()
vm.load_instructions(instructions)
vm.run()
print(f'Memory: {vm.memory}')
"
```

## Environment Specification

### Operating System
- **Primary**: Windows 10/11
- **Compatible**: Linux (Ubuntu 20.04+), macOS 10.15+

### Python Environment
```bash
# Required Python version
Python 3.9 or higher

# Standard library modules used
- re (regular expressions)
- sys (system operations)
- os (operating system interface)
- enum (enumeration types)

# No external dependencies required
pip install -r requirements.txt  # Should be empty or minimal
```

### Development Environment
```bash
# IDE/Editor (any)
- VS Code (recommended)
- PyCharm
- Notepad++
- Vim/Emacs

# Optional development tools
pip install black    # Code formatting
pip install pylint   # Linting
```

## Test Dataset and Expected Outputs

### Test Suite Location
```
tests.py                    # Main test suite
examples/                   # Example programs
├── valid_program.c         # Should compile and run
├── error_program.c         # Should show semantic errors
└── control_flow.c          # Should demonstrate control flow
test_simple.c              # Simple test case
```

### Expected Test Results
```bash
# Run test suite and expect:
python tests.py

# Expected output summary:
Total Tests: 12
Passed: 10
Failed: 2
Success Rate: 83.3%

# Expected passing tests:
- Variable Declaration
- Function Definition  
- Type Checking
- Comments
- If-Else Statement
- While Loop
- For Loop
- Nested Control Flow
- Type Mismatch
- Complete Program

# Known failing tests (under investigation):
- Undeclared Variable (semantic detection issue)
- Variable Shadowing (scope handling issue)
```

### Example Program Outputs

#### valid_program.c
```bash
python main.py examples/valid_program.c

# Expected: No errors, successful compilation and execution
# Final VM state should show variables in memory
```

#### error_program.c
```bash
python main.py examples/error_program.c

# Expected: Semantic errors detected and reported
# Should not reach code generation phase
```

#### test_simple.c
```bash
python main.py test_simple.c

# Expected output:
# Tokens found: 26
# Semantic errors: 0
# Parsing completed successfully
# Bytecode generated: 10 instructions
# VM Memory: {'x': 10, 'y': 20, 'result': 30}
```

## Verification and Validation

### Automated Verification
```bash
# Verify all components work
make test

# Verify examples work
make examples

# Verify build environment
make check-version
```

### Manual Verification Steps
1. **Lexical Analysis**: Tokens generated correctly
2. **Semantic Analysis**: Symbol tables built properly
3. **Parsing**: AST structure matches expectations
4. **Code Generation**: Bytecode instructions are valid
5. **VM Execution**: Program produces correct results

### Output Comparison
```bash
# Save expected outputs
python main.py examples/valid_program.c > expected_output.txt

# Compare current run to expected
python main.py examples/valid_program.c > current_output.txt
diff expected_output.txt current_output.txt

# Should show no differences for deterministic programs
```

## Release Information

### Release Tag
- **Tag**: v1.0.0
- **Commit**: [Latest stable commit hash]
- **Date**: November 2025
- **Status**: Production ready for educational use

### Release Artifacts
- **Source Code**: Complete main.py implementation
- **Documentation**: All .md files
- **Test Suite**: Comprehensive tests.py
- **Examples**: Working sample programs
- **Build Scripts**: Makefile automation

### Version History
- **v1.0.0**: Initial stable release with complete compiler pipeline
- **v0.9.0**: Beta version with basic lexical and semantic analysis
- **v0.5.0**: Alpha version with lexical analysis only

## Troubleshooting

### Common Issues
```bash
# Python version too old
# Solution: Upgrade to Python 3.9+
python --version  # Should show 3.9+

# File not found errors
# Solution: Check working directory
pwd  # Should be in project root
ls   # Should show main.py, tests.py, etc.

# Permission errors
# Solution: Check file permissions
chmod +x main.py  # On Linux/macOS

# Import errors
# Solution: Check Python path
python -c "import sys; print(sys.path)"
```

### Debug Mode
```bash
# Enable verbose output
python -v main.py

# Debug specific components
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from main import LexicalAnalyzer
# ... rest of debug code
"
```

### Performance Issues
```bash
# Measure execution time
time python main.py examples/valid_program.c

# Profile memory usage
python -m memory_profiler main.py examples/valid_program.c
```

## Contact and Support

### Issues and Questions
- **Repository**: https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory
- **Issues**: Use GitHub Issues for bug reports
- **Documentation**: Check existing .md files first

### Academic Context
- **Course**: Computer Theory - SO1-M1
- **Institution**: Universidad de las Américas Puebla
- **Author**: Santiago Patricio Irigoyen Vazquez
- **Submission**: ABET accreditation materials
