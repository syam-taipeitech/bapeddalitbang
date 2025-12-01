import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Poktan Pacitan", layout="wide")

# ===========================
# LOAD DATA
# ===========================
@st.cache_data
def load_data():
    df = pd.read_csv("poktan_clean.csv")
    df["tipe"] = df["nama_poktan"].apply(
        lambda x: "KWT" if "kwt" in str(x).lower() else "Poktan"
    )
    return df

df = load_data()


# ===========================
# SIDEBAR MENU
# ===========================
menu = st.sidebar.selectbox(
    "Pilih Menu Visualisasi",
    [
        "Dashboard Utama",
        "Poktan per Kecamatan",
        "Poktan per Desa",
        "Top Desa Teraktif",
        "KWT vs Poktan",
        "Tabel Data"
    ]
)

st.sidebar.info("Dashboard Kelembagaan Pertanian — Sabda Tani 2025")
st.sidebar.write("Data dari poktan_clean.csv")


# ===========================
# HALAMAN – DASHBOARD UTAMA
# ===========================
if menu == "Dashboard Utama":
    st.title("📊 Dashboard Kelembagaan Poktan Kabupaten Pacitan")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Kecamatan", df["kecamatan"].nunique())
    col2.metric("Total Desa", df["desa"].nunique())
    col3.metric("Total Poktan", df.shape[0])
    col4.metric("Total KWT", df[df["tipe"]=="KWT"].shape[0])

    per_kec = df.groupby("kecamatan").size().reset_index(name="jumlah_poktan")
    fig = px.bar(per_kec, x="kecamatan", y="jumlah_poktan",
                 title="Jumlah Poktan per Kecamatan",
                 color="jumlah_poktan", text="jumlah_poktan")
    st.plotly_chart(fig, use_container_width=True)


# ===========================
# HALAMAN – PER KECAMATAN
# ===========================
elif menu == "Poktan per Kecamatan":
    st.title("📍 Poktan per Kecamatan")

    per_kec = df.groupby("kecamatan").size().reset_index(name="jumlah_poktan")
    fig = px.bar(per_kec, x="kecamatan", y="jumlah_poktan",
                 color="jumlah_poktan", text="jumlah_poktan")
    st.plotly_chart(fig, use_container_width=True)


