import os

class MagazineImage:
    def __init__(self, path: str): 
        self.path = path
        image_file_name = os.path.basename(path)
        
        detected_index = image_file_name.find("detected")
        if detected_index == -1:
            raise ValueError(f"The file '{image_file_name}' does not contain the expected 'detected' keyword.")

        magazine_name_part = image_file_name[:detected_index-3]
        
        # Obtener el nombre de la revista (todo lo que hay antes del primer número después del "_")
        # Buscamos el primer dígito que aparece después de la parte "detected"
        name_metadata = magazine_name_part.split("_")
        
        self.magazine_name = "_".join(name_metadata[2:])
        # Empieza desde el segundo elemento después de "imagen_"
        self.page_index = name_metadata[1]  # El primer número en el nombre del archivo es el índice de la página

    def __repr__(self):
        return f"<MagazineImage magazine_name={self.magazine_name} page_index={self.page_index}>"

# Ejemplo de uso
image_path = "imagen_0_ohcbh_ch_social1917_4_v2_n4_0_detected_0_0_fotos_0.95"
magazine_image = MagazineImage(image_path)
print(magazine_image)
