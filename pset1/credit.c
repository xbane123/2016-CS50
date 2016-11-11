#include <stdio.h>
#include <cs50.h>
#include <math.h>

int validation(int array[16]);

int main(void) 
{
    
    // input the credit card number
    long long credit;
    do
    {
        printf("Please enter a credit card number : ");        
        credit = get_long_long();
    }
    while (credit < 1);
    
    // get each digit of the credit card number
    int array[16];
    for (int i = 0; i < 16 ; i++)
    {
        array[i] = credit % 10;
        credit = (credit - array[i]) / 10;
    // printf("array[%d] is %d\n", i, array[i]);          
    }

// for AMEX card
    if (array[15] == 0 && array[14] == 3)
    {
        if(validation(array) == true)
        {
            printf("AMEX\n");      
        }
        else
        {
            printf("INVALID\n");
        }
    }
    
// for MASTER card
    else if (array[15] == 5)
    {
        if(validation(array) == true)
        {
            printf("MASTERCARD\n");      
        }
        else
        {
            printf("INVALID\n");
        }
    }

// for VISA card - 16 digits
    else if (array[15] == 4)
    {
        if(validation(array) == true)
        {
            printf("VISA\n");      
        }
        else
        {
            printf("INVALID\n");
        }
    }  
    
// forVISA card - 13 digits
    else if (array[15] == 0 && array[14] == 0 && array[13] == 0 && array[12] == 4)
    {
        if(validation(array) == true)
        {
            printf("VISA\n");      
        }
        else
        {
            printf("INVALID\n");
        }
    }
    
    else
    {
        printf("INVALID\n");
    }
    return 0;    
}

int validation(int array[16])
{
    int sum_2 =0 , sum_1 = 0;
    for (int i = 0; i < 16; i += 2)
    {
        if (array[i+1] * 2 >= 10)
        {
            int res = (array[i+1] * 2) % 10;
            sum_2 = sum_2 + res + ((array[i+1] * 2) - res) / 10;
        }
        else 
        {
            sum_2 = sum_2 + array[i+1] * 2;
        }
    }
    for (int i = 0; i < 16; i += 2)
    {
        sum_1 += array[i];
    }
    if((sum_1 + sum_2) % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
