# Import libraries
from cs50 import get_string

# User input
text = get_string("Text: ")

# Variables
letters = 0
words = 1
sentences = 0

# Loop through text. Update letters each time an alphabet is found, and words each time a space is found
# If ., ! or ? is found, update sentences count
for i in range(len(text)):
    if text[i].isalpha():
        letters += 1

    if text[i].isspace():
        words += 1

    if text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences += 1

# Coleman-Liau index formula
index = round(0.0588 * (letters / words * 100) -
              0.296 * (sentences / words * 100) - 15.8)

# Print grade accordingly
if (index < 1):
    print("Before Grade 1")

elif (index > 16):
    print("Grade 16+")

else:
    print("Grade", index)
