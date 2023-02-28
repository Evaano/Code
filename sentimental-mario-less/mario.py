# TODO
from cs50 import get_int

# Imitating a do while loop, if height is between 1 - 8 break out of loop
while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

# Start loop from index 0, upto height and increment by 1. If i + j is less than height - 1,
# else if i + j  is greater than height - 1, print a hash
for i in range(0, height, 1):
    for j in range(0, height, 1):
        if (i + j < height - 1):
            print(" ", end='')
        else:
            print("#", end='')
    print()
