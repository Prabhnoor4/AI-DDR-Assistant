import fitz  # PyMuPDF


class PDFParser:
   #extracts text from pdf
    @staticmethod
    def extract_text(file_path: str) -> str:
        #returns extracted text from pdf
        try:
            document = fitz.open(file_path)
            full_text = ""

            for page in document:
                full_text += page.get_text()

            document.close()
            return full_text.strip()

        except Exception as e:
            raise RuntimeError(f"Failed to read PDF {file_path}: {str(e)}")
