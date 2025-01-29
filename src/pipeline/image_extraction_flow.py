import os
from prefect import flow


@flow
def extract_images_flow():
    db = os.listdir("./external/dataset/data/output")
    if len(db != 0):
        return db[0]
    
    command = [
        'python',
        './image_text_sync/main.py',
        './external/dataset/data/pdfs',
        './external/dataset/data/images',
        './external/dataset/data/captions',
        './external/dataset/data/output/.db'
    ]
    try:
        subprocess.run(command, check=True, text=True, capture_output=True)
        db = os.listdir("./external/dataset/data/output")
        return db[0]

    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando")
        print(e.stderr)