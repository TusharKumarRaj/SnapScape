import torch
from diffusers import StableVideoDiffusionPipeline


def create_video_pipeline():
    """
    Create and return a Stable Video Diffusion pipeline.

    This function initializes the Stable Video Diffusion pipeline with the specified
    pretrained model and sets it to use float16 precision. It also enables model CPU offloading
    to optimize memory usage.

    Returns:
        StableVideoDiffusionPipeline: The initialized Stable Video Diffusion pipeline.
    """
    try:
        # Load the Stable Video Diffusion pipeline
        pipeline = StableVideoDiffusionPipeline.from_pretrained(
            "stabilityai/stable-video-diffusion-img2vid-xt",
            torch_dtype=torch.float16,
            variant="fp16"
        )

        # Enable model CPU offloading
        pipeline.enable_model_cpu_offload()

        return pipeline

    except Exception as e:
        raise Exception(f"An error occurred while generating the video pipeline: {e}")
