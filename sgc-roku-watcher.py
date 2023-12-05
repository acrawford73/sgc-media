#!bin/python3

# Copyright (c) 2023

#       _/_/_/    _/_/_/    _/_/_/
#    _/        _/        _/
#     _/_/    _/  _/_/  _/
#        _/  _/    _/  _/
# _/_/_/      _/_/_/    _/_/_/

### SGC-ROKU-WATCHER (* Video asset ingest for Roku Content Feed *)

# An ingest host for media files, uploaded via SSH or SFTP.
# Bulk upload media files, then edit metadata later.
# CMS like interface for reviewing ingested media.
# API for querying media content.
# API for Roku Content Feed.

# The database schema is already through Django project 'sgc-media' setup.
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
import ffmpeg  ## https://kkroening.github.io/ffmpeg-python/
import psycopg
from PIL import Image
import inotify.adapters
#from videoprops import get_video_properties, get_audio_properties

# ------------------------------
# Functions
# ------------------------------
# string to boolean
def str_to_bool(s):
	if s.lower() in ("true", "1"):
		return True
	elif s.lower() in ("false", "0"):
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
	try:
		with open(asset,'rb') as file:
			# loop till the end of the file
			chunk = 0
			while chunk != b'':
				# read only 1024 bytes at a time
				chunk = file.read(65536)
				h.update(chunk)
		# return the hex representation of digest
		return str(h.hexdigest())
	except IOError as e:
		log.error("Could not retrieve file for sha256 creation. ")
		log.error(e)
		return False


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
def pgql(sql, data, db_meta):
	log.debug("SQL: " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		cur.execute(sql, data)
		return True
	except (Exception, psycopg.DatabaseError) as error:
		log.error(error)
		return False
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

# Find if asset exists
def pgql_find(sql, data, db_meta):
	log.debug("SQL:  " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		cur.execute(sql, data)
		res_count = cur.rowcount  #int
		conn.close()
		return res_count
	except (Exception, psycopg.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

# Add video asset to MediaVideo table
# def asset_video_create_media(asset_title, asset, asset_full_path, asset_media_path, asset_size, \
# 					asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, \
# 					orientation, media_video_frame_rate, media_video_frame_rate_calc, media_video_bitrate, \
# 					media_video_codec, media_video_codec_long_name, media_video_codec_tag_string, \
# 					media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
# 					media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
# 					media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, \
# 					media_audio_sample_rate, created, is_public, tags, doc_format_id, db_meta):
# 	sql = "INSERT INTO media_mediavideo(title, file_name, file_path, media_path, size, sha256, file_uuid, \
# 	media_video_width, media_video_height, media_video_format, orientation, media_video_frame_rate, \
# 	media_video_frame_rate_calc, media_video_bitrate, media_video_codec, media_video_codec_long_name, \
# 	media_video_codec_tag_string, media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
# 	media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
# 	media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, media_audio_sample_rate, \
# 	created, is_public, tags, doc_format_id) \
# 	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# 	data = (asset_title, asset, asset_full_path, asset_media_path, asset_size, \
# 					asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, \
# 					orientation, media_video_frame_rate, media_video_frame_rate_calc, media_video_bitrate, \
# 					media_video_codec, media_video_codec_long_name, media_video_codec_tag_string, \
# 					media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
# 					media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
# 					media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, \
# 					media_audio_sample_rate, created, is_public, tags, doc_format_id)
# 	psql_result = pgql(sql, data, db_meta)
# 	if psql_result == False:
# 		log.error("Failed to create video asset in Media table.")
# 	return psql_result

# Add video asset to Video table
def asset_video_create_video(url, quality, video_type, db_meta):
	sql = "INSERT INTO roku_content_video(url, quality, video_type) \
	VALUES (%s, %s, %s)"
	data = (url, quality, video_type)
	psql_result = pgql(sql, data, db_meta)
	if psql_result == False:
		log.error("Failed to create video asset in Video table.")
	return psql_result

# Add video asset to Content table
def asset_video_create_content():
	sql = "INSERT INTO roku_content_content(title, language, duration, videos, captions, trick_play_files, date_added) \
	VALUES (%s, %s, %s, %s, %s, %s, %s)"
	data = (title, language, duration, videos, captions, trick_play_files, date_added)
	psql_result = pgql(sql, data, db_meta)
	if psql_result == False:
		log.error("Failed to create video asset in Content table.")
	return psql_result


# Delete

def asset_delete_video(asset_full_path, db_meta):
	sql = "DELETE FROM media_mediavideo WHERE file_path=%s"
	data = (asset_full_path,) # comma required!
	psql_result = pgql(sql, data, db_meta)
	if psql_result == True:
		log.debug("Asset deleted from database: {}".format(asset_full_path))
	return psql_result

# Query

def asset_find_video(asset_sha256, db_meta):
	sql = "SELECT sha256 FROM media_mediavideo WHERE sha256=%s"
	data = (asset_sha256,)
	res_count = pgql_find(sql, data, db_meta)
	return res_count

# Update

def asset_update_video(asset_full_path, asset_media_path, asset_sha256, db_meta):
	sql = "UPDATE media_mediavideo SET file_path=%s,media_path=%s WHERE sha256=%s"
	data = (asset_full_path,asset_media_path,asset_sha256,)
	psql_result = pgql(sql, data, db_meta)
	if psql_result == True:
		log.debug("Asset updated in database: {}".format(asset_full_path))
	return psql_result

def get_video_format_id(doc_format_ext, db_meta):
	sql = "SELECT id,doc_format FROM media_mediavideoformat WHERE doc_format=%s"
	data = (doc_format_ext,)
	log.debug("SQL:  " + sql)
	for df in data:
		log.debug("DATA: " + str(df))
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		cur.execute(sql, data)
		if cur.rowcount > 0:
			for record in cur:
				result = record[0]
			conn.close()
			return result
		else:
			conn.close()
			log.error("Document format missing from table.")
			return False
	except (Exception, psycopg.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

def get_video_formats(db_meta):
	sql = "SELECT doc_format FROM media_mediavideoformat"
	log.debug("SQL:  " + sql)
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		cur.execute(sql)
		if cur.rowcount > 0:
			data = []
			for row in cur:
				data.append(row[0])
			conn.close()
			return data
		else:
			log.error("No video formats found.")
			conn.close()
			return False
	except (Exception, psycopg.DatabaseError) as error:
		log.error(error)
	finally:
		if conn is not None:
			conn.close()

### FFMPEG Functions ###

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
###



# ------------------------------
# WATCHER
# ------------------------------
# Check watch folder for new content
def Watcher(watch_path, ext_video):
	
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

			# Ingest video asset
			if ext in ext_video:

				# If asset already exists in database, ignore it
				asset_sha256 = hash_file(asset_full_path)
				asset_exists = asset_find_video(asset_sha256, db_meta)
				if asset_exists is not None:
					if asset_exists > 0:
						log.warning("Asset " + asset_sha256 + " already exists in database: " + asset_full_path)
						continue

				asset_size = int(os.path.getsize(asset_full_path))
				if asset_size == 0:
					log.warning("Asset is empty with 0 bytes. Try reuploading the asset. Skipping for now...")
					continue

				asset_uuid = str(uuid.uuid4())

				# Thumbnails
				# save 1-5 thumbnails based on video length
				thumb_file = "thumb.png"
				asset_thumb_path = os.path.join(path, "thumbs/", asset_uuid)
				make_sure_path_exists(asset_thumb_path)
				asset_thumb_path = os.path.join(path, "thumbs/", asset_uuid, thumb_file)

				# Create thumbnail images for the video asset
				#get_video_thumbnail(asset_full_path, asset_thumb_path)

				# Metadata
				metadata = get_video_metadata(asset_full_path)

				if metadata != False:
					if metadata[0]['codec_type'] == "video":
						media_video_bitrate = metadata[0]['bit_rate']
						media_video_height = int(metadata[0]['height'])
						media_video_width = int(metadata[0]['width'])
						
						#confirm this is correct

						if media_video_width > 1920:
							media_video_format = "UHD"
						elif media_video_width >= 1920:
							media_video_format = "FHD"
						elif media_video_width >= 1280:
							media_video_format = "HD"
						else:
							media_video_format = "SD"
						
						# Display Orientation
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
					# Sometimes the video and audio metadata is in reverse
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
				result = get_video_format_id(doc_format_ext, db_meta)
				if result != False:
					doc_format_id = result

				asset_title = splitext(asset)[0]

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
				
				# The video asset must be added to the Video and Content tables, for auto-insertion of the video duration
				
				ingested1 = asset_video_create_media(asset_title, asset, asset_full_path, asset_media_path, asset_size, \
					asset_sha256, asset_uuid, media_video_width, media_video_height, media_video_format, \
					orientation, media_video_frame_rate, media_video_frame_rate_calc, media_video_bitrate, \
					media_video_codec, media_video_codec_long_name, media_video_codec_tag_string, \
					media_video_duration, media_video_aspect_ratio, media_video_pixel_format, \
					media_video_color_space, media_video_is_avc, media_audio_bitrate, media_audio_codec, \
					media_audio_codec_long_name, media_audio_codec_tag_string, media_audio_channels, \
					media_audio_sample_rate, created, is_public, tags, doc_format_id, db_meta)
				
				ingested2 = asset_video_create_video(url, quality, video_type, db_meta)
				
				ingested3 = asset_video_create_content(title, language, duration, videos, captions, trick_play_files, date_added, db_meta)

				if (ingested1 == True) and (ingested2 == True) and (ingested3 == True):
					log.info("Asset ingested: path=" + asset_full_path + " size=" + str(asset_size) + \
						" sha256=" + asset_sha256 + " uuid="+asset_uuid + " format=" + media_video_format + \
						" duration=" + str(media_video_duration))
				elif ingested1 == False:
					log.error("Failed to ingest to Media database table.")
				elif ingested2 == False:
					log.error("Failed to ingest to Video database table.")
				elif ingested3 == False:
					log.error("Failed to ingest to Content database table.")
				else:
					log.error("Failed to ingest asset: " + asset_full_path)

			else:
				log.error("Invalid file extension " + ext + ", asset not ingested.")


		## FILE DELETED EVENT ##

		# When an asset is deleted it must be removed from Video, Content, Playlist and Content Feed tables
		
		elif type_names[0] == 'IN_DELETE':
			asset_full_path = os.path.join(path, asset)
			file, ext = os.path.splitext(asset)

			if ext != "":
				ext = ext.split(".")[1].upper()
				if delete_db_on_fs_delete == True:
					if ext in ext_video:
						asset_delete_video(asset_full_path, db_meta)
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

			asset_sha256 = hash_file(asset_full_path)
			if ext in ext_video:
				asset_exists = asset_find_video(asset_sha256, db_meta)
				if asset_exists is not None:
					if asset_exists > 0:
						asset_update_video(asset_full_path, asset_media_path, asset_sha256, db_meta)
						log.info("Asset updated: " + asset_sha256 + " moved in file system, database path updated: {}".format(asset_full_path))
			else:
				log.error("Invalid file extension ." + ext)


### THE REAL GAME BEGINS HERE ###
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
	log_file = strftime('sgcmedia-watcher.log')
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

	from decouple import config
	DB_HOST = config('DB_HOST')
	DB_NAME = config('DB_NAME')
	DB_USER = config('DB_USER')
	DB_PASSWORD = config('DB_PASSWORD')
	db_meta = {'DB_HOST':DB_HOST,'DB_NAME':DB_NAME,'DB_USER':DB_USER,'DB_PASSWORD':DB_PASSWORD}

	ext_video = get_video_formats(db_meta)
	if ext_video == False:
		log.error("There are no video formats in the database. Load the 'media' fixtures to add them.")
		quit(1)
	else:
		log.debug(ext_video)
	
	# Start watcher loop
	Watcher(watch_path, ext_video)

	log.info("SGC-Media Watcher Stopped.");print()
