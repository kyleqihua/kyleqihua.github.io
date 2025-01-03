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
                    # Example format: '2025:01:01 07:27:54'
                    dt = datetime.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                    time_str = dt.strftime('%H:%M:%S')
                except ValueError:
                    # Fallback: maybe the date part is parseable separately, or maybe not.
                    # We'll still attempt to get time from SubSecTimeOriginal if present:
                    time_tag = tags.get('EXIF SubSecTimeOriginal') or tags.get('EXIF SubSecTime')
                    if time_tag:
                        try:
                            # Convert that float/int (e.g. 26874.0) to HH:MM:SS
                            total_seconds = float(str(time_tag))
                            td = timedelta(seconds=total_seconds)
                            # datetime.min is 0001-01-01 00:00:00
                            # Adding td shifts that time by the timedelta
                            # which lets us format it with strftime
                            time_str = (datetime.min + td).strftime('%H:%M:%S')
                        except ValueError:
                            time_str = 'Unknown Time'
                    # You might still want to salvage a date from date_time_str 
                    # by slicing out the first part, or just mark it unknown:
                    if ':' in date_time_str:
                        # minimal attempt to parse just the YYYY:MM:DD
                        partial_date_str = date_time_str.split(' ')[0]
                        try:
                            dt_partial = datetime.strptime(partial_date_str, '%Y:%m:%d')
                            date_str = dt_partial.strftime('%Y-%m-%d')
                        except ValueError:
                            pass

            # If there was no date/time in EXIF at all
            else:
                date_str = 'Unknown Date'
                time_str = 'Unknown Time'

        image_data.append({
            'path': filepath,
            'date': date_str,
            'time': time_str
        })

# Write to YAML
with open(output_file, 'w') as file:
    yaml.dump(image_data, file)