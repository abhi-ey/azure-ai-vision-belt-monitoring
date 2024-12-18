import requests
import json
from PIL import Image
import io
import os

# Connect to Azure endpoint through https and subscription key
endpoint = "https://australiaeast.api.cognitive.microsoft.com/"
sub_key = "69c7cdcb3ea549d484ad20b632919823"

# Local image path
image_path = r"C:\Users\DY773VE\OneDrive - EY\Desktop\azure-ai-vision-belt-monitoring\tape_chair.jpeg"

# Ensure the API version is correct
analyze_url = endpoint + "vision/v3.2/analyze"

headers = {
    'Ocp-Apim-Subscription-Key': sub_key,
    'Content-Type': 'application/octet-stream'
}

params = {
    'visualFeatures': 'Objects,Tags,Categories'
}

# Resize the image (optional)
with Image.open(image_path) as img:
    #img = img.resize((800, 800))  # Resize to 800x800 pixels
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    image_data = img_byte_arr.getvalue()

# Make the API request
res = requests.post(analyze_url, headers=headers, params=params, data=image_data)

# Debugging: Print the response content in case of an error
if res.status_code != 200:
    print(f"Error: {res.status_code}")
    print(res.text)

res.raise_for_status()

# Get the JSON response
analysis = res.json()

# Save the JSON response to a file
with open('object_detection_results.json', 'w') as json_file:
    json.dump(analysis, json_file, indent=4)

print("Object detection results saved to object_detection_results.json")

# Extract bounding box parameters
if 'objects' in analysis:
    for obj in analysis['objects']:
        object_type = obj['object']
        confidence = obj['confidence']
        rectangle = obj['rectangle']
        x = rectangle['x']
        y = rectangle['y']
        w = rectangle['w']
        h = rectangle['h']
        print(f"Object: {object_type}, Confidence: {confidence}")
        print(f"Bounding Box: x={x}, y={y}, width={w}, height={h}")
else:
    print("No objects detected.")
