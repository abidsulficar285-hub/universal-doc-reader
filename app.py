import streamlit as st
import os
import tempfile
from pathlib import Path
from markitdown import MarkItDown

# Page Configuration
st.set_page_config(page_title="Universal Doc-to-Text", page_icon="📄")

def get_file_size_mb(file_size_bytes):
    """Converts bytes to Megabytes for display."""
    return file_size_bytes / (1024 * 1024)

def main():
    st.title("📄 Universal File-to-Text Converter")
    
    # 1. Initialize Engine
    md = MarkItDown()

    # 2. Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "zip"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_ext = Path(uploaded_file.name).suffix.lower()
            base_name = Path(uploaded_file.name).stem
            
            # Get Original File Size
            original_size_bytes = uploaded_file.size
            original_size_mb = get_file_size_mb(original_size_bytes)
            
            with st.expander(f"📁 File: {uploaded_file.name}", expanded=True):
                # Create Tabs for the new functionality
                tab1, tab2 = st.tabs(["📝 Conversion & Preview", "📊 File Size Comparison"])
                
                try:
                    # Processing logic
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
                        tmp.write(uploaded_file.getbuffer())
                        tmp_path = tmp.name

                    with st.spinner('Converting...'):
                        result = md.convert(tmp_path)
                        content = result.text_content

                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

                    # --- Tab 1: Conversion & Preview ---
                    with tab1:
                        st.text_area("Preview", value=content, height=300, key=f"p_{uploaded_file.name}")
                        
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

                    # --- Tab 2: File Size Comparison ---
                    with tab2:
                        # Calculate Converted Size
                        converted_size_bytes = len(content.encode('utf-8'))
                        converted_size_mb = get_file_size_mb(converted_size_bytes)
                        
                        # Calculate Percentage Decrease
                        if original_size_bytes > 0:
                            reduction = ((original_size_bytes - converted_size_bytes) / original_size_bytes) * 100
                        else:
                            reduction = 0

                        # Display Table
                        st.table([
                            {"Metric": "Original file size", "Value": f"{original_size_mb:.2f} MB"},
                            {"Metric": "Converted .txt file size", "Value": f"{converted_size_mb:.2f} MB"}
                        ])

                        # Display Percentage Highlight
                        if reduction > 0:
                            st.success(f"💡 Text version is **{reduction:.1f}%** smaller.")
                        else:
                            st.info("The converted version is larger than the original source (common for very small HTML/Text files).")

                except Exception as e:
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                    st.info(f"Technical Detail: {e}")

if __name__ == "__main__":
    main()
