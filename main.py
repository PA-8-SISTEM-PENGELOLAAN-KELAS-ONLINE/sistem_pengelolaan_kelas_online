# class_system.py
import csv
import random
import string
from datetime import datetime
from pwinput import pwinput
from prettytable import PrettyTable

# -----------------------
# Helper CSV utilities
# -----------------------
def ensure_csv_with_header(filename, headers):
    """Buat file dengan header jika belum ada."""
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            # jika bisa dibuka, asumsikan header sudah ada
            pass
    except FileNotFoundError:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

def read_csv(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

def append_csv(filename, row, headers=None):
    # jika file belum ada dan headers diberikan, buat header
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as f:
            if headers:
                writer = csv.DictWriter(f, fieldnames=headers)
            else:
                # ambil header dari file
                with open(filename, mode='r', newline='', encoding='utf-8') as fr:
                    reader = csv.DictReader(fr)
                    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writerow(row)
    except FileNotFoundError:
        # buat file baru dan tulis header jika headers tersedia
        if not headers:
            raise
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerow(row)

def write_csv_all(filename, rows, headers):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def generate_code(n=5):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(n))

# -----------------------
# File names & headers
# -----------------------
USERS_FILE = 'users.csv'
USERS_HDR = ['id','username','password','nama','role','saldo']  # role: student | teacher

CLASSES_FILE = 'classes.csv'
CLASSES_HDR = ['id','kode','judul','dosen','deskripsi','harga','materi_pdf']  # materi_pdf = filename string

PURCHASES_FILE = 'purchases.csv'
PURCHASES_HDR = ['id','user_id','class_id','timestamp']  # akses yang dimiliki user

INVOICES_FILE = 'invoices.csv'
INVOICES_HDR = ['id','user_id','class_id','amount','timestamp']

# pastikan file ada
ensure_csv_with_header(USERS_FILE, USERS_HDR)
ensure_csv_with_header(CLASSES_FILE, CLASSES_HDR)
ensure_csv_with_header(PURCHASES_FILE, PURCHASES_HDR)
ensure_csv_with_header(INVOICES_FILE, INVOICES_HDR)

# -----------------------
# Utility visual
# -----------------------
def show_table(title, headers, rows):
    t = PrettyTable()
    t.field_names = headers
    for r in rows:
        t.add_row([r.get(h,"") for h in headers])
    print("\n" + title)
    print(t)

# -----------------------
# Auth & user management
# -----------------------
def register():
    users = read_csv(USERS_FILE)
    usernames = {u['username'] for u in users}
    print("\n=== REGISTER ===")
    while True:
        username = input("Username: ").strip()
        if not username:
            print("Username tidak boleh kosong.")
            continue
        if username in usernames:
            print("Username sudah dipakai.")
            continue
        break
    password = pwinput("Password: ")
    nama = input("Nama lengkap: ").strip()
    role = ''
    while role not in ('student','teacher'):
        role = input("Role (student / teacher): ").strip().lower()
    user_id = str(len(users)+1)
    # saldo awal 0
    new = {'id': user_id, 'username': username, 'password': password, 'nama': nama, 'role': role, 'saldo': '0'}
    append_csv(USERS_FILE, new, USERS_HDR)
    print(f"Registrasi selesai. Anda terdaftar sebagai {role} dengan saldo 0.")

def login():
    users = read_csv(USERS_FILE)
    by_username = {u['username']: u for u in users}
    print("\n=== LOGIN ===")
    username = input("Username: ").strip()
    password = pwinput("Password: ")
    user = by_username.get(username)
    if user and user['password'] == password:
        print(f"Selamat datang, {user['nama']} ({user['role']})")
        return user
    else:
        print("Login gagal: username atau password salah.")
        return None

