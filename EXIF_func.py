from exif import Image

def dms_coord_to_didgital(coordinates, coordinates_ref):
    decimal_degrees = coordinates[0] + \
                      coordinates[1] / 60 + \
                      coordinates[2] / 3600
    
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def meta_get ():
    meta_dict = {}
    with open ("photo.jpg","rb") as photo_file:
        photo_file = Image(photo_file)
        if photo_file.has_exif:
            meta_dict.setdefault("версия метаданных", photo_file.exif_version) 
            #print(dir(photo_file))
            meta_dict.setdefault("фирма", photo_file.get("make","Unknown"))
            meta_dict.setdefault("модель", photo_file.get("model", "Unnown" ))
            meta_dict.setdefault("дата снимка",photo_file.get('datetime_original',"Unknown"))
            if "gps_latitude" in dir(photo_file):
                didgital_latitude = dms_coord_to_didgital(photo_file.get("gps_latitude","None"),photo_file.get("gps_latitude_ref", "None"))
                didgital_longitude = dms_coord_to_didgital(photo_file.get('gps_longitude', "None"),photo_file.get('gps_longitude_ref', "None"))
                meta_dict.setdefault("координаты снимка",f"{didgital_latitude} {didgital_longitude}" )
                return meta_dict
            meta_dict.setdefault("координаты снимка", "отстутствуют")
            return meta_dict
        meta_dict.setdefault("метаданные", "отсутствуют")
        return meta_dict
        
