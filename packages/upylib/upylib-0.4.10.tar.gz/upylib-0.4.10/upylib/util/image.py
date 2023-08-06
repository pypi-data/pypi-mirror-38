from PIL import Image
from PIL import ExifTags

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def save_thumb(src, dst, size):
    try:
        img = Image.open(src)
    except Exception as e:
        return False

    try:
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif=dict(img._getexif().items())

        if exif[orientation] == 3 : 
            img=img.rotate(180, expand=True)
        elif exif[orientation] == 6 : 
            img=img.rotate(270, expand=True)
        elif exif[orientation] == 8 : 
            img=img.rotate(90, expand=True)
    except Exception as e:
            return False

    try:
        img.thumbnail( size, Image.ANTIALIAS )
        img.save(dst, "JPEG")
    except Exception as e:
        return False

    return True
