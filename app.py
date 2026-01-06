import streamlit as st
from markitdown import MarkItDown
import os
import io

# Page Configuration
st.set_page_config(page_title="Universal Markdown Converter", page_icon="📝")

def main():
    st.title("📂 Universal Doc-to-Markdown Converter")
    st.markdown("Upload Word, Excel, PowerPoint, PDF, or HTML files to convert them into clean Markdown.")

    # Initialize MarkItDown Engine
    # Note: MarkItDown handles various formats natively
    md_engine = MarkItDown()

    # 1. Upload Area (Multiple files allowed)
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=['docx', 'xlsx', 'pptx', 'pdf', 'html'], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.divider()
        
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            try:
                # Process the file
                # MarkItDown can take a file stream or path. 
                # We use the stream directly from Streamlit for efficiency.
                result = md_engine.convert(uploaded_file)
                content = result.text_content
                
                # 2. Instant Preview
                with st.expander(f"📄 Preview: {uploaded_file.name}", expanded=True):
                    st.text_area(
                        label="Converted Content",
                        value=content,
                        height=300,
                        key=f"text_{uploaded_file.name}"
                    )
                    
                    # 3. Download Options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download as Markdown (.md)",
                            data=content,
                            file_name=f"{base_name}_converted.md",
                            mime="text/markdown",
                            key=f"md_{uploaded_file.name}"
                        )
                    
                    with col2:
                        st.download_button(
                            label="📥 Download as Text (.txt)",
                            data=content,
                            file_name=f"{base_name}_converted.txt",
                            mime="text/plain",
                            key=f"txt_{uploaded_file.name}"
                        )

            except Exception as e:
                # 4. Resilience / Error Handling
                st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                # Log the specific error for the developer in the console
                print(f"Error processing {uploaded_file.name}: {e}")

if __name__ == "__main__":
    main()
