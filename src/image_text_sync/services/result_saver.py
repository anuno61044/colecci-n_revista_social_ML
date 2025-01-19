import json
import os
from typing import List


class ResultSaver:
    def __init__(self, output_directory: str):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def save_image_data(self, magazine_name: str, page_index: int, image_path: str, related_pages: List[int], related_text: str):
        json_data = {
            "magazine": magazine_name,
            "image_page_index": page_index,
            "path_to_image": image_path,
            "related_text_pages": related_pages,
            "related_text": related_text.strip().encode('latin1', errors='ignore').decode('utf-8', errors='ignore')
        }

        magazine_output_dir = os.path.join(self.output_directory, magazine_name)
        os.makedirs(magazine_output_dir, exist_ok=True)
        output_path = os.path.join(magazine_output_dir, f"image_{page_index}.json")

        with open(output_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"Saved JSON for image {page_index} to {output_path}")
