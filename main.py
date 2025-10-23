import csv, random, string
from datetime import datetime
from pwinput import pwinput
from prettytable import PrettyTable

# BAGIAN UTILITY
def read_csv(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def write_csv(filename, rows, headers):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def append_csv(filename, row, headers):
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(row)
    except FileNotFoundError:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerow(row)

def generate_code(n=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

def show_table(title, headers, rows):
    table = PrettyTable()
    table.field_names = headers
    for r in rows:
        table.add_row([r.get(h, "") for h in headers])
    print("\n" + title)
    print(table)

# BAGIAN AUTH
def register():
    users = read_csv("users.csv")
    usernames = {u['username'] for u in users}
    print("\n=== REGISTER ===")

    while True:
        username = input("Username: ").strip()
        if not username:
            print("Username tidak boleh kosong.")
        elif username in usernames:
            print("Username sudah dipakai.")
        else:
            break

    password = pwinput("Password: ")
    nama = input("Nama lengkap: ")
    role = ""
    while role not in ("student", "teacher"):
        role = input("Role (student / teacher): ").strip().lower()

    new = {
        'id': str(len(users) + 1),
        'username': username,
        'password': password,
        'nama': nama,
        'role': role,
        'saldo': '0'
    }
    append_csv("users.csv", new, ['id','username','password','nama','role','saldo'])
    print(f"Registrasi selesai. Anda terdaftar sebagai {role} dengan saldo 0.")

# BAGIAN CRUD
def create_class(user):
    print("\n=== BUAT KELAS ===")
    judul = input("Judul kelas: ")
    deskripsi = input("Deskripsi: ")
    harga = input("Harga: ")
    materi = input("Materi : ")
    kode_kelas = generate_code()

    new = {
        'kode': kode_kelas,
        'judul': judul,
        'dosen': user['nama'],
        'deskripsi': deskripsi,
        'harga': harga,
        'materi': materi
    }
    append_csv("classes.csv", new, ['kode','judul','dosen','deskripsi','harga','materi'])
    print(f"Kelas berhasil dibuat dengan kode: {kode_kelas}")

def update_class(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['dosen'] == current_user['nama']]

    if not my_classes:
        print("Anda belum membuat kelas untuk diubah.")
        return

    show_table("Kelas Anda", ['kode','judul','deskripsi','harga','materi'], my_classes)
    kode = input("Masukkan kode kelas yang ingin diupdate: ").strip()
    kelas = next((c for c in classes if c['kode'] == kode and c['dosen'] == current_user['nama']), None)

    if not kelas:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return

    print("Kosongkan jika tidak ingin mengubah data.")
    new_title = input(f"Judul baru ({kelas['judul']}): ").strip() or kelas['judul']
    new_desc = input(f"Deskripsi baru ({kelas['deskripsi']}): ").strip() or kelas['deskripsi']
    new_price = input(f"Harga baru ({kelas['harga']}): ").strip() or kelas['harga']
    new_materi = input(f"Materi baru ({kelas['materi']}): ").strip() or kelas['materi']

    for c in classes:
        if c['kode'] == kode:
            c['judul'] = new_title
            c['deskripsi'] = new_desc
            c['harga'] = new_price
            c['materi'] = new_materi

    write_csv("classes.csv", classes, ['kode','judul','dosen','deskripsi','harga','materi'])
    print("Kelas berhasil diperbarui.")

def delete_class(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['dosen'] == current_user['nama']]

    if not my_classes:
        print("Anda belum membuat kelas untuk dihapus.")
        return

    show_table("Kelas Anda", ['kode','judul','deskripsi','harga','materi'], my_classes)
    kode = input("Masukkan kode kelas yang ingin dihapus: ").strip()
    kelas = next((c for c in classes if c['kode'] == kode and c['dosen'] == current_user['nama']), None)

    if not kelas:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return

    konfirmasi = input(f"Yakin ingin menghapus kelas '{kelas['judul']}'? (y/n): ").strip().lower()
    if konfirmasi != 'y':
        print("Penghapusan dibatalkan.")
        return

    classes = [c for c in classes if c['kode'] != kode]
    write_csv("classes.csv", classes, ['kode','judul','dosen','deskripsi','harga','materi'])
    print(f"Kelas '{kelas['judul']}' telah dihapus.")

def list_classes(detail=False):
    data = read_csv("classes.csv")
    if not data:
        print("Belum ada kelas.")
        return
    headers = ['kode','judul','dosen','deskripsi','harga'] if not detail else ['kode','judul','dosen','deskripsi','harga','materi']
    show_table("Daftar Kelas", headers, data)

def my_classes(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['dosen']==current_user['nama']]
    if not my_classes:
        print("Anda belum membuat kelas.")
        return
    show_table("Kelas saya (Teacher)", ['kode','judul','deskripsi','harga','materi'], my_classes)

def tambah_saldo(user):
    users = read_csv("users.csv")
    topup_opsi = {'1':50000,'2':100000,'3':250000,'4':500000,'5':1000000}

    print("\n=== TOP UP ===")
    for k,v in topup_opsi.items():
        print(f"{k}. Rp{v:,}")
    pilihan = input("Pilih nominal (1-5): ").strip()
    if pilihan not in topup_opsi:
        print("Pilihan tidak valid.")
        return user

    jumlah = topup_opsi[pilihan]
    for u in users:
        if u['id'] == user['id']:
            u['saldo'] = str(int(u['saldo']) + jumlah)
            user['saldo'] = u['saldo']
    write_csv("users.csv", users, ['id','username','password','nama','role','saldo'])
    waktu = datetime.now().isoformat(sep=' ', timespec='seconds')
    
    print("\n=== INVOICE TOP-UP ===")
    print(f"Nama Pengguna : {user['nama']}")
    print(f"Jumlah Top-Up : Rp{jumlah:,}")
    print(f"Waktu Transaksi: {waktu}")
    print(f"Saldo Sekarang : Rp{int(user['saldo']):,}")
    print("=======================")
    return user

def buy_class(user):
    list_classes()
    kode = input("Masukkan kode kelas yang ingin dibeli: ").strip()
    classes = read_csv("classes.csv")
    kelas = next((c for c in classes if c['kode'] == kode), None)
    if not kelas:
        print("Kelas tidak ditemukan.")
        return

    purchases = read_csv("purchases.csv")
    sudah_beli = any(p['user_id'] == user['id'] and p['class_kode'] == kode for p in purchases)
    if sudah_beli:
        print("Anda sudah membeli kelas ini sebelumnya.")
        return

    harga = int(kelas['harga'])
    if int(user['saldo']) < harga:
        print("Saldo tidak cukup.")
        return

    user['saldo'] = str(int(user['saldo']) - harga)
    users = read_csv("users.csv")
    for u in users:
        if u['id'] == user['id']:
            u['saldo'] = user['saldo']

    for u in users:
        if u['nama'] == kelas['dosen'] and u['role'] == 'teacher':
            u['saldo'] = str(int(u['saldo']) + harga)
            break

    write_csv("users.csv", users, ['id','username','password','nama','role','saldo'])

    purchase = {
        'id': str(len(purchases) + 1),
        'user_id': user['id'],
        'class_kode': kode,
        'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')
    }
    append_csv("purchases.csv", purchase, ['id','user_id','class_kode','timestamp'])

    print("\n=== INVOICE PEMBELIAN ===")
    print(f"Nama: {user['nama']}")
    print(f"Kelas: {kelas['judul']}")
    print(f"Dosen: {kelas['dosen']}")
    print(f"Harga: Rp{harga:,}")
    print(f"Waktu: {purchase['timestamp']}")
    print(f"Sisa saldo: Rp{int(user['saldo']):,}")
    print("==========================")

def access_class(user):
    purchases = read_csv("purchases.csv")
    classes = read_csv("classes.csv")
    owned_kodes = {p['class_kode'] for p in purchases if p['user_id']== user['id']}
    owned_classes = [c for c in classes if c['kode'] in owned_kodes]
    show_table("Kelas Dimiliki", ['kode','judul','dosen','deskripsi','materi'], owned_classes)

# BAGIAN MENU
def main_menu():
    while True:
        print("\n=== SISTEM PENGELOLAAN KELAS ONLINE ===")
        print("1. Register")
        print("2. Login")
        print("0. Keluar")
        pil = input("Pilih: ")
        if pil == '1':
            register()
        elif pil == '2':
            user = login()
            if user:
                session(user)
        elif pil == '0':
            print("Keluar dari sistem.")
            break
        else:
            print("Pilihan tidak valid.")

def login():
    while True:
        print("\n=== LOGIN ===")
        username = input("Username: ").strip()
        password = pwinput("Password: ")

        users = read_csv("users.csv")
        for user in users:
            if user['username'] == username and user['password'] == password:
                print(f"Selamat datang, {user['nama']} ({user['role']})")
                return user

        print("Login gagal: username atau password salah.")
        pilihan = input("Apakah Anda ingin mencoba lagi? (y/n): ").strip().lower()
        if pilihan != 'y':
            print("Kembali ke menu utama...")
            return None

def session(user):
    while True:
        print(f"\n=== MENU {user['role'].upper()} ===")
        if user["role"] == "student":
            print("1. Lihat kelas")
            print("2. Top up saldo")
            print("3. Beli kelas")
            print("4. Lihat akses kelas")
            print("0. Logout")
            pil = input("Pilih menu: ")
            if pil == '1': 
                list_classes()
            elif pil == '2': 
                tambah_saldo(user)
            elif pil == '3': 
                buy_class(user)
            elif pil == '4': 
                access_class(user)
            elif pil == '0': 
                break
            else:
                print("Pilihan Anda tidak tersedia!")

        elif user["role"] == "teacher":
            print("1. Lihat semua kelas")
            print("2. Lihat kelas saya")
            print("3. Buat kelas")
            print("4. Perbarui kelas")
            print("5. Hapus kelas")
            print("0. Logout")
            pil = input("Pilih menu: ")
            if pil == '1': 
                list_classes(True)
            elif pil == '2': 
                my_classes(user)
            elif pil == '3': 
                create_class(user)
            elif pil == '4': 
                update_class(user)
            elif pil == '5': 
                delete_class(user)
            elif pil == '0': 
                break
            else:
                print("Pilihan Anda tidak tersedia!")
        else:
            print("role Anda tidak valid! Terdapat kesalahan fatal dalam program. 💁🏻")
            break

main_menu()
