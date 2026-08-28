import streamlit as st
import requests

st.set_page_config(page_title="Multi-Post Pro Dashboard", page_icon="", layout="centered")

WEBHOOK_URL = "https://hook.eu1.make.com/nqumlktukevpysnjc4q18org9ylcnc23"

# --- SISTEM LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title(" Login Dashboard Multi-Post")
    user_email = st.text_input("Alamat Email")
    user_pass = st.text_input("Kata Sandi", type="password")
    
    if st.button("Masuk ke Aplikasi"):
        if user_email and user_pass:
            st.session_state.logged_in = True
            st.session_state.user_email = user_email
            st.rerun()
        else:
            st.error("Email dan Kata Sandi wajib diisi!")

# --- DASHBOARD UTAMA MULTI-POST ---
else:
    st.sidebar.write(f" Akun Terhubung: **{st.session_state.user_email}**")
    if st.sidebar.button("Keluar (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    st.title(" Pengirim Konten Multi-Platform")
    st.caption("Posting sekali ke seluruh media sosial lengkap dengan Tagar, Lokasi & Audio.")

    # 1. PILIH SOSIAL MEDIA TARGET
    st.subheader("1. Pilih Media Sosial Tujuan")
    col1, col2 = st.columns(2)
    with col1:
        target_ig = st.checkbox(" Instagram (Feed / Reels)", value=True)
        target_fb = st.checkbox(" Facebook Page / Profile", value=True)
        target_threads = st.checkbox(" Threads", value=True)
    with col2:
        target_tiktok = st.checkbox(" TikTok", value=True)
        target_yt_short = st.checkbox(" YouTube Shorts", value=True)
        target_yt_long = st.checkbox(" YouTube Video Panjang", value=False)
        target_yt_community = st.checkbox(" YouTube Post Komunitas (Foto)", value=False)

    st.divider()

    # 2. DETAIL POSTINGAN
    st.subheader("2. Detail Konten")
    judul = st.text_input("Judul Postingan / Video (Khusus YouTube/FB)", placeholder="Contoh: Tutorial Terbaru")
    pesan = st.text_area("Deskripsi / Caption Utama", placeholder="Tulis caption postinganmu di sini...")
    
    col_tag, col_loc = st.columns(2)
    with col_tag:
        hashtags = st.text_input(" Tagar / Hashtags", placeholder="#viral #fyp #content")
    with col_loc:
        lokasi = st.text_input(" Lokasi", placeholder="Contoh: Jakarta, Indonesia")

    st.divider()

    # 3. UNGGAH MEDIA & AUDIO DARI GALERI HP
    st.subheader("3. Unggah Media & Audio (Bebas Hak Cipta)")
    uploaded_photo = st.file_uploader(" Upload Foto (JPG, PNG)", type=["jpg", "jpeg", "png"])
    uploaded_short = st.file_uploader(" Upload Video Pendek / Reels / TikTok (MP4)", type=["mp4", "mov"])
    uploaded_long_video = st.file_uploader(" Upload Video Panjang YouTube (MP4, MKV)", type=["mp4", "mkv", "avi"])
    
    # Fitur Musik Bebas Hak Cipta
    uploaded_audio = st.file_uploader("🎵 Upload Musik Backsound / MP3 (Gunakan No-Copyright Audio)", type=["mp3", "wav", "m4a"])
    st.caption(" Catatan Hak Cipta: Gunakan file MP3 bebas hak cipta agar video/foto tidak di-banned atau diklaim hak cipta oleh platform.")

    st.divider()

    # 4. TOMBOL PUBLISH SEKALIGUS
    if st.button(" Publish ke Semua Sosial Media Target"):
        if not pesan:
            st.error("Pesan / Caption tidak boleh kosong!")
        else:
            with st.spinner("Memproses media dan audio ke Make.com..."):
                files = {}
                if uploaded_photo:
                    files["photo"] = (uploaded_photo.name, uploaded_photo.getvalue(), uploaded_photo.type)
                if uploaded_short:
                    files["video_short"] = (uploaded_short.name, uploaded_short.getvalue(), uploaded_short.type)
                if uploaded_long_video:
                    files["video_long"] = (uploaded_long_video.name, uploaded_long_video.getvalue(), uploaded_long_video.type)
                if uploaded_audio:
                    files["audio"] = (uploaded_audio.name, uploaded_audio.getvalue(), uploaded_audio.type)

                payload = {
                    "email": st.session_state.user_email,
                    "judul": judul,
                    "pesan": pesan,
                    "hashtags": hashtags,
                    "lokasi": lokasi,
                    "target_instagram": target_ig,
                    "target_facebook": target_fb,
                    "target_threads": target_threads,
                    "target_tiktok": target_tiktok,
                    "target_youtube_shorts": target_yt_short,
                    "target_youtube_long": target_yt_long,
                    "target_youtube_community": target_yt_community
                }

                try:
                    res = requests.post(WEBHOOK_URL, data=payload, files=files if files else None)
                    if res.status_code == 200:
                        st.success(" Berhasil! Postingan beserta caption, tagar, lokasi, dan audio sedang diproses.")
                    else:
                        st.error(" Gagal terhubung ke Make.com.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
