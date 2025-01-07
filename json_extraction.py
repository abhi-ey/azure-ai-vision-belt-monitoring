import requests
import json
import sqlite3
from PIL import Image
import os
import argparse

parser = argparse.ArgumentParser(description='Process an Image with Azure Custom Vision and store results in SQLite.')
parser.add_argument('image_path', type=str, help='Path to image file')
parser.add_argument('--threshold', type=float, help='Probability threshold for filtering predictions')
args = parser.parse_args()


endpoint = "https://australiaeast.api.cognitive.microsoft.com/"
prediction_key = "69c7cdcb3ea549d484ad20b632919823"
project_id = "d7b27113-f02a-4f82-98b5-6ae4b14d494c"
iteration_name = "Iteration2"

image_path = args.image_path
threshold = args.threshold

prediction_url = f"{endpoint}/customvision/v3.0/Prediction/{project_id}/detect/iterations/{iteration_name}/image"

headers = {
    'Prediction-Key': prediction_key,
    'Content-Type': 'application/octet-stream'
}

db_path = 'predictions.db'
json_file_path = 'custom_vision_results.json'

try:

    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    
    with Image.open(image_path) as img:
        image_width, image_height = img.size

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    res = requests.post(prediction_url, headers=headers, data=image_data)

    if res.status_code != 200:
        print(f"Error: {res.status_code}")
        print(res.text)

    res.raise_for_status()

    analysis = res.json()

    filtered_predictions = [prediction for prediction in analysis.get('predictions', []) if prediction['probability'] > threshold]

    for prediction in filtered_predictions:
        bounding_box = prediction['boundingBox']
        width = bounding_box['width'] * image_width
        height = bounding_box['height'] * image_height
        area = width * height
        prediction['area'] = area

    analysis['predictions'] = filtered_predictions

    with open('custom_vision_results.json', 'w') as json_file:
        json.dump(analysis, json_file, indent=4)


    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS predictions')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT,
            probability REAL,
            left REAL,
            top REAL,
            width REAL,
            height REAL,
            image_path TEXT,
            area REAL
        )
    ''')

    cursor.execute('DELETE FROM predictions')
    conn.commit()

    if filtered_predictions:
        for prediction in filtered_predictions:
            tag_name = prediction['tagName']
            probability = prediction['probability']
            bounding_box = prediction['boundingBox']
            left = bounding_box['left']
            top = bounding_box['top']
            width = bounding_box['width']
            height = bounding_box['height']
            box_area = prediction['area']

            absolute_left = left * image_width
            absolute_top = top * image_height
            absolute_width = width * image_width
            absolute_height = height * image_height

            print(f"Tag: {tag_name}, Probability: {probability}")
            print(f"Bounding Box: left={absolute_left}, top={absolute_top}, width={absolute_width}, height={absolute_height}, area ={box_area}")
            print(" ")

            cursor.execute(
                """
                INSERT INTO predictions (tag_name, probability, left, top, width, height, image_path, area)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (tag_name, probability, left, top, width, height, image_path, box_area)
            )

            conn.commit()
    else:
        print("No objects detected above the threshold.")

    cursor.close()
    conn.close()


# Error handling
except FileNotFoundError:
    print(f"File not found: {image_path}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API request: {e}")
except sqlite3.Error as e:
    print(f"An error occurred with the SQLite database: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")