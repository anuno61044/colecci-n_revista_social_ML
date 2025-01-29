import json
import os
from prefect import flow
from common.social_model import SocialModel, get_blip, get_clip, get_combined_1, get_combined_2, get_tuned_blip, get_tuned_clip

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
    hyperparams_id = os.environ.get('SOCIAL_HYPER_ID')
    model_id = os.environ.get('SOCIAL_MODEL')

    if hyperparams_id == None:
        raise Exception("Hyperparameters id cannot be none")

    model_id = 0 if model_id == None else model_id

    model : SocialModel = None
    if model_id == '0':
        model = get_blip()  
    elif model_id == '1':
        model = get_tuned_blip()
    elif model_id == '2':
        model_id = get_clip()
    elif model_id == '3':
        model = get_tuned_clip()
    elif model_id == '4':
        model = get_combined_1()
    elif model_id == '5':
        model = get_combined_2()

    # Extract images from json
    images = []
    generated_captions = [model.caption(image) for image in images]

    with open(f'../../external/results{hyperparams_id}.json', 'w') as file:
        file.write(json.dumps(generated_captions))
    pass

@flow
def pipeline():
    params_list: list[dict[str, str]]
    with open('../../external/combinations.json', 'r') as file:
        params_list = json.load(file)

    for i, params in enumerate(params_list):
        print(f'Start batch {i}')
        os.environ['SOCIAL_HYPER_ID'] = F'{i}'
        for key, value in params.items():
            os.environ[key] = f'{value}'
        
        print('Extract images')
        extract_images_flow()

        if os.environ.get('SOCIAL_CLEANING') == '1':
            print('Clean data')
            clean_data_flow()

        print('Select model')
        select_model_flow()
        print(f'End batch {i}')

if __name__ == '__main__':
    pipeline()
