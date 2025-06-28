from cryptography.fernet import Fernet
import os
from datetime import datetime

# Path to store your key and encrypted journal
KEY_FILE = "secret.key"
JOURNAL_FILE = "journal.txt"

# Generate and save encryption key if it doesn't exist
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

# Load the encryption key
def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Encrypt the journal entry
def encrypt_entry(entry, key):
    f = Fernet(key)
    return f.encrypt(entry.encode())

# Decrypt the journal entry
def decrypt_entry(encrypted_entry, key):
    f = Fernet(key)
    return f.decrypt(encrypted_entry).decode()

# Write a new journal entry
def write_entry():
    entry = input("Write your journal entry: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_entry = f"Date:[{timestamp}]--{entry}"

    key = load_key()
    encrypted = encrypt_entry(full_entry, key)

    with open(JOURNAL_FILE, "ab") as f:
        f.write(encrypted + b'\n')
    print("Entry saved and encrypted.")

def delete_entries():
    if not os.path.exists(JOURNAL_FILE):
        print("No entries found.")
        return
    else:
        os.remove(JOURNAL_FILE)
        print("All entries deleted.")

# Read all journal entries
def read_entries():
    key =  load_key()
    if not os.path.exists(JOURNAL_FILE):
        print("No journal entries found.")
        return
    
    with open(JOURNAL_FILE, "rb") as f:
        entries = f.readlines()
    
    print("\n--------Your journal entries--------")
    for i in entries:
        try:
            print(decrypt_entry(i.strip(), key))
        except Exception:
            print("[Entry could not be decrypted]")

# Main program
def main():
    generate_key()
    while True:
        print("\n1. Write entry\n2. Read entries\n3. Delete entries\n4. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            write_entry()
        elif choice == "2":
            read_entries()
        elif choice == "3":
            delete_entries()
        elif choice == "4":
            break
        else:
            print("\nEnvalid option, try again.")

if __name__ == "__main__":
    main()