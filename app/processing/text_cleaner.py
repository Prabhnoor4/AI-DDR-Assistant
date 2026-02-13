import re


class TextCleaner:
   #cleans raw extracted text from pdf

    @staticmethod
    def clean(text: str) -> str:

        if not text:
            return ""

        # Remove page numbers that appear alone on lines
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

        # Replace multiple newlines with single newline
        text = re.sub(r"\n{2,}", "\n", text)

        # Replace multiple spaces with single space
        text = re.sub(r"[ \t]{2,}", " ", text)

        # Remove trailing spaces on each line
        text = "\n".join(line.strip() for line in text.splitlines())

        return text.strip()
