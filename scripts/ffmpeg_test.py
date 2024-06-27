#!bin/python3

import os,sys
import ffmpeg

def get_video_metadata(media_path):
	#try:
	metadata = ffmpeg.probe(media_path)["streams"]
	if metadata is not None:
		return metadata
	#except ffmpeg.Error as error:
	#except (Exception, ffmpeg.Error) as error:
		#print(error)
		#print(ffmpeg.Error.stderr)
	else:
		return False

#media_path = "media_assets/drink-one-cup-per-day-as-a.mp4"
media_path = "birds_20210824.mp4"
metadata = get_video_metadata(media_path)
print(metadata)

if metadata != False:

	if 'bit_rate' in metadata[0]:
		video_bitrate = metadata[0]['bit_rate']
	else:
		video_bitrate = 0

	try:
		audio_bitrate = metadata[1]['bit_rate']
	except IndexError:
		audio_bitrate = 0
		print("Index doesn't exist!")

	# if 'bit_rate' in metadata[1]:
	# 	audio_bitrate = metadata[1]['bit_rate']
	# else:
	# 	audio_bitrate = 0
	# else:
	# 	print("NO AUDIO PRESENT")

	print(video_bitrate)
	print(audio_bitrate)
	quit(0)
else:
	quit(1)
