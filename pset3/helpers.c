/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
       
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // ensure argument n is positive
    if (n < 0)
    {
        return false;
    }
    // binary search
    else 
    {
        int upper = n - 1, lower = 0;
        while(upper >= lower)
        {
            int mid = (upper + lower) / 2;
            if(value == values[mid])
            {
                return true;
            }
            else if(value < values[mid])
            {
                upper = mid-1;
            }
            else
            {
                lower = mid+1;
            }
        }
        return false;
    }
}


/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // implement an O(n^2) sorting algorithm
    for(int i = 1; i < n; i++)
    {
        int j = i;
        while(j > 0 && values[j-1] > values[j])
        {
            int temp = values[j];
            values[j] = values[j-1];
            values[j-1] = temp;
            j--;
        }
    }
    return;
}
