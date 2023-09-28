#!bin/python3

# Copyright (c) 2021 Anthony Crawford

#       _/_/_/    _/_/_/    _/_/_/
#    _/        _/        _/
#     _/_/    _/  _/_/  _/
#        _/  _/    _/  _/
# _/_/_/      _/_/_/    _/_/_/

### SGC-MEDIA:
# An ingest host for media files.
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
import base64
import hashlib
import datetime,time
from time import strftime
from decimal import Decimal
from os.path import splitext
# Logging
import logging
import logging.config
import logging.handlers
# Configuration
from configparser import ConfigParser
# Third Party
import ffmpeg
import psycopg2
from PIL import Image
import inotify.adapters
#from videoprops import get_video_properties, get_audio_properties
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
# string to boolean
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

## old method to get video properties
# def get_v_properties(asset_full_path):
# 	props = get_video_properties(asset_full_path)
# 	media_video_codec = props['codec_name']
# 	media_video_width = props['width']
# 	media_video_height = props['height']
# 	media_video_frame_rate = props['r_frame_rate']
# 	media_video_duration = props['duration']
# 	try:
# 		media_audio_codec = "NA"
# 		media_audio_channels = 0
# 		media_audio_sample_rate = 0
# 		props = get_audio_properties(asset_full_path)
# 		if 'codec_name' in props:
# 			media_audio_codec = props['codec_name']
# 		if 'channels' in props:
# 			media_audio_channels = props['channels']
# 		if 'sample_rate' in props:
# 			media_audio_sample_rate = props['sample_rate']
# 	except RuntimeError as error:
# 		print(error)
# 	return [media_video_codec, media_video_width, media_video_height, media_video_frame_rate, \
# 		media_video_duration, media_audio_codec, media_audio_channels, media_audio_sample_rate]


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

# Find if asset exists
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
def asset_video_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, \
					asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, \
					orientation, media_video_frame_rate, media_video_frame_rate_calc, media_video_bitrate, \
					media_video_codec, media_video_codec_long_name, media_video_codec_tag_string, \
					media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
					media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
					media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, \
					media_audio_sample_rate, created, is_public, tags, doc_format_id):
	sql = "INSERT INTO media_mediavideo(title, file_name, file_path, media_path, size, sha256, file_uuid, \
	media_video_width, media_video_height, media_video_format, orientation, media_video_frame_rate, \
	media_video_frame_rate_calc, media_video_bitrate, media_video_codec, media_video_codec_long_name, \
	media_video_codec_tag_string, media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
	media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
	media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, media_audio_sample_rate, \
	created, is_public, tags, doc_format_id) \
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, \
					asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, \
					orientation, media_video_frame_rate, media_video_frame_rate_calc, media_video_bitrate, \
					media_video_codec, media_video_codec_long_name, media_video_codec_tag_string, \
					media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
					media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
					media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, \
					media_audio_sample_rate, created, is_public, tags, doc_format_id)
	pgql(sql, data)

# Add Audio asset to database
def asset_audio_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, \
	asset_sha256, asset_uuid, media_audio_artist, media_audio_album, media_audio_album_artist, \
	media_audio_composer, media_audio_genre, media_audio_year, media_audio_track, media_audio_track_total, \
	media_audio_disc, media_audio_disc_total, media_audio_comments, media_audio_duration, \
	media_audio_bitrate, media_audio_samplerate, created, is_public, tags, media_audio_image, \
	media_audio_extra, doc_format_id, rating):
	sql = "INSERT INTO media_mediaaudio(title, file_name, file_path, media_path, size, sha256, \
	file_uuid, artist, album, album_artist, composer, genre, year, track_num, track_total, \
	disc_num, disc_total, comments, duration, audio_bitrate, audio_sample_rate, created, \
	is_public, tags, image, extra, doc_format_id, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, \
	asset_sha256, asset_uuid, media_audio_artist, media_audio_album, media_audio_album_artist, \
	media_audio_composer, media_audio_genre, media_audio_year, media_audio_track, media_audio_track_total, \
	media_audio_disc, media_audio_disc_total, media_audio_comments, media_audio_duration, \
	media_audio_bitrate, media_audio_samplerate, created, is_public, tags, media_audio_image, \
	media_audio_extra, doc_format_id, rating)
	pgql(sql, data)

# Add Photo asset to database
def asset_photo_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, photo_format, orientation, created, is_public, tags, doc_format_id):
	sql = "INSERT INTO media_mediaphoto(title, file_name, file_path, media_path, size, sha256, file_uuid, width, height, photo_format, orientation, created, is_public, tags, doc_format_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, photo_format, orientation, created, is_public, tags, doc_format_id)
	pgql(sql, data)

