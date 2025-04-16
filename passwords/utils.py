import random
import string

def generate_password(length, use_uppercase=True, use_numbers=True, use_special_chars=True, use_similar=False):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special_chars:
        characters += "!@#$%^&*()_+-=[]{};:,.<>/?"
    if not use_similar:
        for ch in 'il1Lo0O':
            characters = characters.replace(ch, '')
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password