# -----------------------
# Teacher actions: create class
# -----------------------
def create_class(current_user):
    print("\n=== BUAT KELAS (Teacher) ===")
    judul = input("Judul kelas: ").strip()
    deskripsi = input("Deskripsi singkat: ").strip()
    while True:
        harga = input("Harga (numeric, misal 10000): ").strip()
        if harga.isdigit():
            break
        print("Masukkan angka untuk harga.")
    materi = input("Nama file materi PDF (misal materi1.pdf). Simpan file terpisah di tempat yang sesuai: ").strip()
    classes = read_csv(CLASSES_FILE)
    kelas_id = str(len(classes)+1)
    kode = generate_code(5)
    new = {
        'id': kelas_id,
        'kode': kode,
        'judul': judul,
        'dosen': current_user['nama'],
        'deskripsi': deskripsi,
        'harga': harga,
        'materi_pdf': materi
    }
    append_csv(CLASSES_FILE, new, CLASSES_HDR)
    print(f"Kelas dibuat dengan kode {kode} dan id {kelas_id}.")

# -----------------------
# Student actions
# -----------------------
def list_classes(show_all_fields=False):
    classes = read_csv(CLASSES_FILE)
    if not classes:
        print("Belum ada kelas tersedia.")
        return
    if show_all_fields:
        headers = CLASSES_HDR
    else:
        headers = ['id','kode','judul','dosen','deskripsi','harga']
    # tampilkan ringkas
    rows = [{h: c.get(h,"") for h in headers} for c in classes]
    show_table("Daftar Kelas", headers, rows)

def tambah_saldo(current_user):
    users = read_csv(USERS_FILE)
    user = next((u for u in users if u['id']==current_user['id']), None)
    if not user:
        print("User tidak ditemukan (internal error).")
        return
    print(f"Saldo saat ini: {user['saldo']}")
    while True:
        nominal = input("Masukkan jumlah top-up (angka): ").strip()
        if nominal.isdigit():
            break
        print("Masukkan angka valid.")
    new_saldo = int(user['saldo']) + int(nominal)
    user['saldo'] = str(new_saldo)
    # tulis ulang file users
    write_csv_all(USERS_FILE, users, USERS_HDR)
    print(f"Top-up berhasil. Saldo baru: {user['saldo']}")

def buy_class(current_user):
    classes = read_csv(CLASSES_FILE)
    if not classes:
        print("Belum ada kelas untuk dibeli.")
        return
    list_classes()
    class_id = input("Masukkan id kelas yang ingin dibeli: ").strip()
    kelas = next((c for c in classes if c['id']==class_id), None)
    if not kelas:
        print("Kelas tidak ditemukan.")
        return
    price = int(kelas['harga'])
    users = read_csv(USERS_FILE)
    user = next((u for u in users if u['id']==current_user['id']), None)
    if not user:
        print("User tidak ditemukan (internal error).")
        return
    if int(user['saldo']) < price:
        print("Saldo tidak cukup. Silakan top-up terlebih dahulu.")
        return
    # cek apakah sudah memiliki akses
    purchases = read_csv(PURCHASES_FILE)
    has = any(p['user_id']==user['id'] and p['class_id']==kelas['id'] for p in purchases)
    if has:
        print("Anda sudah memiliki akses ke kelas ini.")
        return
    # potong saldo
    user['saldo'] = str(int(user['saldo']) - price)
    write_csv_all(USERS_FILE, users, USERS_HDR)
    # catat pembelian (akses)
    purchase_id = str(len(purchases)+1)
    ts = datetime.now().isoformat(sep=' ', timespec='seconds')
    new_purchase = {'id': purchase_id, 'user_id': user['id'], 'class_id': kelas['id'], 'timestamp': ts}
    append_csv(PURCHASES_FILE, new_purchase, PURCHASES_HDR)
    # buat invoice
    invoices = read_csv(INVOICES_FILE)
    invoice_id = str(len(invoices)+1)
    invoice = {'id': invoice_id, 'user_id': user['id'], 'class_id': kelas['id'], 'amount': str(price), 'timestamp': ts}
    append_csv(INVOICES_FILE, invoice, INVOICES_HDR)
    # tampilkan invoice sederhana
    print("\n--- INVOICE ---")
    print(f"Invoice ID : {invoice_id}")
    print(f"Tanggal    : {ts}")
    print(f"Pelanggan  : {user['nama']} (username: {user['username']})")
    print(f"Kelas      : {kelas['judul']} (kode: {kelas['kode']})")
    print(f"Jumlah     : {price}")
    print("----------------")
    print("Pembelian berhasil. Akses kelas sudah diberikan.")

