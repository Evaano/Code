#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //variables
    int height = 0, i = 0, j = 0;

    do
    {
        // get user input
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    // number of rows
    for (i = 1; i <= height; i++)
    {
        // number of columns
        for (j = 1; j <= height; j++)
        {
            // print hash or space
            if (j >= height + 1 - i)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        // new line
        printf("\n");
    }
}