# Image analysis using ollama-vision3.2

## Deployment
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

Returns:
```
{
  "power_button_color": "red"
}
```
when the water heater has a problem, for instance.