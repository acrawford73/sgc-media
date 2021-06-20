#!bin/python3

# Copyright (c) 2021 Anthony Crawford

#       _/_/_/    _/_/_/    _/_/_/
#    _/        _/        _/
#     _/_/    _/  _/_/  _/
#        _/  _/    _/  _/
# _/_/_/      _/_/_/    _/_/_/

### SGC MEDIA ###
# Watches for new media in watch folder, uploaded via SSH or SFTP
# Copies new media from private to public storage
# Adds new media to Postgres database
# Removes media from Postgres database upon deletion if enabled
# The database schema is already created through Django project 'sgcmedia' setup

import os
import sys
import json
import uuid
import errno
import hashlib
import datetime,time
from time import strftime
from decimal import Decimal
from distutils.util import strtobool
# Logging
import logging
import logging.config
import logging.handlers
# Configuration
from configparser import SafeConfigParser
# Third Party
import psycopg2
from PIL import Image
import inotify.adapters
from videoprops import get_video_properties, get_audio_properties

# ------------------------------
# Functions
# ------------------------------
def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

# Check if field is empty
def is_empty(any_structure):
	if any_structure:
		#print('Structure is not empty.')
		return False
	else:
		#print('Structure is empty.')
		return True

# Check if asset list inputfile is present
def file_check_exists(inputfile):
	exists = os.path.isfile(inputfile)
	if exists:
		if debug:
			print('Assets file ' + inputfile + ' found.')
		return True
	else:
		if debug:
			print('Assets file ' + inputfile + ' not found!')
		return False

# Create SHA256 value of file
def hash_file(asset):
	""""This function returns the SHA-256 hash of the file passed into it"""
	# make a hash object
	h = hashlib.sha256()
	# open file for reading in binary mode
	with open(asset,'rb') as file:

		## check for file open errors here - if so return False

		# loop till the end of the file
		chunk = 0
		while chunk != b'':
			# read only 1024 bytes at a time
			chunk = file.read(65536)
			h.update(chunk)
	file.close()
	# return the hex representation of digest
	return h.hexdigest()

def get_v_properties(asset_full_path):
	props = get_video_properties(asset_full_path)
	media_video_codec = props['codec_name']
	media_video_width = props['width']
	media_video_height = props['height']
	media_video_frame_rate = props['r_frame_rate']
	media_video_duration = props['duration']
	try:
		media_audio_codec = "NA"
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
	return [media_video_codec, media_video_width, media_video_height, media_video_frame_rate, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate]


#def asset_audit():
#	log.info("Auditing existing assets with database...")
#	# Get assets in database
#	# Get assets in storage
#	# Determine which assets are not in database, add to database.
#	# Determine which assets are not in storage, delete in DB.


## NOTE:
# psycopg.org/docs/usage.html#passing-parameters-to-sql-queries

