import streamlit as st
import random
import string
import io
import base64
import os

# Create a persistent folder to store files
SAVE_DIR = "uploaded_files"
os.makedirs(SAVE_DIR, exist_ok=True)

# Verification code generator
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Create base64 download link
def get_file_download_link(filepath, filename):
    try:
        with open(filepath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'data:application/octet-stream;base64,{b64}'
    except MemoryError:
        return None

# HTML/CSS Template
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>File Sharing App</title>
    <link href=\"https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css\" rel=\"stylesheet\">
    <style>
        body {
            background: linear-gradient(135deg, #1e3a8a, #7c3aed);
        }
        .container {
            background: linear-gradient(135deg, #1e1b4b, #2e1065);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .btn-gradient {
            background: linear-gradient(90deg, #06b6d4, #ec4899);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn-gradient:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body class=\"font-sans min-h-screen flex items-center justify-center\">
    <div class=\"container mx-auto p-6\">
        <div class=\"shadow-lg rounded-lg p-8 max-w-lg mx-auto\">
            <h1 class=\"text-4xl font-bold text-center text-cyan-300 mb-6 animate-pulse\">IPCS File Sharing</h1>
            <div id=\"content\" class=\"space-y-6\">
            </div>
        </div>
    </div>
</body>
</html>
"""

# Render HTML
st.markdown(html_content, unsafe_allow_html=True)

# Upload section
st.markdown("<h2 class='text-xl font-semibold text-white mb-4'>\ud83d\udcc4 \u0d2b\u0d2f\u0d32\u0d4d \u0d05\u0d2a\u0d4d\u0d32\u0d4b\u0d1f\u0d4d \u0d1a\u0d46\u0d2f\u0d4d\u0d2f\u0d42 (Maximum 1GB)</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("ഒരു ഫയൽ തിരഞ്ഞെടുക്കുക", type=None)

if uploaded_file is not None:
    if uploaded_file.size > 1024 * 1024 * 1024:
        st.error("❌ ഫയൽ വലുപ്പം 1GB-നെ കവിയുന്നു. ചെറിയ ഫയൽ തിരഞ്ഞെടുക്കൂ.")
    else:
        verification_code = generate_verification_code()
        save_path = os.path.join(SAVE_DIR, f"{verification_code}_{uploaded_file.name}")
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"✅ ഫയൽ അപ്‌ലോഡ് വിജയകരം: {uploaded_file.name}")
        st.info(f"🔐 Verification Code: `{verification_code}`\n\nഈ കോഡ് ഷെയർ ചെയ്യൂ.")

# Download section
st.markdown("<h2 class='text-xl font-semibold text-white mb-4 mt-8'>\ud83d\udcc5 \u0d2b\u0d2f\u0d32\u0d4d \u0d21\u0d57\u0d23\u0d4d\u0d32\u0d4b\u0d21\u0d4d \u0d1a\u0d46\u0d2f\u0d4d\u0d2f\u0d42</h2>", unsafe_allow_html=True)
user_code = st.text_input("Verification Code നൽകൂ", max_chars=6)

if st.button("✅ ഡൗൺലോഡ് ചെയ്യൂ"):
    matched_files = [f for f in os.listdir(SAVE_DIR) if f.startswith(user_code)]
    if matched_files:
        file_path = os.path.join(SAVE_DIR, matched_files[0])
        filename = matched_files[0].split("_", 1)[1]
        link = get_file_download_link(file_path, filename)
        if link:
            st.markdown(
                f"""
                <div class='bg-blue-200 p-4 rounded-md'>
                    ✅ Verification വിജയിച്ചു! <br>
                    <a href='{link}' download='{filename}' class='text-blue-600 underline btn-gradient inline-block px-4 py-2 rounded-md text-white'>👉 {filename} ഡൗൺലോഡ് ചെയ്യാൻ ഇവിടെ ക്ലിക്ക് ചെയ്യൂ</a>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("❌ പിശക്: ഫയൽ ഡൗൺലോഡ് ലിങ്ക് സൃഷ്ടിക്കാൻ സാധിച്ചില്ല.")
    else:
        st.error("❌ പിശക്: Verification Code തെറ്റാണ് അല്ലെങ്കിൽ ഫയൽ ഇല്ല.")

# Footer
st.markdown(
    """
    <div class='mt-8 text-center text-gray-300'>
        <p>⚙️ Powered by Streamlit + Tailwind CSS | 1GB വരെയുള്ള ഫയലുകൾ പിന്തുണയ്ക്കുന്നു.</p>
    </div>
    """,
    unsafe_allow_html=True
)
