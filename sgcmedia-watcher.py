#!bin/python3

# Copyright (c) 2021 Anthony Crawford

#       _/_/_/    _/_/_/    _/_/_/
#    _/        _/        _/
#     _/_/    _/  _/_/  _/
#        _/  _/    _/  _/
# _/_/_/      _/_/_/    _/_/_/

### SGC-MEDIA:
# Acts as an ingest host for media files.
# Files are uploaded via SSH or SFTP. 
# CMS like interface for reviewing ingested media.
# API for querying media content.

# The database schema is already through Django project 'sgcmedia' setup.
# Features: 
# - Watches for new media in watch folder.
# - Copies new media from private to public storage.
# - Adds new media to Postgres database.
# - Removes media from Postgres database upon deletion, if enabled.

import os
import sys
import json
import uuid
import errno
import hashlib
import datetime,time
from time import strftime
from decimal import Decimal
# Logging
import logging
import logging.config
import logging.handlers
# Configuration
from configparser import ConfigParser
# Third Party
import psycopg2
from PIL import Image
import inotify.adapters
from videoprops import get_video_properties, get_audio_properties
# Videoprops

from tinytag import TinyTag
# TinyTag supported formats:
# MP3/MP2/MP1 (ID3 v1, v1.1, v2.2, v2.3+)
# Wave/RIFF
# OGG
# OPUS
# FLAC
# WMA
# MP4/M4A/M4B/M4R/M4V/ALAC/AAX/AAXC
# AIFF/AIFF-C

# ------------------------------
# Functions
# ------------------------------
# string to boolean function
def str_to_bool(s):
	if s in ("True", "TRUE", "true", "1"):
		return True
	elif s in ("False", "FALSE", "false", "0"):
		return False
	else:
		return None

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
	return [media_video_codec, media_video_width, media_video_height, media_video_frame_rate, \
		media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate]


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
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
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
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
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
def asset_video_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, orientation, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags):
	sql = "INSERT INTO media_mediavideo(title, file_name, file_path, media_path, size, sha256, file_uuid, media_video_width, media_video_height, media_video_format, orientation, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, orientation, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags)
	pgql(sql, data)

# Add Audio asset to database
def asset_audio_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, \
	asset_sha256, asset_uuid, media_audio_artist, media_audio_album, media_audio_genre, \
	media_audio_year, media_audio_duration, media_audio_bitrate, media_audio_samplerate, \
	created, is_public, tags):
	sql = "INSERT INTO media_mediaaudio(title, file_name, file_path, media_path, size, sha256, \
	file_uuid, artist, album, genre, year, duration, audio_bitrate, audio_sample_rate, \
	created, is_public, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, \
	asset_sha256, asset_uuid, media_audio_artist, media_audio_album, media_audio_genre, \
	media_audio_year, media_audio_duration, media_audio_bitrate, media_audio_samplerate, \
	created, is_public, tags)
	pgql(sql, data)

# Add Photo asset to database
def asset_photo_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, photo_format, orientation, created, is_public, tags):
	sql = "INSERT INTO media_mediaphoto(title, file_name, file_path, media_path, size, sha256, file_uuid, width, height, photo_format, orientation, created, is_public, tags) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, photo_format, orientation, created, is_public, tags)
	pgql(sql, data)

# Delete
def asset_delete_photo(asset_full_path):
	sql = "DELETE FROM media_mediaphoto WHERE file_path=%s"
	data = (asset_full_path,)
	pgql(sql, data)
	log.debug("Asset deleted from database: {}".format(asset_full_path))

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

# Query
def asset_find_photo(asset_sha256):
	sql = "SELECT sha256 FROM media_mediaphoto WHERE sha256=%s"
	data = (asset_sha256,)
	res_count = pgql_find(sql, data)
	return res_count

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

# Update
def asset_update_photo(asset_full_path, asset_media_path, asset_sha256):
	sql = "UPDATE media_mediaphoto SET file_path=%s,media_path=%s WHERE sha256=%s"
	data = (asset_full_path,asset_media_path,asset_sha256,)
	pgql(sql, data)

def asset_update_video(asset_full_path, asset_media_path, asset_sha256):
	sql = "UPDATE media_mediavideo SET file_path=%s,media_path=%s WHERE sha256=%s"
	data = (asset_full_path,asset_media_path,asset_sha256,)
	pgql(sql, data)
	
def asset_update_audio(asset_full_path, asset_media_path, asset_sha256):
	sql = "UPDATE media_mediavideo SET file_path=%s,media_path=%s WHERE sha256=%s"
	data = (asset_full_path,asset_media_path,asset_sha256,)
	pgql(sql, data)
	

