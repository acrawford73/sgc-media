#!bin/python3

# Copyright (c) 2021 Anthony Crawford

#       _/_/_/    _/_/_/    _/_/_/
#    _/        _/        _/
#     _/_/    _/  _/_/  _/
#        _/  _/    _/  _/
# _/_/_/      _/_/_/    _/_/_/

### SGC-CONTENT ###

# SGC-FETCHER Data Importer to SGC-MEDIA Database

import os
import json
import uuid
import errno
import shutil
import hashlib
import datetime,time
from time import strftime
from decimal import Decimal
# Third-party
import psycopg2
from PIL import Image
from videoprops import get_video_properties, get_audio_properties


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
	props = get_video_properties(asset_full_path)
	media_video_codec = props['codec_name']
	media_video_width = props['width']
	media_video_height = props['height']
	media_video_aspect_ratio = props['display_aspect_ratio']
	media_video_frame_rate = props['avg_frame_rate']
	media_video_duration = props['duration']
	try:
		media_audio_codec = "na"
		media_audio_channels = 0
		media_audio_sample_rate = 0
		props = get_audio_properties(asset_full_path)
		if 'codec_name' in props:
			media_audio_codec = props['codec_name']
		if 'channels' in props:
			media_audio_channels = props['channels']
		if 'sample_rate' in props:
			media_audio_sample_rate = props['sample_rate']
	except RuntimeError as error:
		print(error)
	return [media_video_codec, media_video_width, media_video_height, media_video_aspect_ratio, media_video_frame_rate, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate]


def asset_find(table, asset_sha256):
	sql = "SELECT file_sha256 FROM %s WHERE file_sha256=%s"
	data = (asset_sha256,)
	#log.debug("SQL: " + sql)
	#for df in data:
		#log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="localhost", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
		res_count = cur.rowcount  #int
		conn.close()
		return res_count
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


# Create SHA256 value of file
def hash_file(asset):
	""""This function returns the SHA-256 hash of the file passed into it"""
	h = hashlib.sha256()
	with open(asset,'rb') as file:
		chunk = 0
		while chunk != b'':
			chunk = file.read(65536)
			h.update(chunk)
	file.close()
	return h.hexdigest()


def pgql(sql, data):
	#log.debug("SQL: " + sql)
	#for df in data:
		#log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="localhost", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()


# Add Video asset to database
def asset_video_create(title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, orientation, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_aspect_ratio, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, service, location_name, location_latitude, location_longitude, username, long_description):
	sql = "INSERT INTO media_mediavideo(title, file_name, file_path, media_path, file_size, file_sha256, file_uuid, orientation, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_aspect_ratio, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, service, location_name, location_latitude, location_longitude, username, long_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, orientation, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_aspect_ratio, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, service, location_name, location_latitude, location_longitude, username, long_description)
	pgql(sql, data)


# Add Photo asset to database
def asset_photo_create(title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, tags, service, location_name, location_latitude, location_longitude, username, long_description):
	sql = "INSERT INTO media_mediaphoto(title, file_name, file_path, media_path, file_size, file_sha256, file_uuid, width, height, orientation, created, is_public, tags, service, location_name, location_latitude, location_longitude, username,long_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, tags, service, location_name, location_latitude, location_longitude, username, long_description)
	pgql(sql, data)


