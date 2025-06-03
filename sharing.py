import streamlit as st
import os
from pathlib import Path
import base64
import uuid

# Streamlit App Setup
st.set_page_config(
    page_title="📤 ഫയൽ ഷെയർ ചെയ്യൂ",
    page_icon="📤",
    layout="centered",
)

# Title & subtitle
st.title("📤 ഫയൽ ഷെയർ ചെയ്യൂ")
st.subheader("ഫയൽ അപ്‌ലോഡ് ചെയ്യൂ (Maximum 1GB)")

# Create a directory to store uploaded files
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

# File uploader widget
uploaded_file = st.file_uploader("ഒരു ഫയൽ തിരഞ്ഞെടുക്കുക", type=None)

if uploaded_file is not None:
    # Check file size
    uploaded_file.seek(0, os.SEEK_END)
    file_size = uploaded_file.tell()
    uploaded_file.seek(0)

    if file_size > 1_000_000_000:  # 1GB = 1,000,000,000 bytes
        st.error("⚠️ 1GB-ലും കുറഞ്ഞ ഫയലുകൾ മാത്രം അപ്‌ലോഡ് ചെയ്യാവുന്നതാണ്.")
    else:
        # Unique filename to avoid overwrite
        unique_id = str(uuid.uuid4())
        save_path = UPLOAD_DIR / f"{unique_id}_{uploaded_file.name}"

        # Save the file locally
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        # Create download link using base64
        def get_download_link(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            file_name = os.path.basename(file_path)
            return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">📥 ഫയൽ ഡൗൺലോഡ് ചെയ്യുക</a>'

        # Show success message and download link
        st.success("✅ ഫയൽ അപ്‌ലോഡ് വിജയകരം!")
        st.markdown("ഫയൽ ഷെയർ ചെയ്യാനുള്ള ലിങ്ക്:")
        st.markdown(get_download_link(save_path), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🧪 ഈ സേവനം പരീക്ഷണാടിസ്ഥാനത്തിലാണ്. കൂടുതൽ മെച്ചപ്പെടുത്തലുകൾ വരാനുണ്ട്.")
