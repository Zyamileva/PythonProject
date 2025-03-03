import glob
import logging
import os

from PIL import Image, ImageFilter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

INPUT_IMG = "Input"

FOLDER_IMG = "Processing"

NEW_SIZE = (300, 300)

parent_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))

input_folder = os.path.join(parent_folder, INPUT_IMG)

correct_folder = os.path.join(parent_folder, FOLDER_IMG)

os.makedirs(correct_folder, exist_ok=True)

list_img = glob.glob(f"{input_folder}/*.jpg")

input_img = [os.path.abspath(f) for f in list_img]


def processing_images(image_path: str) -> None:
    """Processes and saves an image.

    Args:
        image_path: Path to the image file.

    Raises:
        FileNotFoundError: If the input image file is not found.
        OSError: If any error occurs during image processing or saving.
    """

    output_path = os.path.join(correct_folder, os.path.basename(image_path))

    try:
        if os.path.exists(output_path):
            logging.info(f"Файл {output_path} уже существует, пропускаем обработку.")
            return

        with Image.open(image_path) as img:
            img = img.resize(NEW_SIZE)
            img = img.filter(ImageFilter.GaussianBlur(2))
            img.save(output_path)
            logging.info(f"Файл сохранён: {output_path}")

    except FileNotFoundError:
        logging.error(f"Файл не найден: {image_path}")
    except OSError as e:
        logging.error(f"Ошибка обработки {image_path}: {e}")


for img in input_img:
    processing_images(img)

logging.info("Все изображения обработаны.")
