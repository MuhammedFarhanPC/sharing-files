import streamlit as st
import random
import string
import io
import base64

# ✅ Verification code generation
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# ✅ Convert file to download link (base64)
def get_file_download_link(file_buffer, filename):
    try:
        b64 = base64.b64encode(file_buffer.getvalue()).decode()
        return f'data:application/octet-stream;base64,{b64}'
    except MemoryError:
        return None

# ✅ Initialize session state
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = None
if 'file_buffer' not in st.session_state:
    st.session_state.file_buffer = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# ✅ Custom UI (TailwindCSS + Gradient Background)
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1e3a8a, #7c3aed);
        }
        .container {
            background: linear-gradient(135deg, #1e1b4b, #2e1065);
            padding: 30px;
            border-radius: 16px;
            color: white;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            0% {opacity: 0; transform: translateY(20px);}
            100% {opacity: 1; transform: translateY(0);}
        }
        .btn {
            background: linear-gradient(to right, #06b6d4, #ec4899);
            padding: 10px 20px;
            border-radius: 8px;
            color: white;
            text-decoration: none;
        }
        .btn:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='container'>", unsafe_allow_html=True)

# ✅ Title
st.markdown("<h1 style='text-align:center;'>📁 IPCS File Sharing App</h1>", unsafe_allow_html=True)

# ✅ Upload Section
st.markdown("<h3>ഫയൽ അപ്‌ലോഡ് ചെയ്യുക (Maximum 1GB):</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("ഫയൽ തിരഞ്ഞെടുക്കുക", type=None)

if uploaded_file is not None:
    max_size = 1024 * 1024 * 1024  # 1GB

    if uploaded_file.size > max_size:
        st.error("⚠️ 1GB-നേക്കാൾ വലുതായ ഫയൽ അപ്‌ലോഡ് ചെയ്യാനാകില്ല.")
    else:
        try:
            file_buffer = io.BytesIO(uploaded_file.read())
            st.session_state.file_buffer = file_buffer
            st.session_state.filename = uploaded_file.name

            if st.session_state.verification_code is None:
                st.session_state.verification_code = generate_verification_code()

            st.success(f"✅ '{uploaded_file.name}' ഫയൽ വിജയകരമായി അപ്‌ലോഡ് ചെയ്തു.")
            st.info(f"🔐 Verification Code: `{st.session_state.verification_code}` (ഇത് പങ്കുവെച്ചാലേ ഡൗൺലോഡ് ചെയ്യാൻ കഴിയൂ)")

        except MemoryError:
            st.error("🚫 മെമ്മറി പോരായ്മ കാരണം ഫയൽ പ്രോസസ് ചെയ്യാൻ കഴിയുന്നില്ല. ചെറിയ ഫയൽ ശ്രമിക്കുക.")

# ✅ Download Section
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3>ഫയൽ ഡൗൺലോഡ് ചെയ്യുക:</h3>", unsafe_allow_html=True)
user_code = st.text_input("Verification Code നൽകുക", type="password")

if st.button("✅ സ്ഥിരീകരിക്കുക & ഡൗൺലോഡ് ചെയ്യുക"):
    if st.session_state.verification_code is None or st.session_state.file_buffer is None:
        st.error("⚠️ ഫയൽ അപ്‌ലോഡ് ചെയ്തിട്ടില്ല.")
    elif user_code == st.session_state.verification_code:
        download_link = get_file_download_link(st.session_state.file_buffer, st.session_state.filename)
        if download_link:
            st.markdown(
                f"<a href='{download_link}' download='{st.session_state.filename}' class='btn'>📥 '{st.session_state.filename}' ഡൗൺലോഡ് ചെയ്യാൻ ക്ലിക്കുചെയ്യുക</a>",
                unsafe_allow_html=True
            )
        else:
            st.error("🚫 ഡൗൺലോഡ് ലിങ്ക് സൃഷ്ടിക്കാനാകില്ല. ചെറിയ ഫയൽ ശ്രമിക്കുക.")
    else:
        st.error("❌ Verification Code തെറ്റാണ്.")

# ✅ Footer
st.markdown("""
    <br><br>
    <p style='text-align:center; color:lightgray;'>© 2025 IPCS File Share App | Built with 💙 Streamlit & Tailwind CSS</p>
</div>
""", unsafe_allow_html=True)