# Importer
def importer(data, media_path):

	export_json = data['hits']['hits']
	import_count = 1

	for media in export_json:

		if file_check_exists(media['_source']['path']):

			print("[" + str(import_count) + "] " + media['_source']['blog_name'] + ", " + media['_source']['path'].split('/')[-1])

			content_type = media['_source']['type'].capitalize()

			## Fields from imported data ###
			service = media['_source']['service'].capitalize()
			username = media['_source']['blog_name']
			orientation = media['_source']['orientation'].capitalize()

			location_name = ""
			location_latitude = 0.0
			location_longitude = 0.0
			if service == "Flickr" or service == "Instagram":
				location_name = media['_source']['location']['name']
				if media['_source']['location']['latitude'] != 0:
					if media['_source']['location']['latitude'] != "":
						location_latitude = Decimal(media['_source']['location']['latitude'])
				if media['_source']['location']['longitude'] != 0:
					if media['_source']['location']['latitude'] != "":
						location_longitude = Decimal(media['_source']['location']['longitude'])

			long_description = media['_source']['caption']
			title = ""
			if service == "Flickr":
				title = media['_source']['title']
			elif service == "Tumblr":
				title = media['_source']['slug']

			if media['_source']['tags'] is not None:
				if (media['_source']['tags'] == [""]) or (media['_source']['tags'] == []):
					tags = json.dumps([])
				else:
					tags = json.dumps(media['_source']['tags'])
				if service == "Flickr":
					if media['_source']['tags'] == "":
						tags = json.dumps([])
					else:
						# Convert string a,b,c to json list {"a","b","c"}
						tag_list = list(media['_source']['tags'].split(','))
						tags = json.dumps(tag_list)


			### Fields for media record ###

			src_path = media['_source']['path']

			# Determine if asset exists already
			asset_sha256 = str(hash_file(src_path))
			if content_type == "Photo":
				asset_exists = asset_find("media_mediaphoto", asset_sha256)
			else:
				asset_exists = asset_find("media_mediavideo", asset_sha256)
			if asset_exists is not None:
				if asset_exists > 0:
					print("Asset already exists in database.")
					continue
			
			# Get asset file size, if 0 bytes ignore
			asset_size = int(os.path.getsize(src_path))
			if asset_size == 0:
				print("Asset is empty with 0 bytes. Skipping...")
				continue

			if content_type == "Photo":
				img=Image.open(src_path)
				width,height=img.size
				img.close()
				if width > height:
					orientation = "Landscape"
				elif height > width:
					orientation = "Portrait"
				else:
					orientation = "Square"

			elif content_type == "Video":
				media_properties = get_v_properties(src_path)
				media_video_codec = str(media_properties[0])
				media_video_width = int(media_properties[1])
				if media_video_width > 1920:
					media_video_format = "4K"
				elif media_video_width >= 1920:
					media_video_format = "HD1080"
				elif media_video_width >= 1280:
					media_video_format = "HD720"
				else:
					media_video_format = "SD"
				media_video_height = int(media_properties[2])
				media_video_aspect_ratio = str(media_properties[3])
				media_video_frame_rate = str(media_properties[4])
				media_video_duration = Decimal(media_properties[5])
				media_audio_codec = str(media_properties[6].upper())
				media_audio_channels = int(media_properties[7])
				media_audio_sample_rate = str(media_properties[8])
				if media_video_width > media_video_height:
					orientation = "Landscape"
				elif media_video_height > media_video_width:
					orientation = "Portrait"
				else:
					orientation = "Square"

			asset = media['_source']['path'].split('/')[-1]
			asset_uuid = str(uuid.uuid4())
			is_public = True

			created_utc = datetime.datetime.utcnow()
			created = created_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

			date_path = created_utc.strftime("%Y/%m/%d/")
			make_sure_path_exists(os.path.join(media_path, date_path))
			asset_path_date = os.path.join(media_path, date_path)  # media_assets/Y/M/D/
			# media path for website
			asset_media_path = os.path.join(date_path, asset)  # Y/M/D/asset.jpg
			# full path to asset
			asset_full_path = os.path.join(asset_path_date, asset)  # media_assets/Y/M/D/asset.jpg

			# If file already exists in media storage don't add it again
			if not file_check_exists(asset_full_path):
				if content_type == "Photo":
					asset_photo_create(title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, tags, service, location_name, location_latitude, location_longitude, username, long_description)
				else:
					asset_video_create(title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, orientation, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_aspect_ratio, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, service, location_name, location_latitude, location_longitude, username, long_description)
				shutil.copy(src_path, asset_full_path)
				import_count += 1
			else:
				continue
				

		else:
			print("Media file missing: " + media['_source']['path'])
			continue

	
	# ^ media loop



if __name__ == "__main__":

	media_path = "media_assets/"

	f = open("export_pretty.json", "r")
	data = json.load(f)
	f.close()

	importer(data, media_path)

	print()
	quit()
