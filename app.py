#-------------------------------------------------------------------------------
# app: fixdatetime
# descricao: Busca data/hora no arquivo .json e salva nos metadados dos arquivos de mídia
# versao: 20220523
#-------------------------------------------------------------------------------
import piexif
import os, datetime
from resources import get_config

input_directory = get_config('input_directory')

for path, dirs, files in os.walk(input_directory):
	print(path)
	for filename in files:
		filepath = os.path.join(path, filename)
		file_extension = filepath.rpartition('.')[-1]
		if file_extension == "json":
			file = open(filepath)
			content = file.readlines()
			photodate = int(content[9][18:27] + "0")
			photodate = datetime.datetime.fromtimestamp(photodate)
			photodate_str = str(photodate).replace('-', '').replace(':', '').replace(' ', '_')

			filepath_media = filepath.rpartition('.')[0]
			media_extension = filepath_media.rpartition('.')[-1]
			if "(" in media_extension:
				filepath_media = filepath_media.rpartition('.')[0] + media_extension[3:6] + "." + media_extension[0:3]
				media_extension = media_extension[0:3]

			filepath_media_new = filepath_media.rpartition('.')[0]+ "-" + photodate_str + "." + media_extension

			print(filepath_media)
			if (media_extension.upper() == "JPG") or (media_extension.upper() == "JPEG"):
				photodate = datetime.datetime.strptime(str(photodate), "%Y-%m-%d %H:%M:%S")
				photodate = datetime.datetime(photodate.year, photodate.month, photodate.day, photodate.hour, photodate.minute, photodate.second).strftime("%Y:%m:%d %H:%M:%S")
				exif_dict = piexif.load(filepath_media)
				exif_dict['0th'][piexif.ImageIFD.DateTime] = photodate
				exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = photodate
				exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = photodate
				exif_bytes = piexif.dump(exif_dict)
				piexif.insert(exif_bytes, filepath_media)
				
			print(filepath_media_new)
			os.rename(input_directory + filename, "/media/cascaes/maxHD/json/" + filename)
			os.rename(filepath_media, filepath_media_new)

# FIM