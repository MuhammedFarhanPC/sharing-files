import streamlit as st
import random
import string
import io
import base64

# Verification code generator
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Create base64 download link
def get_file_download_link(file_buffer, filename):
    try:
        b64 = base64.b64encode(file_buffer.getvalue()).decode()
        return f'data:application/octet-stream;base64,{b64}'
    except MemoryError:
        return None

# Session states
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = None
if 'file_buffer' not in st.session_state:
    st.session_state.file_buffer = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# HTML/CSS Template
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Sharing App</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
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
<body class="font-sans min-h-screen flex items-center justify-center">
    <div class="container mx-auto p-6">
        <div class="shadow-lg rounded-lg p-8 max-w-lg mx-auto">
            <h1 class="text-4xl font-bold text-center text-cyan-300 mb-6 animate-pulse">IPCS File Sharing</h1>
            <div id="content" class="space-y-6">
            </div>
        </div>
    </div>
</body>
</html>
"""

# Render HTML
st.markdown(html_content, unsafe_allow_html=True)

# Upload section
st.markdown("<h2 class='text-xl font-semibold text-white mb-4'>📤 ഫയൽ അപ്‌ലോഡ് ചെയ്യൂ (Maximum 1GB)</h2>", unsafe_allow_html=True)
st.markdown("<p class='text-gray-300 mb-4'>1GB-ലും കുറഞ്ഞ ഫയലുകൾ മാത്രം അപ്‌ലോഡ് ചെയ്യാവുന്നതാണ്. Verification code ഉപയോഗിച്ച് അത് ഷെയർ ചെയ്യാം.</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("ഒരു ഫയൽ തിരഞ്ഞെടുക്കുക", type=None)

if uploaded_file is not None:
    max_size = 1024 * 1024 * 1024
    if uploaded_file.size > max_size:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800'>❌ പിശക്: ഫയൽ വലുപ്പം 1GB-നെ കവിയുന്നു. ചെറിയ ഫയൽ അപ്‌ലോഡ് ചെയ്യൂ.</div>",
            unsafe_allow_html=True
        )
    else:
        try:
            file_buffer = io.BytesIO(uploaded_file.read())
            st.session_state.file_buffer = file_buffer
            st.session_state.filename = uploaded_file.name

            if st.session_state.verification_code is None:
                st.session_state.verification_code = generate_verification_code()

            st.markdown(
                f"""
                <div class='bg-green-200 p-4 rounded-md'>
                    <p class='text-green-800'>✅ ഫയൽ അപ്‌ലോഡ് വിജയകരം: <strong>{uploaded_file.name}</strong> ({uploaded_file.size / (1024 * 1024):.2f} MB)</p>
                    <p class='text-green-800'>ഈ Verification Code share ചെയ്യൂ: <strong>{st.session_state.verification_code}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )
        except MemoryError:
            st.markdown(
                "<div class='bg-red-200 p-4 rounded-md text-red-800'>❌ പിശക്: ഫയൽ process ചെയ്യാൻ memory പോരാ. ചെറിയ ഫയൽ പരീക്ഷിക്കുക.</div>",
                unsafe_allow_html=True
            )

# Download section
st.markdown("<h2 class='text-xl font-semibold text-white mb-4 mt-8'>📥 ഫയൽ ഡൗൺലോഡ് ചെയ്യൂ</h2>", unsafe_allow_html=True)
st.markdown("<p class='text-gray-300 mb-4'>Verification Code ഉപയോഗിച്ച് ഫയൽ ഡൗൺലോഡ് ചെയ്യാം.</p>", unsafe_allow_html=True)
user_code = st.text_input("Verification Code നൽകൂ", type="password")

if st.button("✅ ഡൗൺലോഡ് ചെയ്യൂ"):
    if st.session_state.verification_code is None or st.session_state.file_buffer is None:
        st.markdown(
            """
            <div class='bg-red-200 p-4 rounded-md text-red-800'>
                ❌ പിശക്: ഫയൽ ഇപ്പോഴും അപ്‌ലോഡ് ചെയ്തിട്ടില്ല. ദയവായി ആദ്യം ഫയൽ അപ്‌ലോഡ് ചെയ്യൂ.
            </div>
            """,
            unsafe_allow_html=True
        )
    elif user_code == st.session_state.verification_code:
        download_link = get_file_download_link(st.session_state.file_buffer, st.session_state.filename)
        if download_link:
            st.markdown(
                f"""
                <div class='bg-blue-200 p-4 rounded-md'>
                    ✅ Verification വിജയിച്ചു! <br>
                    <a href='{download_link}' download='{st.session_state.filename}' class='text-blue-600 underline btn-gradient inline-block px-4 py-2 rounded-md text-white'>👉 {st.session_state.filename} ഡൗൺലോഡ് ചെയ്യാൻ ഇവിടെ ക്ലിക്ക് ചെയ്യൂ</a>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='bg-red-200 p-4 rounded-md text-red-800'>❌ പിശക്: ഫയൽ ഡൗൺലോഡ് ലിങ്ക് സൃഷ്ടിക്കാൻ സാധിച്ചില്ല. ചെറിയ ഫയൽ പരീക്ഷിക്കുക.</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800'>❌ പിശക്: Verification Code തെറ്റാണ്. വീണ്ടും പരിശോധിക്കുക.</div>",
            unsafe_allow_html=True
        )

# Footer
st.markdown(
    """
    <div class='mt-8 text-center text-gray-300'>
        <p>⚙️ Powered by Streamlit + Tailwind CSS | 1GB വരെയുള്ള ഫയലുകൾ പിന്തുണയ്ക്കുന്നു.</p>
    </div>
    """,
    unsafe_allow_html=True
)
