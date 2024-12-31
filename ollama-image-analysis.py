from flask import Flask, request, jsonify
from pydantic import BaseModel, create_model
from pathlib import Path
from typing import Literal
import cv2
from ollama import Client
import os

app = Flask(__name__)

# Define the route for the web server
@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        # Parse the JSON input
        data = request.json
        prompt = data.get("prompt")
        camera_feed = data.get("camera_feed")
        schema_definition = data.get("schema", {})
        model_name = data.get("model", "llama3.2-vision")

        # Validate inputs
        if not prompt or not camera_feed or not schema_definition:
            return jsonify({"error": "Missing prompt, camera_feed, or schema"}), 400

        # Open the video capture
        cap = cv2.VideoCapture(camera_feed)
        if not cap.isOpened():
            return jsonify({"error": "Unable to open the RTSPS stream"}), 500

        # Read a single frame
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return jsonify({"error": "Unable to capture a frame from the camera feed"}), 500

        # Save the frame as an image
        snapshot_filename = "snapshot.jpg"
        cv2.imwrite(snapshot_filename, frame)

        # Dynamically create the schema using Pydantic
        allowed_types = {"Literal": Literal, "str": str, "int": int, "float": float, "bool": bool}
        fields = {}
        for key, value in schema_definition.items():
            field_type = allowed_types[value['type']]  # Use allowed_types to map type strings to actual types
            field_args = tuple(value.get('args', []))
            fields[key] = (field_type if not field_args else field_type[field_args], None)

        DynamicImageDescription = create_model("DynamicImageDescription", **fields)

        # Use the client to analyze the image
        client = Client(host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'))
        response = client.chat(
            model=model_name,
            format=DynamicImageDescription.model_json_schema(),
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [Path(snapshot_filename)],
                },
            ],
            options={'temperature': 0},
        )

        # Parse the response into the dynamically created schema
        image_analysis = DynamicImageDescription.model_validate_json(response.message.content)

        # Return the analysis as JSON
        return jsonify(image_analysis.dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)