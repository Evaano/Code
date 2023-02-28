# TODO
from cs50 import get_float

# Ask how many cents the customer is owed
while True:
    cents = get_float("Change owed: ")
    if cents > 0:
        break

# Multiply the input by 100 and round it
cents = round(cents * 100)
counter = 0

# Calculate the number of quarters to give the customer
while cents >= 25:
    cents = cents - 25
    counter += 1

# Calculate the number of dimes to give the customer
while cents >= 10:
    cents = cents - 10
    counter += 1

# Calculate the number of nickels to give the customer
while cents >= 5:
    cents = cents - 5
    counter += 1

# Calculate the number of pennies to give the customer
while cents >= 1:
    cents = cents - 1
    counter += 1

print(counter)
