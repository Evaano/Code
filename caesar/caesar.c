#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// argc takes number of arguments, argv takes an array of strings
int main(int argc, string argv[])
{
    // check if argc took 2 arguments, print instructions
    if (argc != 2)
    {
        printf("Usage: ./ceasar key\n");
        return 1;
    }

    // Checking if the argument is alphabets or not
    for (int key = 0; key < strlen(argv[1]); key++)
    {
        if (isalpha(argv[1][key]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    // ASCII to Integer
    int key = atoi(argv[1]) % 26;

    // Takes user input
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");

    // Iterates over the plain text with a for loop
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        if (!isalpha(plaintext[i]))
        {
            // Prints the current element of the array
            printf("%c", plaintext[i]);
            continue;
        }

        int offset = isupper(plaintext[i]) ? 65 : 97;
        // Calculating how far the current element is from lowercase "a" or uppercase "A"
        int pi = plaintext[i] - offset;
        // Index of cipher
        int ci = (pi + key) % 26;

        // printing the ciphertext
        printf("%c", ci + offset);
    }

    printf("\n");
    return 0;
}