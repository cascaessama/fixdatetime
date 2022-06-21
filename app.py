#-------------------------------------------------------------------------------
# app: fixdatetime
# descricao: Busca data/hora no arquivo .json e salva nos metadados dos arquivos de mídia
# versao: 20220523
#-------------------------------------------------------------------------------
import piexif
import os, datetime
from pathlib import Path
from resources import get_config

input_directory = get_config('input_directory')
media_directory = get_config('media_directory')
json_directory = get_config('json_directory')
index = 1

if not os.path.exists(media_directory):
    os.makedirs(media_directory)

if not os.path.exists(json_directory):
    os.makedirs(json_directory)

for path, dirs, files in os.walk(input_directory):
	print("path: " + path)
	for filename in files:
		filepath = os.path.join(path, filename)
		file_extension = filepath.rpartition('.')[-1]
		if file_extension == "json":
			file = open(filepath)
			content = file.readlines()
			photodate = int(content[9][18:27] + "0")
			file.close()
			photodate = datetime.datetime.fromtimestamp(photodate)
			photodate_str = str(photodate).replace('-', '').replace(':', '').replace(' ', '_')

			filepath_media = filepath.rpartition('.')[0]
			media_extension = filepath_media.rpartition('.')[-1]
			if "(" in media_extension:
				print(len(media_extension))
				if len(media_extension) == 7:
					filepath_media = filepath_media.rpartition('.')[0] + media_extension[4:7] + "." + media_extension[0:4]
					media_extension = media_extension[0:4]
				else: 
					filepath_media = filepath_media.rpartition('.')[0] + media_extension[3:6] + "." + media_extension[0:3]
					media_extension = media_extension[0:3]
			
			print("filepath_media: " + filepath_media)

			if (media_extension.upper() == "JPG") or (media_extension.upper() == "JPEG"):
				photodate = datetime.datetime.strptime(str(photodate), "%Y-%m-%d %H:%M:%S")
				photodate = datetime.datetime(photodate.year, photodate.month, photodate.day, photodate.hour, photodate.minute, photodate.second).strftime("%Y:%m:%d %H:%M:%S")
				exif_dict = piexif.load(filepath_media)
				exif_dict['0th'][piexif.ImageIFD.DateTime] = photodate
				exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = photodate
				exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = photodate
				exif_bytes = piexif.dump(exif_dict)
				piexif.insert(exif_bytes, filepath_media)

			filepath_media_new = media_directory + photodate_str + "." + media_extension
			if Path(filepath_media_new).exists():
				filepath_media_new = media_directory + photodate_str + "(" + str(index) + ")." + media_extension
				index = index + 1

			print("filepath_media_new: " + filepath_media_new)
			os.rename(filepath_media, filepath_media_new)

			filepath_json = json_directory + filename
			print("filepath: " + filepath)
			print("filepath_json: " + filepath_json)
			os.rename(filepath, filepath_json)
		
			
# FIM