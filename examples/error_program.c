// Example program with semantic errors for testing

int main() {
    // Error 1: Using undeclared variable
    x = 10;
    
    // Error 2: Type mismatch - assigning string to int
    int y = "hello";
    
    // Error 3: Type mismatch in assignment
    int z = 3.14;
    
    // Error 4: Redeclaration of variable
    int a = 5;
    float a = 2.5;
    
    // Error 5: Using undeclared variable in expression
    int result = x + y;
    
    return 0;
}
