import json
import os
from prefect import flow

from pipeline.data_cleaning_flow import clean_data_flow
from pipeline.image_extraction_flow import extract_images_flow
from pipeline.model_selection_flow import select_model_flow

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
