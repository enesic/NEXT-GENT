from cryptography.fernet import Fernet
with open("key.txt", "wb") as f:
    f.write(Fernet.generate_key())