# Add Document asset to database
def asset_doc_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, \
	asset_sha256, asset_uuid, doc_format_id, created, is_public, tags):
	sql = "INSERT INTO media_mediadoc(title, file_name, file_path, media_path, size, sha256, \
	file_uuid, doc_format_id, created, is_public, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, \
	asset_uuid, doc_format_id, created, is_public, tags)
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

def asset_delete_doc(asset_full_path):
	sql = "DELETE FROM media_mediadoc WHERE file_path=%s"
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

def asset_find_doc(asset_sha256):
	sql = "SELECT sha256 FROM media_mediadoc WHERE sha256=%s"
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
	
def asset_update_doc(asset_full_path, asset_media_path, asset_sha256):
	sql = "UPDATE media_mediadoc SET file_path=%s,media_path=%s WHERE sha256=%s"
	data = (asset_full_path,asset_media_path,asset_sha256,)
	pgql(sql, data)

def get_video_format_id(doc_format_ext):
	sql = "SELECT id,doc_format FROM media_mediavideoformat WHERE doc_format=%s"
	data = (doc_format_ext,)
	log.debug("SQL:  " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
		if cur.rowcount > 0:
			for record in cur:
				result = record[0]
			conn.close()
			return result
		else:
			conn.close()
			log.error("Document format missing from MediaVideoFormat table.")
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

def get_audio_format_id(doc_format_ext):
	sql = "SELECT id,doc_format FROM media_mediaaudioformat WHERE doc_format=%s"
	data = (doc_format_ext,)
	log.debug("SQL:  " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
		if cur.rowcount > 0:
			for record in cur:
				result = record[0]
			conn.close()
			return result
		else:
			conn.close()
			log.error("Document format missing from MediaAudioFormat table.")
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

def get_photo_format_id(doc_format_ext):
	sql = "SELECT id,doc_format FROM media_mediaphotoformat WHERE doc_format=%s"
	data = (doc_format_ext,)
	log.debug("SQL:  " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
		if cur.rowcount > 0:
			for record in cur:
				result = record[0]
			conn.close()
			return result
		else:
			conn.close()
			log.error("Document format missing from MediaPhotoFormat table.")
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

def get_doc_format_id(doc_format_ext):
	sql = "SELECT id,doc_format FROM media_mediadocformat WHERE doc_format=%s"
	data = (doc_format_ext,)
	log.debug("SQL:  " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql, data)
		if cur.rowcount > 0:
			for record in cur:
				result = record[0]
			conn.close()
			return result
		else:
			conn.close()
			log.error("Document format missing from MediaDocFormat table.")
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()


def get_video_formats():
	sql = "SELECT doc_format FROM media_mediavideoformat"
	log.debug("SQL:  " + sql)
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql)
		if cur.rowcount > 0:
			data = []
			for row in cur:
				data.append(row[0])
			conn.close()
			return data
		else:
			log.error("No video formats available.")
			conn.close()
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

def get_audio_formats():
	sql = "SELECT doc_format FROM media_mediaaudioformat"
	log.debug("SQL:  " + sql)
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql)
		if cur.rowcount > 0:
			data = []
			for row in cur:
				data.append(row[0])
			conn.close()
			return data
		else:
			log.error("No audio formats available.")
			conn.close()
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

def get_photo_formats():
	sql = "SELECT doc_format FROM media_mediaphotoformat"
	log.debug("SQL:  " + sql)
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql)
		if cur.rowcount > 0:
			data = []
			for row in cur:
				data.append(row[0])
			conn.close()
			return data
		else:
			log.error("No photo formats available.")
			conn.close()
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

