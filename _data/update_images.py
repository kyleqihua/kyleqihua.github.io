import os
import yaml
import exifread
from datetime import datetime

image_directory = '../images/sunrises'
output_file = './images.yml'

image_data = []

for filename in sorted(os.listdir(image_directory)):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        filepath = f"/{image_directory}/{filename}"
        with open(os.path.join(image_directory, filename), 'rb') as img_file:
            tags = exifread.process_file(img_file, details=False)
            
            # Get EXIF time data
            date_taken = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
            date_str = 'Unknown Date'
            time_str = 'Unknown Time'

            if date_taken:
                date_time_str = str(date_taken).strip()
                try:
                    # Convert EXIF time to proper format
                    dt = datetime.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                    # Store time as string in HH:MM:SS format
                    time_str = dt.strftime('%H:%M:%S')
                except ValueError:
                    print(f"Warning: Could not parse date/time for {filename}")
                    continue

        image_data.append({
            'path': filepath,
            'date': date_str,
            'time': time_str
        })

# Sort images by date and time
image_data.sort(key=lambda x: (x['date'], x['time']), reverse=True)

# Write to YAML file
with open(output_file, 'w') as f:
    yaml.dump(image_data, f, allow_unicode=True, sort_keys=False)