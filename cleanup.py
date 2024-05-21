import os
import shutil

def clean_duplicates():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_images_dir = os.path.join(base_dir, 'static', 'images')
    media_images_dir = os.path.join(base_dir, 'media', 'images')

    if os.path.exists(static_images_dir):
        for filename in os.listdir(static_images_dir):
            static_file_path = os.path.join(static_images_dir, filename)
            media_file_path = os.path.join(media_images_dir, filename)

            if os.path.exists(media_file_path):
                os.remove(static_file_path)
            else:
                shutil.move(static_file_path, media_file_path)

if __name__ == "__main__":
    clean_duplicates()