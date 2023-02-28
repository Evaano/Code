from cs50 import get_int

coke = 50

# do the following loop while amount due is more than 0
while coke > 0:
    print("Amount Due:", + coke)
    amount = get_int("Insert Coin: ")
    # only accept user input of 25,10,5
    if amount == 25 or amount == 10 or amount == 5:
        coke = coke - amount
        # If amount due is greater than or equal to 0, print the amount due
        if coke > 0:
            print(f"Amount Due: {coke}")
        # If the amount due is less than 0, print the change owed
        elif coke <= 0:
            print(f"Change Owed: {coke*(-1)}")
