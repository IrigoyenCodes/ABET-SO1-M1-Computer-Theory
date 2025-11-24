// Example demonstrating control flow structures

int find_max(int a, int b, int c) {
    // Find maximum of three numbers
    if (a > b) {
        if (a > c) {
            return a;
        } else {
            return c;
        }
    } else {
        if (b > c) {
            return b;
        } else {
            return c;
        }
    }
}

int sum_array(int n) {
    // Calculate sum of first n numbers
    int sum = 0;
    int i = 0;
    
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    
    return sum;
}

int factorial_loop(int n) {
    // Calculate factorial using for loop
    int result = 1;
    int i = 1;
    
    for (i = 1; i <= n; i = i + 1) {
        result = result * i;
    }
    
    return result;
}

int main() {
    int max_val = find_max(10, 20, 15);
    int sum_val = sum_array(5);
    int fact_val = factorial_loop(5);
    
    return 0;
}
