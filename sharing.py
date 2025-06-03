import streamlit as st
import random
import string
import os
import json

UPLOAD_DIR = "C:\Users\USER\Desktop\farhan\upload file""
DATA_FILE = "data.json"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

st.title("📁 ഫയൽ ഷെയറിങ് ആപ്പ്")

data = load_data()

uploaded_file = st.file_uploader("ഫയൽ തിരഞ്ഞെടുക്കുക (Max 1GB)", type=None)

if uploaded_file is not None:
    max_size = 1024 * 1024 * 1024  # 1GB
    if uploaded_file.size > max_size:
        st.error("⚠️ 1GB-നേക്കാൾ വലുതായ ഫയൽ അപ്‌ലോഡ് ചെയ്യാനാകില്ല.")
    else:
        save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        verification_code = generate_verification_code()
        data[verification_code] = uploaded_file.name
        save_data(data)
        st.success(f"✅ '{uploaded_file.name}' വിജയകരമായി അപ്‌ലോഡ് ചെയ്തു.")
        st.info(f"🔐 Verification Code: `{verification_code}`")

st.markdown("---")
st.header("ഫയൽ ഡൗൺലോഡ് ചെയ്യുക")

user_code = st.text_input("Verification Code നൽകുക", type="password")

if st.button("ഡൗൺലോഡ് ചെയ്യാൻ പരിശോധന നടത്തുക"):
    if user_code == "":
        st.error("⚠️ Verification Code നൽകുക.")
    elif user_code in data:
        filename = data[user_code]
        filepath = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                bytes_data = f.read()
            st.download_button(
                label=f"📥 '{filename}' ഡൗൺലോഡ് ചെയ്യാൻ ക്ലിക്കുചെയ്യുക",
                data=bytes_data,
                file_name=filename,
                mime="application/octet-stream"
            )
        else:
            st.error("⚠️ ഫയൽ കണ്ടെത്താനായില്ല. ദയവായി വീണ്ടും അപ്‌ലോഡ് ചെയ്യുക.")
    else:
        st.error("❌ Verification Code തെറ്റാണ്.")
