import os
import yaml
import exifread

image_directory = '../images/sunrises'
output_file = './images.yml'

image_data = []

for filename in sorted(os.listdir(image_directory)):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        filepath = f"/{image_directory}/{filename}"
        with open(f"{image_directory}/{filename}", 'rb') as img_file:
            tags = exifread.process_file(img_file)
            date_taken = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
            if date_taken:
                date_str = str(date_taken).split(' ')[0].replace(':', '-')
            else:
                date_str = 'Unknown Date'
        image_data.append({'path': filepath, 'date': date_str})

# 写入到 YAML 文件
with open(output_file, 'w') as file:
    yaml.dump(image_data, file)