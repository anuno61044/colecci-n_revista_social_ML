import os
from prefect import flow
from common.social_model import SocialModel, get_blip, get_tuned_blip

@flow
def extract_images_flow():
    # Valida que existe la base de datos ya creada
    pass

@flow
def clean_data_flow():
    # Limpia la base de datos
    pass

@flow
def select_model_flow():
    hyperparams_id = os.environ['SOCIAL_HYPER_ID']
    model_id = os.environ['SOCIAL_MODEL']

    model : SocialModel = None
    if model_id == '0':
        model = get_blip()  
    elif model_id == '1':
        model = get_tuned_blip()

    # Extract images from json
    images = []
    generated_captions = [model.caption(image) for image in images]

    # Store into json the results

    pass

@flow
def pipeline():

    extract_images_flow()
    clean_data_flow()
    select_model_flow()

if __name__ == '__main__':
    pipeline()
