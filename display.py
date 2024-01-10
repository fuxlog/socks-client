def welcome():
    print("\nWelcome to FUXLOG client")
    print("    1. Authenticate")
    print("    2. Register")
    print("    3. Change password")
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


def change_password_input():
    print("\nChange PASSWORD. Submit 3 fields empty to exit")
    username = input("Username: ")
    password = input("Password: ")
    new_password = input("New Password: ")
    return username, password, new_password


def user_select() -> int:
    user = input("[USER] > ")
    if user != "1" and user != "2" and user != "0":
        print("Invalid input from user")
        return -1
    return int(user)
