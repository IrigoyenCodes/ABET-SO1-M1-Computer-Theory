#!/usr/bin/env python3
"""
Comprehensive test suite for the Lexical and Semantic Analyzer
"""

import sys
import os
from main import LexicalAnalyzer, SemanticAnalyzer

class TestSuite:
    def __init__(self):
        self.lexer = LexicalAnalyzer()
        self.semantic = SemanticAnalyzer()
        self.test_results = []
        self.pass_count = 0
        self.fail_count = 0
    
    def run_test(self, test_name, source_code, expected_lexical_errors=0, expected_semantic_errors=0):
        """Run a single test case"""
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'='*60}")
        
        # Reset analyzers
        self.lexer = LexicalAnalyzer()
        self.semantic = SemanticAnalyzer()
        
        # Run lexical analysis
        self.lexer.analyze(source_code)
        lexical_errors = len(self.lexer.errors)
        
        # Run semantic analysis
        semantic_errors = len(self.semantic.analyze(self.lexer.tokens))
        
        # Check results
        lexical_passed = lexical_errors == expected_lexical_errors
        semantic_passed = semantic_errors == expected_semantic_errors
        test_passed = lexical_passed and semantic_passed
        
        # Record result
        result = {
            'name': test_name,
            'passed': test_passed,
            'lexical_errors': lexical_errors,
            'expected_lexical': expected_lexical_errors,
            'semantic_errors': semantic_errors,
            'expected_semantic': expected_semantic_errors
        }
        self.test_results.append(result)
        
        # Update counters
        if test_passed:
            self.pass_count += 1
            status = "✅ PASS"
        else:
            self.fail_count += 1
            status = "❌ FAIL"
        
        # Print result
        print(f"Status: {status}")
        print(f"Lexical Errors: {lexical_errors} (expected: {expected_lexical_errors})")
        print(f"Semantic Errors: {semantic_errors} (expected: {expected_semantic_errors})")
        
        # Show source code
        print(f"\nSource Code:\n{source_code}")
        
        # Show errors if any
        if self.lexer.errors:
            print("\nLexical Errors:")
            for error in self.lexer.errors:
                print(f"  Line {error['line']}, Column {error['column']}: {error['message']}")
        
        if self.semantic.errors:
            print("\nSemantic Errors:")
            for error in self.semantic.errors:
                print(f"  Line {error['line']}, Column {error['column']}: {error['message']}")
        
        return test_passed
    
    def run_all_tests(self):
        """Run all test cases"""
        print("="*80)
        print("LEXICAL AND SEMANTIC ANALYZER - TEST SUITE")
        print("="*80)
        
        # Basic Tests (4)
        self.run_basic_tests()
        
        # Control Flow Tests (4)
        self.run_control_flow_tests()
        
        # Semantic Error Tests (2)
        self.run_semantic_error_tests()
        
        # Integration Tests (2)
        self.run_integration_tests()
        
        # Print summary
        self.print_summary()
    
    def run_basic_tests(self):
        """Run basic functionality tests"""
        print("\n" + "="*60)
        print("BASIC TESTS")
        print("="*60)
        
        # Test 1: Variable Declaration
        self.run_test(
            "Variable Declaration",
            """
int main() {
    int x = 10;
    float y = 3.14;
    char z = 'A';
    return 0;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
        
        # Test 2: Function Definition
        self.run_test(
            "Function Definition",
            """
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(5, 3);
    return result;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
        
        # Test 3: Type Checking
        self.run_test(
            "Type Checking",
            """
int main() {
    int x = 10;
    float y = x + 5.5;  // Implicit conversion
    return 0;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
        
        # Test 4: Comments
        self.run_test(
            "Comments",
            """
// This is a single line comment
int main() {
    /* This is a
       multi-line comment */
    int x = 10; // End line comment
    return 0;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
    
    def run_control_flow_tests(self):
        """Run control flow tests"""
        print("\n" + "="*60)
        print("CONTROL FLOW TESTS")
        print("="*60)
        
        # Test 1: If-Else
        self.run_test(
            "If-Else Statement",
            """
int main() {
    int x = 10;
    if (x > 5) {
        return 1;
    } else {
        return 0;
    }
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
        
        # Test 2: While Loop
        self.run_test(
            "While Loop",
            """
int main() {
    int x = 5;
    while (x > 0) {
        x = x - 1;
    }
    return x;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
        
        # Test 3: For Loop
        self.run_test(
            "For Loop",
            """
int main() {
    int sum = 0;
    for (int i = 0; i < 10; i = i + 1) {
        sum = sum + i;
    }
    return sum;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
        
        # Test 4: Nested Control Flow
        self.run_test(
            "Nested Control Flow",
            """
int main() {
    int x = 10;
    int y = 5;
    
    if (x > 0) {
        while (y > 0) {
            if (x > y) {
                x = x - 1;
            }
            y = y - 1;
        }
    }
    return x;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
    
    def run_semantic_error_tests(self):
        """Run semantic error detection tests"""
        print("\n" + "="*60)
        print("SEMANTIC ERROR TESTS")
        print("="*60)
        
        # Test 1: Undeclared Variable
        self.run_test(
            "Undeclared Variable",
            """
int main() {
    x = 10;  // Error: x not declared
    return 0;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=1
        )
        
        # Test 2: Type Mismatch
        self.run_test(
            "Type Mismatch",
            """
int main() {
    int x = "hello";  // Error: type mismatch
    return 0;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=1
        )
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("\n" + "="*60)
        print("INTEGRATION TESTS")
        print("="*60)
        
        # Test 1: Complete Program
        self.run_test(
            "Complete Program",
            """
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
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
        
        # Test 2: Variable Shadowing
        self.run_test(
            "Variable Shadowing",
            """
int x = 5;  // Global variable

int main() {
    int x = 10;  // Local variable (shadowing)
    return x;
}
""",
            expected_lexical_errors=0,
            expected_semantic_errors=0
        )
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        total_tests = len(self.test_results)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.pass_count}")
        print(f"Failed: {self.fail_count}")
        print(f"Success Rate: {(self.pass_count/total_tests)*100:.1f}%")
        
        # Print failed tests
        if self.fail_count > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  ❌ {result['name']}")
                    print(f"     Lexical: {result['lexical_errors']}/{result['expected_lexical']}")
                    print(f"     Semantic: {result['semantic_errors']}/{result['expected_semantic']}")
        
        # Print detailed results table
        print("\nDetailed Results:")
        print("-" * 80)
        print(f"{'Test Name':<30} {'Status':<8} {'Lexical':<10} {'Semantic':<10}")
        print("-" * 80)
        for result in self.test_results:
            status = "PASS" if result['passed'] else "FAIL"
            lexical = f"{result['lexical_errors']}/{result['expected_lexical']}"
            semantic = f"{result['semantic_errors']}/{result['expected_semantic']}"
            print(f"{result['name']:<30} {status:<8} {lexical:<10} {semantic:<10}")
        
        print("\n" + "="*80)

if __name__ == '__main__':
    # Run the test suite
    test_suite = TestSuite()
    test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if test_suite.fail_count == 0 else 1)
