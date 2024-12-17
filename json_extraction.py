import requests
import json

# Custom Vision endpoint and prediction key
endpoint = "https://australiaeast.api.cognitive.microsoft.com/"  # Replace with your endpoint
prediction_key = "69c7cdcb3ea549d484ad20b632919823"  # Replace with your Prediction Key
project_id = "d7b27113-f02a-4f82-98b5-6ae4b14d494c"  # Replace with your Project ID
iteration_name = "Iteration 2"  # Replace with your Iteration Name

# Local image path
image_path = r"C:\\Users\\SQ488TD\\OneDrive - EY\\Desktop\\test-images-1\\dirty\\dirty14.jpeg"  # Replace with your image path

# Custom Vision prediction URL
# prediction_url = f"{endpoint}/customvision/v3.0/Prediction/{project_id}/detect/iterations/{iteration_name}/image"
prediction_url = "https://australiaeast.api.cognitive.microsoft.com/customvision/v3.0/Prediction/d7b27113-f02a-4f82-98b5-6ae4b14d494c/detect/iterations/Iteration2/image"

headers = {
    'Prediction-Key': prediction_key,
    'Content-Type': 'application/octet-stream'
}

try:
    # Read the image file
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Make the API request
    res = requests.post(prediction_url, headers=headers, data=image_data)

    # Debugging: Print the response content in case of an error
    if res.status_code != 200:
        print(f"Error: {res.status_code}")
        print(res.text)

    res.raise_for_status()

    # Get the JSON response
    analysis = res.json()

    # Save the JSON response to a file
    with open('custom_vision_results.json', 'w') as json_file:
        json.dump(analysis, json_file, indent=4)

    print("Custom Vision results saved to custom_vision_results.json")

    # Extract bounding box parameters
    if 'predictions' in analysis:
        for prediction in analysis['predictions']:
            tag_name = prediction['tagName']
            probability = prediction['probability']
            bounding_box = prediction['boundingBox']
            left = bounding_box['left']
            top = bounding_box['top']
            width = bounding_box['width']
            height = bounding_box['height']
            print(f"Tag: {tag_name}, Probability: {probability}")
            print(f"Bounding Box: left={left}, top={top}, width={width}, height={height}")
    else:
        print("No objects detected.")

except FileNotFoundError:
    print(f"File not found: {image_path}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API request: {e}")