def access_class(current_user):
    # tampilkan kelas yang user punya akses dan detail materi
    purchases = read_csv(PURCHASES_FILE)
    classes = read_csv(CLASSES_FILE)
    user_purchases = [p for p in purchases if p['user_id']==current_user['id']]
    if not user_purchases:
        print("Anda belum memiliki akses ke kelas apapun.")
        return
    # gabungkan
    rows = []
    for p in user_purchases:
        kelas = next((c for c in classes if c['id']==p['class_id']), None)
        if kelas:
            rows.append({
                'id': kelas['id'],
                'kode': kelas['kode'],
                'judul': kelas['judul'],
                'dosen': kelas['dosen'],
                'deskripsi': kelas['deskripsi'],
                'materi_pdf': kelas.get('materi_pdf','(tidak ada)')
            })
    show_table("Kelas yang Anda Akses", ['id','kode','judul','dosen','deskripsi','materi_pdf'], rows)
    # opsi: lihat materi (menampilkan nama file)
    pilihan = input("Masukkan id kelas untuk melihat nama file materi (atau ENTER untuk kembali): ").strip()
    if pilihan:
        sel = next((r for r in rows if r['id']==pilihan), None)
        if sel:
            print(f"Nama file materi untuk kelas '{sel['judul']}': {sel['materi_pdf']}")
            print("Catatan: sistem ini hanya menyimpan nama file. Untuk membuka file, buka file PDF tersebut di luar aplikasi ini.")
        else:
            print("Kelas tidak ditemukan pada daftar akses Anda.")

# -----------------------
# Admin / Teacher: lihat kelas yang dibuatnya
# -----------------------
def my_classes(current_user):
    classes = read_csv(CLASSES_FILE)
    my = [c for c in classes if c['dosen']==current_user['nama']]
    if not my:
        print("Anda belum membuat kelas.")
        return
    show_table("Kelas saya (Teacher)", ['id','kode','judul','deskripsi','harga','materi_pdf'], my)

# -----------------------
# Main menu loop
# -----------------------
def main_menu():
    while True:
        print("\n=== SISTEM PENGELOLAAN KELAS ONLINE (Sederhana) ===")
        print("1. Register")
        print("2. Login")
        print("0. Keluar")
        choice = input("Pilih: ").strip()
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                user_session(user)
        elif choice == '0':
            print("Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid.")

def user_session(user):
    while True:
        print(f"\n--- Menu ({user['role']}) ---")
        if user['role'] == 'student':
            print("1. Lihat daftar kelas")
            print("2. Tambah saldo")
            print("3. Beli kelas")
            print("4. Lihat akses kelas & materi")
            print("0. Logout")
            c = input("Pilih: ").strip()
            if c == '1':
                list_classes()
            elif c == '2':
                tambah_saldo(user)
            elif c == '3':
                buy_class(user)
            elif c == '4':
                access_class(user)
            elif c == '0':
                break
            else:
                print("Pilihan tidak valid.")
        elif user['role'] == 'teacher':
            print("1. Buat kelas")
            print("2. Lihat kelas saya")
            print("3. Lihat semua kelas")
            print("0. Logout")
            c = input("Pilih: ").strip()
            if c == '1':
                create_class(user)
            elif c == '2':
                my_classes(user)
            elif c == '3':
                list_classes(show_all_fields=True)
            elif c == '0':
                break
            else:
                print("Pilihan tidak valid.")
        else:
            print("Role tidak dikenali. Logout.")
            break

main_menu()
