import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import math

# Atur tampilan halaman
st.set_page_config(page_title="Aplikasi Industri Keju", layout="wide")

# ---------------------
# Sidebar dokumentasi
# ---------------------
st.sidebar.title("📘 Dokumentasi Aplikasi")
st.sidebar.markdown("""
Aplikasi ini digunakan untuk analisis matematika industri keju, terdiri dari:
1. Optimasi Produksi (Linear Programming)
2. Model Persediaan (EOQ)
3. Model Antrian (M/M/1)
4. Model Matematika Lainnya (Prediksi Permintaan)
""")

# Pilih menu
menu = st.sidebar.radio("Pilih Menu:", [
    "Optimasi Produksi",
    "Model Persediaan (EOQ)",
    "Model Antrian (M/M/1)",
    "Model Industri Lainnya"
])

# =============================
# MENU 1: Optimasi Produksi
# =============================
if menu == "Optimasi Produksi":
    st.title("1. Optimasi Produksi (Linear Programming)")

    # Fungsi tujuan: Maksimalkan 40x1 + 30x2
    # Kendala:
    # 2x1 + x2 <= 100 (bahan baku)
    # x1 + 2x2 <= 80  (jam kerja)

    c = [-40, -30]  # tanda minus karena linprog meminimalkan
    A = [[2, 1], [1, 2]]
    b = [100, 80]
    bounds = [(0, None), (0, None)]  # x1 dan x2 >= 0

    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds)

    if result.success:
        x1, x2 = result.x
        st.success(f"Produksi Optimal: Keju A = {x1:.2f}, Keju B = {x2:.2f}")
        st.info(f"Keuntungan Maksimum: Rp {abs(result.fun):,.0f}")
    
        # Visualisasi area solusi
        x = np.linspace(0, 60, 400)
        y1 = (100 - 2*x)
        y2 = (80 - x) / 2

        fig, ax = plt.subplots()
        ax.plot(x, y1, label='Batas Bahan Baku')
        ax.plot(x, y2, label='Batas Waktu Kerja')
        ax.fill_between(x, 0, np.minimum(y1, y2), where=(y1 > 0) & (y2 > 0),
                        color='lightblue', alpha=0.5)
        ax.set_xlabel("Keju A")
        ax.set_ylabel("Keju B")
        ax.legend()
        ax.set_title("Wilayah Solusi")
        st.pyplot(fig)

# =============================
# MENU 2: Model Persediaan (EOQ)
# =============================
elif menu == "Model Persediaan (EOQ)":
    st.title("2. Model Persediaan EOQ")

    # Input variabel EOQ
    D = st.number_input("Permintaan Tahunan (kg)", value=12000)
    S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", value=50000)
    H = st.number_input("Biaya Penyimpanan per Unit/Tahun (Rp)", value=2000)

    # Rumus EOQ
    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"EOQ = {EOQ:.2f} kg/pesanan")

        # Grafik Total Cost vs Q
        Q = np.linspace(100, 2 * EOQ, 100)
        TC = (D / Q) * S + (Q / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q, TC, label='Total Biaya')
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
        ax.set_title("Biaya Total vs Jumlah Pemesanan")
        ax.set_xlabel("Jumlah Pesan (Q)")
        ax.set_ylabel("Biaya Total")
        ax.legend()
        st.pyplot(fig)

# =============================
# MENU 3: Model Antrian (M/M/1)
# =============================
elif menu == "Model Antrian (M/M/1)":
    st.title("3. Model Antrian M/M/1")

    # Input variabel antrian
    lambd = st.number_input("Tingkat Kedatangan λ (org/jam)", value=8.0)
    mu = st.number_input("Tingkat Pelayanan μ (org/jam)", value=10.0)

    # Hitung parameter antrian
    if mu > lambd and lambd > 0:
        rho = lambd / mu
        L = rho / (1 - rho)          # jumlah pelanggan dalam sistem
        W = 1 / (mu - lambd)         # waktu dalam sistem

        st.markdown(f"**Utilisasi (ρ):** {rho:.2f}")
        st.markdown(f"**Jumlah Pelanggan dalam Sistem (L):** {L:.2f}")
        st.markdown(f"**Waktu Rata-rata (W):** {W:.2f} jam")

        # Grafik: ρ vs L
        p = np.linspace(0.01, 0.99, 100)
        L_vals = p / (1 - p)

        fig, ax = plt.subplots()
        ax.plot(p, L_vals)
        ax.axvline(rho, color='red', linestyle='--', label=f"ρ = {rho:.2f}")
        ax.set_title("Utilisasi vs Pelanggan")
        ax.set_xlabel("Utilisasi (ρ)")
        ax.set_ylabel("Jumlah dalam Sistem (L)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Sistem tidak stabil (λ ≥ μ)")

# =============================
# MENU 4: Model Industri Lainnya
# =============================
elif menu == "Model Industri Lainnya":
    st.title("4. Prediksi Permintaan Musiman")

    # Model musiman sederhana menggunakan fungsi sinus
    bulan = np.arange(1, 13)
    permintaan = 200 + 50 * np.sin(2 * np.pi * bulan / 12)  # musiman

    st.line_chart(permintaan)
    st.markdown("**Model ini menggambarkan fluktuasi musiman permintaan keju per bulan.**")
