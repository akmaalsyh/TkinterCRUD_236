import sqlite3  # Mengimpor modul SQLite untuk mengelola database lokal.
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Mengimpor modul Tkinter untuk GUI.

# Fungsi untuk membuat database dan tabel jika belum ada.
def create_database():
    con = sqlite3.connect('nilai_siswa.db')  # Membuat koneksi ke database bernama 'nilai_siswa.db'.
    cursor = con.cursor()  # Membuat cursor untuk menjalankan perintah SQL.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nama_siswa TEXT,  
            biologi INTEGER,  
            fisika INTEGER,  
            inggris INTEGER,  
            prediksi_fakultas TEXT  
        )
    """)  # Membuat tabel jika belum ada.
    con.commit()  # Menyimpan perubahan ke database.
    con.close()  # Menutup koneksi ke database.

# Fungsi untuk mengambil semua data dari tabel 'nilai_siswa'.
def fetch_data():
    con = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database.
    cursor = con.cursor()  # Membuat cursor untuk menjalankan perintah SQL.
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel.
    rows = cursor.fetchall()  # Menyimpan hasil query dalam bentuk list.
    con.close()  # Menutup koneksi ke database.
    return rows  # Mengembalikan data.

# Fungsi untuk menyimpan data baru ke database.
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    con = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database.
    cursor = con.cursor()  # Membuat cursor untuk menjalankan perintah SQL.
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)  # Menambahkan data dengan placeholder untuk parameter.
    """, (nama, biologi, fisika, inggris, prediksi))  # Mengisi parameter dengan nilai dari fungsi.
    con.commit()  # Menyimpan perubahan ke database.
    con.close()  # Menutup koneksi ke database.

# Fungsi untuk memperbarui data di database berdasarkan ID.
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    con = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database.
    cursor = con.cursor()  # Membuat cursor untuk menjalankan perintah SQL.
    cursor.execute("""
        UPDATE nilai_siswa
        SET nama_siswa = ?, 
        biologi = ?,
        fisika = ?,
        inggris = ?,
        prediksi_fakultas = ?
        WHERE id = ?  # Memperbarui data berdasarkan ID.
    """, (nama, biologi, fisika, inggris, prediksi, record_id))
    con.commit()  # Menyimpan perubahan ke database.
    con.close()  # Menutup koneksi ke database.

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai.
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai biologi tertinggi.
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:  # Jika nilai fisika tertinggi.
        return "Teknik"
    elif inggris > biologi and inggris > fisika:  # Jika nilai bahasa Inggris tertinggi.
        return "Bahasa"
    else:
        return "Tidak Diketahui"  # Jika nilai sama.

# Fungsi untuk menambahkan data baru ke database melalui GUI.
def submit():
    try:
        nama = nama_var.get()  # Mengambil input nama dari field GUI.
        biologi = int(biologi_var.get())  # Mengambil dan mengonversi nilai biologi ke integer.
        fisika = int(fisika_var.get())  # Mengambil dan mengonversi nilai fisika ke integer.
        inggris = int(inggris_var.get())  # Mengambil dan mengonversi nilai bahasa Inggris ke integer.

        if not nama:  # Jika nama kosong, maka akan muncul error.
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas.
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan data ke database.

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Pesan sukses.
        clear_inputs()  # Kosongkan input field.
        populate_table()  # Perbarui tabel.
    except ValueError as e:  # Jika input tidak valid, tampilkan pesan error.
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data yang dipilih di database.
def update():
    try:
        if not selected_record_id.get():  # Jika tidak ada data yang dipilih, munculkan error.
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID data yang dipilih.
        nama = nama_var.get()  # Mengambil input nama.
        biologi = int(biologi_var.get())  # Mengambil nilai biologi sebagai integer.
        fisika = int(fisika_var.get())  # Mengambil nilai fisika sebagai integer.
        inggris = int(inggris_var.get())  # Mengambil nilai bahasa Inggris sebagai integer.

        if not nama:  # Jika nama kosong, munculkan error.
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas.
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Perbarui data di database.

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Pesan sukses.
        clear_inputs()  # Kosongkan input field.
        populate_table()  # Perbarui tabel.
    except ValueError as e:  # Jika input tidak valid, munculkan pesan error.
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih dari database.
def delete():
    try:
        if not selected_record_id.get():  # Jika tidak ada data yang dipilih, munculkan error.
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID data yang dipilih.
        con = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database.
        cursor = con.cursor()  # Membuat cursor untuk menjalankan perintah SQL.
        cursor.execute("DELETE FROM nilai_siswa WHERE id = ?", (record_id,))  # Menghapus data berdasarkan ID.
        con.commit()  # Menyimpan perubahan ke database.
        con.close()  # Menutup koneksi ke database.

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Pesan sukses.
        clear_inputs()  # Kosongkan input field.
        populate_table()  # Perbarui tabel.
    except ValueError as e:  # Jika terjadi kesalahan, munculkan pesan error.
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan semua input di GUI.
def clear_inputs():
    nama_var.set("")  # Mengosongkan input nama.
    biologi_var.set("")  # Mengosongkan input nilai biologi.
    fisika_var.set("")  # Mengosongkan input nilai fisika.
    inggris_var.set("")  # Mengosongkan input nilai bahasa Inggris.
    selected_record_id.set("")  # Mengosongkan ID data yang dipilih.

