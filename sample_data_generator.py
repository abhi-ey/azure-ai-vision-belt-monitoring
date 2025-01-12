import csv
import random
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()
parser.add_argument('num_records', type=int)
parser.add_argument('output_file', type=str)
args = parser.parse_args()

NUM_SECTIONS = 10
TAG_NAME = 'carryback'
IMAGE_PATH_TEMPLATE = 'https://example.com/image_{}.jpg'
AREA_SCALER_MIN = 1000
AREA_SCALER_MAX = 10000

def generate_random_data(num_records):
    data = []
    current_timestamp = datetime.now()
    
    box_id = 1
    section_id = 1
    while box_id <= num_records:
        # Determine the number of boxes in the current section
        boxes_in_section = random.randint(1, 10)
        
        for _ in range(boxes_in_section):
            if box_id > num_records:
                break
            
            timestamp = current_timestamp + timedelta(seconds=box_id)  # Progressive timestamp
            tag_name = TAG_NAME
            probability = random.uniform(0, 1)
            left = random.uniform(0, 1)
            top = random.uniform(0, 1)
            width = random.uniform(0.1, 0.5)  # Assuming width is between 10% and 50% of the image width
            height = random.uniform(0.1, 0.5)  # Assuming height is between 10% and 50% of the image height
            image_path = IMAGE_PATH_TEMPLATE.format(box_id)
            area_scaler = random.uniform(AREA_SCALER_MIN, AREA_SCALER_MAX)
            area = area_scaler * width * height
            
            data.append({
                'box_id': box_id,
                'section_id': section_id,
                'timestamp': timestamp.isoformat(),
                'tag_name': tag_name,
                'probability': probability,
                'left': left,
                'top': top,
                'width': width,
                'height': height,
                'image_path': image_path,
                'area': area
            })
            
            box_id += 1
        
        section_id = (section_id % NUM_SECTIONS) + 1  # Loop back to 1 after reaching 10
    
    return data

def write_to_csv(data, output_file):
    fieldnames = ['box_id', 'section_id', 'timestamp', 'tag_name', 'probability', 'left', 'top', 'width', 'height', 'image_path', 'area']

    with open(output_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    num_records = args.num_records
    output_file = args.output_file

    data = generate_random_data(num_records)

    write_to_csv(data, output_file)
    print(f'Successfulyyg srtstrgsergs')

if __name__ == '__main__':
    main()

