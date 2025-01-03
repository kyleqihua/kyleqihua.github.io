import os
import yaml
import exifread
from datetime import datetime, timedelta

image_directory = '../images/sunrises'
output_file = './images.yml'

image_data = []

for filename in sorted(os.listdir(image_directory)):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        filepath = f"/{image_directory}/{filename}"
        with open(os.path.join(image_directory, filename), 'rb') as img_file:
            tags = exifread.process_file(img_file, details=False)

            date_taken = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
            date_str = 'Unknown Date'
            time_str = 'Unknown Time'

            if date_taken:
                date_time_str = str(date_taken).strip()
                try:
                    dt = datetime.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                    time_str = dt.strftime('%H:%M:%S')
                except ValueError:
                    pass # If parsing fails, we'll try to get time from SubSecTime
            else:
                # If no full date and time, try to extract date from filename if possible
                parts = filename.split('-')
                if len(parts) > 2 and all(part.isdigit() and len(part) in [4, 2] for part in parts[:3]):
                    try:
                        date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
                        datetime.strptime(date_str, '%Y-%m-%d') # Validate date format
                    except ValueError:
                        pass  # Keep 'Unknown Date' if filename doesn't match

            # Attempt to get time from SubSecTime only if we don't have a valid time yet
            if time_str == 'Unknown Time':
                time_tag = tags.get('EXIF SubSecTimeOriginal') or tags.get('EXIF SubSecTime')
                if time_tag:
                    try:
                        total_seconds = float(str(time_tag))
                        td = timedelta(seconds=total_seconds)
                        time_of_day = datetime.min + td
                        time_str = time_of_day.strftime('%H:%M:%S')
                    except ValueError:
                        pass

        image_data.append({
            'path': filepath,
            'date': date_str,
            'time': time_str
        })

# Write to YAML
with open(output_file, 'w') as file:
    yaml.dump(image_data, file)