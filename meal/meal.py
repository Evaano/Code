def main():
    # user input
    user_input = input("What time is it? ")
    # function call
    time = convert(user_input)
    if time >= 7 and time <= 8:
        print("breakfast time")

    elif time >= 12 and time <= 13:
        print("lunch time")

    elif time >= 18 and time <= 19:
        print("dinner time")


def convert(time):
    # split time into hours and minutes
    hours, minutes = time.split(":")
    float_minutes = float(minutes) / 60
    return float(hours) + float_minutes


if __name__ == "__main__":
    main()
