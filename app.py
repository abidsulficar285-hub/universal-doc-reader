import streamlit as st
import os
import tempfile
from pathlib import Path
from markitdown import MarkItDown

# Page Configuration
st.set_page_config(page_title="Universal Doc-to-Text", page_icon="📄")

def main():
    st.title("📄 Universal File-to-Text Converter")
    st.markdown("Professional-grade conversion for Office and PDF.")

    # 1. Initialize Engine (Requirement [1])
    # Note: Ensure Python 3.10+ is used
    md = MarkItDown()

    # 2. Upload Area (Requirement [2])
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "zip"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_ext = Path(uploaded_file.name).suffix.lower()
            base_name = Path(uploaded_file.name).stem
            
            with st.expander(f"📁 Processing: {uploaded_file.name}", expanded=True):
                try:
                    # Creating a named temp file so MarkItDown can see the extension
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
                        tmp.write(uploaded_file.getbuffer())
                        tmp_path = tmp.name

                    with st.spinner('Converting...'):
                        # Requirement [3]: Stable processing
                        result = md.convert(tmp_path)
                        content = result.text_content

                    # Cleanup temp file immediately
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

                    # 3. Instant Preview
                    st.text_area("Preview", value=content, height=300, key=f"p_{uploaded_file.name}")

                    # 4. Download Options
                    col1, col2 = st.columns(2)
                    with col1:
                        fmt = st.radio("Format:", ["Markdown (.md)", "Text (.txt)"], key=f"f_{uploaded_file.name}", horizontal=True)
                    
                    final_ext = ".md" if "Markdown" in fmt else ".txt"
                    
                    with col2:
                        st.download_button(
                            label=f"📥 Download {final_ext}",
                            data=content,
                            file_name=f"{base_name}_converted{final_ext}",
                            mime="text/plain",
                            key=f"d_{uploaded_file.name}"
                        )

                except Exception as e:
                    # Requirement [3]: Resilience
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                    # Developer insight:
                    if "NoneType" in str(e):
                        st.warning("Hint: This usually means the parser for this file type is missing or the file is empty.")
                    else:
                        st.info(f"Technical Detail: {e}")

if __name__ == "__main__":
    main()
