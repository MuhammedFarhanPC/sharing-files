import streamlit as st
import random
import string
import io
import base64
import time

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

# Initialize session state with a unique key
session_key = f"file_sharing_session_{int(time.time())}"  # Unique key to avoid conflicts
if session_key not in st.session_state:
    st.session_state[session_key] = {
        "verification_code": None,
        "file_buffer": None,
        "filename": None,
        "upload_status": False,
        "last_input": None
    }

# Custom HTML/CSS for a colorful, mobile-friendly design
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
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
        }
        .btn-gradient:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        .copy-button {
            background: linear-gradient(90deg, #34d399, #10b981);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .copy-button:hover {
            transform: scale(1.05);
        }
        @media (max-width: 640px) {
            .container {
                padding: 1rem;
            }
            h1 {
                font-size: 2rem;
            }
            h2 {
                font-size: 1.25rem;
            }
            .btn-gradient, .copy-button {
                width: 100%;
                text-align: center;
            }
            input[type="password"] {
                font-size: 1rem;
                padding: 0.5rem;
            }
        }
    </style>
</head>
<body class="font-sans min-h-screen flex items-center justify-center">
    <div class="container mx-auto p-4 sm:p-6">
        <div class="shadow-lg rounded-lg p-6 sm:p-8 max-w-lg mx-auto">
            <h1 class="text-3xl sm:text-4xl font-bold text-center text-cyan-300 mb-6 animate-pulse">IPCS File Sharing</h1>
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
st.markdown("<h2 class='text-lg sm:text-xl font-semibold text-white mb-4'>Upload a File (Max 1GB)</h2>", unsafe_allow_html=True)
st.markdown("<p class='text-gray-300 mb-4 text-sm sm:text-base'>Drag and drop or tap to select a file to share securely. Each file must be 1GB or smaller.</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file to share", type=None, key=f"file_uploader_{session_key}")

if uploaded_file is not None:
    # Check file size (1GB = 1024 * 1024 * 1024 bytes)
    max_size = 1024 * 1024 * 1024  # 1GB in bytes
    if uploaded_file.size > max_size:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800 text-sm sm:text-base'>Error: File size exceeds 1GB limit. Please upload a file smaller than 1GB.</div>",
            unsafe_allow_html=True
        )
        st.session_state[session_key]["upload_status"] = False
    else:
        try:
            # Reset session state for new file
            st.session_state[session_key] = {
                "file_buffer": io.BytesIO(uploaded_file.read()),
                "filename": uploaded_file.name,
                "verification_code": generate_verification_code(),
                "upload_status": True,
                "last_input": None
            }
            
            # JavaScript for copy-to-clipboard functionality
            copy_script = f"""
            <script>
                function copyCode() {{
                    navigator.clipboard.writeText('{st.session_state[session_key]["verification_code"]}');
                    alert('Verification code copied to clipboard!');
                }}
            </script>
            """
            st.markdown(
                f"""
                <div class='bg-green-200 p-4 rounded-md text-sm sm:text-base'>
                    <p class='text-green-800'>File uploaded successfully: <strong>{st.session_state[session_key]["filename"]}</strong> ({uploaded_file.size / (1024 * 1024):.2f} MB)</p>
                    <p class='text-green-800'>Verification code: <strong>{st.session_state[session_key]["verification_code"]}</strong></p>
                    <button class='copy-button mt-2' onclick='copyCode()'>Copy Code</button>
                </div>
                {copy_script}
                """,
                unsafe_allow_html=True
            )
        except MemoryError:
            st.markdown(
                "<div class='bg-red-200 p-4 rounded-md text-red-800 text-sm sm:text-base'>Error: Insufficient memory to process the file. Try a smaller file.</div>",
                unsafe_allow_html=True
            )
            st.session_state[session_key]["upload_status"] = False

# Display upload status
if st.session_state[session_key]["upload_status"]:
    st.markdown(
        "<div class='bg-blue-200 p-2 rounded-md text-blue-800 text-sm sm:text-base'>Status: File uploaded and ready for sharing.</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='bg-yellow-200 p-2 rounded-md text-yellow-800 text-sm sm:text-base'>Status: No file uploaded yet.</div>",
        unsafe_allow_html=True
    )

# Verification code input for downloading
st.markdown("<h2 class='text-lg sm:text-xl font-semibold text-white mb-4 mt-8'>Download a File</h2>", unsafe_allow_html=True)
st.markdown("<p class='text-gray-300 mb-4 text-sm sm:text-base'>Enter the 6-digit verification code provided by the sender to download the file.</p>", unsafe_allow_html=True)
user_code = st.text_input("Enter the verification code", type="text", key=f"code_input_{session_key}")
if st.button("Verify and Download", key=f"download_button_{session_key}", help="Tap to verify and download the file"):
    user_code = user_code.strip() if user_code else ""  # Trim whitespace
    st.session_state[session_key]["last_input"] = user_code  # Log input for debugging
    if not user_code:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800 text-sm sm:text-base'>Error: Please enter a verification code.</div>",
            unsafe_allow_html=True
        )
    elif not st.session_state[session_key]["upload_status"] or st.session_state[session_key]["file_buffer"] is None:
        st.markdown(
            "<div class='bg-red-200 p-4 rounded-md text-red-800 text-sm sm:text-base'>Error: No file has been uploaded yet. Please upload a file first.</div>",
            unsafe_allow_html=True
        )
    elif user_code == st.session_state[session_key]["verification_code"]:
        download_link = get_file_download_link(st.session_state[session_key]["file_buffer"], st.session_state[session_key]["filename"])
        if download_link:
            st.markdown(
                f"""
                <div class='bg-blue-200 p-4 rounded-md text-sm sm:text-base'>
                    <p class='text-blue-800'>Verification successful! <a href='{download_link}' download='{st.session_state[session_key]["filename"]}' class='text-white underline btn-gradient inline-block px-4 py-2 rounded-md'>Tap to download {st.session_state[session_key]["filename"]}</a></p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='bg-red-200 p-4 rounded-md text-red-800 text-sm sm:text-base'>Error: Failed to generate download link due to memory issues. Try a smaller file.</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            f"""
            <div class='bg-red-200 p-4 rounded-md text-red-800 text-sm sm:text-base'>Error: Incorrect verification code. You entered: <strong>{user_code}</strong>. Please try again.</div>
            """,
            unsafe_allow_html=True
        )

# Debug information (visible only to sender for troubleshooting)
if st.session_state[session_key]["upload_status"]:
    debug_info = f"""
    <div class='bg-gray-200 p-4 rounded-md text-gray-800 text-sm sm:text-base mt-4'>
        <p>Debug Info (for sender): File: <strong>{st.session_state[session_key]["filename"]}</strong>, Code: <strong>{st.session_state[session_key]["verification_code"]}</strong></p>
        <p>Last entered code: <strong>{st.session_state[session_key]["last_input"] or "None"}</strong></p>
    </div>
    """
    st.markdown(debug_info, unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class='mt-8 text-center text-gray-300 text-sm sm:text-base'>
        <p>Built with Streamlit & Tailwind CSS | Supports drag-and-drop files up to 1GB</p>
    </div>
    """,
    unsafe_allow_html=True
)
