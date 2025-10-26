# Sistem Pengelolaan Kelas Online
PROJECT AKHIR: DASAR PEMROGRAMAN SEMESTER 1.
Kelompok 8 Anggota:
Zefri Al Rizqullah	2509116084
Muhammad Aqia Yudha Yulian Putra	2509116105
Rifaa Zainul Arifin	2509116092

👨‍🎓 Fitur untuk Student:
<br>
1. Registrasi dan Login - Sistem autentikasi user
<br>
2. Top Up Saldo - Menambah saldo dengan berbagai nominal
<br>
3. Beli Kelas - Membeli kelas online yang tersedia
<br>
4. Lihat Kelas - Melihat daftar kelas yang tersedia
<br>
5. Akses Kelas - Mengakses kelas yang telah dibeli

👨‍🏫 Fitur untuk Teacher:
<br>
1. Kelola Kelas - Membuat, mengedit, dan menghapus kelas
<br>
2. Lihat Pembeli - Melihat daftar student yang membeli kelas
<br>
3. Pendapatan - Menerima pembayaran dari penjualan kelas
<br>
4. Konten Materi - Mengelola materi pembelajaran

🛠 Teknologi
<br>
1. Python - Bahasa pemrograman utama
<br>
2. CSV - Penyimpanan data (users, classes, purchases)
<br>
3. PrettyTable - Menampilkan data dalam format tabel
<br>
4. pwinput - Input password yang tersembunyi
<br>
5. datetime - Penanganan timestamp transaksi

<h2>Flowchart Menu Utama</h2>
<img width="1331" height="962" alt="1 drawio" src="https://github.com/user-attachments/assets/1d1834f1-d428-4e41-88d9-56b0ceb0a8a6" />
<br>
<br>

<h2>Flowchart Menu Teacher</h2>
<img width="1681" height="1201" alt="2 drawio" src="https://github.com/user-attachments/assets/647c84bf-fc03-4ca8-a209-35b66c6a79ce" />
<br>
<br>

<h2>Flowchart Menu User</h2>
<img width="1681" height="1201" alt="3 drawio" src="https://github.com/user-attachments/assets/52ba6533-0d8b-405b-9936-fa9833874e54" />
<br>
<br>

<h3>Menu Utama</h3>
<img width="287" height="89" alt="image" src="https://github.com/user-attachments/assets/c557b76c-b855-4d54-b98f-9d27aefd83bc" />
<br>
Saat program dijalankan, sistem akan menampilkan menu utama dengan tiga pilihan, yaitu:
1)	Register
2)	Login
3)	Keluar
Pengguna dapat memilih 1 untuk melakukan registrasi akun baru, 2 untuk login, atau 0 untuk keluar dari sistem.
<br>
<br>

<h3>Registrasi</h3>
<img width="322" height="73" alt="image" src="https://github.com/user-attachments/assets/b5dd2a39-d160-4174-9dd7-3ae83f6c02ae" />
<br>
Jika pengguna memilih opsi Register, sistem akan meminta input berupa:
1)	Username
2)	Password
3)	Nama lengkap
4)	Role (student / teacher)
Setelah pengguna mengisi data dengan benar, sistem menyimpannya dalam file users.csv dan memberikan saldo awal sebesar 0. Proses ini menjamin setiap pengguna memiliki identitas unik sebelum menggunakan sistem
<br>
<br>

<h3>Login</h3>
<img width="322" height="73" alt="image" src="https://github.com/user-attachments/assets/c55db739-4e33-41cc-8e69-38f67e48de56" />
<br>
Jika pengguna memilih opsi Register, sistem akan meminta input berupa:
1)	Username
2)	Password
3)	Nama lengkap
4)	Role (student / teacher)
Setelah pengguna mengisi data dengan benar, sistem menyimpannya dalam file users.csv dan memberikan saldo awal sebesar 0. Proses ini menjamin setiap pengguna memiliki identitas unik sebelum menggunakan sistem.
<br>
<br>

<h3>Menu User</h3>
<img width="176" height="129" alt="image" src="https://github.com/user-attachments/assets/839e8529-c0e1-4903-88b9-cb5a42e8c163" />
<br>
Bagi pengguna dengan peran student, sistem menampilkan pilihan sebagai berikut:
1)	Lihat daftar kelas
2)	Top up saldo
3)	Beli kelas
4)	Lihat akses kelas
5)	Logout
<br>
<br>

<h3>Menu Lihat Daftar Kelas</h3>
<img width="313" height="98" alt="image" src="https://github.com/user-attachments/assets/e5503682-04d0-46fc-ac02-094d84468748" />
<br>
Menampilkan seluruh kelas yang tersedia di classes.csv dalam bentuk tabel rapi menggunakan modul PrettyTable
<br>
<br>

