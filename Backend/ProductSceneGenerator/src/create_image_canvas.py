from PIL import Image
import os

def create_image_canvas(no_bg_path):
    """
    Create a large white canvas and place the product image on it.

    This function takes an input image file path (a product image with a removed background),
    and creates a larger white canvas. The product image is pasted onto the center of the canvas,
    allowing for additional background generation around the product.

    Args:
        no_bg_path (str): The path to the product image file with the background removed.

    Returns:
        Image: The final image with the product placed on a white canvas.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: If there is an error during image processing.
    """
    # Check if the input file exists
    if not os.path.isfile(no_bg_path):
        raise FileNotFoundError(f"The input file '{no_bg_path}' does not exist.")

    try:
        # Load the product image (PNG file with transparency)
        product_img = Image.open(no_bg_path).convert("RGBA")  # Ensure it's in RGBA mode to handle transparency

        # Get the size of the product image
        product_width, product_height = product_img.size

        # Define the size of the new larger image (for example, 2x the size of the product image)
        new_width = product_width * 2
        new_height = product_height * 2

        # Create a new white background image (RGBA mode, to retain alpha channel)
        canvas = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))  # White background with full opacity

        # Calculate the position to center the product image
        x_offset = (new_width - product_width) // 2
        y_offset = (new_height - product_height) // 2

        # Paste the product image onto the center of the white background, using the product's alpha channel
        canvas.paste(product_img, (x_offset, y_offset), product_img)  # Use the product_img itself as the mask

        return canvas

    except Exception as e:
        raise Exception(f"An error occurred while creating the image canvas: {e}")
