import streamlit as st
import requests

st.set_page_config(page_title="Multi-Post Sosial Media", page_icon="📲", layout="centered")

st.title("📲 Aplikasi Multi-Post Pribadi")
st.subheader("Kirim konten ke semua media sosialmu sekaligus secara gratis!")

st.sidebar.header("🔑 Otorisasi Pribadi")
user_email = st.sidebar.text_input("Masukkan Email Kamu:")

with st.form("multi_post_form"):
    content = st.text_area("Tulis pesan / deskripsi konten:", height=150, placeholder="Tulis postinganmu di sini...")
    media_url = st.text_input("Link Foto/Video (Opsional):", placeholder="https://link-gambar-kamu.com/foto.jpg")
    
    st.markdown("### Pilih Platform Tujuan:")
    col1, col2 = st.columns(2)
    
    with col1:
        post_fb = st.checkbox("Facebook Page", value=True)
        post_ig = st.checkbox("Instagram", value=True)
        post_tiktok = st.checkbox("TikTok", value=True)
        
    with col2:
        post_yt = st.checkbox("YouTube Shorts", value=False)
        post_pin = st.checkbox("Pinterest", value=False)
        post_threads = st.checkbox("Threads", value=False)
        
    submitted = st.form_submit_button("🚀 Publish Postingan")

if submitted:
    if not user_email:
        st.error("Silakan masukkan email kamu di menu samping (sidebar) terlebih dahulu!")
    elif not content.strip():
        st.error("Isi konten tidak boleh kosong!")
    else:
        WEBHOOK_URL = "https://hook.eu1.make.com/YOUR_WEBHOOK_URL_HERE"
        
        payload = {
            "email_pengirim": user_email,
            "pesan": content,
            "media": media_url,
            "targets": {
                "facebook": post_fb,
                "instagram": post_ig,
                "tiktok": post_tiktok,
                "youtube": post_yt,
                "pinterest": post_pin,
                "threads": post_threads
            }
        }
        
        with st.spinner("Mengirim ke semua platform..."):
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("✅ Postingan berhasil dikirim!")
                else:
                    st.warning("⚠️ Berhasil diproses oleh aplikasi web.")
            except Exception as e:
                st.error(f"Gagal menghubungkan ke server webhook: {e}")
