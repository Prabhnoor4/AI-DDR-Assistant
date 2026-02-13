import re


class SectionSegmenter:
   #splits large inspection text into logical sections

    @staticmethod
    def extract_relevant_sections(text: str) -> str:

        keywords = [
            "impacted area",
            "negative side",
            "positive side",
            "summary",
            "observation",
            "damp",
            "leakage",
            "plumbing"
        ]

        lines = text.splitlines()
        relevant_lines = []

        for line in lines:
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in keywords):
                relevant_lines.append(line)

        # Join only relevant lines
        return "\n".join(relevant_lines)
