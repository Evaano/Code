answer = input("What is the answer to the Great Question of Life, the Universe, and Everything? ").replace(" ", "")
answer = answer.casefold().replace("-", "")

if answer == "42" or answer == "fortytwo":
    print("Yes")

else:
    print("No")