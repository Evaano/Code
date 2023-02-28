string = input("Input: ")
characters = "aeiouAEIOU"

new_string = ""
for char in string:
    if char not in characters:
        new_string += char + ""

print(new_string)