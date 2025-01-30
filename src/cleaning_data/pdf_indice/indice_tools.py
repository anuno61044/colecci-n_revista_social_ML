import re
import fitz  # PyMuPDF
import pickle

def save_indice_data_by_page(num_page):
    '''
        Guardar la información del Índice Analítico relacionada con las imágenes y sus nombres.
        
        Estará guardada en un array formado por arrays `a` con la siguiente estructura:
        - a[0] : Id
        - a[1] : Autor
        - a[2] : Título
        - a[3] : Año de vida de la publicación
        - a[4] : Número de entrega
        - a[5] : Paginación
        - a[6] : Fecha de la publicación
    '''
    
    pattern = r'([1-9]\d*)[\.|\s]+(\s|[A-Z|Á|É|Í|Ó|Ú|á|é|í|ó|ú][A-Z|,| |Á|É|Í|Ó|Ú|á|é|í|ó|ú]+)\.\s([^\.]*)\.[\s]+([1-9]\d*)[ ]?\(([1-9]\d*)\)[\s]*:[\s]*([1-9][\d|\-|,| ]*)\s+[^\']+[\s|\']+([1-9]\d*)'

    documento = fitz.open('./src/indice_manager/Índice analítico de la revista Social, 1916-1938.pdf')
    page = documento.load_page(num_page)
    text = page.get_text()

    partes = re.findall(pattern, text, re.DOTALL)

    # partes = ['. '.join([str(e).replace('\n',' ') for e in parte if e != '\n']) for parte in partes]

    pictures_data = []

    for parte in partes:
        new_line = []
        for string in parte:
            if string != '\n':
                new_line.append(str(string).replace('\n',''))
            else:
                new_line.append('unknown')
        if new_line[2] == 'unknown':
            continue
        pictures_data.append(new_line)
    
    # print('\n', text, '\n')
    return pictures_data
    
def save_indice_data():
    
    indice_data = []
    
    for i in range(5,299):
        indice_data = indice_data + save_indice_data_by_page(i)
    
    with open('./src/indice_manager/indice_data.pkl', 'wb') as archivo:
        pickle.dump(indice_data, archivo)

    # for e in indice_data:
    #     print(e)
    #     print('----')
    
def load_indice_data():
    '''
        Carga la información del archivo pickle
        
        Estará guardada en un array formado por arrays `a` con la siguiente estructura:
        - a[0] : Id
        - a[1] : Autor
        - a[2] : Título
        - a[3] : Año de vida de la publicación
        - a[4] : Número de entrega (mes)
        - a[5] : Paginación
        - a[6] : Fecha de la publicación

        Las rutas de las imágenes en la base de datos están guardadas con esta propiedad:
            
            path: 'imagen_${a[5]}_ohcbh_ch_social19${a[6]}_2_v1_n2_0_detected_0_0_fotos_0.95.jpg'
    '''
    
    # Cargar el array desde el archivo
    with open('./src/indice_manager/indice_data.pkl', 'rb') as archivo:
        indice_data = pickle.load(archivo)
    
    # for e in indice_data[:10]:
    #     print(e)
    #     print('----')
        
    return indice_data
