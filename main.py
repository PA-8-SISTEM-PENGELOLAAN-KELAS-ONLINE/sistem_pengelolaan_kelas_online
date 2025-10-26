import csv, random, string
from datetime import datetime
from pwinput import pwinput
from prettytable import PrettyTable, ALL

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
    table.hrules = ALL
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
        elif len(username) > 15:
            print("Username tidak boleh melebihi 15 karakter!")
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

    while True:
        try:
            harga = int(input("Harga: "))
            if harga < 50000 or harga > 5000000:
                print("Harga tidak boleh kurang dari Rp. 50.000 dan lebih dari Rp. 5.000.000")
            else:
                break
        except ValueError:
            print("Harga yang Anda inputkan tidak valid!")

    materi = input("Materi : ")
    kode_kelas = generate_code()

    new = {
        'kode': kode_kelas,
        'judul': judul,
        'teacher': user['nama'],
        'deskripsi': deskripsi,
        'harga': harga,
        'materi': materi
    }
    append_csv("classes.csv", new, ['kode','judul','teacher','deskripsi','harga','materi'])
    print(f"Kelas berhasil dibuat dengan kode: {kode_kelas}")

def update_class(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['teacher'] == current_user['nama']]

    if not my_classes:
        print("Anda belum membuat kelas untuk diubah.")
        return

    show_table("Kelas Anda", ['kode','judul','deskripsi','harga','materi'], my_classes)
    kode = input("Masukkan kode kelas yang ingin diupdate: ").strip()
    kelas = next((c for c in classes if c['kode'] == kode and c['teacher'] == current_user['nama']), None)

    if not kelas:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return

    print("Kosongkan jika tidak ingin mengubah data.")
    judul_baru = input(f"Judul baru ({kelas['judul']}): ").strip() or kelas['judul']
    deskripsi_baru = input(f"Deskripsi baru ({kelas['deskripsi']}): ").strip() or kelas['deskripsi']
    while True:
        try:
            harga_baru = int(input(f"Harga baru ({kelas['harga']}): ").strip() or kelas['harga'])
            if harga_baru < 50000 or harga_baru > 5000000:
                print("Harga tidak boleh kurang dari Rp. 50.000 dan lebih dari Rp. 5.000.000")
            else:
                break
        except ValueError:
            print("Harga yang Anda inputkan tidak valid!")

    materi_baru = input(f"Materi baru ({kelas['materi']}): ").strip() or kelas['materi']

    for c in classes:
        if c['kode'] == kode:
            c['judul'] = judul_baru
            c['deskripsi'] = deskripsi_baru
            c['harga'] = harga_baru
            c['materi'] = materi_baru

    write_csv("classes.csv", classes, ['kode','judul','teacher','deskripsi','harga','materi'])
    print("Kelas berhasil diperbarui.")

def delete_class(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['teacher'] == current_user['nama']]

    if not my_classes:
        print("Anda belum membuat kelas untuk dihapus.")
        return

    show_table("Kelas Anda", ['kode','judul','deskripsi','harga','materi'], my_classes)
    kode = input("Masukkan kode kelas yang ingin dihapus: ").strip()
    kelas = next((c for c in classes if c['kode'] == kode and c['teacher'] == current_user['nama']), None)

    if not kelas:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return

    konfirmasi = input(f"Yakin ingin menghapus kelas '{kelas['judul']}'? (y/n): ").strip().lower()
    if konfirmasi != 'y':
        print("Penghapusan dibatalkan.")
        return

    classes = [c for c in classes if c['kode'] != kode]
    write_csv("classes.csv", classes, ['kode','judul','teacher','deskripsi','harga','materi'])
    print(f"Kelas '{kelas['judul']}' telah dihapus.")

