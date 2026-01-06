import streamlit as st
from markitdown import MarkItDown
import os

# Page styling
st.set_page_config(page_title="MarkItDown Converter", page_icon="🚀")

def main():
    st.title("📄 Document to Markdown Converter")
    st.markdown("Convert Office docs, PDFs, and HTML into clean Markdown instantly.")

    # [Requirement 3] Initialize engine with custom web request settings
    # We define a user-agent and a 5-second timeout for stable web fetching
    md_engine = MarkItDown(
        requests_kwargs={
            "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            "timeout": 5
        }
    )

    # [Requirement 2] Drag and drop area
    uploaded_files = st.file_uploader(
        "Upload files (.docx, .xlsx, .pptx, .pdf, .html)", 
        type=['docx', 'xlsx', 'pptx', 'pdf', 'html'], 
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # [Requirement 4] Use OS to manage file naming
            original_filename = uploaded_file.name
            base_name = os.path.splitext(original_filename)[0]
            
            try:
                # [Requirement 1] Core Engine Conversion
                result = md_engine.convert(uploaded_file)
                content = result.text_content
                
                # [Requirement 2] Instant Preview
                with st.expander(f"✅ Processed: {original_filename}", expanded=True):
                    st.text_area(
                        label="Markdown Preview",
                        value=content,
                        height=250,
                        key=f"area_{original_filename}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download .md",
                            data=content,
                            file_name=f"{base_name}_converted.md",
                            mime="text/markdown",
                            key=f"md_{original_filename}"
                        )
                    with col2:
                        st.download_button(
                            label="Download .txt",
                            data=content,
                            file_name=f"{base_name}_converted.txt",
                            mime="text/plain",
                            key=f"txt_{original_filename}"
                        )

            except Exception as e:
                # [Requirement 3] Resilience / Error Handling
                st.error(f"⚠️ Could not read {original_filename}. Please check the format.")
                # Optional: st.caption(f"Error details: {e}")

if __name__ == "__main__":
    main()
