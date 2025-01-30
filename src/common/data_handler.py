import os

import pandas as pd
from sqlalchemy import create_engine

_image_path = "image_path"
_surrounding_text = "related_text"
_base_path = "../../../external/dataset/images"
_chunk_size = 1

def process_images_k_by_k(database_path):
    engine = create_engine(database_path)
    query = "SELECT * FROM ImageData"
    for chunk in pd.read_sql(query, engine, chunksize=_chunk_size):
        for _, row in chunk.iterrows():
            image_path = row[_image_path]
            image_path = image_path.replace("\\", "/")
            image_name = os.path.basename(image_path)
            new_image_path = os.path.join(_base_path, image_name)
            yield new_image_path, str(row[_surrounding_text])

def get_image_captions(image_id, database_path = "sqlite:///../../../external/dataset/metadata.db"):
    engine = create_engine(database_path)
    query = f"SELECT image_path, related_text FROM ImageData WHERE image_id = '{image_id}'"
    result = pd.read_sql(query, engine)

    if not result.empty:
        image_path = result.iloc[0][_image_path]
        surrounding_text = result.iloc[0][_surrounding_text]
        return image_path, surrounding_text
    else:
        return None, None