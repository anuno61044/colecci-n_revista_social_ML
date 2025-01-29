import json
import os
from prefect import flow

from common.social_model import SocialModel, get_blip, get_clip, get_combined_1, get_combined_2, get_tuned_blip, get_tuned_clip


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
        # model = get_tuned_blip()
        pass
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

    with open(f'../../external/results/results{hyperparams_id}.json', 'w') as file:
        file.write(json.dumps(generated_captions))
    pass
