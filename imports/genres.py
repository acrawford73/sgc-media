#!/usr/bin/python3
import os
import sys
import json

with open('search-genres.json', "r") as file:
	genres = json.load(file)
	counter = len(genres)
	print(counter)
	file.close()

file = open('genres-fixture.json', "w")
file.write("[\n")

count=1
for genre in genres:
	file.write("{\n")
	file.write("  \"model\": \"roku_content.genre\",\n")
	file.write("  \"pk\": " + str(count) + ",\n")
	file.write("  \"fields\": {\n")
	file.write("    \"genre\": \"" + genre + "\"\n")
	file.write("  }\n")
	if count == counter:
		file.write("}\n")
		file.write("]\n")
		break
	else:
		file.write("},\n")
	count+=1
file.close()
quit(0)
