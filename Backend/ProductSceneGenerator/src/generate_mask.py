import rembg
import numpy as np
from PIL import Image,ImageOps

def create_mask(canvas_image):
    """
    Create a mask from the canvas image.

    This function takes a canvas image containing a product and creates a mask by effectively making the product black while leaving the background white.
    The output mask can be used for further processing, such as generating a background.

    Args:
        canvas_image (Image): A PIL Image object containing the product on a white canvas.

    Returns:
        Image: The inverted mask image where the product is black and the background is white.

    Raises:
        Exception: If there is an error during mask creation or processing.
    """
    try:
        # Convert the input canvas image to a numpy array
        input_array = np.array(canvas_image)

        # Extract mask using rembg
        mask_array = rembg.remove(input_array, only_mask=True)

        # Create a PIL Image from the output array
        mask_image = Image.fromarray(mask_array)

        # Invert the mask image
        mask_image_inverted = ImageOps.invert(mask_image)

        return mask_image_inverted

    except Exception as e:
        raise Exception(f"An error occurred while creating the mask: {e}")
