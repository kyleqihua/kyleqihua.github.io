import os
import exifread

image_directory = "../images/sunrises"
filename = "IMG_2398.JPG"  # replace with the actual file that shows 27357.0

with open(os.path.join(image_directory, filename), "rb") as f:
    tags = exifread.process_file(f, details=False)

print("All EXIF tags for", filename)
for tag_key in tags.keys():
    print(f"{tag_key}: {tags[tag_key]}")