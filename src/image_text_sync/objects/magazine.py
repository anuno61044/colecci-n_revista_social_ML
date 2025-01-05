from typing import List
from services.pdf_reader import IPdfReader
from objects.magazine_page import MagazinePage


class Magazine:
    """Representa los datos extraídos directamente del PDF."""
    def __init__(self, path: str, pdf_reader: IPdfReader):
        self.path = path
        self.name = path.split("\\")[-1].removesuffix(".pdf")
        self.pages: List[MagazinePage] = pdf_reader.from_pdf_to_magazine_pages(path)