# ------------------------------
# WATCHER
# ------------------------------
# Check watch folder for new content
def Watcher(watch_path):
	
	ext_photo = ['.jpeg', '.jpg', '.png', '.gif', '.bmp']
	ext_audio = ['.mp3', '.m4a', '.ogg', '.wav', '.flac']
	ext_video = ['.mp4', '.ts', '.wmv', '.mkv']

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
		log.debug("Asset=[{}/{}] Event_Type=[{}]".format(path, asset, type_names))

		## FILE CREATED EVENT ## (Completed file system write)
		if type_names[0] == 'IN_CLOSE_WRITE':

			created_utc = datetime.datetime.utcnow()
			created = created_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
			
			asset_full_path = os.path.join(path, asset)
			asset_media_path = os.path.join(path.split(watch_path,)[1], asset)

			file, ext = os.path.splitext(asset)
			ext = ext.lower()
			tags = json.dumps([])  # empty

			log.debug("ASSET_FULL_PATH=" + asset_full_path)
			log.debug("ASSET_MEDIA_PATH=" + asset_media_path)
			log.debug("FILE=" + file)
			log.debug("EXT=" + ext)

			# Ingest photo asset
			if ext in ext_photo:
				
				asset_sha256 = str(hash_file(asset_full_path))
				asset_exists = asset_find_photo(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warning("Asset " + asset_sha256 + " already exists in database: " + asset_full_path)
						continue
				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warning("Asset is empty with 0 bytes. Skipping...")
					continue
				asset_uuid = str(uuid.uuid4())

				img=Image.open(asset_full_path)
				width,height=img.size
				img.close()

				if width > 1920:
					photo_format = "UHD"
				elif width >= 1920:
					photo_format = "FHD"
				elif width >= 1280:
					photo_format = "HD"
				else:
					photo_format = "SD"

				if width > height:
					orientation = "Landscape"
				elif height > width:
					orientation = "Portrait"
				else:
					orientation = "Square"

				is_public = True
				asset_title = asset.split(".")[0]
				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid+" width="+str(width)+" height="+str(height)+" orientation="+orientation+" format="+photo_format)
				log.debug("File:         " + asset)
				log.debug("Size:         " + str(asset_size))
				log.debug("Hash:         " + asset_sha256)
				log.debug("UUID:         " + asset_uuid)
				log.debug("Width:        " + str(width))
				log.debug("Height:       " + str(height))
				log.debug("Orientation:  " + orientation)

				asset_photo_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, photo_format, orientation, created, is_public, tags)


			# Ingest audio/music asset

			elif ext in ext_audio:
				
				asset_sha256 = str(hash_file(asset_full_path))
				asset_exists = asset_find_audio(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warning("Asset " + asset_sha256 + " already exists in database: " + asset_full_path)
						continue
				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warning("Asset is empty with 0 bytes. Skipping...")
					continue

				is_public = True
				asset_title = asset.split(".")[0]
				asset_uuid = str(uuid.uuid4())
				audio_metadata = TinyTag.get(asset_full_path)
				if audio_metadata.title != "":
					asset_title = audio_metadata.title
				media_audio_artist = audio_metadata.artist
				media_audio_album = audio_metadata.album
				media_audio_genre = audio_metadata.genre
				media_audio_year = audio_metadata.year
				media_audio_duration = round(audio_metadata.duration,3)
				media_audio_filesize = asset_size
				media_audio_bitrate = str(round(audio_metadata.bitrate,3))
				media_audio_samplerate = str(audio_metadata.samplerate)

				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid)
				log.debug("File:        " + asset)
				log.debug("Size:        " + str(asset_size) + " bytes")
				log.debug("Hash:        " + asset_sha256)
				log.debug("UUID:        " + asset_uuid)
				log.debug("Title:       " + asset_title)
				log.debug("Artist:      " + media_audio_artist)
				log.debug("Album:       " + media_audio_album)
				log.debug("Genre:       " + media_audio_genre)
				log.debug("Year:        " + media_audio_year)
				log.debug("Duration:    " + str(media_audio_duration) + " seconds")
				log.debug("Bit Rate:    " + media_audio_bitrate + " KB/s")
				log.debug("Sample Rate: " + media_audio_samplerate)

				asset_audio_create(asset_title, asset, asset_full_path, asset_media_path, \
					asset_size, asset_sha256, asset_uuid, media_audio_artist, media_audio_album, \
					media_audio_genre, media_audio_year, media_audio_duration, \
					media_audio_bitrate, media_audio_samplerate, created, is_public, tags)


			# Ingest video asset
			elif ext in ext_video:

				# If asset already exists in database, ignore it
				asset_sha256 = str(hash_file(asset_full_path))
				asset_exists = asset_find_video(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warning("Asset " + asset_sha256 + " already exists in database: " + asset_full_path)
						continue

				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warning("Asset is empty with 0 bytes. Skipping...")
					continue

				asset_uuid = str(uuid.uuid4())
				media_properties = get_v_properties(asset_full_path)
				media_video_codec = str(media_properties[0])
				media_video_width = int(media_properties[1])
				if media_video_width > 1920:
					media_video_format = "UHD"
				elif media_video_width >= 1920:
					media_video_format = "FHD"
				elif media_video_width >= 1280:
					media_video_format = "HD"
				else:
					media_video_format = "SD"
				media_video_height = int(media_properties[2])
				media_video_frame_rate = str(media_properties[3])
				media_video_duration = Decimal(media_properties[4])
				media_audio_codec = str(media_properties[5].upper())
				media_audio_channels = int(media_properties[6])
				media_audio_sample_rate = str(media_properties[7])

				if media_video_width > media_video_height:
					orientation = "Landscape"
				elif media_video_height > media_video_width:
					orientation = "Portrait"
				else:
					orientation = "Square"

				is_public = True
				asset_title = asset.split(".")[0]

				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid+" width="+str(media_video_width)+" height="+str(media_video_height)+" orientation="+orientation+" format="+media_video_format+" duration="+str(media_video_duration))
				log.debug("File:         " + asset)
				log.debug("Size:         " + str(asset_size))
				log.debug("Hash:         " + asset_sha256)
				log.debug("UUID:         " + asset_uuid)
				log.debug("Height:       " + str(media_video_height))
				log.debug("Width:        " + str(media_video_width))
				log.debug("Orientation:  " + orientation)
				log.debug("Format:       " + media_video_format)
				log.debug("Duration:     " + str(media_video_duration))
				log.debug("Frame Rate:   " + media_video_frame_rate)
				log.debug("Video Codec:  " + media_video_codec)
				log.debug("Audio Codec:  " + media_audio_codec)
				log.debug("Channels:     " + str(media_audio_channels))
				log.debug("Sample Rate:  " + media_audio_sample_rate)
				
				asset_video_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, orientation, media_video_frame_rate, media_video_codec, media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate, created, is_public, tags)

			else:
				log.error("Invalid file extension " + ext + ", asset not ingested.")

		## FILE DELETED EVENT ##
		elif type_names[0] == 'IN_DELETE':
			asset_full_path = os.path.join(path, asset)
			file, ext = os.path.splitext(asset)
			ext = ext.lower()
			#asset_sha256 = str(hash_file(asset_full_path))
			if delete_db_on_fs_delete == True:
				if ext in ext_photo:
					asset_delete_photo(asset_full_path)
				elif ext in ext_audio:
					asset_delete_audio(asset_full_path)
				elif ext in ext_video:
					asset_delete_video(asset_full_path)
				else:
					pass
				#log.info("Asset " + asset_sha256 + " deleted from file system and database: {}".format(asset_full_path))
				log.info("Asset deleted from file system and database: {}".format(asset_full_path))

			else:
				#log.info("Asset " + asset_sha256 + " deleted from file system: {}".format(asset_full_path))
				log.info("Asset deleted from file system and database: {}".format(asset_full_path))

		## FILE UPDATE EVENT ##
		elif type_names[0] == "IN_MOVED_TO":
			asset_full_path = os.path.join(path, asset)
			asset_media_path = os.path.join(path.split(watch_path,)[1], asset)
			file, ext = os.path.splitext(asset)
			ext = ext.lower()

			asset_sha256 = str(hash_file(asset_full_path))
			if ext in ext_video:
				asset_exists = asset_find_video(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						asset_update_video(asset_full_path, asset_media_path, asset_sha256)
						log.info("Asset updated: " + asset_sha256 + " moved in file system, database path updated: {}".format(asset_full_path))
			elif ext in ext_photo:
				asset_exists = asset_find_photo(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						asset_update_photo(asset_full_path, asset_media_path, asset_sha256)
						log.info("Asset updated: " + asset_sha256 + " moved in file system, database path updated: {}".format(asset_full_path))
			elif ext in ext_audio:
				asset_exists = asset_find_audio(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						asset_update_audio(asset_full_path, asset_sha256)
						log.info("Asset " + asset_sha256 + " moved in file system, database path updated: {}".format(asset_full_path))
			else:
				log.error("Invalid file extension " + ext)
			



### STARTS HERE ###
if __name__ == "__main__":

	# ------------------------------
	# Configuration
	# ------------------------------
	config = ConfigParser()
	config.read('etc/config.conf')
	debug = str_to_bool(config.get('sgc', 'debug'))
	delete_db_on_fs_delete = str_to_bool(config.get('sgc', 'delete_db_on_fs_delete'))
	db_host = config.get('sgc', 'db_host')
	db_user = config.get('sgc', 'db_user')
	db_pass = config.get('sgc', 'db_pass')
	db_port = int(config.get('sgc', 'db_port'))
	watch_path = config.get('sgc', 'watch_path')
	#watch_interval = int(config.get('sgc', 'watch_interval'))
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
