#!../bin/python3

import os
import json
import psycopg2


def import_genres(data):
	for item in data:
		print(item)
		sql = "INSERT INTO media_audiogenre(genre) VALUES (%s)"
		data = (item,)
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


def import_services(data):
	for item in data:
		print(item)
		sql = "INSERT INTO media_mediaservice(service) VALUES (%s)"
		data = (item,)
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
				


if __name__ == "__main__":

	print();print("Importing data...");print()

	# Audio Genres
	f = open("genres.json", "r")
	data = json.load(f)
        f.close()
	import_genres(data)
	print()

	# Services
	f = open("services.json", "r")
	data = json.load(f)
        f.close()
	import_services(data)
	print()


	quit()
