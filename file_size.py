#!bin/python3

# Copyright (c) 2022 Anthony Crawford

#       _/_/_/    _/_/_/    _/_/_/
#    _/        _/        _/
#     _/_/    _/  _/_/  _/
#        _/  _/    _/  _/
# _/_/_/      _/_/_/    _/_/_/

### SGC-MEDIA ###

# Determine file size and dimensions of video files
# Create CSV
# Convert to 360p for archive purpose

import os
import csv
import errno
import shutil
import datetime,time
from time import strftime
from pathlib import Path
# Third-party
from videoprops import get_video_properties


###


def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise


# Check if asset list inputfile is present
def file_check_exists(inputfile):
	exists = os.path.isfile(inputfile)
	if exists:
		#if debug:
		#	print('Assets file ' + inputfile + ' found.')
		return True
	else:
		#if debug:
		#	print('Assets file ' + inputfile + ' not found!')
		return False


def get_v_properties(asset_full_path):
	try:
		props = get_video_properties(asset_full_path)
		media_video_width = props['width']
		media_video_height = props['height']
	except RuntimeError as error:
		print(error)
	return [media_video_width, media_video_height]



if __name__ == "__main__":
 
	#media_path = "/home/ubuntu/Downloads/SS/"

	with open("file_size.csv","a") as f:
		f.write("path,width,height\n")

		for current_dir, _, files in os.walk('.'):
			for filename in files:
				if filename.endswith('.mp4'):
					relative_path = os.path.join(current_dir, filename)
					absolute_path = os.path.abspath(relative_path)
					
					media_properties = get_v_properties(absolute_path)
					media_width = int(media_properties[0])
					media_height = int(media_properties[1])

					print(absolute_path + "," + str(media_width) + "," + str(media_height))

					f.write(absolute_path + "," + str(media_width) + "," + str(media_height) + "\n")
		
	f.close()


	print();quit()

