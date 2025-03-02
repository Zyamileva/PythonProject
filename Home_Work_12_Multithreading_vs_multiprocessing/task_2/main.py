import glob
import os

from PIL import Image, ImageFilter

INPUT_IMG = "Input"

FOLDER_IMG = "Processing"

parent_folder = os.path.abspath(
    os.path.join(os.getcwd(), "..")
)

input_folder = os.path.join(parent_folder, INPUT_IMG)

correct_folder = os.path.join(parent_folder, FOLDER_IMG)

NEW_SIZE = (300, 300)


list_img = glob.glob(f"{input_folder}/*.jpg")

input_img = [os.path.abspath(f) for f in list_img]


os.makedirs(correct_folder, exist_ok=True)


def processing_images(image_path):
    """Processes and saves an image.

    Args:
        image_path: The path to the image file.
    """

    img = Image.open(image_path)

    img = img.resize(NEW_SIZE)
    img = img.filter(ImageFilter.GaussianBlur(2))

    output_path = os.path.join(correct_folder, os.path.basename(image_path))
    print(output_path)
    img.save(output_path)


for img in input_img:
    processing_images(img)
