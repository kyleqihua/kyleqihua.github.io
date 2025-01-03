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
        with open(f"{image_directory}/{filename}", 'rb') as img_file:
            tags = exifread.process_file(img_file, details=False)

            # 尝试获取日期时间信息
            date_taken = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')

            if date_taken:
                date_time_str = str(date_taken)

                try:
                    # 解析日期时间字符串，例如 '2025:01:01 07:27:54'
                    dt = datetime.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                    time_str = dt.strftime('%H:%M:%S')
                except ValueError:
                    # 如果解析失败，可能时间部分是数值，需要转换
                    # 尝试获取时间（以秒为单位），并将其转换为 HH:MM:SS 格式
                    time_tag = tags.get('EXIF SubSecTimeOriginal') or tags.get('EXIF SubSecTime')
                    if time_tag:
                        total_seconds = float(str(time_tag))
                        dt = timedelta(seconds=total_seconds)
                        time_str = str(dt)
                    else:
                        time_str = 'Unknown Time'
                    date_str = date_time_str.replace(':', '-')
            else:
                date_str = 'Unknown Date'
                time_str = 'Unknown Time'

        image_data.append({'path': filepath, 'date': date_str, 'time': time_str})

# 写入到 YAML 文件
with open(output_file, 'w') as file:
    yaml.dump(image_data, file)