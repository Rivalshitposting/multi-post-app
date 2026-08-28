import streamlit as st
import requests

st.set_page_config(page_title="Multi-Post Manager", page_icon="🐱", layout="centered")

WEBHOOK_URL = "https://hook.eu1.make.com/nqumlktukevpysnjc4q18org9ylcnc23"

# --- HALAMAN UTAMA / LOGIN (DENGAN LOGO KUCING) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🐱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Multi-Post Manager</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Kelola dan publikasikan konten gratis ke seluruh media sosial secara serentak.</p>", unsafe_allow_html=True)
    
    st.write("---")
    col_fb, col_ig = st.columns(2)
    with col_fb:
        if st.button("Masuk dengan Facebook", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user_email = "facebook_user@login"
            st.rerun()
    with col_ig:
        if st.button("Masuk dengan Instagram", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user_email = "instagram_user@login"
            st.rerun()
            
    st.markdown("<p style='text-align: center; color: gray; margin-top: 10px;'>Atau gunakan email aktif</p>", unsafe_allow_html=True)
    
    with st.form("login_email_form"):
        user_email = st.text_input("Alamat Email")
        submit_login = st.form_submit_button("Masuk dengan Email", use_container_width=True)
        
        if submit_login:
            if user_email and "@" in user_email:
                st.session_state.logged_in = True
                st.session_state.user_email = user_email
                st.rerun()
            else:
                st.error("Masukkan alamat email yang valid.")

# --- DASHBOARD UTAMA SETELAH MASUK ---
else:
    st.sidebar.markdown(f"👤 **{st.session_state.user_email}**")
    if st.sidebar.button("Keluar (Logout)", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.title("Buat Postingan Baru")
    st.caption("Pilih jaringan target, masukkan konten, dan publikasikan secara serentak ke semua platform.")

    # 1. Pilih Platform Target
    st.subheader("1. Pilih Jaringan Sosial")
    c1, c2, c3 = st.columns(3)
    with c1:
        ig = st.checkbox("Instagram", value=True)
        fb = st.checkbox("Facebook", value=True)
    with c2:
        tt = st.checkbox("TikTok", value=True)
        threads = st.checkbox("Threads", value=True)
    with c3:
        yt_short = st.checkbox("YT Shorts", value=True)
        yt_long = st.checkbox("YT Video", value=False)

    st.divider()

    # 2. Konten dan Detail
    st.subheader("2. Konten & Detail")
    judul = st.text_input("Judul / Topik Postingan", placeholder="Contoh: Video Terbaru Hari Ini")
    pesan = st.text_area("Tulis Caption...", placeholder="Tulis deskripsi atau teks postingan di sini...")
    
    col_h, col_l = st.columns(2)
    with col_h:
        hashtags = st.text_input("Tagar (#)", placeholder="#fyp #viral")
    with col_l:
        lokasi = st.text_input("Lokasi", placeholder="Nama Kota")

    st.divider()

    # 3. Berkas Lampiran (Foto, Video, Musik)
    st.subheader("3. Berkas Lampiran")
    uploaded_photo = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    uploaded_video = st.file_uploader("Upload Video / Reels / Shorts", type=["mp4", "mov"])
    uploaded_audio = st.file_uploader("Upload Musik / Audio (Opsional)", type=["mp3", "wav"])

    st.divider()

    # 4. Tombol Publikasi
    if st.button("Publikasikan Sekarang", use_container_width=True):
        if not pesan:
            st.error("Caption tidak boleh kosong.")
        else:
            with st.spinner("Mengirim data ke peladen otomatisasi..."):
                files = {}
                if uploaded_photo:
                    files["photo"] = (uploaded_photo.name, uploaded_photo.getvalue(), uploaded_photo.type)
                if uploaded_video:
                    files["video"] = (uploaded_video.name, uploaded_video.getvalue(), uploaded_video.type)
                if uploaded_audio:
                    files["audio"] = (uploaded_audio.name, uploaded_audio.getvalue(), uploaded_audio.type)

                payload = {
                    "email": st.session_state.user_email,
                    "judul": judul,
                    "pesan": pesan,
                    "hashtags": hashtags,
                    "lokasi": lokasi,
                    "target_instagram": ig,
                    "target_facebook": fb,
                    "target_tiktok": tt,
                    "target_threads": threads,
                    "target_youtube_shorts": yt_short,
                    "target_youtube_long": yt_long
                }

                try:
                    res = requests.post(WEBHOOK_URL, data=payload, files=files if files else None)
                    if res.status_code == 200:
                        st.success("Berhasil! Postingan sedang diproses untuk diterbitkan ke semua platform.")
                    else:
                        st.error("Gagal mengirim data ke server.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
