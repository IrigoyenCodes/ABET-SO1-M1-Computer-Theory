// Example of a valid program for the lexical and semantic analyzer

int factorial(int n) {
    // Calculate factorial recursively
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int fibonacci(int n) {
    // Calculate fibonacci number
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    // Variable declarations
    int number = 5;
    int fact_result;
    int fib_result;
    
    // Calculate factorial
    fact_result = factorial(number);
    
    // Calculate fibonacci
    fib_result = fibonacci(number);
    
    // Loop example
    int i = 0;
    int sum = 0;
    while (i < number) {
        sum = sum + i;
        i = i + 1;
    }
    
    // Conditional example
    if (sum > 10) {
        return 1;
    } else {
        return 0;
    }
}
