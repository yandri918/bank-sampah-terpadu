import streamlit as st
from modules import auth_service
import time

def show():
    # Centralized Clean Layout
    st.markdown("""
    <style>
        .login-container {
            padding: 30px;
            border-radius: 15px;
            background-color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-top: 50px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            flex-grow: 1;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            # Header
            st.image("https://img.icons8.com/color/144/000000/recycle-sign.png", width=80)
            st.markdown("<h2 style='text-align: center; color: #2E7d32; margin-bottom: 0;'>AgriSensa Access</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #666; font-size: 0.9em;'>Bank Sampah Terpadu & Ecosystem</p>", unsafe_allow_html=True)
            st.markdown("---")

            tab_login, tab_register = st.tabs(["🔐 Masuk Akun", "📝 Daftar Baru"])
            
            with tab_login:
                st.caption("Silakan masuk menggunakan email terdaftar.")
                email_login = st.text_input("Email", key="login_email", placeholder="nama@email.com")
                pass_login = st.text_input("Password", type="password", key="login_pass", placeholder="******")
                
                st.markdown("")
                if st.button("🚀 Masuk Sekarang", type="primary", use_container_width=True):
                    if not email_login or not pass_login:
                        st.warning("Mohon isi Email dan Password.")
                    elif auth_service.login(email_login, pass_login):
                        st.success(f"Login Berhasil!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Kombinasi Email atau Password salah.")

            with tab_register:
                st.caption("Buat akun baru untuk mulai menabung sampah.")
                name_reg = st.text_input("Nama Lengkap", key="reg_name", placeholder="Contoh: Budi Santoso")
                email_reg = st.text_input("Email", key="reg_email", placeholder="nama@email.com")
                pass_reg = st.text_input("Password", type="password", key="reg_pass", help="Minimal 6 karakter")
                
                st.markdown("")
                if st.button("✨ Buat Akun", type="secondary", use_container_width=True):
                    success, msg = auth_service.register(email_reg, pass_reg, name_reg)
                    if success:
                        st.success(msg)
                        st.balloons()
                    else:
                        st.error(msg)
            
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("<center>© 2026 AgriSensa System | Secure Access</center>", unsafe_allow_html=True)
