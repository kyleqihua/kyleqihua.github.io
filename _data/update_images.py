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

            # 获取常用的两个时间字段，优先使用 EXIF DateTimeOriginal
            date_taken = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
            date_str = 'Unknown Date'
            time_str = 'Unknown Time'

            if date_taken:
                date_time_str = str(date_taken).strip()
                try:
                    # 按照常见的 EXIF 日期格式 'YYYY:MM:DD HH:MM:SS' 解析
                    dt = datetime.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                    time_str = dt.strftime('%H:%M:%S')
                except ValueError:
                    # 如果解析失败，不再做其他数值（SubSecTimeOriginal等）的额外转换，直接忽略
                    pass

        image_data.append({
            'path': filepath,
            'date': date_str,
            'time': time_str
        })

# 写入 YAML 文件
with open(output_file, 'w') as file:
    yaml.dump(image_data, file)