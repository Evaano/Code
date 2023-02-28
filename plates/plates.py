import string


def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):

    if not s.isalnum():
        return False

    if len(s) < 2 or len(s) > 6:
        return False

    if not s[:2].isalpha():
        return False

    for i in range(1, len(s)):
        if (s[i-1].isdigit() and s[i].isalpha()) or (s[i].isdigit() and s[i-1] == '0'):
            return False

    return True

main()
