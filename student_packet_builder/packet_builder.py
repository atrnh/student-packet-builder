from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

PAGE_LOOKUP = {}


def populate_page_lookup_for_pdf(pdf_file: Path):
    reader = PdfReader(str(pdf_file))
    cover, *rest = reader.pages

    PAGE_LOOKUP["_cover"] = cover
    for page in rest:
        name = page.extract_text().splitlines()[0]
        PAGE_LOOKUP[name] = page


def write_pdf(outfile: Path, resumes: dict):
    writer = PdfWriter()
    writer.add_page(PAGE_LOOKUP["_cover"])

    for student, packet_page in PAGE_LOOKUP.items():
        writer.add_page(packet_page)
        if student in resumes:
            resume_reader = PdfReader(str(resumes[student]))
            for page in resume_reader.pages:
                writer.add_page(page)
        else:
            continue

    with open(outfile, "wb") as f:
        writer.write(f)
