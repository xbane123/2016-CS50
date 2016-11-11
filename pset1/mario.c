#include <stdio.h>
#include <cs50.h>

void space(int n);
void hash(int n);

int main(void) 
{
    int counter;
    do
    {
        printf("Please enter a number between 0 and 23 : ");        
        counter = get_int();
    }
    while (counter < 0 || counter > 23);

    if (counter == 0) 
    {
        return 0;
    }
//    printf("counter is %d\n", counter);

    for (int i = 0; i < counter; i++)
    {
        space(counter-1-i);
        hash(i+1);
        space(2);
        hash(i+1);
        printf("\n");
    }
    return 0;
}

void space(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%c", 32);
    }
}

void hash(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%c", 35);
    }
}
