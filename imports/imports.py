#!../bin/python3

import os
import json
import psycopg
import argparse


# Dictionary with three key:value pairs
def import_dict_3(sqlstr, key1, key2, key3, data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			#media_mediacountry(country_name,country_code)
			sql = "INSERT INTO " + sqlstr + " VALUES (%s, %s, %s)"
			data = (item[key1],item[key2],item[key3],)
			cur.execute(sql, data)
			print(str(data1) + ", " + str(data2) + ", " + str(data3))
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

# Dictionary with two key:value pairs
def import_dict_2(sqlstr, key1, key2, data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for item in data:
			sql = "INSERT INTO " + sqlstr + " VALUES (%s, %s)"
			data1 = item[key1]
			data2 = item[key2]
			data = (data1,data2,)
			cur.execute(sql, data)
			print(str(data1) + ", " + str(data2))
	except (Exception, psycopg.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.commit()
			conn.close()

def import_dict(data, db_meta):
	conn = None
	try:
		conn = psycopg.connect(host=db_meta['DB_HOST'], dbname=db_meta['DB_NAME'], user=db_meta['DB_USER'], password=db_meta['DB_PASSWORD'])
		cur = conn.cursor()
		for key, value in data.items():
			print(key, value)
			sql = "INSERT INTO " + sqlstr + " VALUES (%s, %s)"
			data = (key,value,)
			cur.execute(sql, data)
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

if __name__ == "__main__":

	from decouple import config
	DB_HOST = config('DB_HOST')
	DB_NAME = config('DB_NAME')
	DB_USER = config('DB_USER')
	DB_PASSWORD = config('DB_PASSWORD')
	db_meta = {'DB_HOST':DB_HOST,'DB_NAME':DB_NAME,'DB_USER':DB_USER,'DB_PASSWORD':DB_PASSWORD}

	parser = argparse.ArgumentParser(prog='Importer', description='Imports JSON data files into database', epilog='Text at the bottom of help')
	parser.add_argument('all', '--all')
	parser.add_argument('country', '--country')

	parser.add_argument('vf', '--video-format')
	parser.add_argument('vs', '--video-service')
	parser.add_argument('vg', '--video-genre')

	parser.add_argument('af', '--audio-format')
	parser.add_argument('as', '--audio-service')
	parser.add_argument('ag', '--audio-genre')

	parser.add_argument('pf', '--photo-format')
	parser.add_argument('ps', '--photo-service')
	parser.add_argument('df', '--doc-format')

	parser.add_argument('lang', '--language')
	parser.add_argument('cg', '--content-genre')
	parser.add_argument('eit', '--external-id-type')
	parser.add_argument('rs', '--rating-source')
	parser.add_argument('pr', '--parental-rating')
	parser.add_argument('rating', '--rating')
	parser.add_argument('sg', '--search-genre')

	args = parser.parse_args()
	args = args.lower()

	if args == "all"

		print();print("Importing data...");print()

		# Languages
		print("Importing languages...")
		f = open("language-codes.json", "r")
		data = json.load(f)
		f.close()
		import_dict3("roku_content_language(code_iso_639_2,code_iso_639_1,language_name_eng)", "code_iso_639_2", "code_iso_639_1", "language_name_eng", data, db_meta)

		# External ID Types
		print();print("Importing external IDs types...")
		f = open("external-id-types.json", "r")
		data = json.load(f)
		f.close()
		import_dict("roku_content_externalidtype(external_id_type,external_id_long_name)", data, db_meta)

		# Content Genres
		print();print("Importing content genres...")
		f = open("content-genres.json", "r")
		data = json.load(f)
		f.close()
		import_list("roku_content_genre(genre)", data, db_meta)

		# Parental Ratings
		print();print("Importing parental ratings...")
		f = open("parental-ratings.json", "r")
		data = json.load(f)
		f.close()
		import_list("roku_content_parentalrating(parental_rating)", data, db_meta)

		# Rating Sources
		print();print("Importing rating sources...")
		f = open("rating-sources.json", "r")
		data = json.load(f)
		f.close()
		import_dict2("roku_content_ratingsource(source_name,source_long_name)", "source_name", "source_long_name", data, db_meta)

		### MEDIA

		# Countries
		print();print("Importing countries...")
		f = open("country-list.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediacountry(country_name,country_code)", data, db_meta)

		# Video Formats
		print();print("Importing video formats...")
		f = open("video-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediavideoformat(doc_format,doc_format_name)", data, db_meta)

		# Video Services
		print();print("Importing video services...")
		f = open("video-services.json", "r")
		data = json.load(f)
		f.close()
		import_list("media_mediavideoservice(service_name)", data, db_meta)
		
		# Video Genres
		print();print("Importing video genres...")
		f = open("video-genres.json", "r")
		data = json.load(f)
		f.close()
		import_list("media_mediavideogenre(genre)", data, db_meta)

		# Audio Genres
		print();print("Importing audio genres...")
		f = open("audio-genres.json", "r")
		data = json.load(f)
		f.close()
		import_list("media_mediavaudiogenre(genre)", data, db_meta)

		# Audio Formats
		print();print("Importing audio formats...")
		f = open("audio-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediaaudioformat(doc_format,doc_format_name)", data, db_meta)

		# Photo Formats
		print();print("Importing photo formats...")
		f = open("photo-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediaphotoformat(doc_format,doc_format_name)", data, db_meta)

		# Document Formats
		print();print("Importing document formats...")
		f = open("doc-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediadocformat(doc_format,doc_format_name)", data, db_meta)

	elif args == "country":

		# Countries
		print();print("Importing countries...")
		f = open("country-list.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediacountry(country_name,country_code)", data, db_meta)

	elif args == "vf":

		# Video Formats
		print();print("Importing video formats...")
		f = open("video-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediavideoformat(doc_format,doc_format_name)", data, db_meta)

	elif args == "vs":

		# Video Services
		print();print("Importing video services...")
		f = open("video-services.json", "r")
		data = json.load(f)
		f.close()
		import_list("media_mediavideoservice(service_name)", data, db_meta)

	elif args == "vg":
		
		# Video Genres
		print();print("Importing video genres...")
		f = open("video-genres.json", "r")
		data = json.load(f)
		f.close()
		import_list("media_mediavideogenre(genre)", data, db_meta)

	elif args == "ag":

		# Audio Genres
		print();print("Importing audio genres...")
		f = open("audio-genres.json", "r")
		data = json.load(f)
		f.close()
		import_list("media_mediavaudiogenre(genre)", data, db_meta)

	elif args == "af":

		# Audio Formats
		print();print("Importing audio formats...")
		f = open("audio-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediaaudioformat(doc_format,doc_format_name)", data, db_meta)

	elif args == "pf":

		# Photo Formats
		print();print("Importing photo formats...")
		f = open("photo-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediaphotoformat(doc_format,doc_format_name)", data, db_meta)

	elif args == "df":

		# Document Formats
		print();print("Importing document formats...")
		f = open("doc-formats.json", "r")
		data = json.load(f)
		f.close()
		import_dict("media_mediadocformat(doc_format,doc_format_name)", data, db_meta)

	# ROKU CONTENT

	elif args == "lang":

		# Languages
		print("Importing languages...")
		f = open("language-codes.json", "r")
		data = json.load(f)
		f.close()
		import_dict3("roku_content_language(code_iso_639_2,code_iso_639_1,language_name_eng)", "code_iso_639_2", "code_iso_639_1", "language_name_eng", data, db_meta)

	elif args == "eit":

		# External ID Types
		print();print("Importing external IDs...")
		f = open("external-id-types.json", "r")
		data = json.load(f)
		f.close()
		import_dict("roku_content_externalidtype(external_id_type,external_id_long_name)", data, db_meta)

	elif args == "cg":

		# Content Genres
		print();print("Importing content genres...")
		f = open("content-genres.json", "r")
		data = json.load(f)
		f.close()
		import_list("roku_content_genre(genre)", data, db_meta)

	elif args == "pr":

		# Parental Ratings
		print();print("Importing parental ratings...")
		f = open("parental-ratings.json", "r")
		data = json.load(f)
		f.close()
		import_list("roku_content_parentalrating(parental_rating)", data, db_meta)

	elif args == "rs":

		# Rating Sources
		print();print("Importing rating sources...")
		f = open("rating-sources.json", "r")
		data = json.load(f)
		f.close()
		import_dict2("roku_content_ratingsource(source_name,source_long_name)", "source_name", "source_long_name", data, db_meta)

	elif args == "rating":

		# Ratings
		print("Importing ratings...")
		f = open("ratings.json", "r")
		data = json.load(f)
		f.close()
		import_dict("roku_content_rating(rating_id,rating_source_id)", data, db_meta)

	elif args == "sg":

		print("NOT IMPLEMENTED YET")
		break

		# Search Genres
		print();print("Importing content genres...")
		f = open("search-genres.json", "r")
		data = json.load(f)
		f.close()
		import_list("roku_search_genre(genre)", data, db_meta)

print()
quit(0)
