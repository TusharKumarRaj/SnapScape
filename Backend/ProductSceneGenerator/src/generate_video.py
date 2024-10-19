import torch
from PIL import Image
from pathlib import Path
from diffusers.utils import load_image, export_to_video

def generate_video(video_pipeline, scene, output_path):
    """
    Generate a video from the given scene using the specified video pipeline.

    This function loads the conditioning image (scene), resizes it,
    and then generates a video using the video pipeline. The generated
    video is saved to the specified output path.

    Args:
        video_pipeline (StableVideoDiffusionPipeline): The Stable Video Diffusion pipeline for video generation.
        scene (Image): The path to the conditioning image (scene) to be used for video generation.
        output_path (str): The directory where the generated video will be saved.

    Returns:
        str: The path to the saved video file.

    Raises:
        Exception: If there is an error during video generation or saving the video.
    """
    try:
        # Load the conditioning image
        image = scene
        image = image.resize((854, 480))

        # Set the random seed for reproducibility
        generator = torch.manual_seed(42)

        # Generate frames from the video pipeline
        frames = video_pipeline(image, decode_chunk_size=8, generator=generator).frames[0]

        # Ensure the output directory exists
        Path(output_path).mkdir(parents=True, exist_ok=True)

        # Save the video
        output_file_path = Path(output_path) / "video.mp4"
        export_to_video(frames, output_file_path, fps=8)

        return str(output_file_path)

    except Exception as e:
        raise Exception(f"An error occurred while generating the video: {e}")
