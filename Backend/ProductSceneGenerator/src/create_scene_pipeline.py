import torch
from diffusers import AutoPipelineForInpainting
from diffusers.utils import load_image, make_image_grid
from diffusers import StableDiffusionInpaintPipeline

def create_scene_pipeline():
    """
    Create a Stable Diffusion Inpainting pipeline.

    This function initializes a Stable Diffusion Inpainting pipeline from the pre-trained model.
    It checks if a CUDA-enabled GPU is available and uses it if possible; otherwise, it defaults to CPU.

    Returns:
        StableDiffusionInpaintPipeline: The initialized inpainting pipeline ready for generating scenes.

    Raises:
        Exception: If there is an error during the pipeline creation.
    """
    try:
        # Load the Stable Diffusion Inpainting pipeline
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-inpainting",
            torch_dtype=torch.float16,
        )

        # Move the pipeline to the appropriate device
        if torch.cuda.is_available():
            pipe.to("cuda")  # Move the pipeline to GPU
        else:
            pipe.to("cpu")  # Use CPU if GPU is not available

        return pipe

    except Exception as e:
        raise Exception(f"An error occurred while creating the scene generation pipeline: {e}")
