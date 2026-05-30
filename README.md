# 🧪 Ankim-Card & Calc

> Asisten Pintar Hafalan Reaksi & Perhitungan Larutan Kimia Analitik

Web app interaktif berbasis **Streamlit** yang membantu mahasiswa kimia menghafal reaksi dan melakukan perhitungan larutan secara cepat dan mudah.

---

## ✨ Fitur Utama

### 🃏 Flashcard Interaktif
- **3 Kategori**: Analisis Jenis (Anjen), Gravimetri, Titrimetri/Volumetri
- **Animasi flip kartu** yang halus
- **Mode Acak (Shuffle)** agar tidak hafal urutan
- **Sistem skor** Ingat / Lupa setiap sesi
- **Sesi Ulang** — ulangi hanya kartu yang salah
- Progress bar kartu berjalan

### 🧮 Kalkulator Kimia
- **Pengenceran Larutan** (C₁V₁ = C₂V₂)
- **Molaritas** dari massa dan berat molekul
- **Normalitas** dari massa dan berat ekuivalen
- **Konversi Satuan** (ppm, mg/L, %, g/L, mol/L)

---

## 🚀 Cara Menjalankan

### Lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Deploy ke Streamlit Cloud
1. Push repo ini ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Pilih repo → set `app.py` sebagai main file
4. Klik **Deploy**!

---

## 📁 Struktur File

```
ankim_card/
├── app.py                    # Aplikasi utama Streamlit
├── requirements.txt          # Dependensi Python
├── README.md                 # Dokumentasi ini
├── .streamlit/
│   └── config.toml           # Konfigurasi tema warna
└── data/
    └── flashcards.json       # Database soal flashcard
```

---

## 🎨 Tampilan

- Tema **Hijau & Krem** bernuansa laboratorium alami
- Font **Playfair Display** (judul) + **Lato** (teks)
- Responsif di desktop & mobile

---

## 🛠️ Teknologi

| Stack | Keterangan |
|---|---|
| Python 3.10+ | Bahasa utama |
| Streamlit | Framework web app |
| HTML/CSS Custom | Animasi flip kartu & tema |
| JSON | Database flashcard |

---

## 📖 Cara Menambah Soal

Buka `data/flashcards.json` dan tambahkan objek baru ke array `cards` di kategori yang sesuai:

```json
{
  "id": 99,
  "front": "Pertanyaan kamu di sini...",
  "back": "Jawaban lengkap di sini..."
}
```

---

*Dibuat untuk Tugas Akhir Project — Kimia Analitik*
