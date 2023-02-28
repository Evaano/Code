greet = input("Greeting: ").strip()

if greet.startswith(('hello', 'Hello')):
    print("$0")

elif greet.startswith(('h', 'H')):
    print("$20")

else:
    print("$100")