import csv, random, string
from datetime import datetime
from pwinput import pwinput
from prettytable import PrettyTable

# === UTILITY DASAR ===
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
            if f.tell() == 0:  # tulis header jika file baru
                writer.writeheader()
            writer.writerow(row)
    except FileNotFoundError:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerow(row)

def generate_code(n=5):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(n))

def show_table(title, headers, rows):
    table = PrettyTable()
    table.field_names = headers
    for r in rows:
        table.add_row([r.get(h, "") for h in headers])
    print("\n" + title)
    print(table)

# === AUTH ===
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
def login():
    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = pwinput("Password: ")
    for u in read_csv("users.csv"):
        if u['username'] == username and u['password'] == password:
            print(f"Selamat datang, {u['nama']} ({u['role']})")
            return u
    print("Login gagal: username atau password salah.")
    return None

def create_class(user):
    print("\n=== BUAT KELAS ===")
    judul = input("Judul kelas: ")
    deskripsi = input("Deskripsi: ")
    harga = input("Harga: ")
    materi = input("Nama file materi PDF: ")
    data = read_csv("classes.csv")
    new = {
        'id': str(len(data) + 1),
        'kode': generate_code(),
        'judul': judul,
        'dosen': user['nama'],
        'deskripsi': deskripsi,
        'harga': harga,
        'materi_pdf': materi
    }
    append_csv("classes.csv", new, ['id','kode','judul','dosen','deskripsi','harga','materi_pdf'])
    print("Kelas berhasil dibuat.")

def update_class(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['dosen'] == current_user['nama']]

    if not my_classes:
        print("Anda belum membuat kelas untuk diubah.")
        return

    show_table("Kelas Anda", ['id','kode','judul','deskripsi','harga','materi_pdf'], my_classes)
    cid = input("Masukkan ID kelas yang ingin diupdate: ").strip()
    kelas = next((c for c in classes if c['id'] == cid and c['dosen'] == current_user['nama']), None)

    if not kelas:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return

    print("Kosongkan jika tidak ingin mengubah data.")
    new_title = input(f"Judul baru ({kelas['judul']}): ").strip() or kelas['judul']
    new_desc = input(f"Deskripsi baru ({kelas['deskripsi']}): ").strip() or kelas['deskripsi']
    new_price = input(f"Harga baru ({kelas['harga']}): ").strip() or kelas['harga']
    new_pdf = input(f"File materi baru ({kelas['materi_pdf']}): ").strip() or kelas['materi_pdf']

    for c in classes:
        if c['id'] == cid:
            c['judul'] = new_title
            c['deskripsi'] = new_desc
            c['harga'] = new_price
            c['materi_pdf'] = new_pdf

    write_csv("classes.csv", classes, ['id','kode','judul','dosen','deskripsi','harga','materi_pdf'])
    print("Kelas berhasil diperbarui.")

def delete_class(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['dosen'] == current_user['nama']]

    if not my_classes:
        print("Anda belum membuat kelas untuk dihapus.")
        return

    show_table("Kelas Anda", ['id','kode','judul','deskripsi','harga','materi_pdf'], my_classes)
    cid = input("Masukkan ID kelas yang ingin dihapus: ").strip()
    kelas = next((c for c in classes if c['id'] == cid and c['dosen'] == current_user['nama']), None)

    if not kelas:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return

    konfirmasi = input(f"Yakin ingin menghapus kelas '{kelas['judul']}'? (y/n): ").strip().lower()
    if konfirmasi != 'y':
        print("Penghapusan dibatalkan.")
        return

    classes = [c for c in classes if c['id'] != cid]
    write_csv("classes.csv", classes, ['id','kode','judul','dosen','deskripsi','harga','materi_pdf'])
    print(f"Kelas '{kelas['judul']}' telah dihapus.")

def list_classes(detail=False):
    data = read_csv("classes.csv")
    if not data:
        print("Belum ada kelas.")
        return
    headers = ['id','kode','judul','dosen','deskripsi','harga'] if not detail else ['id','kode','judul','dosen','deskripsi','harga','materi_pdf']
    show_table("Daftar Kelas", headers, data)

def my_classes(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['dosen']==current_user['nama']]
    if not my_classes:
        print("Anda belum membuat kelas.")
        return
    show_table("Kelas saya (Teacher)", ['id','kode','judul','deskripsi','harga','materi_pdf'], my_classes)

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
    print(f"Top up berhasil! Saldo: Rp{int(user['saldo']):,}")
    return user

def buy_class(user):
    list_classes()
    cid = input("Masukkan id kelas yang ingin dibeli: ").strip()
    classes = read_csv("classes.csv")
    kelas = next((c for c in classes if c['id']==cid), None)
    if not kelas:
        print("Kelas tidak ditemukan.")
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
    write_csv("users.csv", users, ['id','username','password','nama','role','saldo'])

    purchase = {
        'id': str(len(read_csv("purchases.csv")) + 1),
        'user_id': user['id'],
        'class_id': cid,
        'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')
    }
    append_csv("purchases.csv", purchase, ['id','user_id','class_id','timestamp'])
    print("Pembelian berhasil.")

def access_class(user):
    purchases = read_csv("purchases.csv")
    classes = read_csv("classes.csv")
    akses = [p for p in purchases if p['user_id']==user['id']]
    if not akses:
        print("Belum ada kelas yang Anda miliki.")
        return
    data = []
    for a in akses:
        k = next((c for c in classes if c['id']==a['class_id']), None)
        if k: data.append(k)
    show_table("Kelas yang Dimiliki", ['id','kode','judul','dosen','deskripsi','materi_pdf'], data)

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
            elif pil == '0': break
        else:
            print("role Anda tidak valid! Terdapat kesalahan fatal dalam program. 💁🏻")
            break

main_menu()
