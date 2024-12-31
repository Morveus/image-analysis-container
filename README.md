# Image analysis using ollama-vision3.2
## Context
This is a simple Flask application that uses ollama-vision3.2 to analyze images.

It is meant to run on my cluster, and be called periodically to check on various equipment in my home.

My motivation to build this was that I often have issues with the grid, and my water heater goes into safe mode. 
Which we don't realize until we have to shower, the water is cold, and we're late for work. Fixing it is as simple as cutting power to the device, waiting a bit and powering it back on. Now thanks to AI, I can get a notification when it happens.

## Deployment
An image is available on my docker hub repository: `https://hub.docker.com/r/morveus/ollama-image-analysis`

You need to provide the following environment variable:
- OLLAMA_HOST: The host and port of the Ollama server (default: http://localhost:11434)

# Example curl command to check if my water heater is working
## The image comes from a camera in the same room

```
curl -X POST http://host:5000/analyze \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Analyze this image and describe the state of the water heater.",
  "camera_feed": "rtsps://192.168.1.x:xxx/feed",
  "model": "llama3.2-vision",
  "schema": {
    "power_button_color": {"type": "Literal", "args": ["red", "green", "off"]},
  }
}'
```

## Details
- prompt: The prompt to send to the Ollama server. 
- camera_feed: The RTSP stream of the camera (it will take a snapshot to analyse)
- model: The model to use for the analysis (default: llama3.2-vision)
- schema: The schema to use for the analysis. It is a JSON object that defines the structure of the data that will be returned by the analysis.

Returns:
```
{
  "power_button_color": "red"
}
```
when the water heater has a problem, for instance.