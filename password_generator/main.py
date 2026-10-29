from generator import generate_password


def ask_yes_no(question: str) -> bool:
    """Ask the user a yes/no question."""

    while True:
        answer = input(question).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")


def main():
    print("=" * 40)
    print("       PYTHON PASSWORD GENERATOR")
    print("=" * 40)

    try:
        length = int(
            input("\nEnter password length: ")
        )

        use_uppercase = ask_yes_no(
            "Include uppercase letters? (y/n): "
        )

        use_lowercase = ask_yes_no(
            "Include lowercase letters? (y/n): "
        )

        use_numbers = ask_yes_no(
            "Include numbers? (y/n): "
        )

        use_symbols = ask_yes_no(
            "Include special characters? (y/n): "
        )

        password = generate_password(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers,
            use_symbols=use_symbols,
        )

        print("\n" + "=" * 40)
        print(f"Generated Password: {password}")
        print("=" * 40)

        print("\nPassword generated successfully!")

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
