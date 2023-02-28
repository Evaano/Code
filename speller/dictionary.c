// Implements a dictionary's functionality
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Variables
unsigned int dictionary_size;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long total = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        total += toupper(word[i]);
    }

    return total % 'N';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dictionary_file = fopen(dictionary, "r");
    if (dictionary_file == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }

    char word[LENGTH + 1];

    // Load words into the hash table one at a time until the end of file
    while ((fscanf(dictionary_file, "%s", word)) != EOF)
    {
        // Increase dictionary size
        dictionary_size++;

        // Allocate memory for new node
        node *new_node = (node *)malloc(sizeof(node));

        // Copy words into the new node
        strcpy(new_node->word, word);

        // Get the index of word
        hash_value = hash(word);

        //
        if (table[hash_value] != NULL)
        {
            new_node->next = table[hash_value];
            table[hash_value] = new_node;
        }
    }

    fclose(dictionary_file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    return false;
}
