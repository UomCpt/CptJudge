#include <stdio.h>
#include <stdlib.h>


int main() {
    int num1, num2;

    
    if (scanf("%d %d", &num1, &num2) != 2) {
        
        fprintf(stderr, "Error: Could not read two integers from input.\n");
        return 1; 
    }

   
    printf("The sum is: %d\n", num1 + num2);

    return 0; 
}