def list_classes(detail=False):
    data = read_csv("classes.csv")
    if not data:
        print("Belum ada kelas.")
        return
    headers = ['kode','judul','teacher','deskripsi','harga'] if not detail else ['kode','judul','teacher','deskripsi','harga','materi']
    show_table("Daftar Kelas", headers, data)

def my_classes(current_user):
    classes = read_csv("classes.csv")
    my_classes = [c for c in classes if c['teacher']==current_user['nama']]
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

    invoice = {
        'id': str(len(read_csv("invoices.csv")) + 1),
        'user_id': user['id'],
        'jenis_transaksi': 'topup',
        'deskripsi': f"Top up saldo Rp{jumlah:,}",
        'jumlah': str(jumlah),
        'waktu': waktu
    }
    append_csv("invoices.csv", invoice, ['id','user_id','jenis_transaksi','deskripsi','jumlah','waktu'])
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
        if u['nama'] == kelas['teacher'] and u['role'] == 'teacher':
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
    print(f"teacher: {kelas['teacher']}")
    print(f"Harga: Rp{harga:,}")
    print(f"Waktu: {purchase['timestamp']}")
    print(f"Sisa saldo: Rp{int(user['saldo']):,}")
    print("==========================")

    invoice = {
    'id': str(len(read_csv("invoices.csv")) + 1),
    'user_id': user['id'],
    'jenis_transaksi': 'pembelian',
    'deskripsi': f"Beli kelas '{kelas['judul']}' dari {kelas['teacher']}",
    'jumlah': f"-{harga}",
    'waktu': purchase['timestamp']
    }
    append_csv("invoices.csv", invoice, ['id','user_id','jenis_transaksi','deskripsi','jumlah','waktu'])

def access_class(user):
    purchases = read_csv("purchases.csv")
    classes = read_csv("classes.csv")
    owned_kodes = {p['class_kode'] for p in purchases if p['user_id']== user['id']}
    owned_classes = [c for c in classes if c['kode'] in owned_kodes]
    show_table("Kelas Dimiliki", ['kode','judul','teacher','deskripsi','materi'], owned_classes)

def lihat_akses_kelas(teacher):
    purchases = read_csv("purchases.csv")
    classes = read_csv("classes.csv")
    users = read_csv("users.csv")

    kelas_saya = [c for c in classes if c['teacher'] == teacher['nama']]
    if not kelas_saya:
        print("Anda belum membuat kelas, jadi belum ada pembeli.")
        return

    kode_kelas_saya = {c['kode'] for c in kelas_saya}

    pembelian_terkait = [p for p in purchases if p['class_kode'] in kode_kelas_saya]
    if not pembelian_terkait:
        print("Belum ada user yang membeli kelas Anda.")
        return

    data_tabel = []
    for p in pembelian_terkait:
        user_data = next((u for u in users if u['id'] == p['user_id']), None)
        kelas_data = next((c for c in classes if c['kode'] == p['class_kode']), None)
        if user_data and kelas_data:
            data_tabel.append({
                'Nama Siswa': user_data['nama'],
                'Username': user_data['username'],
                'Kelas': kelas_data['judul'],
                'Kode': kelas_data['kode'],
                'Tanggal Beli': p['timestamp']
            })

    show_table("Daftar yang Mengakses Kelas Anda", ['Nama Siswa','Username','Kelas','Kode','Tanggal Beli'], data_tabel)

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
            print("6. Lihat yang Punya Akses Kelas")
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
            elif pil == '6': 
                lihat_akses_kelas(user)
            elif pil == '0': 
                break
            else:
                print("Pilihan Anda tidak tersedia!")
        else:
            print("role Anda tidak valid! Terdapat kesalahan fatal dalam program. 💁🏻")
            break

try:
    main_menu()
except KeyboardInterrupt:
    print("\n\nProgram dihentikan!")
except EOFError:
    print("\n\nInput dihentikan, program ditutup.")
except Exception as e:
    print("\n\nTerjadi kesalahan")
finally:
    print("\nProgram Selesai")
