#!../bin/python3

import os
import json
import psycopg

# Dictionary with three items
def import_dict_3(sqlstr, key1, key2, key3, data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			#media_mediacountry(country_name,country_code)
			sql = "INSERT INTO " + sqlstr + " VALUES (%s, %s, %s)"
			data1 = item[key1]
			data2 = item[key2]
			data3 = item[key3]
			data = (data1,data2,data3,)
			cur.execute(sql, data)
			print(str(data1) + ", " + str(data2) + ", " + str(data3))
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

# Dictionary with two items
def import_dict_2(sqlstr, key1, key2, data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			#media_mediacountry(country_name,country_code)
			sql = "INSERT INTO " + sqlstr + " VALUES (%s, %s)"
			data1 = item[key1]
			data2 = item[key2]
			data = (data1,data2,)
			cur.execute(sql, data)
			print(str(data1) + " : " + str(data2))
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

def import_list(sqlstr, data, db_meta):
	conn = None	
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			print(item)
			sql = "INSERT INTO " + sqlstr + " VALUES (%s)"
			data = (item,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()





###

def import_countries(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			print(item['name'] + " : " + item['code'])
			sql = "INSERT INTO media_mediacountry(country_name,country_code) VALUES (%s, %s)"
			country_name = item['name']
			country_code = item['code']
			data = (country_name,country_code,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

### Video

def import_video_services(data, db_meta):
	conn = None	
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			print(item)
			sql = "INSERT INTO media_mediavideoservice(service_name) VALUES (%s)"
			data = (item,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

def import_video_genres(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			print(item)
			sql = "INSERT INTO media_mediavideogenre(genre) VALUES (%s)"
			data = (item,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

def import_video_formats(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for key, value in data.items():
			print(key, value)
			sql = "INSERT INTO media_mediavideoformat(doc_format,doc_format_name) VALUES (%s, %s)"
			data = (key,value,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()


### Audio

def import_audio_genres(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			print(item)
			sql = "INSERT INTO media_audiogenre(genre) VALUES (%s)"
			data = (item,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

def import_audio_formats(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for key, value in data.items():
			print(key, value)
			sql = "INSERT INTO media_mediaaudioformat(doc_format,doc_format_name) VALUES (%s, %s)"
			data = (key,value,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()


### Photo

def import_photo_formats(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for key, value in data.items():
			print(key, value)
			sql = "INSERT INTO media_mediaphotoformat(doc_format,doc_format_name) VALUES (%s, %s)"
			data = (key,value,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()


### Documents

def import_doc_formats(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for key, value in data.items():
			print(key, value)
			sql = "INSERT INTO media_mediadocformat(doc_format,doc_format_name) VALUES (%s, %s)"
			data = (key,value,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()


def import_services(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			print(item)
			sql = "INSERT INTO media_mediaservice(service) VALUES (%s)"
			data = (item,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()
		

### ROKU_CONTENT

def import_languages(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			print(item['code_iso_639_2'] + ", " + item['code_iso_639_1'] + ", " + item['language_name_eng'])
			sql = "INSERT INTO roku_content_language(code_iso_639_2,code_iso_639_1,language_name_eng) VALUES (%s, %s, %s)"
			lang1 = item['code_iso_639_2']
			lang2 = item['code_iso_639_1']
			lang3 = item['language_name_eng']
			data = (lang1,lang2,lang3,)
			cur.execute(sql, data)
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()



if __name__ == "__main__":

	print();print("Importing data...");print()

	from decouple import config
	DB_HOST = config('DB_HOST')
	DB_NAME = config('DB_NAME')
	DB_USER = config('DB_USER')
	DB_PASSWORD = config('DB_PASSWORD')
	db_meta = {'DB_HOST':DB_HOST,'DB_NAME':DB_NAME,'DB_USER':DB_USER,'DB_PASSWORD':DB_PASSWORD}


	# Languages
	# print("Importing languages...")
	# f = open("language-codes.json", "r")
	# data = json.load(f)
	# f.close()
	# import_languages(data,db_meta)
	# print()

	# Import Genres
	print("Importing content genres...")
	f = open("content-genres.json", "r")
	data = json.load(f)
	f.close()
	import_list("roku_content_genre(genre)", data, db_meta)
	print()
	
	# Countries
	# f = open("country-list.json", "r")
	# data = json.load(f)
	# f.close()
	# import_countries(data,db_meta)
	# print()

	### Video

	# Video Services
	#f = open("video-services.json", "r")
	#data = json.load(f)
	#f.close()
	#import_video_services(data,db_meta)
	#print()
	
	# Video Genres
	# f = open("video-genres.json", "r")
	# data = json.load(f)
	# f.close()
	# import_video_genres(data,db_meta)
	# print()

	#Video Formats
	# f = open("video-formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_video_formats(data,db_meta)
	# print()


	### Audio
	# Audio Genres
	# f = open("audio-genres.json", "r")
	# data = json.load(f)
	# f.close()
	# import_audio_genres(data,db_meta)
	# print()

	#Audio Formats
	# f = open("audio-formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_audio_formats(data,db_meta)
	# print()


	### Photo
	#Photo Formats
	# f = open("photo-formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_photo_formats(data,db_meta)
	# print()

	### Documents
	#Doc Formats
	# f = open("doc-formats.json", "r")
	# data = json.load(f)
	# f.close()
	# import_doc_formats(data,db_meta)
	# print()


	quit()
