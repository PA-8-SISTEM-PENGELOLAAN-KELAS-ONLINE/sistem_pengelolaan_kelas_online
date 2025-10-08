import csv
from pwinput import pwinput

def login():
    username = input("Input username: ")
    password = pwinput("Input password: ")

    with open("users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["username"] == username and user["password"] == password:
                print(f"Selamat datang, {user['nama_lengkap']}, sebagai {user['role']}!")
                return user
        
        print("Login failed! username atau password salah!")
        return None
            
def menu_dosen():
    print("Menu Dosen")

def menu_mhs():
    print("Menu Mahasiswa")

def mulai():
    auth = login()

    if auth:
        if auth["role"] == "dosen":
            menu_dosen()
        elif auth["role"] == "mahasiswa":
            menu_mhs()
        else:
            print("Role Anda tidak valid!")

mulai()