# For insert and delete
def pgql(sql, data):
	log.debug("SQL: " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="localhost", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

def pgql_find(sql, data):
	log.debug("SQL:  " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="localhost", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
		res_count = cur.rowcount  #int
		conn.close()
		return res_count
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

# Add Video asset to database
def asset_video_create(asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, content_type):
	sql = "INSERT INTO media_mediavideo(file_name, file_path, media_path, size, sha256, file_uuid, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, content_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, content_type)
	pgql(sql, data)

# Add Audio asset to database
# def asset_audio_create(asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, content_type):
# 	sql = "INSERT INTO media_mediaphoto(file_name, file_path, media_path, size, sha256, file_uuid, width, height, orientation, created, is_public, content_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# 	data = (asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, content_type)
# 	pgql(sql, data)

# Add Photo asset to database
def asset_photo_create(asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, tags, content_type):
	sql = "INSERT INTO media_mediaphoto(file_name, file_path, media_path, size, sha256, file_uuid, width, height, orientation, created, is_public, tags, content_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, tags, content_type)
	pgql(sql, data)

def asset_delete_video(asset_full_path):
	sql = "DELETE FROM media_mediavideo WHERE file_path=%s"
	data = (asset_full_path,) # comma required!
	pgql(sql, data)
	log.debug("Asset deleted from database: {}".format(asset_full_path))

def asset_delete_audio(asset_full_path):
	sql = "DELETE FROM media_mediaaudio WHERE file_path=%s"
	data = (asset_full_path,)
	pgql(sql, data)
	log.debug("Asset deleted from database: {}".format(asset_full_path))

def asset_delete_photo(asset_full_path):
	sql = "DELETE FROM media_mediaphoto WHERE file_path=%s"
	data = (asset_full_path,)
	pgql(sql, data)
	log.debug("Asset deleted from database: {}".format(asset_full_path))

def asset_find_video(asset_sha256):
	sql = "SELECT sha256 FROM media_mediavideo WHERE sha256=%s"
	data = (asset_sha256,)
	res_count = pgql_find(sql, data)
	return res_count

def asset_find_audio(asset_sha256):
	sql = "SELECT sha256 FROM media_mediaaudio WHERE sha256=%s"
	data = (asset_sha256,)
	res_count = pgql_find(sql, data)
	return res_count

def asset_find_photo(asset_sha256):
	sql = "SELECT sha256 FROM media_mediaphoto WHERE sha256=%s"
	data = (asset_sha256,)
	res_count = pgql_find(sql, data)
	return res_count
	


# ------------------------------
# WATCHER
# ------------------------------
# Check watch folder for new content
def Watcher(watch_path):
	
	ext_photo = ['.jpeg','.jpg','.JPG','.png','.PNG','.gif','.GIF','.bmp','.BMP']
	ext_audio = ['.mp3','.MP3','.m4a','.M4A']
	ext_video = ['.mp4','.MP4','.ts','.TS','.wmv','.WMV','.mkv','.MKV']

	# Recursive
	inw = inotify.adapters.InotifyTree(watch_path)
	#inw.block_duration_s = 2
	#

	# Non-Recursive
	#inw = inotify.adapters.Inotify()
	#inw.add_watch(watch_path)
	#

	for event in inw.event_gen(yield_nones=False):
	
		(_, type_names, path, asset) = event
		log.debug("Asset=[{}{}] Event_Type=[{}]".format(path, asset, type_names))

		## FILE CREATED EVENT ## (Completed file system write)
		if type_names[0] == 'IN_CLOSE_WRITE':

			created_utc = datetime.datetime.utcnow()
			created = created_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
			
			asset_full_path = os.path.join(path, asset)
			asset_media_path = os.path.join(path.split(watch_path,)[1], asset)

			file, ext = os.path.splitext(asset)

			log.debug("ASSET_FULL_PATH=" + asset_full_path)
			log.debug("ASSET_MEDIA_PATH=" + asset_media_path)
			log.debug("FILE=" + file)
			log.debug("EXT=" + ext)

			# Ingest photo asset
			if ext in ext_photo:
				
				content_type = "Photo"

				asset_sha256 = str(hash_file(asset_full_path))
				asset_exists = asset_find_photo(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warn("Asset already exists in database: " + asset_full_path)
						continue
				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warn("Asset is empty with 0 bytes. Skipping...")
					continue
				asset_uuid = str(uuid.uuid4())

				img=Image.open(asset_full_path)
				width,height=img.size
				img.close()

				if width > height:
					orientation = "Landscape"
				elif height > width:
					orientation = "Portrait"
				else:
					orientation = "Square"

				is_public = True
				
				tags = []

				log.info("Asset created: " + asset_full_path)
				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid+" width="+str(width)+" height="+str(height)+" orientation="+orientation)
				#log.info("Asset created: {\"path\":\""+asset_full_path+"\", \"size\":"+str(asset_size)+", \"sha256\":\""+asset_sha256+"\", \"uuid\":\""+asset_uuid+"\", \"width\":"+str(width)+", \"height\":"+str(height)+", \"orientation\":\""+orientation+"\"}")
				log.debug("File:         " + asset)
				log.debug("Size:         " + str(asset_size))
				log.debug("Hash:         " + asset_sha256)
				log.debug("UUID:         " + asset_uuid)
				log.debug("Width:        " + str(width))
				log.debug("Height:       " + str(height))
				log.debug("Orientation:  " + orientation)

				asset_photo_create(asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, orientation, created, is_public, tags, content_type)


			# Ingest audio/music asset

			elif ext in ext_audio:
				
				content_type = "Audio"

				asset_sha256 = str(hash_file(asset_full_path))
				asset_exists = asset_find_audio(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warn("Asset already exists in database: " + asset_full_path)
						continue
				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warn("Asset is empty with 0 bytes. Skipping...")
					continue
				asset_uuid = str(uuid.uuid4())
				#duration = get_audio_properties()
				log.info("Asset created: " + asset_full_path)
				log.debug("File:         " + asset)


			# Ingest video asset
			elif ext in ext_video:

				content_type = "Video"

				# If asset already exists, ignore it
				asset_sha256 = str(hash_file(asset_full_path))
				asset_exists = asset_find_video(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warn("Asset already exists in database: " + asset_full_path)
						continue

				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warn("Asset is empty with 0 bytes. Skipping...")
					continue
				asset_uuid = str(uuid.uuid4())
				
				media_properties = get_video_properties(asset_full_path)
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
				media_video_frame_rate = str(media_properties[3])
				media_video_duration = Decimal(media_properties[4])
				media_audio_codec = str(media_properties[5].upper())
				media_audio_channels = int(media_properties[6])
				media_audio_sample_rate = str(media_properties[7])

				is_public = True

				tags = json.dumps([])  # empty

				# Debug
				log.info("Asset:        " + asset_full_path)
				log.debug("File:         " + asset)
				log.debug("Size:         " + str(asset_size))
				log.debug("Hash:         " + asset_sha256)
				log.debug("UUID:         " + asset_uuid)
				log.debug("Height:       " + str(media_video_height))
				log.debug("Width:        " + str(media_video_width))
				log.debug("Format:       " + media_video_format)
				log.debug("Duration:     " + str(media_video_duration))
				log.debug("Frame Rate:   " + media_video_frame_rate)
				log.debug("Video Codec:  " + media_video_codec)
				log.debug("Audio Codec:  " + media_audio_codec)
				log.debug("Channels:     " + str(media_audio_channels))
				log.debug("Sample Rate:  " + media_audio_sample_rate)
				
				asset_video_create(asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags, content_type)

			else:
				log.error("Invalid file extension " + ext + ", asset not ingested.")

		## FILE DELETED EVENT ##
		elif type_names[0] == 'IN_DELETE':
			asset_full_path = os.path.join(path, asset)
			if delete_db_on_fs_delete == True:
				if ext in ext_photo:
					asset_delete_photo(asset_full_path)
				elif ext in ext_audio:
					asset_delete_audio(asset_full_path)
				elif ext in ext_video:
					asset_delete_video(asset_full_path)
				else:
					pass
				log.info("Asset deleted from file system and database: {}".format(asset_full_path))
			else:
				log.info("Asset deleted from file system: {}".format(asset_full_path))



### STARTS HERE
if __name__ == "__main__":

	# ------------------------------
	# Configuration
	# ------------------------------
	config = SafeConfigParser()
	config.read('etc/config.conf')
	debug = strtobool(config.get('sgc', 'debug'))
	delete_db_on_fs_delete = strtobool(config.get('sgc', 'delete_db_on_fs_delete'))
	db_host = config.get('sgc', 'db_host')
	db_user = config.get('sgc', 'db_user')
	db_pass = config.get('sgc', 'db_pass')
	db_port = int(config.get('sgc', 'db_port'))
	watch_path = config.get('sgc', 'watch_path')
	watch_interval = int(config.get('sgc', 'watch_interval'))
	log_path = config.get('sgc', 'log_path')

	# ------------------------------
	# Initialize Logging
	# ------------------------------
	#log_file = strftime('sgcmedia_%Y%m%d_%H%M%S.log')
	log_file = strftime('sgcmedia.log')
	log_path = config.get('sgc', 'log_path')
	logfile = os.path.join(log_path, log_file)
	make_sure_path_exists(log_path)
	if debug:
		logging.basicConfig(level=logging.DEBUG) # log to stdout
	else:
		logging.basicConfig(level=logging.INFO) # log to stdout
	log = logging.getLogger('SGC')
	handler = logging.FileHandler(logfile)
	if debug:
		handler.setLevel(logging.DEBUG)  # log to console
	else:
		handler.setLevel(logging.INFO)  # log to console
	formatter = logging.Formatter('%(asctime)s.%(msecs)03d:%(levelname)s:%(message)s','%Y-%m-%d %H:%M:%S')
	handler.setFormatter(formatter)
	log.addHandler(handler)

	# ------------------------------
	# Start Watcher
	# ------------------------------
	print();log.info("SGC-Media Watcher Started.");print()
	log.info("Watching folder: " + watch_path);print()

	# Audit existing files with database...
	#asset_audit()

	# Start watcher loop
	Watcher(watch_path)

	log.info("SGC-Media Watcher Stopped.");print()
