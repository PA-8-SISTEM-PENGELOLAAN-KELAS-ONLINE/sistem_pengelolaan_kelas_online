import csv, os
from pwinput import pwinput
from prettytable import PrettyTable

# BAGIAN UTILITY
def table(title, headers, rows):
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row([row.get(head,"") for head in headers])
    print("\n" + title)
    print(table)

def read_csv(csvname):
    try:
        with open (csvname, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            return data
    
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file: {csvname}")
        return []
    
def write_csv(filename, rows):
    if not rows:
        return

    headers = rows[0].keys()
    with open (filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

# BAGIAN CRUD PROGRAMNYA
def login():
    try:
        username = input("Input username: ")
        password = pwinput("Input password: ")
    except KeyboardInterrupt:
        print("\nAnda keluar dari Login!")
        return None

    with open("users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["username"] == username and user["password"] == password:
                print(f"Selamat datang, {user['nama_lengkap']}, sebagai {user['role']}!\n")
                return user
        
    print("Login failed! username atau password salah!\n")
            
def read_user():
    users = read_csv("users.csv")

    if not users:
        print("Tidak ada data yang tersedia!")
        return

    headers = ["username", "nama_lengkap", "role"]
    table("Daftar Pengguna", headers, users)

def create_user():
    data = read_csv("users.csv")
    username = input("Masukkan Username: ")

    for user in data :
        if user["username"] == username:
            print("Username sudah tersedia, coba lagi!")
            return

    nama_lengkap = input("Masukkan Nama Lengkap: ")
    role = input("Pilih Role (Mahasiswa / Dosen): ")

    if role not in {"mahasiswa", "dosen"}:
        print("Role yang anda masukkan tidak valid!")
        return
    
    password = pwinput("Masukkan Password: ")
    
    id = len(data) + 1 if data else 1 

    data.append({
        "username": username,
        "password": password,
        "role": role,
        "nama_lengkap": nama_lengkap
    })

    write_csv("users.csv", data)
    print("Pengguna berhasil ditambahkan")

def update_user():
    data = read_user("users.csv")

    if not data:
        print("saat ini belum ada pengguna")
        return
    
    username = input("masukkan username yang ingin diubah: ")
    found = False

    for user in data:
        if user["username"] == username:
            found = True
            print(f"Username yang ingin diubah: {username}")

            nama_baru = input("Masukkan nama lengkap baru (kosongkan jika tidak ingin diubah): ")
            password_baru = pwinput("Masukkan password baru (kosongkan jika tidak ingin diubah): ")

            user["nama_lengkap"] = nama_baru
            user["password"] = password_baru
            write_csv("users.csv", data)

            print(f"Data pengguna {username} berhasil diubah!")
            break

    if not found:
        print(f"Username yang Anda inputkan '{username}' tidak ditemukan!")

def delete_user():
    data = read_user("users.csv")

    if not data:
        print("saat ini belum ada pengguna")
        return
    
    username = input("masukkan username yang ingin diubah: ")
    # new_data = [user for user in data if user["username"] != username]
    for user in data:
        if user["username"] == username:
            confirm = input("Apakah Anda yakin ingin menghapus pengguna ini? (y/n) ")

            if confirm.lower() == "y":
                data.remover(user)
                write_csv("users.csv", data)
                print("Pengguna {username} berhasil dihapus!")
            else:
                print("Batal Menghapus.")
            return
    print(f"Username {username} tidak ditemukan")

# BAGIAN MENU DAN MAIN UTAMA
def menu_admin():
    while True:
        print("\n")

        print("=" * 19, "Menu Admin", "=" * 19)
        print("1. Lihat/Search/Sort Pengguna")
        print("2. Tambah Pengguna")
        print("3. Ubah Pengguna")
        print("4. Hapus Pengguna")
        print("5. Lihat/Search/Sort Kelas")
        print("6. Tambah Kelas")
        print("7. Ubah Kelas")
        print("8. Hapus Kelas")
        print("9. Lihat Semua Request")
        print("10. Logout")
        print("0. Exit")
        print("="* 50)
        
        pil_menu = input("Pilih menu diatas: ")
        
        if pil_menu == "1":
            read_user()
        elif pil_menu == "2":
            print("\n")
            print("=" * 16, "Tambah Penggunaa", "=" * 16)
            create_user()
            print("="* 50)
            print("\n")
        elif pil_menu == "3":
            print("test")
        elif pil_menu == "4":
            print("test")
        elif pil_menu == "5":
            print("test")
        elif pil_menu == "6":
            print("test")
        elif pil_menu == "7":
            print("test")
        elif pil_menu == "8":
            print("test")
        elif pil_menu == "9":
            print("test")
        elif pil_menu == "10":
            print("Anda telah logout!")
            break
        elif pil_menu == "0":
            print("Anda telah keluar dari program!")
            exit()
        else:
            print("Anda keluar dari program ini!")
            exit()

        print("\n")
            
def menu_mhs():
    while True:
        print("\n")

        print("=" * 17, "Menu Mahasiswa", "=" * 17)
        print("1. Lihat Semua Kelas")
        print("2. Daftar Kelas")
        print("3. Batalkan Kelas")
        print("4. Lihat Pengajuan Kelas")
        print("5. Logout")
        print("0. Exit")
        print("="* 50)

        pil_menu = input("Pilih menu diatas: ")
        
        if pil_menu == "1":
            print("test")
        if pil_menu == "2":
            print("test")
        elif pil_menu == "3":
            print("test")
        elif pil_menu == "4":
            print("test")
        elif pil_menu == "5":
            print("Anda telah logout!")
            break
        elif pil_menu == "0":
            print("Anda telah keluar dari program!")
            exit()
        else:
            print("Pilih Anda tidak ada!")
            exit()

        print("\n")

def menu_dosen():
    while True:
        print("\n")
        print("=" * 19,"Menu Dosen", "=" * 19)
        print("1. Lihat/Search/Sort Kelas")
        print("2. Tambah Kelas")
        print("3. Ubah Kelas")
        print("4. Hapus Kelas")
        print("5. Lihat Pengajuan")
        print("6. Terima/Tolak Pengajuan")
        print("7. Logout")
        print("0. Exit")
        print("="* 50)

        pil_menu = input("Pilih menu diatas: ")
        
        if pil_menu == "1":
            print("test")
        if pil_menu == "2":
            print("test")
        elif pil_menu == "3":
            print("test")
        elif pil_menu == "4":
            print("test")
        elif pil_menu == "5":
            print("test")
        elif pil_menu == "6":
            print("test")
        elif pil_menu == "7":
            print("Anda telah logout!")
            break
        elif pil_menu == "0":
            print("Anda telah keluar dari program!")
            exit()
        else:
            print("Pilihan Anda tidak ada!")

        print("\n")

def mulai():
    while True:
        auth = login()

        if not auth:
            coba = input("Coba lagi? (y/n): ")
            if coba != "y":
                print("Anda telah keluar dari program!")
                break
            continue

        if auth["role"] == "admin":
            menu_admin()
        elif auth["role"] == "dosen":
            menu_dosen()
        elif auth["role"] == "mahasiswa":
            menu_mhs()
        else:
            print("Role Anda tidak valid!")

mulai()