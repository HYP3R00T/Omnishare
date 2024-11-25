from keypress import get_key


def confirm(prompt) -> bool:
    print(f"{prompt} [y/N]\n")
    pressed_key = get_key()
    if pressed_key in ["y", "Y"]:
        return True
    return False
