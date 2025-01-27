import os
import sqlite3
from typing import List

class ResultSaver:
    def __init__(self, db_path: str):
        self.db_path = db_path
        db_directory = os.path.dirname(self.db_path)
        if db_directory and not os.path.exists(db_directory):
            os.makedirs(db_directory, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ImageData (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    magazine_name TEXT NOT NULL,
                    caption TEXT,
                    page_index INTEGER NOT NULL,
                    image_path TEXT NOT NULL,
                    related_pages TEXT NOT NULL,
                    related_text TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def save_image_data(self, magazine_name: str, page_index: int, image_path: str, related_pages: List[int], related_text: str, caption: List[str]):
        related_pages_str = ",".join(map(str, related_pages)) 
        captions = ",".join(map(str, caption)) 

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ImageData (magazine_name, page_index, image_path, related_pages, related_text, caption)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (magazine_name, page_index, image_path, related_pages_str, related_text.strip(), captions)
            )
            conn.commit()

    def count_images_with_caption(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ImageData WHERE caption IS NOT NULL AND caption != ''")
            count = cursor.fetchone()[0]
        return count