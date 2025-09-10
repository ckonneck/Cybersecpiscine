def print_gps_location(img):
    try:
        exif_data = img._getexif()
        gps_info = None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_info = value
                break

        def get_decimal_from_dms(dms, ref):
            degrees, minutes, seconds = dms
            decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
            if ref in ['S', 'W']:
                decimal = -decimal
            return decimal

        if gps_info and 1 in gps_info and 2 in gps_info and 3 in gps_info and 4 in gps_info:
            lat = get_decimal_from_dms(gps_info[2], gps_info[1])
            lon = get_decimal_from_dms(gps_info[4], gps_info[3])
            print(f"GPS Location: Latitude {lat}, Longitude {lon}")
            get_location_name(lat, lon)
        else:
            print("No valid GPS location data found.")
    except Exception as e:
        print(f"Error extracting GPS data: {e}")


def get_location_name(lat, lon):
    geolocator = Nominatim(user_agent="image_metadata_app")
    location = geolocator.reverse((lat, lon), language='en')
    if location:
        print("Location:", location.address)
    else:
        print("Location not found.")

from geopy.geocoders import Nominatim
from args import get_args
import os
from integrity import is_allowed_file
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def print_image_info(img, filename):
    print("Format:", img.format)
    print("Dimensions:", img.size)
    print("Color Mode:", img.mode)
    stats = os.stat(filename)
    print("Creation Time:    ", datetime.fromtimestamp(stats.st_ctime))
    print("Modification Time:", datetime.fromtimestamp(stats.st_mtime))

def print_exif_metadata(img):
    try:
        exif_data = img._getexif()
        if not exif_data:
            print("No EXIF metadata found.")
            return
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "MakerNote":
                if isinstance(value, bytes):
                    user_input = input("MakerNote contains binary data. Display it anyway? (y/n): ")
                    if user_input.lower() == 'y':
                        print("MakerNote (binary):", value)
                    else:
                        print("MakerNote not displayed.")
                else:
                    print("MakerNote:", value)
            elif tag == "GPSInfo":
                print_gps_location(img)
            else:
                print(f"{tag}: {value}")
    except Exception as e:
        print(f"Error extracting Metadata: {e}")

def main():
    args = get_args()
    filename = args.file
    print(f"Filename: {filename}")

    if not is_allowed_file(filename):
        print("Invalid File extension")
        exit(1)

    try:
        img = Image.open(filename)
        print_image_info(img, filename)
        print_exif_metadata(img)
    except Exception as e:
        print(f"Error opening image: {e}")

if __name__ == "__main__":
    main()







        # if tag == "MakerNote":
        #     # MakerNote is usually binary, so decode carefully
        #     if isinstance(value, bytes):
        #         print("MakerNote (decoded):", value.decode('utf-8', errors='replace'))
        #     else:
        #         print("MakerNote:", value)