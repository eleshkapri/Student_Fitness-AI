"""
PDF Reporting Service for StudentFit AI.
Encapsulates PDF formatting, glyph encoding, layout typography, and A4 page breaks.
"""

from typing import Optional


class PDFReportGenerator:
    """
    Object-oriented PDF generation engine converting schedule text into formatted A4 binaries.
    """

    CHAR_REPLACEMENTS = {
        "₹": "Rs. ",
        "€": "EUR ",
        "£": "GBP ",
        "$": "USD ",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "**": ""
    }

    @classmethod
    def generate(cls, raw_text: str) -> Optional[bytes]:
        """Compiles clean, styled A4 PDF binary stream."""
        if not raw_text:
            return None

        try:
            from fpdf import FPDF

            class StyledPDF(FPDF):
                def header(self):
                    self.set_font('Helvetica', 'B', 14)
                    self.set_text_color(255, 107, 84) # Coral
                    self.cell(0, 10, 'StudentFit AI - Weekly Fitness & Nutrition Plan', align='C', new_x='LMARGIN', new_y='NEXT')
                    self.ln(2)

                def footer(self):
                    self.set_y(-15)
                    self.set_font('Helvetica', 'I', 8)
                    self.set_text_color(133, 130, 172)
                    self.cell(0, 10, f'StudentFit AI | Page {self.page_no()}', align='C')

            pdf = StyledPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            epw = pdf.epw

            clean_text = raw_text
            for key, val in cls.CHAR_REPLACEMENTS.items():
                clean_text = clean_text.replace(key, val)

            lines = clean_text.split('\n')

            for line in lines:
                line = line.strip()
                if not line:
                    pdf.ln(2)
                    continue

                safe_line = line.encode('latin-1', 'ignore').decode('latin-1')

                if safe_line.startswith('Day:') or safe_line.startswith('#'):
                    pdf.ln(3)
                    pdf.set_font("Helvetica", 'B', 12)
                    pdf.set_text_color(255, 107, 84)
                    pdf.cell(epw, 7, safe_line.replace('#', '').strip(), new_x="LMARGIN", new_y="NEXT")
                elif safe_line.startswith('Workout:') or safe_line.startswith('Meal:') or safe_line.startswith('GROCERY'):
                    pdf.set_font("Helvetica", 'B', 10)
                    pdf.set_text_color(156, 140, 255)
                    pdf.cell(epw, 6, safe_line, new_x="LMARGIN", new_y="NEXT")
                elif safe_line.startswith('*') or safe_line.startswith('-'):
                    pdf.set_font("Helvetica", '', 9)
                    pdf.set_text_color(40, 40, 40)
                    pdf.multi_cell(epw, 5, "- " + safe_line[1:].strip(), new_x="LMARGIN", new_y="NEXT")
                else:
                    pdf.set_font("Helvetica", '', 9)
                    pdf.set_text_color(40, 40, 40)
                    pdf.multi_cell(epw, 5, safe_line, new_x="LMARGIN", new_y="NEXT")

            return bytes(pdf.output())
        except Exception:
            return None


def create_fitness_pdf(raw_text: str) -> Optional[bytes]:
    """Functional facade delegating to PDFReportGenerator."""
    return PDFReportGenerator.generate(raw_text)
