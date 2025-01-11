#!bin/python3

import psycopg2
import os
import datetime,time
from time import strftime


def getauth():
	sql = "SELECT * FROM auth_user"
	conn = psycopg2.connect(host="localhost", dbname="sgc", user="sgc", password="sgcmedia")
	cur = conn.cursor()
	cur.execute(sql)
	print("Results: " + str(cur.rowcount))

if __name__ == "__main__":

	created = datetime.datetime.now()
	print("NOW: " + created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

	created = datetime.datetime.utcnow()
	print("UTC: " + created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

	path = "media_assets/photo/Alberta/file.jpg"
	asset_full_path = path.split('media_assets/',)[1]
	print(asset_full_path)

	print()
	media_path = "media_assets/"
	date_path = created.strftime("%Y/%m/%d/")
	print(os.path.join(media_path,date_path))
	print()

	import shutil
	shutil.copy('/var/www/html/channel/content/photo/tumblr_oghydyty401reae9uo1_1280.jpg', 'media_assets/')

	getauth()
	quit()
