#include <stdio.h>
#include <string.h>

int main(void) {
        int r = 10;
        char s1[3] = {0};
        char s2[4] = {0};
        long q = 0;
        if (scanf("%s", s1) <= 0) {
                printf("234");
        } else if (s1[0] == '7') {
                strcat(strcat(s2, "11"), s1);
                s2[3] = 0;
                r = r + s1[1] * q;
                printf("%s", s2);
                printf("%s", s1);
        } else {
                printf("345");
        }        
}