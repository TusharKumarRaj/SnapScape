from flask import Flask, request, jsonify
from flask_cors import CORS  # To enable CORS for your Flutter app
import os
import base64
from datetime import datetime
from pathlib import Path
from src.remove_background import remove_background
from src.create_image_canvas import create_image_canvas
from src.generate_mask import create_mask
from src.create_scene_pipeline import create_scene_pipeline
from src.generate_scene import generate_scene
from src.create_video_pipeline import create_video_pipeline
from src.generate_video import generate_video

app = Flask(__name__)
CORS(app)  # Allow requests from any origin


# Main image processing function that includes the entire pipeline
def generate_image(image_path, text_prompt):
    try:
        image_name = Path(image_path).stem  # Get the file name without extension
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Create a timestamp
        output_path = f"Results/{image_name}_{timestamp}"  # Create output path as a string
        os.makedirs(output_path, exist_ok=True)  # Create the output directory

        # Step 1: Remove background
        no_bg_path = remove_background(image_path, output_path)

        # Step 2: Generate mask
        canvas = create_image_canvas(no_bg_path)
        print("Image Canvas Created Successfully!")
        mask = create_mask(canvas)
        print("Mask Created Successfully!")

        # Step 3: Create scene pipeline
        scene_pipeline = create_scene_pipeline()
        print("Scene Generation Pipeline Created Successfully!")

        # Step 4: Generate scene
        scene = generate_scene(text_prompt, canvas, mask, output_path)
        print("Scene Generated Successfully!")

        return scene  # Return the generated scene file path

    except Exception as e:
        print(f"Error in generate_image: {e}")
        raise


# Flask API route to process the image and return the generated scene
@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Get the JSON data from the request
        data = request.json
        image_data = data['image']
        text = data['text']

        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data.split(",")[1])

        # Save the image temporarily
        with open("temp_image.png", "wb") as temp_image:
            temp_image.write(image_bytes)

        # Call the function to generate the scene image
        resultant_image_path = generate_image("/home/tusharkumarraj/SnapScape/Backend/ProductSceneGenerator/temp_image.png", text)

        # Load the resultant image and encode it to base64
        with open(resultant_image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

        # Return the encoded image as JSON response
        return jsonify({'result_image': f'data:image/png;base64,{encoded_string}'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
