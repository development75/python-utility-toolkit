import secrets
import string


def generate_password(
    length: int,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_numbers: bool = True,
    use_symbols: bool = True,
) -> str:
    """Generate a secure password based on selected character types."""

    if length < 1:
        raise ValueError("Password length must be at least 1.")

    characters = ""
    required_characters = []

    if use_uppercase:
        characters += string.ascii_uppercase
        required_characters.append(
            secrets.choice(string.ascii_uppercase)
        )

    if use_lowercase:
        characters += string.ascii_lowercase
        required_characters.append(
            secrets.choice(string.ascii_lowercase)
        )

    if use_numbers:
        characters += string.digits
        required_characters.append(
            secrets.choice(string.digits)
        )

    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{};:,.?"
        characters += symbols
        required_characters.append(
            secrets.choice(symbols)
        )

    if not characters:
        raise ValueError(
            "Select at least one character type."
        )

    if length < len(required_characters):
        raise ValueError(
            "Password length is too short for the selected "
            "character types."
        )

    remaining_length = length - len(required_characters)

    password_characters = required_characters + [
        secrets.choice(characters)
        for _ in range(remaining_length)
    ]

    # Securely shuffle the characters.
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)