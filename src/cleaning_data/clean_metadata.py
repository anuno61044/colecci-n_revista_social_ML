import pandas as pd
from sqlalchemy import create_engine, text
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import torch
import lorem
import os
import sqlite3

def clone_database():
    # Conectar a la base de datos original
    engine_original = create_engine('sqlite:///./external/dataset/metadata.db')

    # Obtener las tablas de la base de datos original, excluyendo la tabla sqlite_sequence
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';", engine_original)

    # Leer los datos de cada tabla en un DataFrame
    dataframes = {}
    for table in tables['name']:
        dataframes[table] = pd.read_sql(f"SELECT * FROM {table}", engine_original)

    # Ver los primeros datos de una tabla (por ejemplo, la primera tabla)
    print(dataframes[tables['name'][0]].head())

    # Conectar a la base de datos clonada
    engine_copia = create_engine('sqlite:///./external/dataset/clean_metadata.db')

    # Escribir los DataFrames en la nueva base de datos
    for table, df in dataframes.items():
        df.to_sql(table, engine_copia, index=False, if_exists='replace')
    
    # Cerrar el engine y liberar los recursos
    engine_copia.dispose()
    
    print("Base de datos clonada exitosamente.")


# Cargar el modelo y el procesador de CLIP
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

def evaluate_caption(image_path, caption):

    if caption == '':
        return caption

    # Lista de captions
    captions = [caption[:70]]

    for i in range(5):
        captions.append(lorem.sentence())

    if image_path.startswith('.\data\detected_images_1\\'):
      new_image_path = image_path.replace('.\data\detected_images_1\\', '/external/dataset/data/detected_images_1/')
    else:
      new_image_path = image_path

    if not os.path.exists(new_image_path):
        return caption

    # Cargar y procesar la imagen
    imagen = Image.open(new_image_path)
    inputs = processor(text= captions, images= [imagen]*len(captions), return_tensors="pt", padding=True)

    # Generar embeddings
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)  # Convertir a probabilidades

    # Ordenar los captions y probabilidades en orden decreciente
    captions_prob = list(zip(captions, probs[0]))
    captions_prob.sort(key=lambda x: x[1], reverse=True)

    # # Mostrar los captions y probabilidades ordenadas
    # for caption, prob in captions_prob:
    #     print(f"Caption: {caption} - Probabilidad: {prob:.4f}")

    if caption != captions_prob[0][0]:
        # print(caption)
        # print("------------------")
        return ''
    else:
        return caption
            
def clean_database():

    clone_database()

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('./external/dataset/clean_metadata.db')
    cursor = conn.cursor()

    # Consultar las filas de la tabla ImageData
    cursor.execute('SELECT image_path, caption FROM ImageData')

    print('... Detectar malos captions ...')
    # Recorrer las filas una por una
    for row in cursor.fetchall():
        image_path = row[0]  # 'image_path' está en la primera columna
        caption = row[1]     # 'caption' está en la segunda columna
        if caption == '':
            continue
        new_caption = evaluate_caption(image_path, caption)
        if new_caption == caption:
            continue
        # Actualizar el caption en la base de datos para esta fila específica
        cursor.execute('''
            UPDATE ImageData
            SET caption = ?
            WHERE image_path = ?
        ''', (new_caption, image_path))

    # Guardar los cambios (commit) y cerrar la conexión
    conn.commit()
    conn.close()