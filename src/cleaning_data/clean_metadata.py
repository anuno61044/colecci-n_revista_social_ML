import pandas as pd
from sqlalchemy import create_engine
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import torch
import lorem

def clone_database():
    # Conectar a la base de datos original
    engine_original = create_engine('sqlite:///./external/dataset/metadata.db')

    # Conectar a la base de datos clonada
    engine_copia = create_engine('sqlite:///./external/dataset/clean_metadata.db')

    # Obtener los nombres de las tablas
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", engine_original)

    # Recorrer cada tabla y copiarla a la nueva base de datos
    for table in tables['name']:
        df = pd.read_sql(f"SELECT * FROM {table};", engine_original)  # Leer la tabla original
        df.to_sql(table, engine_copia, if_exists='replace', index=False)  # Guardar en la nueva BD

    print("Base de datos clonada exitosamente.")

def clean_database():

    clone_database()

    # Conectar a la base de datos
    engine = create_engine('sqlite:///./external/dataset/clean_metadata.db')

    # Leer los datos
    metadata_df = pd.read_sql('ImageData', engine)

    # Recorrer las filas verificando si caption es NULL o vacío
    for index, row in metadata_df.iterrows():
        image_path = row['image_path']
        caption = row['caption']
        
        if not pd.isna(caption):
        
            # Definir el image_path que queremos modificar y el nuevo caption
            image_path_to_modify, new_caption = evaluate_caption(image_path, caption)

            # Modificar el caption en el DataFrame
            metadata_df.loc[metadata_df['image_path'] == image_path_to_modify, 'caption'] = new_caption
            
            # Guardar los cambios en la base de datos
            metadata_df.to_sql('ImageData', engine, if_exists='replace', index=False)
            
def evaluate_caption(image_path, caption):

    if caption is '':
        return caption

    # Cargar el modelo y el procesador de CLIP
    model_name = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(model_name)
    processor = CLIPProcessor.from_pretrained(model_name)

    # Lista de captions
    captions = [caption]

    for i in range(5):
        captions.append(lorem.sentence())

    # Cargar y procesar la imagen
    imagen = Image.open(image_path)
    inputs = processor(text= captions, images= [imagen]*len(captions), return_tensors="pt", padding=True)

    # Generar embeddings
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)  # Convertir a probabilidades

    # Ordenar los captions y probabilidades en orden decreciente
    captions_prob = list(zip(captions, probs[0]))
    captions_prob.sort(key=lambda x: x[1], reverse=True)

    # Mostrar los captions y probabilidades ordenadas
    # for caption, prob in captions_prob:
    #     print(f"Caption: {caption} - Probabilidad: {prob:.4f}")

    if caption != captions_prob[0][0]:
        print("Cambio de - ", caption)
        return ''
    else:
        return caption
