import pandas as pd
from sqlalchemy import create_engine

_image_path = "image_path"
_surrounding_text = "related_text"

_chunk_size = 1

def process_images_k_by_k(database_path):
    engine = create_engine(database_path)
    query = "SELECT * FROM ImageData"
    for chunk in pd.read_sql(query, engine, chunksize=_chunk_size):
        for _, row in chunk.iterrows():
            yield str(row[_image_path]), str(row[_surrounding_text])
