# user input
camelCase = input("camelCase: ")

# print "snake_case"
print("snake_case: ", end="")

# loop through every letter in camelCase and if letter is upper print _ and convert to lower
# else just print the letter
for letter in camelCase:
    if letter.isupper():
        print("_" + letter.lower(), end="")
    else:
        print(letter, end="")
print()