import os
from typing import Dict

class MagazineImage:
    def __init__(self, path: str): 
        self.path = path
        result = self.extract_info(path)
        self.caption = []
        self.magazine_name =  result['magazine_name']
        self.page_index = result['page_index'] 

    def extract_info(self, path: str) -> Dict[str, str]:
        image_file_name = os.path.basename(path)

        detected_index = image_file_name.find("detected")
        if detected_index == -1:
            raise ValueError(f"The file '{image_file_name}' does not contain the expected 'detected' keyword.")

        magazine_name_part = image_file_name[:detected_index-3]
        
        # Obtener el nombre de la revista (todo lo que hay antes del primer número después del "_")
        # Buscamos el primer dígito que aparece después de la parte "detected"
        name_metadata = magazine_name_part.split("_")
        result = {}
        result['magazine_name'] = "_".join(name_metadata[2:])
        result['page_index'] = name_metadata[1] 
        return result

    def __repr__(self):
        return f"<MagazineImage magazine_name={self.magazine_name} page_index={self.page_index}>"
