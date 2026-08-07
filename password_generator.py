import random
import string

print("===== Random Password Generator =====")

while True:
    # Get password length
    while True:
        try:
            length = int(input("\nEnter password length (minimum 8): "))

            if length < 8:
                print("Password length must be at least 8 characters.")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    # Character type selection
    print("\nSelect character types to include:")

    uppercase = input("Include Uppercase letters? (y/n): ").lower()
    lowercase = input("Include Lowercase letters? (y/n): ").lower()
    numbers = input("Include Numbers? (y/n): ").lower()
    symbols = input("Include Symbols? (y/n): ").lower()

    characters = ""
    selected_types = 0

    if uppercase == "y":
        characters += string.ascii_uppercase
        selected_types += 1

    if lowercase == "y":
        characters += string.ascii_lowercase
        selected_types += 1

    if numbers == "y":
        characters += string.digits
        selected_types += 1

    if symbols == "y":
        characters += string.punctuation
        selected_types += 1

    # Validate character selection
    if selected_types < 2:
        print("\nError: Please select at least TWO character types.")
        continue

    # Generate password
    password = ""

    for i in range(length):
        password += random.choice(characters)

    # Display password
    print("\nGenerated Password:")
    print(password)

    # Generate another password?
    again = input("\nGenerate another password? (y/n): ").lower()

    if again != "y":
        print("\nThank you for using the Random Password Generator!")
        break
