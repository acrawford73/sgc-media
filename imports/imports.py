#!../bin/python3

import os
import json
import psycopg2


### Video

def import_video_services(data,host):
	for item in data:
		print(item)
		sql = "INSERT INTO media_mediavideoservice(service_name) VALUES (%s)"
		data = (item,)
		conn = None
		try:
			conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
			cur = conn.cursor()
			cur.execute(sql, data)
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.commit()
				conn.close()

def import_video_genres(data,host):
	for item in data:
		print(item)
		sql = "INSERT INTO media_mediavideogenre(genre) VALUES (%s)"
		data = (item,)
		conn = None
		try:
			conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
			cur = conn.cursor()
			cur.execute(sql, data)
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.commit()
				conn.close()

def import_video_formats(data,host):
	conn = None
	conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
	cur = conn.cursor()
	for key, value in data.items():
		print(key, value)
		sql = "INSERT INTO media_mediavideoformat(doc_format,doc_format_name) VALUES (%s, %s)"
		data = (key,value,)
		cur.execute(sql, data)
	if conn is not None:
		conn.commit()
		conn.close()


### Audio

def import_audio_genres(data,host):
	for item in data:
		print(item)
		sql = "INSERT INTO media_audiogenre(genre) VALUES (%s)"
		data = (item,)
		conn = None
		try:
			conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
			cur = conn.cursor()
			cur.execute(sql, data)
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.commit()
				conn.close()

def import_audio_formats(data,host):
	conn = None
	conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
	cur = conn.cursor()
	for key, value in data.items():
		print(key, value)
		sql = "INSERT INTO media_mediaaudioformat(doc_format,doc_format_name) VALUES (%s, %s)"
		data = (key,value,)
		cur.execute(sql, data)
	if conn is not None:
		conn.commit()
		conn.close()


### Photo

def import_photo_formats(data,host):
	conn = None
	conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
	cur = conn.cursor()
	for key, value in data.items():
		print(key, value)
		sql = "INSERT INTO media_mediaphotoformat(doc_format,doc_format_name) VALUES (%s, %s)"
		data = (key,value,)
		cur.execute(sql, data)
	if conn is not None:
		conn.commit()
		conn.close()


### Documents

def import_doc_formats(data,host):
	conn = None
	conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
	cur = conn.cursor()
	for key, value in data.items():
		print(key, value)
		sql = "INSERT INTO media_mediadocformat(doc_format,doc_format_name) VALUES (%s, %s)"
		data = (key,value,)
		cur.execute(sql, data)
	if conn is not None:
		conn.commit()
		conn.close()


def import_services(data,host):
	conn = None
	conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
	cur = conn.cursor()
	for item in data:
		print(item)
		sql = "INSERT INTO media_mediaservice(service) VALUES (%s)"
		data = (item,)
		cur.execute(sql, data)
	if conn is not None:
		conn.commit()
		conn.close()
		
		# try:
		# 	conn = psycopg2.connect(host=host, dbname="sgc", user="sgc", password="sgcmedia")
		# 	cur = conn.cursor()
		# 	cur.execute(sql, data)
		# except (Exception, psycopg2.DatabaseError) as error:
		# 	print(error)
		# finally:
		# 	if conn is not None:
		# 		conn.commit()
		# 		conn.close()


if __name__ == "__main__":

	print();print("Importing data...");print()

	host="192.168.0.13"


	### Video

	# Video Services
	f = open("video_services.json", "r")
	data = json.load(f)
	f.close()
	import_video_services(data,host)
	print()
	
	# Video Genres
	# f = open("video_genres.json", "r")
	# data = json.load(f)
	# f.close()
	# import_video_genres(data,host)
	# print()

	#Video Formats
	# f = open("video_formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_video_formats(data,host)
	# print()


	### Audio
	# Audio Genres
	# f = open("audio_genres.json", "r")
	# data = json.load(f)
	# f.close()
	# import_audio_genres(data,host)
	# print()

	#Audio Formats
	# f = open("audio_formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_audio_formats(data,host)
	# print()


	### Photo
	#Photo Formats
	# f = open("photo_formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_photo_formats(data,host)
	# print()

	### Documents
	#Doc Formats
	# f = open("doc_formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_doc_formats(data,host)
	# print()


	quit()
