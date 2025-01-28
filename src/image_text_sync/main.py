import os
from typing import Dict, List
from services.result_saver import ResultSaver
from services.pdf_reader import FitzPdfReader
from objects.magazine_image import MagazineImage
from objects.magazine import Magazine

class Main:
    def __init__(self, pdf_directory: str, img_directory: str, cap_directory: str, output_directory: str):
        self.pdf_directory = pdf_directory
        self.img_directory = img_directory
        self.cap_directory = cap_directory
        self.output_directory = output_directory
        self.result_saver = ResultSaver(output_directory)
        self.magazines: List[Magazine] = []
        self.images: List[MagazineImage] = []
        self.pdf_reader = FitzPdfReader()

    def load_data(self):
        if not os.path.isdir(self.pdf_directory):
            print(f"The route {self.pdf_directory} is not a valid folder.")
            return
        if not os.path.isdir(self.img_directory):
            print(f"The route {self.img_directory} is not a valid folder.")
            return
        if not os.path.isdir(self.cap_directory):
            print(f"The route {self.cap_directory} is not a valid folder.")
            return

        pdf_files = [file for file in os.listdir(self.pdf_directory) if file.endswith('.pdf')]
        img_files = [file for file in os.listdir(self.img_directory) if file.endswith('.jpg')]
        cap_files = [file for file in os.listdir(self.cap_directory) if file.endswith('.txt')]

        if not pdf_files:
            print("There is not any pdf in the specified route.")
            return

        if not img_files:
            print("There is not any image in the specified route.")
            return

        if not cap_files:
            print("There is not any captions in the specified route.")
            return

        for pdf_file in pdf_files:
            full_path = os.path.join(self.pdf_directory, pdf_file)
            print(f"Processing file: {full_path}")
            try:
                magazine = Magazine(full_path, self.pdf_reader)
                self.magazines.append(magazine)
                print(f"Creating magazine: {magazine.name} with {len(magazine.pages)} pages.")
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")

        for img_file in img_files:
            full_path = os.path.join(self.img_directory, img_file)
            print(f"Processing file: {full_path}")
            try:
                magazine_image = MagazineImage(full_path)
                for cap_file in cap_files:
                    cap_file_info = magazine_image.extract_info(cap_file)
                    if int(magazine_image.page_index) == int(cap_file_info['page_index']) and magazine_image.magazine_name.lower() == cap_file_info['magazine_name'].lower():
                        cap_full_path = os.path.join(self.cap_directory, cap_file)                        
                        with open(cap_full_path, 'r') as cap_file:
                            magazine_image.caption.append(cap_file.read())
                            break

                self.images.append(magazine_image)
                print(f"Adding image from magazine: {magazine_image.magazine_name} at page {magazine_image.page_index}.")
            except Exception as e:
                print(f"Error processing {img_file}: {e}")

    def associate_images_with_text(self, num_pages):
        for image in self.images:
            magazine = next((mag for mag in self.magazines if mag.name == image.magazine_name), None)
            if not magazine:
                print(f"Magazine {image.magazine_name} not found for image {image}")
                continue

            page_index = int(image.page_index)
            related_pages = [page_index, page_index + 1]

            related_text = ""
            for page in related_pages:
                if 0 <= page - 1 < len(magazine.pages):
                    for i in range(1, num_pages):
                        related_text += magazine.pages[page - i].text

            self.result_saver.save_image_data(
                magazine_name=magazine.name,
                page_index=page_index,
                image_path=image.path,
                related_pages=related_pages,
                related_text=related_text,
                caption=image.caption
            )

    def list_magazines(self):
        for magazine in self.magazines:
            print(f"Magazine: {magazine.name}, Páginas: {len(magazine.pages)}")

    def list_images(self):
        for magazine in self.images:
            print(f"Magazine: {magazine.magazine_name}, Páginas: {magazine.page_index}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_directory", type=str)
    parser.add_argument("img_directory", type=str)
    parser.add_argument("cap_directory", type=str)
    parser.add_argument("output_directory", type=str)
    args = parser.parse_args()

    route_to_pdf_files = args.pdf_directory
    route_to_img_files = args.img_directory
    route_to_cap_files = args.cap_directory
    route_to_output_files = args.output_directory

    main_app = Main(
        pdf_directory=route_to_pdf_files,
        img_directory=route_to_img_files,
        cap_directory=route_to_cap_files,
        output_directory=route_to_output_files
    )
    main_app.load_data()
    main_app.associate_images_with_text(1)