<h3>Menu Top Up Saldo</h3>
<img width="225" height="167" alt="image" src="https://github.com/user-attachments/assets/3b30f798-23bd-418c-98f2-3a434cd69bde" />
<br>
Pengguna dapat menambah saldo dengan nominal tertentu (Rp50.000, Rp100.000, Rp250.000, Rp500.000, dan Rp1.000.000). Setelah top up berhasil, sistem menampilkan invoice transaksi yang memuat nama, jumlah top up, waktu transaksi, dan saldo terkini.
<br>
<br>

<h3>Menu Beli Kelas</h3>
<img width="301" height="183" alt="image" src="https://github.com/user-attachments/assets/cc11f6ab-98d3-4d0c-a4b1-5682f8d1a3c2" />
<br>
Student dapat membeli kelas dengan memasukkan kode kelas yang diinginkan. Sistem akan memverifikasi saldo pengguna dan mencatat transaksi pembelian ke purchases.csv Jika saldo cukup, saldo otomatis berkurang dan teacher yang bersangkutan menerima tambahan saldo sesuai harga kelas.
<br>
<br>

<h3>Menu Lihat Akses Kelas</h3>
<img width="348" height="93" alt="image" src="https://github.com/user-attachments/assets/e67f6984-f971-44fb-b4a3-92b08197b163" />
<br>
Menampilkan daftar kelas yang telah dibeli oleh student, termasuk nama teacher, deskripsi kelas
<br>
<br>

<h3>Menu Teacher</h3>
<img width="236" height="154" alt="image" src="https://github.com/user-attachments/assets/946554ff-9e25-4c5c-83a5-ac6650f206a0" />
<br>
Untuk pengguna dengan peran teacher, sistem menampilkan menu berbeda, yaitu:
1)	Lihat semua kelas
2)	Lihat kelas saya
3)	Buat kelas
4)	Perbarui kelas
5)	Hapus kelas
6)	Lihat yang Punya Akses Kelas ini
7)	Logout
<br>
<br>

<h3>Menu Lihat Semua Kelas</h3>
<img width="313" height="98" alt="image" src="https://github.com/user-attachments/assets/14d092ec-3325-4709-af4c-5708175b6553" />
<br>
Menampilkan semua kelas beserta detail seperti kode, judul, deskripsi, harga, dan nama teacher (mirip dengan dengan menu student).
<br>
<br>

<h3>Menu Lihat Kelas Saya</h3>
<img width="314" height="61" alt="image" src="https://github.com/user-attachments/assets/6f1496d0-a94c-4388-85e6-6ac3a634cd7f" />
<br>
Menampilkan hanya kelas yang dibuat oleh teacher tersebut.
<br>
<br>

<h3>Menu Lihat Buat Kelas</h3>
<img width="274" height="107" alt="image" src="https://github.com/user-attachments/assets/5e163b24-f3e3-4afd-9c07-19d4c771c472" />
<br>
Teacher dapat membuat kelas baru dengan mengisi form berisi judul, deskripsi, harga, dan materi. Sistem akan menghasilkan kode kelas unik menggunakan fungsi generate_code() yang terdiri dari kombinasi huruf kapital dan angka acak.
<br>
<br>

<h3>Menu Lihat Perbarui Kelas</h3>
<img width="315" height="163" alt="image" src="https://github.com/user-attachments/assets/78d6cc1d-738b-4503-84eb-dffd94e00402" />
<br>
Teacher dapat memperbarui data kelas berdasarkan kode kelas yang mereka miliki. Program akan menampilkan data lama dan memberi kesempatan untuk mengubah sebagian atau seluruhnya.
<br>
<br>

<h3>Menu Lihat yang Punya Akses Kelas</h3>
<img width="347" height="65" alt="image" src="https://github.com/user-attachments/assets/e2d3c294-2867-4047-a44b-f3ed5cac4694" />
<br>
Teacher dapat melihat data user yang memiliki akses kelas ia.
<br>
<br>

<h3>Menu Lihat Hapus Kelas</h3>
<img width="324" height="89" alt="image" src="https://github.com/user-attachments/assets/3bc7af13-6ef6-47e9-bc11-97b926b38acf" />
<br>
Teacher dapat menghapus kelas yang sudah dibuat dengan memasukkan kode kelas dan melakukan konfirmasi penghapusan.
<br>
<br>

<h3>Menu Logout</h3>
<img width="283" height="139" alt="image" src="https://github.com/user-attachments/assets/13492f91-cd74-40db-bc19-4eabca5bc63e" />
<br>
Dengan demikian, alur program ini mencerminkan bagaimana sistem bekerja secara terstruktur dan terintegrasi. Mulai dari registrasi, login, pengelolaan data, hingga transaksi digital sederhana seluruh proses dilakukan secara otomatis menggunakan bahasa Python dan modul PrettyTable untuk menampilkan hasil keluaran dengan format tabel yang mudah dibaca di terminal.

<br>
<br>
