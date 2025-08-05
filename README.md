# Data Storytelling Automator

## Deskripsi
Data Storytelling Automator adalah sebuah skrip yang dirancang untuk menyederhanakan proses analisis data dan pembuatan laporan. Dengan menerima dataset mentah dalam format CSV, skrip ini secara otomatis akan mengidentifikasi pola menarik seperti korelasi dan anomali. Hasil analisis ini kemudian akan disajikan dalam bentuk laporan naratif yang komprehensif, dilengkapi dengan visualisasi data yang relevan.

## Fitur Utama
- **Input File CSV**: Menerima dan memproses dataset dari file CSV.
- **Analisis Korelasi**: Mengidentifikasi secara otomatis hubungan antar variabel numerik dalam dataset.
- **Deteksi Anomali**: Menemukan titik data yang tidak biasa (outlier) dalam kolom numerik.
- **Pembuatan Laporan Otomatis**: Menghasilkan laporan naratif dalam format Markdown yang merangkum temuan analisis.
- **Visualisasi Data Otomatis**: Membuat dan menyertakan visualisasi seperti heatmap korelasi, scatter plot, dan box plot untuk memperjelas wawasan.

## Teknologi yang Digunakan
- **Bahasa:** Python
- **Kerangka Kerja/Library:** Pandas, NumPy, Matplotlib, Seaborn

## Instalasi
1.  Pastikan Anda memiliki Python 3.6 atau lebih tinggi terinstal.
2.  Clone repositori ini atau unduh file-filenya.
3.  Buka terminal atau command prompt dan navigasikan ke direktori proyek.
4.  Instal dependensi yang diperlukan dengan menjalankan perintah berikut:
    ```bash
    pip install -r requirements.txt
    ```

## Penggunaan
1.  Tempatkan file CSV Anda di dalam direktori `data` (atau di mana saja, tetapi pastikan Anda tahu path-nya).
2.  Jalankan skrip dari terminal dengan memberikan path ke file CSV Anda sebagai argumen.

    Contoh penggunaan dengan data sampel yang disediakan:
    ```bash
    python main.py data/sample_data.csv
    ```
3.  Setelah eksekusi selesai, laporan analisis (`report.md`) dan file gambar visualisasi akan tersedia di dalam direktori `reports`.

## Kontribusi
Kami menyambut baik kontribusi! Jika Anda ingin berkontribusi pada proyek ini, silakan ikuti langkah-langkah berikut:
1.  Fork repositori ini.
2.  Buat branch baru untuk fitur Anda (`git checkout -b fitur/NamaFitur`).
3.  Commit perubahan Anda (`git commit -m 'Menambahkan fitur baru'`).
4.  Push ke branch Anda (`git push origin fitur/NamaFitur`).
5.  Buka Pull Request.

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT.
