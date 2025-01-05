from typing import List
import fitz
from abc import ABC, abstractmethod
from objects.magazine_page import MagazinePage



class IPdfReader(ABC):
    @abstractmethod
    def from_pdf_to_magazine_pages(self, path: str) -> List['MagazinePage']:
        """Extrae las páginas de un PDF y las devuelve como una lista de MagazinePage."""
        pass


class FitzPdfReader(IPdfReader):
    def from_pdf_to_magazine_pages(self, path: str) -> List['MagazinePage']:
        magazine_pages = []
        try:
            pdf_document = fitz.open(path)
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text = page.get_text()
                
                magazine_pages.append(MagazinePage(index=page_num + 1, text=text))
            
            pdf_document.close()
        except Exception as e:
            print(f"Error procesando el archivo {path}: {e}")
     
        return magazine_pages


