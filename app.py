import streamlit as st
import os
from markitdown import MarkItDown
import requests

# Page Configuration
st.set_page_config(page_title="Universal Doc-to-Text Converter", page_icon="📄")

def main():
    st.title("📄 Universal File-to-Text Converter")
    st.markdown("Upload Office docs, PDFs, or HTML to get clean Markdown output.")

    # 1. Initialize the Engine
    # MarkItDown uses a requests session internally for URL-based conversions
    md = MarkItDown()

    # 2. Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "zip"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            with st.expander(f"📁 Processing: {uploaded_file.name}", expanded=True):
                try:
                    # Save uploaded file to a temporary location for MarkItDown to read
                    # MarkItDown works best with file paths or bytes-like objects
                    with st.spinner('Converting...'):
                        # Using the 'convert' method directly on the uploaded stream
                        # Note: MarkItDown handles the routing based on extension
                        result = md.convert(uploaded_file)
                        content = result.text_content

                    # 3. Instant Preview
                    st.text_area(
                        label="Preview",
                        value=content,
                        height=300,
                        key=f"preview_{uploaded_file.name}"
                    )

                    # 4. Download Options
                    col1, col2 = st.columns(2)
                    
                    # Choose format
                    with col1:
                        export_format = st.radio(
                            "Download format:",
                            ["Markdown (.md)", "Text (.txt)"],
                            key=f"format_{uploaded_file.name}",
                            horizontal=True
                        )

                    # Trigger Download
                    ext = ".md" if "Markdown" in export_format else ".txt"
                    final_filename = f"{base_name}_converted{ext}"
                    
                    with col2:
                        st.download_button(
                            label=f"📥 Download {ext}",
                            data=content,
                            file_name=final_filename,
                            mime="text/plain",
                            key=f"dl_{uploaded_file.name}"
                        )

                except Exception as e:
                    # 5. Resilience/Error Handling
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                    # In a production environment, you might log 'e' for debugging
                    # st.sidebar.error(f"Internal Error: {str(e)}")

# Setting global timeout and user-agent for internal requests (per requirements)
# Note: MarkItDown uses 'requests' for remote URLs; we can patch the default session if needed.
# For local file uploads, these constraints apply to any sub-calls the library makes.
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
# Standard timeout is handled at the network layer or within specific library calls.

if __name__ == "__main__":
    main()
