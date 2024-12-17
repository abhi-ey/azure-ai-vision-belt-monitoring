import requests
import json

endpoint = "https://australiaeast.api.cognitive.microsoft.com/"
prediction_key = "69c7cdcb3ea549d484ad20b632919823"
project_id = "d7b27113-f02a-4f82-98b5-6ae4b14d494c"
iteration_name = "Iteration2"

image_path = r"C:\\Users\\SQ488TD\\OneDrive - EY\\Desktop\\test-images-1\\dirty\\dirty14.jpeg"

prediction_url = f"{endpoint}/customvision/v3.0/Prediction/{project_id}/detect/iterations/{iteration_name}/image"

headers = {
    'Prediction-Key': prediction_key,
    'Content-Type': 'application/octet-stream'
}

try:
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    res = requests.post(prediction_url, headers=headers, data=image_data)

    if res.status_code != 200:
        print(f"Error: {res.status_code}")
        print(res.text)

    res.raise_for_status()

    analysis = res.json()

    threshold = 0.6
    filtered_predictions = [prediction for prediction in analysis.get('predictions', []) if prediction['probability'] > threshold]
    analysis['predictions'] = filtered_predictions

    with open('custom_vision_results.json', 'w') as json_file:
        json.dump(analysis, json_file, indent=4)

    print("Custom Vision results saved to custom_vision_results.json")

    if filtered_predictions:
        for prediction in filtered_predictions:
            tag_name = prediction['tagName']
            probability = prediction['probability']
            bounding_box = prediction['boundingBox']
            left = bounding_box['left']
            top = bounding_box['top']
            width = bounding_box['width']
            height = bounding_box['height']
            print(f"Tag: {tag_name}, Probability: {probability}")
            print(f"Bounding Box: left={left}, top={top}, width={width}, height={height}")
            print(" ")
    else:
        print("No objects detected above the threshold.")

except FileNotFoundError:
    print(f"File not found: {image_path}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API request: {e}")
