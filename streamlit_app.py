import streamlit as st
import tempfile
import os
from pathlib import Path

# Import backend components
from app.processing.pdf_parser import PDFParser
from app.processing.text_cleaner import TextCleaner
from app.extraction.inspection_extractor import InspectionExtractor
from app.extraction.thermal_extractor import ThermalExtractor
from app.intelligence.data_normalizer import DataNormalizer
from app.intelligence.deduplicator import Deduplicator
from app.intelligence.area_linker import AreaLinker
from app.intelligence.conflict_detector import ConflictDetector
from app.intelligence.missing_detector import MissingDetector
from app.reporting.ddr_builder import DDRBuilder
from app.reporting.markdown_renderer import MarkdownRenderer
from app.processing.section_segmenter import SectionSegmenter


# Page configuration
st.set_page_config(
    page_title="AI DDR Assistant",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
    }
    h2 {
        color: #34495e;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)


def process_reports(inspection_file, thermal_file):
    """
    Process uploaded inspection and thermal reports to generate DDR.
    """
    try:
        # Create temporary directory for uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            inspection_path = os.path.join(temp_dir, "inspection.pdf")
            thermal_path = os.path.join(temp_dir, "thermal.pdf")
            
            with open(inspection_path, "wb") as f:
                f.write(inspection_file.getvalue())
            
            with open(thermal_path, "wb") as f:
                f.write(thermal_file.getvalue())
            
            # Process files through the pipeline
            with st.spinner("📄 Extracting text from PDFs..."):
                raw_inspection_text = TextCleaner.clean(
                    PDFParser.extract_text(inspection_path)
                )
                inspection_text = SectionSegmenter.extract_relevant_sections(
                    raw_inspection_text
                )
                thermal_text = TextCleaner.clean(
                    PDFParser.extract_text(thermal_path)
                )
            
            with st.spinner("🤖 Extracting structured data with AI..."):
                inspection_data = InspectionExtractor().extract(inspection_text)
                thermal_data = ThermalExtractor().extract(thermal_text)
            
            with st.spinner("🔄 Processing and analyzing data..."):
                normalized_data = DataNormalizer.normalize(inspection_data, thermal_data)
                normalized_data = Deduplicator.deduplicate(normalized_data)
                normalized_data = AreaLinker.link(normalized_data)
                conflicts = ConflictDetector.detect(normalized_data)
                missing = MissingDetector.detect(normalized_data)
            
            with st.spinner("📝 Generating Detailed Diagnostic Report..."):
                ddr_sections = DDRBuilder().build(normalized_data, conflicts, missing)
                final_markdown = MarkdownRenderer.render(ddr_sections)
            
            return final_markdown, None
            
    except Exception as e:
        return None, str(e)


def main():
    # Header
    st.title("🏗️ AI DDR Assistant")
    st.markdown("### Automated Detailed Diagnostic Report Generation")
    st.markdown("Upload your **Inspection Report** and **Thermal Report** to generate a comprehensive DDR.")
    
    st.divider()
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This AI-powered system automatically generates Detailed Diagnostic Reports (DDR) 
        by analyzing inspection and thermal reports.
        
        **Features:**
        - 📄 PDF text extraction
        - 🤖 AI-powered data extraction
        - 🔍 Conflict detection
        - 📊 Missing data identification
        - 📝 Professional report generation
        """)
        
        st.divider()
        
        st.header("⚙️ Settings")
        st.info("Using configured LLM provider from `config.py`")
        
        st.divider()
        
        st.header("📚 Instructions")
        st.markdown("""
        1. Upload Inspection Report PDF
        2. Upload Thermal Report PDF
        3. Click "Generate DDR"
        4. Download the generated report
        """)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Inspection Report")
        inspection_file = st.file_uploader(
            "Upload Inspection Report (PDF)",
            type=["pdf"],
            key="inspection",
            help="Upload the property inspection report PDF"
        )
        
        if inspection_file:
            st.success(f"✅ Uploaded: {inspection_file.name}")
            st.caption(f"Size: {inspection_file.size / 1024:.2f} KB")
    
    with col2:
        st.subheader("🌡️ Thermal Report")
        thermal_file = st.file_uploader(
            "Upload Thermal Report (PDF)",
            type=["pdf"],
            key="thermal",
            help="Upload the thermal imaging report PDF"
        )
        
        if thermal_file:
            st.success(f"✅ Uploaded: {thermal_file.name}")
            st.caption(f"Size: {thermal_file.size / 1024:.2f} KB")
    
    st.divider()
    
    # Generate button
    if inspection_file and thermal_file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate DDR", use_container_width=True):
                # Process reports
                result, error = process_reports(inspection_file, thermal_file)
                
                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.success("✅ DDR Generated Successfully!")
                    
                    # Display result
                    st.divider()
                    st.subheader("📄 Generated Detailed Diagnostic Report")
                    
                    # Show markdown preview
                    with st.expander("📖 View Report", expanded=True):
                        st.markdown(result)
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Markdown download
                        st.download_button(
                            label="⬇️ Download Markdown",
                            data=result,
                            file_name="generated_ddr.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col2:
                        # PDF download
                        try:
                            from app.reporting.pdf_renderer import PDFRenderer
                            import tempfile as tmp
                            
                            # Generate PDF in temp file
                            with tmp.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
                                pdf_path = tmpfile.name
                            
                            PDFRenderer.render(result, pdf_path)
                            
                            with open(pdf_path, 'rb') as pdf_file:
                                pdf_bytes = pdf_file.read()
                            
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=pdf_bytes,
                                file_name="generated_ddr.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
                            # Clean up temp file
                            os.unlink(pdf_path)
                            
                        except Exception as e:
                            st.warning(f"⚠️ PDF generation unavailable: {str(e)}")
                    
                    # Also save to outputs folder
                    output_path = "data/outputs/generated_ddr.md"
                    os.makedirs("data/outputs", exist_ok=True)
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result)
                    
                    # Also save PDF
                    try:
                        from app.reporting.pdf_renderer import PDFRenderer
                        pdf_output = "data/outputs/generated_ddr.pdf"
                        PDFRenderer.render(result, pdf_output)
                        st.info(f"💾 Reports saved to: `data/outputs/` (Markdown & PDF)")
                    except:
                        st.info(f"💾 Report saved to: `{output_path}`")
    else:
        st.warning("⚠️ Please upload both Inspection and Thermal reports to continue.")
    
    # Footer
    st.divider()
    st.caption("🤖 Powered by AI | Built with Streamlit")


if __name__ == "__main__":
    main()
