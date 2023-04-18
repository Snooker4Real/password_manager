from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, "rb") as f:
            self.key = f.read()

    def create_password_file(self, path, initial_passwords=None):
        self.password_file = path
        if initial_passwords is not None:
            for key, value in initial_passwords.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]


def main():
    password = {
        "email": "123456",
        "facebook": "myfacebookpassword",
        "twitter": "mytwitterpassword",
        "youtube": "myyoutubepassword",
        "instagram": "myinstagrampassword"
    }

    pm = PasswordManager()

    print("""What do you want to do?
    (1) Create a new key 🔑
    (2) Load an existing key 🔒
    (3) Create a new password file 🗃
    (4) Load an existing password file 🔒
    (5) Add a new password 🤫
    (6) Get a password 🛡️
    (q) Exit
    """)

    done = False

    while not done:
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter the path to save the key: ")
            pm.create_key(path)
            print("🔑 Key created successfully! ✅")
        elif choice == "2":
            path = input("Enter the path to load the key: ")
            pm.load_key(path)
            print("🔒 Key loaded successfully! ✅")
        elif choice == "3":
            path = input("Enter the path to save the password file: ")
            pm.create_password_file(path, password)
            print("🗃 Password file created successfully! ✅")
        elif choice == "4":
            path = input("Enter the path to load the password file: ")
            pm.load_password_file(path)
            print("️🔒 Password file loaded successfully! ✅")
        elif choice == "5":
            site = input("Enter the site name: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
            print("🤫 Password added successfully! ✅")
        elif choice == "6":
            site = input("What site do you want: ")
            print(f"The password for {site} is {pm.get_password(site)} 🛡️")
        elif choice == "q":
            done = True
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