# ================================
# HALAMAN - PER DESA
# ================================
elif menu == "Poktan per Desa":
    st.title("🏘️ Poktan per Desa")

    # dictionary desa per kecamatan
    desa_per_kecamatan = {
        "Arjosari": [
            "Desa Arjosari","Desa Borang","Desa Gayuhan","Desa Gegeran",
            "Desa Gembong","Desa Gunungsari","Desa Jatimalang","Desa Jetis Kidul",
            "Desa Karanggede","Desa Karangrejo","Desa Kedungbendo","Desa Mangunharjo",
            "Desa Milati","Desa Pagutan","Desa Sedayu","Desa Temon","Desa Tremas"
        ],
        "Bandar": [
            "Desa Bandar","Desa Bangunsari","Desa Jeruk","Desa Kedung",
            "Desa Ngunut","Desa Petungsinarang","Desa Tumpuk","Desa Watupatok"
        ],
        "Donorojo": [
            "Desa Cemeng","Desa Donorojo","Desa Gedompol","Desa Gendran",
            "Desa Kalak","Desa Klepu Donorojo","Desa Sawahan","Desa Sekar",
            "Desa Sendang","Desa Sukodono","Desa Widoro (Donorojo)"
        ],
        "Kebonagung": [
            "Desa Bangkir","Desa Gembuk","Desa Karanganyar","Desa Karangnongko",
            "Desa Katipugal","Desa Kebonagung","Desa Ketepung","Desa Ketro (Kebonagung)",
            "Desa Klaten","Desa Marten (Kebonagung)","Desa Plumbungan","Desa Punjung",
            "Desa Purwosari","Desa Sanggrahan","Desa Sidomulyo (Kebonagung)",
            "Desa Wonogondo","Desa Worawari"
        ],
        "Nawangan": [
            "Desa Badran","Desa Bogoharjo","Desa Cokrokembang","Desa Hadiluwih",
            "Desa Hadiwarno","Desa Joho","Desa Ngepeh","Desa Nogosari",
            "Desa Ojier","Desa Penggur","Desa Sogatan","Desa Tokawi",
            "Desa Tugurejo","Desa Widoro"
        ],
        "Ngadirojo": [
            "Desa Bodag","Desa Cangkring","Desa Hadiluwih","Desa Hadiwarno",
            "Desa Ngadirojo","Desa Nogosari","Desa Pagerijo","Desa Sidomulyo",
            "Desa Tanjungpuro","Desa Widoro","Desa Wonorejo Kulon","Desa Wonodadi Wetan",
            "Desa Wonokarto","Desa Wonosobo"
        ],
        "Pacitan": [
            "Desa Arjowinangun","Kelurahan Baleharjo","Desa Bangunsari (Pacitan)",
            "Desa Boloasri","Desa Kayen","Desa Kembang","Desa Mentoro",
            "Desa Nanggungan","Kelurahan Pacitan","Kelurahan Ploso",
            "Kelurahan Pucangsawit","Desa Sambah","Desa Sedeng","Desa Semanten",
            "Kelurahan Sidoharjo","Desa Sirnoboyo","Desa Sukoharjo",
            "Desa Sumberharjo","Desa Tambakrejo","Desa Tanjungsari",
            "Desa Widoro (Pacitan)"
        ],
        "Pringkuku": [
            "Desa Candi","Desa Dadapan","Desa Dorosan","Desa Glinggang",
            "Desa Jlubang","Desa Ndagrejan","Desa Pelem","Desa Poko",
            "Desa Pringkuku","Desa Sobo","Desa Sugihwaras","Desa Tamanasri",
            "Desa Watukarung"
        ],
        "Punung": [
            "Desa Bomo","Desa Gondosari","Desa Kebonsari","Desa Kendal",
            "Desa Mantren (Punung)","Desa Mendolo Lor","Desa Piton",
            "Desa Ploso (Punung)","Desa Sooka","Desa Tintar","Desa Wareng"
        ],
        "Sudimoro": [
            "Desa Gunung Rejo","Desa Karang Mulyo","Desa Ketanggung","Desa Klepu (Sudimoro)",
            "Desa Pager Kidul","Desa Sembowo","Desa Sudimoro","Desa Sukorejo",
            "Desa Sumber Rejo"
        ],
        "Tegalombo": [
            "Desa Gedangan","Desa Gemaharjo","Desa Kasihan","Desa Kebondalem",
            "Desa Kemuning","Desa Ngroeo","Desa Ploso (Tegalombo)",
            "Desa Pucanganom","Desa Tahunan Baru","Desa Tahunan"
        ],
        "Tulakan": [
            "Desa Bubakan","Desa Bungur","Desa Gasang","Desa Jatigunung",
            "Desa Jetak","Desa Kali Kringin","Desa Ketep Harjo","Desa Kluwih",
            "Desa Losari","Desa Ngile","Desa Ngumbul","Desa Pagdi",
            "Desa Tulakan","Desa Wonocati","Desa Wonosidi"
        ]
    }

    # PILIH KECAMATAN
    kec_select = st.selectbox("Pilih Kecamatan", list(desa_per_kecamatan.keys()))

    # PILIH DESA BERDASARKAN KECAMATAN
    desa_select = st.selectbox("Pilih Desa", desa_per_kecamatan[kec_select])

    # FILTER DATA POKTAN
    filtered = df[(df["kecamatan"] == kec_select) & (df["desa"] == desa_select)]

    # TAMPILKAN DATA
    st.subheader(f"Daftar Poktan – {desa_select}")
    st.dataframe(filtered)

    # GRAFIK
    fig = px.bar(filtered, x="nama_poktan", y="nama_poktan",
                 title=f"Poktan di Desa {desa_select}",
                 labels={"nama_poktan": "Daftar Poktan"})
    st.plotly_chart(fig, use_container_width=True)



# ===========================
# HALAMAN – TOP DESA
# ===========================
elif menu == "Top Desa Teraktif":
    st.title("🔥 Top Desa dengan Poktan Terbanyak")

    per_desa = df.groupby(["kecamatan", "desa"]).size().reset_index(name="jumlah_poktan")
    top_desa = per_desa.sort_values("jumlah_poktan", ascending=False).head(15)

    fig = px.bar(top_desa, x="jumlah_poktan", y="desa",
                 orientation="h",
                 color="jumlah_poktan",
                 title="Top 15 Desa Paling Aktif")
    st.plotly_chart(fig, use_container_width=True)


# ===========================
# HALAMAN – KWT VS POKTAN
# ===========================
elif menu == "KWT vs Poktan":
    st.title("🌾 Komposisi KWT vs Poktan")

    counts = df["tipe"].value_counts().reset_index()
    counts.columns = ["tipe", "jumlah"]
    fig = px.pie(counts, names="tipe", values="jumlah")
    st.plotly_chart(fig, use_container_width=True)


# ===========================
# HALAMAN – TABEL DATA
# ===========================
elif menu == "Tabel Data":
    st.title("📋 Data Lengkap Kelompok Tani")
    st.dataframe(df)
