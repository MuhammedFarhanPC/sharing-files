import streamlit as st
import random
import string
import io
import base64
import sys

# Function to generate a 6-digit verification code
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Function to encode file to base64 for download
def get_file_download_link(file_buffer, filename):
    try:
        b64 = base64.b64encode(file_buffer.getvalue()).decode()
        return f'data:application/octet-stream;base64,{b64}'
    except MemoryError:
        return None

# Initialize session state variables
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = None
if 'file_buffer' not in st.session_state:
    st.session_state.file_buffer = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# Custom HTML/CSS for a colorful design
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
                <!-- Streamlit will inject content here -->
            </div>
        </div>
    </div>
</body>
</html>
"""

# Render the HTML template
st.markdown(html_content, unsafe_allow_html=True)

# Streamlit app logic
st.markdown("<h2 class='text-xl font-semibold text-white mb-4'>Upload a File (Max 1GB per file)</h2>", unsafe_allow_html=True)
st.markdown("<p class='text-gray-300 mb-4'>Drag and drop or click to select a file to share securely. Each file must be 1GB or smaller.</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file to share", type=None)

if uploaded_file is not None:
    # Check file size (1GB = 1024 * 1024 * 1024 bytes)
    max_size = 1024 * 1024 * 1024  # 1GB in bytes
    if uploaded_file.size > max_size:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800'>Error: File size exceeds 1GB limit. Please upload a file smaller than 1GB.</div>",
            unsafe_allow_html=True
        )
    else:
        try:
            # Read file into memory
            file_buffer = io.BytesIO(uploaded_file.read())
            st.session_state.file_buffer = file_buffer
            st.session_state.filename = uploaded_file.name
            
            # Generate or retrieve verification code
            if st.session_state.verification_code is None:
                st.session_state.verification_code = generate_verification_code()
            
            st.markdown(
                f"""
                <div class='bg-green-200 p-4 rounded-md'>
                    <p class='text-green-800'>File uploaded successfully: <strong>{uploaded_file.name}</strong> ({uploaded_file.size / (1024 * 1024):.2f} MB)</p>
                    <p class='text-green-800'>Share this verification code with the receiver: <strong>{st.session_state.verification_code}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )
        except MemoryError:
            st.markdown(
                "<div class='bg-red-200 p-4 rounded-md text-red-800'>Error: Insufficient memory to process the file. Try a smaller file.</div>",
                unsafe_allow_html=True
            )

# Verification code input for downloading
st.markdown("<h2 class='text-xl font-semibold text-white mb-4 mt-8'>Download a File</h2>", unsafe_allow_html=True)
st.markdown("<p class='text-gray-300 mb-4'>Enter the verification code to download the shared file.</p>", unsafe_allow_html=True)
user_code = st.text_input("Enter the verification code", type="password")
if st.button("Verify and Download", key="download_button", help="Click to verify and download the file"):
    if st.session_state.verification_code is None or st.session_state.file_buffer is None:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800'>Error: No file has been uploaded yet.</div>",
            unsafe_allow_html=True
        )
    elif user_code == st.session_state.verification_code:
        download_link = get_file_download_link(st.session_state.file_buffer, st.session_state.filename)
        if download_link:
            st.markdown(
                f"""
                <div class='bg-blue-200 p-4 rounded-md'>
                    <p class='text-blue-800'>Verification successful! <a href='{download_link}' download='{st.session_state.filename}' class='text-blue-600 underline btn-gradient inline-block px-4 py-2 rounded-md text-white'>Click here to download {st.session_state.filename}</a></p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='bg-red-200 p-4 rounded-md text-red-800'>Error: Failed to generate download link due to memory issues. Try a smaller file.</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800'>Error: Incorrect verification code.</div>",
            unsafe_allow_html=True
        )

# Footer
st.markdown(
    """
    <div class='mt-8 text-center text-gray-300'>
        <p>Built with Streamlit & Tailwind CSS | Supports drag-and-drop files up to 1GB</p>
    </div>
    """,
    unsafe_allow_html=True
)