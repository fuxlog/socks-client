def welcome():
    print("\nWelcome to FUXLOG client")
    print("    1. Connect to proxy")
    print("    2. Register")
    print("    0. Exit")


def authenticate_input():
    print("\nAuthentication USERNAME/PASSWORD. Submit 2 fields empty to exit")
    username = input("Username: ")
    password = input("Password: ")
    return username, password


def register_input():
    print("\nRegister USERNAME/PASSWORD. Submit 2 fields empty to exit")
    username = input("Username: ")
    password = input("Password: ")
    return username, password


def user_select() -> int:
    user = input("[USER] > ")
    if user != "1" and user != "2" and user != "0":
        print("Invalid input from user")
        return -1
    return int(user)
