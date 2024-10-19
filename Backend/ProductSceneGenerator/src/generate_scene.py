from PIL import Image
import os

def generate_scene(pipe, prompt, canvas, mask, output_path):
    """
    Generate a scene image based on the provided prompt, canvas, and mask.

    This function uses the Stable Diffusion pipeline to create a scene image by combining
    the given canvas and mask images. The generated image is saved to the specified output path.

    Args:
        pipe (StableDiffusionInpaintPipeline): The Stable Diffusion Inpainting pipeline.
        prompt (str): The text prompt describing the scene to generate.
        canvas (Image): A PIL Image object representing the canvas image.
        mask (Image): A PIL Image object representing the mask image.
        output_path (str): The directory where the generated scene will be saved.

    Returns:
        Image: The generated scene image.

    Raises:
        Exception: If there is an error during scene generation or saving the image.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Get the dimensions of the canvas
        scene_height, scene_width = canvas.size

        # Make height and width divisible by 8
        scene_height -= (scene_height % 8)
        scene_width -= (scene_width % 8)

        # Generate the scene image using the pipeline
        scene_image = pipe(
            prompt=prompt,
            image=canvas,
            mask_image=mask,
            num_inference_steps=200,
            height=scene_height,
            width=scene_width
        ).images[0]

        # Save the generated image
        output_file_path = os.path.join(output_path, "scene.jpg")
        scene_image.save(output_file_path)

        return scene_image

    except Exception as e:
        raise Exception(f"An error occurred while generating the scene: {e}")
