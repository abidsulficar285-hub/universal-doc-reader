import streamlit as st
import os
import tempfile
from markitdown import MarkItDown

# Page Configuration
st.set_page_config(page_title="Universal Doc-to-Text", page_icon="📄")

def main():
    st.title("📄 Universal File-to-Text Converter")
    st.markdown("Convert Office docs, PDFs, and HTML to clean Markdown.")

    # 1. Initialize the Engine 
    # We create a single instance to be efficient
    md = MarkItDown()

    # 2. Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "zip"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            with st.expander(f"📁 Processing: {uploaded_file.name}", expanded=True):
                try:
                    # To ensure stability across all file types (especially PDF/XLSX),
                    # we save the upload to a temporary file.
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    with st.spinner('Converting...'):
                        # Process the file using the temporary path
                        result = md.convert(tmp_path)
                        content = result.text_content

                    # Cleanup the temporary file
                    os.remove(tmp_path)

                    # 3. Instant Preview
                    st.text_area("Preview", value=content, height=300, key=f"preview_{uploaded_file.name}")

                    # 4. Download Options
                    col1, col2 = st.columns(2)
                    with col1:
                        fmt = st.radio("Format:", ["Markdown (.md)", "Text (.txt)"], key=f"fmt_{uploaded_file.name}", horizontal=True)
                    
                    ext = ".md" if "Markdown" in fmt else ".txt"
                    
                    with col2:
                        st.download_button(
                            label=f"📥 Download {ext}",
                            data=content,
                            file_name=f"{base_name}_converted{ext}",
                            mime="text/plain",
                            key=f"dl_{uploaded_file.name}"
                        )

                except Exception as e:
                    # 5. Resilience
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                    # Developer Note: Uncomment below to see the exact error during debugging
                    # st.info(f"Debug Info: {str(e)}")

if __name__ == "__main__":
    main()