def get_doc_formats():
	sql = "SELECT doc_format FROM media_mediadocformat"
	log.debug("SQL:  " + sql)
	conn = None
	try:
		conn = psycopg2.connect(host="192.168.0.13", dbname="sgc", user="sgc", password="sgcmedia")
		cur = conn.cursor()
		cur.execute(sql)
		if cur.rowcount > 0:
			data = []
			for row in cur:
				data.append(row[0])
			conn.close()
			return data
		else:
			log.error("No document formats available.")
			conn.close()
			return False
	except (Exception, psycopg2.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

### FFMPEG Functions

# Get Video Bitrate
def get_video_metadata(asset_full_path):
	try:
		metadata = ffmpeg.probe(asset_full_path)["streams"]
		if metadata is not None:
			return metadata
	except (Exception, ffmpeg.Error) as error:
		log.error(error)
		return False

# Get Video Thumbnail
def get_video_thumbnail(asset_full_path, asset_thumb_path):
	probe = ffmpeg.probe(asset_full_path)
	time = float(probe['streams'][0]['duration']) // 2
	width = probe['streams'][0]['width']
	try:
		(
			ffmpeg
			.input(asset_full_path, ss=time)
			.filter('scale', width, -1)
			.output(asset_thumb_path, vframes=1)
			.overwrite_output()
			.run(capture_stdout=True, capture_stderr=True)
		)
		log.info("Thumbnail created for asset: " + asset_thumb_path)
		return True
	except ffmpeg.Error as e:
		log.error(e.stderr.decode())
		#print(e.stderr.decode(), file=sys.stderr)
		return False


# ------------------------------
# WATCHER
# ------------------------------
# Check watch folder for new content
def Watcher(watch_path, ext_video, ext_audio, ext_photo, ext_doc):
	
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

			file, ext = os.path.splitext(asset) # "path/file"  ".txt"
		
			# Check for hidden files
			if file.startswith("."):
				log.warning("Cannot ingest hidden filenames starting with a period (.), file skipped.")
				continue

			tags = json.dumps([])  # empty
			is_public = True

			log.debug("ASSET_FULL_PATH=" + asset_full_path)
			log.debug("ASSET_MEDIA_PATH=" + asset_media_path)
			log.debug("FILE=" + file)
			log.debug("EXT=" + ext)
			
			ext = ext.split(".")[1].upper()  # remove the period .

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

				doc_format_ext = ext
				result = get_photo_format_id(doc_format_ext)
				if result != False:
					doc_format_id = result

				asset_title = splitext(asset)[0]
				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid+" width="+str(width)+" height="+str(height)+" orientation="+orientation+" format="+photo_format)
				log.debug("File:         " + asset)
				log.debug("Size:         " + str(asset_size))
				log.debug("Hash:         " + asset_sha256)
				log.debug("UUID:         " + asset_uuid)
				log.debug("Width:        " + str(width))
				log.debug("Height:       " + str(height))
				log.debug("Orientation:  " + orientation)
				log.debug("Format ID:    " + str(doc_format_id))

				asset_photo_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, width, height, photo_format, orientation, created, is_public, tags, doc_format_id)


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

				asset_title = splitext(asset)[0]
				asset_uuid = str(uuid.uuid4())
				
				audio_metadata = TinyTag.get(asset_full_path, image=True)

				if (audio_metadata.title is not None) and (audio_metadata.title != ""):
					asset_title = audio_metadata.title.strip()

				if (audio_metadata.artist is not None):
					media_audio_artist = audio_metadata.artist.strip()
				else:
					media_audio_artist = ""

				if (audio_metadata.album is not None):
					media_audio_album = audio_metadata.album.strip()
				else:
					media_audio_album = ""

				if (audio_metadata.albumartist is not None):
					media_audio_album_artist = audio_metadata.albumartist.strip()
				else:
					media_audio_album_artist = ""

				if (audio_metadata.composer is not None):
					media_audio_composer = audio_metadata.composer.strip()
				else:
					media_audio_composer = ""

				if (audio_metadata.genre is not None):
					media_audio_genre = audio_metadata.genre.strip()
				else:
					media_audio_genre = ""

				if (audio_metadata.year is not None):
					media_audio_year = audio_metadata.year
				else:
					media_audio_year = ""

				if (audio_metadata.track is not None):
					media_audio_track = audio_metadata.track
				else:
					media_audio_track = ""

				if (audio_metadata.track_total is not None):
					media_audio_track_total = audio_metadata.track_total
				else:
					media_audio_track_total = ""

				if (audio_metadata.disc is not None):
					media_audio_disc = audio_metadata.disc
				else:
					media_audio_disc = ""

				if (audio_metadata.disc_total is not None):
					media_audio_disc_total = audio_metadata.disc_total
				else:
					media_audio_disc_total = ""

				if (audio_metadata.duration is not None):
					media_audio_duration = round(audio_metadata.duration,3)
				else:
					media_audio_duration = 0.0

				media_audio_filesize = asset_size

				if audio_metadata.bitrate is not None:
					media_audio_bitrate = str(int(audio_metadata.bitrate))
				else:
					media_audio_bitrate = ""

				if audio_metadata.samplerate is not None:
					media_audio_samplerate = str(audio_metadata.samplerate)
				else:
					media_audio_samplerate = ""

				if audio_metadata.comment is not None:
					media_audio_comments = str(audio_metadata.comment).strip()
				else:
					media_audio_comments = ""

				image_data = audio_metadata.get_image()
				if image_data is not None:
					image = base64.b64encode(image_data).decode('utf-8')
					media_audio_image = image
				else:
					media_audio_image = ""

				if audio_metadata.extra is not None:
					media_audio_extra = str(audio_metadata.extra).strip()
				else:
					media_audio_extra = ""

				doc_format_ext = ext
				result = get_audio_format_id(doc_format_ext)
				if result != False:
					doc_format_id = result
				rating = 0

				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid+" artist="+media_audio_artist+" album="+media_audio_album+" title="+asset_title)
				log.debug("File:        " + asset)
				log.debug("Size:        " + str(asset_size) + " bytes")
				log.debug("Hash:        " + asset_sha256)
				log.debug("UUID:        " + asset_uuid)
				# Metadata
				log.debug("Title:        " + asset_title)
				log.debug("Artist:       " + media_audio_artist)
				log.debug("Album:        " + media_audio_album)
				log.debug("Album Artist: " + media_audio_album_artist)
				log.debug("Composer:     " + media_audio_composer)
				log.debug("Genre:        " + media_audio_genre)
				log.debug("Year:         " + media_audio_year)
				log.debug("Track Num:    " + media_audio_track)
				log.debug("Track Total:  " + media_audio_track_total)
				log.debug("Disc Num:     " + media_audio_disc)
				log.debug("Disc Total:   " + media_audio_disc_total)
				log.debug("Duration:     " + str(media_audio_duration) + " seconds")
				log.debug("Bit Rate:     " + media_audio_bitrate + " Kb/s")
				log.debug("Sample Rate:  " + media_audio_samplerate)
				log.debug("Comment:      " + media_audio_comments)
				log.debug("Extra:        " + media_audio_extra)
				log.debug("Format ID:    " + str(doc_format_id))
				log.debug("Rating:       " + str(rating))
				
				asset_audio_create(asset_title, asset, asset_full_path, asset_media_path, \
					asset_size, asset_sha256, asset_uuid, media_audio_artist, media_audio_album, \
					media_audio_album_artist, media_audio_composer, media_audio_genre, media_audio_year, \
					media_audio_track, media_audio_track_total, media_audio_disc, media_audio_disc_total, \
					media_audio_comments, media_audio_duration, media_audio_bitrate, \
					media_audio_samplerate, created, is_public, tags, media_audio_image, \
					media_audio_extra, doc_format_id, rating)


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

				# Thumbnails
				# save 1-5 thumbnails based on video length
				thumb_file = "thumb.png"
				asset_thumb_path = os.path.join(path, "thumbs/", asset_uuid)
				make_sure_path_exists(asset_thumb_path)
				asset_thumb_path = os.path.join(path, "thumbs/", asset_uuid, thumb_file)
				#get_video_thumbnail(asset_full_path, asset_thumb_path)

				# Metadata
				metadata = get_video_metadata(asset_full_path)
				if metadata != False:
					if metadata[0]['codec_type'] == "video":
						media_video_bitrate = metadata[0]['bit_rate']
						media_video_height = int(metadata[0]['height'])
						media_video_width = int(metadata[0]['width'])
						if media_video_width > 1920:
							media_video_format = "UHD"
						elif media_video_width >= 1920:
							media_video_format = "FHD"
						elif media_video_width >= 1280:
							media_video_format = "HD"
						else:
							media_video_format = "SD"
						if media_video_width > media_video_height:
							orientation = "Landscape"
						elif media_video_height > media_video_width:
							orientation = "Portrait"
						else:
							orientation = "Square"
						media_video_codec = metadata[0]['codec_name']
						media_video_codec_long_name = metadata[0]['codec_long_name']
						media_video_codec_tag_string = metadata[0]['codec_tag_string']
						media_video_frame_rate = metadata[0]['r_frame_rate']
						frame_rate = media_video_frame_rate.split("/")
						media_video_frame_rate_calc = round(Decimal(frame_rate[0]) / Decimal(frame_rate[1]),2)
						media_video_duration = round(Decimal(metadata[0]['duration']),3)
						# Removed because not always available
						# if metadata[0]['display_aspect_ratio'] is not None:
						# 	media_video_aspect_ratio = metadata[0]['display_aspect_ratio']
						# else:
						media_video_aspect_ratio = ""
						media_video_pixel_format = metadata[0]['pix_fmt']
						media_video_color_space = metadata[0]['color_space']
						if metadata[0]['is_avc'].lower() == "true":
							media_video_is_avc = True
						else:
							media_video_is_avc = False
						media_audio_bitrate = metadata[1]['bit_rate']
						media_audio_codec = metadata[1]['codec_name']
						media_audio_codec_long_name = metadata[1]['codec_long_name']
						media_audio_codec_tag_string = metadata[1]['codec_tag_string']
						media_audio_channels = int(metadata[1]['channels'])
						media_audio_sample_rate = metadata[1]['sample_rate']
					elif metadata[0]['codec_type'] == "audio":
						media_video_bitrate = metadata[1]['bit_rate']
						media_video_height = int(metadata[1]['height'])
						media_video_width = int(metadata[1]['width'])
						if media_video_width > 1920:
							media_video_format = "UHD"
						elif media_video_width >= 1920:
							media_video_format = "FHD"
						elif media_video_width >= 1280:
							media_video_format = "HD"
						else:
							media_video_format = "SD"
						if media_video_width > media_video_height:
							orientation = "Landscape"
						elif media_video_height > media_video_width:
							orientation = "Portrait"
						else:
							orientation = "Square"
						media_video_codec = metadata[1]['codec_name']
						media_video_codec_long_name = metadata[1]['codec_long_name']
						media_video_codec_tag_string = metadata[1]['codec_tag_string']
						media_video_frame_rate = metadata[1]['r_frame_rate']
						frame_rate = media_video_frame_rate.split("/")
						media_video_frame_rate_calc = round(Decimal(frame_rate[1]) / Decimal(frame_rate[1]),2)
						media_video_duration = round(Decimal(metadata[1]['duration']),3)
						# Removed because not always available
						# if metadata[1]['display_aspect_ratio'] is not None:
						# 	media_video_aspect_ratio = metadata[1]['display_aspect_ratio']
						# else:
						media_video_aspect_ratio = ""
						media_video_pixel_format = metadata[1]['pix_fmt']
						media_video_color_space = metadata[1]['color_space']
						if metadata[1]['is_avc'].lower() == "true":
							media_video_is_avc = True
						else:
							media_video_is_avc = False
						media_audio_bitrate = metadata[0]['bit_rate']
						media_audio_codec = metadata[0]['codec_name']
						media_audio_codec_long_name = metadata[0]['codec_long_name']
						media_audio_codec_tag_string = metadata[0]['codec_tag_string']
						media_audio_channels = int(metadata[0]['channels'])
						media_audio_sample_rate = metadata[0]['sample_rate']
				else:
					log.error("Failed to get video properties for asset: " + asset_full_path)
					continue

				# File format
				doc_format_ext = ext
				result = get_video_format_id(doc_format_ext)
				if result != False:
					doc_format_id = result

				asset_title = splitext(asset)[0]

				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid+" width="+str(media_video_width)+" height="+str(media_video_height)+" orientation="+orientation+" format="+media_video_format+" duration="+str(media_video_duration))
				log.debug("File:            " + asset)
				log.debug("Size:            " + str(asset_size))
				log.debug("Hash:            " + asset_sha256)
				log.debug("UUID:            " + asset_uuid)
				log.debug("> Video Properties:")
				log.debug("Width:           " + str(media_video_width))
				log.debug("Height:          " + str(media_video_height))
				log.debug("Orientation:     " + orientation)
				log.debug("Format:          " + media_video_format)
				log.debug("Duration:        " + str(media_video_duration))
				log.debug("Frame Rate:      " + media_video_frame_rate)
				log.debug("Frame Rate Calc: " + str(media_video_frame_rate_calc))
				log.debug("Bitrate:         " + media_video_bitrate)
				log.debug("Codec:           " + media_video_codec)
				log.debug("Codec Long:      " + media_video_codec_long_name)
				log.debug("Codec Tag:       " + media_video_codec_tag_string)
				log.debug("Aspect Ratio:    " + media_video_aspect_ratio)
				log.debug("Is AVC:          " + str(media_video_is_avc))
				log.debug("Pixel Format:    " + media_video_pixel_format)
				log.debug("> Audio Properties:")
				log.debug("Bitrate:         " + media_audio_bitrate)
				log.debug("Codec:           " + media_audio_codec)
				log.debug("Codec Long:      " + media_audio_codec_long_name)
				log.debug("Codec Tag:       " + media_audio_codec_tag_string)
				log.debug("Channels:        " + str(media_audio_channels))
				log.debug("Sample Rate:     " + media_audio_sample_rate)
				log.debug("Format ID:       " + str(doc_format_id))
				
				asset_video_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, \
					asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, \
					orientation, media_video_frame_rate, media_video_frame_rate_calc, media_video_bitrate, \
					media_video_codec, media_video_codec_long_name, media_video_codec_tag_string, \
					media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
					media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
					media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, \
					media_audio_sample_rate, created, is_public, tags, doc_format_id)


			# Documents
			elif ext in ext_doc:
				
				asset_sha256 = str(hash_file(asset_full_path))
				asset_exists = asset_find_doc(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warning("Asset " + asset_sha256 + " already exists in database: " + asset_full_path)
						continue
				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warning("Asset is empty with 0 bytes. Skipping...")
					continue
				asset_uuid = str(uuid.uuid4())

				doc_format_ext = ext
				result = get_doc_format_id(doc_format_ext)
				if result != False:
					doc_format_id = result

				asset_title = splitext(asset)[0]
				log.info("Asset created: path="+asset_full_path+" size="+str(asset_size)+" sha256="+asset_sha256+" uuid="+asset_uuid+" doc_format="+doc_format_ext)
				log.debug("File:        " + asset)
				log.debug("Size:        " + str(asset_size))
				log.debug("Hash:        " + asset_sha256)
				log.debug("UUID:        " + asset_uuid)
				log.debug("Format:      " + doc_format_ext)
				log.debug("Format ID:   " + str(doc_format_id))

				asset_doc_create(asset_title, asset, asset_full_path, asset_media_path, asset_size, asset_sha256, asset_uuid, doc_format_id, created, is_public, tags)

			else:
				log.error("Invalid file extension " + ext + ", asset not ingested.")


		## FILE DELETED EVENT ##
		elif type_names[0] == 'IN_DELETE':
			asset_full_path = os.path.join(path, asset)
			file, ext = os.path.splitext(asset)

			if ext != "":
				ext = ext.split(".")[1].upper()
			
				#asset_sha256 = str(hash_file(asset_full_path))
				if delete_db_on_fs_delete == True:
					if ext in ext_photo:
						asset_delete_photo(asset_full_path)
					elif ext in ext_audio:
						asset_delete_audio(asset_full_path)
					elif ext in ext_video:
						asset_delete_video(asset_full_path)
					elif ext in ext_doc:
						asset_delete_doc(asset_full_path)
					else:
						pass
					#log.info("Asset " + asset_sha256 + " deleted from file system and database: {}".format(asset_full_path))
					log.info("Asset deleted from file system and database: {}".format(asset_full_path))

				else:
					#log.info("Asset " + asset_sha256 + " deleted from file system: {}".format(asset_full_path))
					log.info("Asset deleted from file system: {}".format(asset_full_path))


		## FILE UPDATE EVENT ##
		elif type_names[0] == "IN_MOVED_TO":
			asset_full_path = os.path.join(path, asset)
			asset_media_path = os.path.join(path.split(watch_path,)[1], asset)
			file, ext = os.path.splitext(asset)
			ext = ext.split(".")[1].upper()

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
			elif ext in ext_doc:
				asset_exists = asset_find_doc(asset_sha256)
				if asset_exists is not None:
					if asset_exists > 0:
						asset_update_doc(asset_full_path, asset_sha256)
						log.info("Asset " + asset_sha256 + " moved in file system, database path updated: {}".format(asset_full_path))
			else:
				log.error("Invalid file extension ." + ext)



### SCRIPT STARTS HERE ###
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

	ext_video = get_video_formats()
	if ext_video == False:
		log.error("There are no video formats listed in the database.")
		quit(1)
	else:
		log.debug(ext_video)
	
	ext_audio = get_audio_formats()
	if ext_audio == False:
		log.error("There are no audio formats listed in the database.")
		quit(1)
	else:
		log.debug(ext_audio)

	ext_photo = get_photo_formats()
	if ext_photo == False:
		log.error("There are no photo formats listed in the database.")
		quit(1)
	else:
		log.debug(ext_photo)

	ext_doc = get_doc_formats()
	if ext_doc == False:
		log.error("There are no document formats listed in the database.")
		quit(1)
	else:
		log.debug(ext_doc)


	# Start watcher loop
	Watcher(watch_path, ext_video, ext_audio, ext_photo, ext_doc)

	log.info("SGC-Media Watcher Stopped.");print()
