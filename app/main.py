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


def main():
    # Input PDF paths
    inspection_path = "data/raw/inspection.pdf"
    thermal_path = "data/raw/thermal.pdf"

    # Extract text from PDFs and clean up formatting
    raw_inspection_text = TextCleaner.clean(
        PDFParser.extract_text(inspection_path)
    )

    # Remove irrelevant sections to reduce LLM token usage
    inspection_text = SectionSegmenter.extract_relevant_sections(
        raw_inspection_text
    )

    thermal_text = TextCleaner.clean(
        PDFParser.extract_text(thermal_path)
    )

    # Use LLM to extract structured data from raw text
    inspection_data = InspectionExtractor().extract(inspection_text)
    thermal_data = ThermalExtractor().extract(thermal_text)

    # Combine inspection and thermal data into unified structure
    normalized_data = DataNormalizer.normalize(inspection_data, thermal_data)

    # Remove duplicate observations across areas
    normalized_data = Deduplicator.deduplicate(normalized_data)

    # Link related areas together (e.g., "Hall" and "Living Room")
    normalized_data = AreaLinker.link(normalized_data)

    # Detect conflicting information in the data
    conflicts = ConflictDetector.detect(normalized_data)

    # Identify what information is missing from reports
    missing = MissingDetector.detect(normalized_data)

    # Generate final DDR using LLM
    ddr_sections = DDRBuilder().build(normalized_data, conflicts, missing)

    # Convert to markdown format
    final_markdown = MarkdownRenderer.render(ddr_sections)

    print("\n\n===== GENERATED DDR =====\n")
    print(final_markdown)

    # Save markdown output
    md_output_path = "data/outputs/generated_ddr.md"
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write(final_markdown)
    print(f"\n✅ Markdown saved: {md_output_path}")
    
    # Try to generate PDF version
    try:
        from app.reporting.pdf_renderer import PDFRenderer
        pdf_output_path = "data/outputs/generated_ddr.pdf"
        PDFRenderer.render(final_markdown, pdf_output_path)
        print(f"✅ PDF saved: {pdf_output_path}")
    except Exception as e:
        print(f"⚠️  PDF generation failed: {e}")
        print("   Markdown version is still available.")


if __name__ == "__main__":
    main()
