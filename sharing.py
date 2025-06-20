import streamlit as st
import random
import string
import os
import json

# Raw string to avoid escape character problems
UPLOAD_DIR = r"C:\Users\USER\Desktop\farhan\upload file"
DATA_FILE = r"C:\Users\USER\Desktop\farhan\upload file\data.json"

# Create uploads folder if it doesn't exist
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

st.title("📁 File Sharing App")

data = load_data()

uploaded_file = st.file_uploader("Choose a file (Max 5GB)", type=None)

if uploaded_file is not None:
    max_size = 5 * 1024 * 1024 * 1024  # 5GB
    if uploaded_file.size > max_size:
        st.error("⚠️ Cannot upload files larger than 5GB.")
    else:
        save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        verification_code = generate_verification_code()
        data[verification_code] = uploaded_file.name
        save_data(data)
        st.success(f"✅ '{uploaded_file.name}' successfully uploaded.")
        st.info(f"🔐 Verification Code: `{verification_code}`")

st.markdown("---")
st.header("Download File")

user_code = st.text_input("Enter Verification Code", type="password")

if st.button("Verify to Download"):
    if user_code == "":
        st.error("⚠️ Please enter a Verification Code.")
    elif user_code in data:
        filename = data[user_code]
        filepath = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                bytes_data = f.read()
            st.download_button(
                label=f"📥 Click to download '{filename}'",
                data=bytes_data,
                file_name=filename,
                mime="application/octet-stream"
            )
        else:
            st.error("⚠️ File not found. Please upload again.")
    else:
        st.error("❌ Invalid Verification Code.")
