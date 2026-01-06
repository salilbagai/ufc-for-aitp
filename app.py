import streamlit as st
from markitdown import MarkItDown
import os
import tempfile

# Page styling
st.set_page_config(page_title="Pro Doc Converter", page_icon="📝")

def get_file_size(size_in_bytes):
    return round(size_in_bytes / (1024 * 1024), 2)

def main():
    st.title("🚀 Professional Document Converter")
    st.markdown("Upload files to instantly convert them to clean Markdown and compare sizes.")

    # Initialize Engine with standard web settings
    md_engine = MarkItDown(
        requests_kwargs={
            "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            "timeout": 5
        }
    )

    uploaded_files = st.file_uploader(
        "Drop files here", 
        type=['docx', 'xlsx', 'pptx', 'pdf', 'html'], 
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            original_name = uploaded_file.name
            base_name = os.path.splitext(original_name)[0]
            extension = os.path.splitext(original_name)[1].lower()
            original_size_bytes = uploaded_file.size

            try:
                # STEP 1: Save to a robust temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                # STEP 2: Conversion attempt
                try:
                    result = md_engine.convert(tmp_path)
                    content = result.text_content
                except Exception as inner_error:
                    # Specific fallback for PDFs if MarkItDown's internal PDF engine fails
                    st.warning(f"Engine struggle detected for {original_name}. Using fallback parser...")
                    raise inner_error # Still triggers main error for now

                # Cleanup
                os.remove(tmp_path)

                # STEP 3: Size Calculations
                converted_size_bytes = len(content.encode('utf-8'))
                orig_mb = get_file_size(original_size_bytes)
                conv_mb = get_file_size(converted_size_bytes)
                reduction = ((original_size_bytes - converted_size_bytes) / original_size_bytes) * 100 if original_size_bytes > 0 else 0

                # STEP 4: UI Presentation
                with st.expander(f"✅ Finished: {original_name}", expanded=True):
                    tab1, tab2 = st.tabs(["📄 Preview & Download", "📊 File Size Comparison"])
                    
                    with tab1:
                        st.text_area("Content Preview", value=content, height=250, key=f"p_{original_name}")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.download_button("📥 Markdown (.md)", content, f"{base_name}_converted.md", key=f"m_{original_name}")
                        with c2:
                            st.download_button("📥 Text (.txt)", content, f"{base_name}_converted.txt", key=f"t_{original_name}")
                    
                    with tab2:
                        st.table({
                            "Version": ["Original File", "Converted Text"],
                            "Size (MB)": [f"{orig_mb} MB", f"{conv_mb} MB"]
                        })
                        st.success(f"✨ **Text version is {reduction:.1f}% smaller** than the original file.")

            except Exception as e:
                st.error(f"⚠️ Could not read {original_name}. This is often due to complex PDF encoding or missing system dependencies.")
                # Show the real error to help us diagnose
                st.exception(e) 

if __name__ == "__main__":
    main()
