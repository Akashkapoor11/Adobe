import fitz  # PyMuPDF

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_title_and_headings(self):
        doc = fitz.open(self.pdf_path)
        headings = []
        title_candidates = []

        # ---------- TITLE EXTRACTION ----------
        max_font = 0
        max_font_spans = []

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > max_font and len(span["text"].strip()) > 5:
                            max_font = span["size"]

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    line_text = " ".join([span["text"].strip() for span in line["spans"] if span["size"] == max_font])
                    if line_text and len(line_text.strip()) > 5:
                        title_candidates.append(line_text)

        title = "  ".join(title_candidates).strip() if title_candidates else ""

        # ---------- HEADING EXTRACTION ----------
        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    spans = line["spans"]
                    if not spans:
                        continue

                    font_size = spans[0]["size"]
                    text = " ".join(span["text"].strip() for span in spans).strip()

                    if not text or len(text) < 3:
                        continue

                    # Assign heading levels more conservatively
                    if font_size >= max_font:
                        level = "H1"
                    elif font_size >= max_font - 2:
                        level = "H2"
                    elif font_size >= max_font - 4:
                        level = "H3"
                    else:
                        continue

                    # Skip if it's part of the title already
                    if any(text.lower() in t.lower() for t in title_candidates):
                        continue

                    # Skip if mostly non-alphabetic
                    if sum(c.isalpha() for c in text) < 3:
                        continue

                    headings.append({
                        "level": level,
                        "text": text,
                        "page": page_num + 1
                    })

        return title, headings
