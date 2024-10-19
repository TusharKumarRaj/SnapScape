from rembg import remove
from PIL import Image
import io
import os


def remove_background(input_path, output_path):
    """
    Remove the background from an image.

    This function takes an input image file path, removes its background using the
    rembg library, and saves the output image with the background removed. The output
    file is saved in PNG format and is named according to the input filename, with
    '_no_bg' appended before the file extension.

    Args:
        input_path (str): The path to the input image file with the background.
        output_path (str): The directory where the output image should be saved.

    Returns:
        str: The path to the output image file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: If there is an error during background removal or saving the image.
    """
    # Check if the input file exists
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"The input file '{input_path}' does not exist.")

    # Get the filename without extension
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)

    # Construct output filename
    output_filename = f"{name}_no_bg.png"
    output_file_path = os.path.join(output_path, output_filename)

    try:
        # Load the image
        with open(input_path, "rb") as file:
            input_image = file.read()

        # Remove the background
        output_image = remove(input_image)

        # Save the output image
        with open(output_file_path, "wb") as out_file:
            out_file.write(output_image)

    except Exception as e:
        raise Exception(f"An error occurred while processing the image: {e}")

    return output_file_path
