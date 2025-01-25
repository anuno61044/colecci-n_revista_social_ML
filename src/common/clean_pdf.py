import fitz  # PyMuPDF
import os

def extraer_imagenes_pdf(ruta_pdf, carpeta_destino="imagenes"):
    """
    Extrae todas las imágenes de un PDF y las guarda en una carpeta.

    Args:
        ruta_pdf: La ruta al archivo PDF.
        carpeta_destino: La ruta a la carpeta donde se guardarán las imágenes. Se crea si no existe.
    """
    os.makedirs(carpeta_destino, exist_ok=True)

    try:
        doc = fitz.open(ruta_pdf)
        for page_num in range(doc.page_count):
            page = doc[page_num]
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                ext = base_image["ext"]
                filename = os.path.join(carpeta_destino, f"imagen_{page_num}_{os.path.splitext(os.path.basename(ruta_pdf))[0]}_{img_index}.{ext}") # Cambiado el nombre del archivo
                
                with open(filename, "wb") as file:
                    file.write(image_bytes)
                print(f"Imagen extraída y guardada como: {filename}")

    except fitz.fitz.EmptyFileError:
        print(f"Error: El archivo PDF '{ruta_pdf}' está vacío.")
    except FileNotFoundError:
        print(f"Error: El archivo PDF '{ruta_pdf}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")



def procesar_pdfs_en_carpeta(carpeta_pdfs, carpeta_destino="imagenes"):
    """
    Procesa todos los archivos PDF en una carpeta y extrae sus imágenes.

    Args:
        carpeta_pdfs: La ruta a la carpeta que contiene los archivos PDF.
        carpeta_destino: La ruta a la carpeta donde se guardarán las imágenes. Se crea si no existe.
    """
    for filename in os.listdir(carpeta_pdfs):
        if filename.lower().endswith(".pdf"):  # Asegura que solo se procesen archivos .pdf
            ruta_pdf = os.path.join(carpeta_pdfs, filename)
            print(f"Procesando: {ruta_pdf}")
            extraer_imagenes_pdf(ruta_pdf, carpeta_destino)
            print(f"Procesado el archivo {ruta_pdf}")
        else:
            print(f"El archivo {filename} no es un PDF, se omite.")

# Ejemplo de uso:
carpeta_pdfs = "PDF"  # Reemplazar con la ruta a la carpeta con PDFs
procesar_pdfs_en_carpeta(carpeta_pdfs)
