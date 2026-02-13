class MarkdownRenderer:
   #markdown format

    @staticmethod
    def render(ddr_sections: dict) -> str:
        
        md = "# Detailed Diagnostic Report (DDR)\n\n"
        
        # Adding metadata header
        from datetime import datetime
        md += f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n"
        md += "---\n\n"
        
        # Property Issue Summary
        md += "## 1. Property Issue Summary\n\n"
        summary = ddr_sections.get("property_summary", "Not Available")
        md += summary + "\n\n"
        md += "---\n\n"
        
        # Area-wise Observations
        md += "## 2. Area-wise Observations\n\n"
        observations = ddr_sections.get("area_observations", "Not Available")
        md += observations + "\n\n"
        md += "---\n\n"
        
        # Probable Root Cause
        md += "## 3. Probable Root Cause\n\n"
        root_cause = ddr_sections.get("root_cause", "Not Available")
        md += root_cause + "\n\n"
        md += "---\n\n"
        
        # Severity Assessment
        md += "## 4. Severity Assessment\n\n"
        severity = ddr_sections.get("severity", "Not Available")
        md += severity + "\n\n"
        md += "---\n\n"
        
        # Recommended Actions
        md += "## 5. Recommended Actions\n\n"
        recommendations = ddr_sections.get("recommendations", "Not Available")
        md += recommendations + "\n\n"
        md += "---\n\n"
        
        # Additional Notes
        md += "## 6. Additional Notes\n\n"
        notes = ddr_sections.get("additional_notes", "Not Available")
        md += notes + "\n\n"
        md += "---\n\n"
        
        # Missing or Unclear Information
        md += "## 7. Missing or Unclear Information\n\n"
        missing = ddr_sections.get("missing_info", "Not Available")
        md += missing + "\n\n"
        
        # Footer
        md += "---\n\n"
        md += "*This report was generated using AI-powered analysis of inspection and thermal imaging data. "
        md += "All findings are based strictly on the provided documentation.*\n"
        
        return md.strip()
