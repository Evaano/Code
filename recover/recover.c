#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Print error message if more than 1 argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    // Open file card.raw. If file doesn't exist, print error message
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    // Variable declaration
    unsigned char buffer[512];
    int counter = 0;
    FILE *output = NULL;
    char *filename = malloc(8 * sizeof(char));
    // Read from card.raw
    while (fread(buffer, sizeof(char), BLOCK_SIZE, input))
    {
        // Check if first 4 bytes matches JPEG header sequence
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If image count higher than 0 close the file before proceeding
            if (counter > 0)
            {
                fclose(output);
            }
            // Create a string of ###.jpg
            sprintf(filename, "%03i.jpg", counter);
            output = fopen(filename, "w");
            counter++;
        }
        // If output file exists write data into output
        if (output != NULL)
        {
            fwrite(buffer, sizeof(char), BLOCK_SIZE, output);
        }
    }
    // Close all files and free memory leaks
    free(filename);
    fclose(input);
    fclose(output);
}