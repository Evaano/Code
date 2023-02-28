#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>

// Function prototype
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get input from user
    string text = get_string("Text: ");

    int index;

    int count1 = count_letters(text);
    int count2 = count_words(text);
    int count3 = count_sentences(text);

    index = round(0.0588 * (count1 / (float)count2 * 100) - 0.296 * (count3 / (float)count2 * 100) - 15.8);

    // If index less than 1 print before grade 1
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }

    // If index greater than 16 print grade 16+
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }

    // If Grade between 1-15 print the exact grade
    else
    {
        printf("Grade %i\n", index);
    }
}
int count_letters(string text)
{
    int letters = 0;

    // Counts each letter
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}
int count_words(string text)
{
    // Isspace counts spaces not words so skips the first word
    int words = 1;

    // Counts the number of spaces
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words;
}
int count_sentences(string text)
{
    int sentences = 0;
    
    // If the string contains .,!,? count sentences
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i]) == '.' || (text[i]) == '!' || (text[i]) == '?')
        {
            sentences++;
        }
    }
    return sentences;
}