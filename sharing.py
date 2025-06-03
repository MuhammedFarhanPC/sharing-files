import streamlit as st
import random
import string
import os

UPLOAD_DIR = "uploads"

# Uploads folder ഉണ്ടാക്കൂ, ഇല്ലെങ്കിൽ
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Verification code generate ചെയ്യുന്നത്
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Session state variables
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = None
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = None

st.title("📁 IPCS File Sharing App")

uploaded_file = st.file_uploader("ഫയൽ തിരഞ്ഞെടുക്കുക (Max 1GB)", type=None)

if uploaded_file is not None:
    max_size = 1024 * 1024 * 1024  # 1GB
    if uploaded_file.size > max_size:
        st.error("⚠️ 1GB-നേക്കാൾ വലുതായ ഫയൽ അപ്‌ലോഡ് ചെയ്യാനാകില്ല.")
    else:
        # Save file to disk
        save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Update session state
        st.session_state.uploaded_filename = uploaded_file.name
        if st.session_state.verification_code is None:
            st.session_state.verification_code = generate_verification_code()

        st.success(f"✅ '{uploaded_file.name}' ഫയൽ വിജയകരമായി അപ്‌ലോഡ് ചെയ്തു.")
        st.info(f"🔐 Verification Code: `{st.session_state.verification_code}`")

st.markdown("---")
st.header("ഫയൽ ഡൗൺലോഡ് ചെയ്യുക")

user_code = st.text_input("Verification Code നൽകുക", type="password")

if st.button("✅ സ്ഥിരീകരിക്കുക & ഡൗൺലോഡ് ചെയ്യുക"):
    if st.session_state.uploaded_filename is None:
        st.error("⚠️ ഫയൽ അപ്‌ലോഡ് ചെയ്തിട്ടില്ല.")
    elif user_code == st.session_state.verification_code:
        filepath = os.path.join(UPLOAD_DIR, st.session_state.uploaded_filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                bytes_data = f.read()
            st.download_button(
                label=f"📥 '{st.session_state.uploaded_filename}' ഡൗൺലോഡ് ചെയ്യാൻ ക്ലിക്കുചെയ്യുക",
                data=bytes_data,
                file_name=st.session_state.uploaded_filename,
                mime="application/octet-stream"
            )
        else:
            st.error("⚠️ ഫയൽ കണ്ടെത്താനായില്ല. ദയവായി ഫയൽ വീണ്ടും അപ്‌ലോഡ് ചെയ്യുക.")
    else:
        st.error("❌ Verification Code തെറ്റാണ്.")
