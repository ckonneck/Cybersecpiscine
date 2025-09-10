from geopy.geocoders import Nominatim
from PIL import Image
from PIL.ExifTags import TAGS
import os

def meta_check(filename):
	img = Image.open(filename)
	has_gps = print_gps_location(img)
	if not has_gps:
		print(f"Removing {filename}: no GPS data")
		os.remove(filename)

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
            return True
        else:
            print("No valid GPS location data found.")
            return False
    except Exception as e:
        print(f"Error extracting GPS data: {e}")
        return False
        


def get_location_name(lat, lon):
    geolocator = Nominatim(user_agent="image_metadata_app")
    location = geolocator.reverse((lat, lon), language='en')
    if location:
        print("Location:", location.address)
    else:
        print("Location not found.")