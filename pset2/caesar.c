#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{

    if (argc != 2 || atoi(argv[1]) <= 0)
    {
        printf("Please enter a positive integer as the argument!\n");
        return 1;
    }
    int k = atoi(argv[1]);
    printf("plaintext: ");
    string p = get_string();
    printf("ciphertext: ");
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if(isalpha(p[i]) && p[i] >= 'A' && p[i] <= 'Z')
        {
            if(p[i] + k % 26 < 'A' || p[i] + k % 26 >'Z')
            {
                printf("%c", p[i] + k % 26 - 26);
            }
            else
            {
                printf("%c", p[i] + k % 26);
            }
        }
        else if(isalpha(p[i]) && p[i] >= 'a' && p[i] <= 'z')
        {
            if(p[i] + k % 26 < 'a' || p[i] + k % 26 > 'z')
            {
                printf("%c", p[i] + k % 26 - 26);
            }
            else
            {
                printf("%c", p[i] + k % 26);
            }
        }
        else
        {
            printf("%c", p[i]);
        }
    }
    printf("\n");
    return 0;
}
