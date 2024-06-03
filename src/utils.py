import os
import random
import string


def generate_password(length=16):
    if length < 16:
        raise ValueError("Password length should be at least 16 characters.")
    letters = string.ascii_letters
    digits = string.digits
    special_chars = "!@#$%&*()"
    all_chars = letters + digits + special_chars
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special_chars)
    ]
    password += [random.choice(all_chars) for _ in range(length - 3)]
    random.shuffle(password)
    return ''.join(password)


def get_file_size(file_path):
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            return file_size
        else:
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