# Fungsi untuk mengisi tabel di GUI dengan data dari database.
def populate_table():
    for row in tree.get_children():  # Menghapus semua data di tabel GUI.
        tree.delete(row)
    for row in fetch_data():  # Mengambil data dari database dan menambahkannya ke tabel GUI.
        tree.insert('', 'end', values=row)  # Menambah baris data ke tabel.

# Fungsi untuk mengisi input field berdasarkan data yang dipilih di tabel.
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mendapatkan item yang dipilih di tabel.
        selected_row = tree.item(selected_item)['values']  # Mengambil nilai dari item yang dipilih.

        selected_record_id.set(selected_row[0])  # Mengisi ID data yang dipilih.
        nama_var.set(selected_row[1])  # Mengisi input nama.
        biologi_var.set(selected_row[2])  # Mengisi input nilai biologi.
        fisika_var.set(selected_row[3])  # Mengisi input nilai fisika.
        inggris_var.set(selected_row[4])  # Mengisi input nilai bahasa Inggris.
    except IndexError:  # Jika tidak ada data yang dipilih, munculkan pesan error.
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database.
create_database()

# Membuat GUI dengan Tkinter.
root = Tk()  # Membuat jendela utama aplikasi.
root.title("Prediksi Fakultas Siswa")  # Memberikan judul pada jendela.

# Variabel untuk menyimpan input dari pengguna.
nama_var = StringVar()  # Variabel untuk menyimpan nama siswa.
biologi_var = StringVar()  # Variabel untuk menyimpan nilai biologi.
fisika_var = StringVar()  # Variabel untuk menyimpan nilai fisika.
inggris_var = StringVar()  # Variabel untuk menyimpan nilai bahasa Inggris.
selected_record_id = StringVar()  # Variabel untuk menyimpan ID data yang dipilih.

# Komponen GUI untuk input data.
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)  # Label untuk nama siswa.
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)  # Field input untuk nama siswa.

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)  # Label untuk nilai biologi.
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)  # Field input untuk nilai biologi.

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)  # Label untuk nilai fisika.
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)  # Field input untuk nilai fisika.

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)  # Label untuk nilai bahasa Inggris.
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)  # Field input untuk nilai bahasa Inggris.

# Tombol untuk mengelola data.
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)  # Tombol untuk menambahkan data.
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)  # Tombol untuk memperbarui data.
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)  # Tombol untuk menghapus data.

# Tabel untuk menampilkan data.
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")  # Kolom tabel.
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel dengan kolom di atas.

# Menyesuaikan header tabel agar rata tengah.
for col in columns:
    tree.heading(col, text=col.capitalize())  # Menambahkan judul kolom.
    tree.column(col, anchor='center')  # Mengatur isi kolom agar rata tengah.

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan tabel di GUI.

# Event untuk mengambil data dari tabel saat diklik.
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel dengan data dari database.
populate_table()

# Menjalankan aplikasi.
root.mainloop()  # Memulai loop utama aplikasi GUI.

