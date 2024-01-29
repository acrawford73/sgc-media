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
media_path = "media_assets/6G From Connecting Things to Connected Intelligence (World Government Summit 2022).mp4"
metadata = get_video_metadata(media_path)
print(metadata)
if metadata != False:
	if metadata[0]['bit_rate'] is not None:
		video_bitrate = metadata[0]['bit_rate']
	else:
		video_bitrate = 0
	if metadata[1]['bit_rate'] is not None:
		audio_bitrate = metadata[1]['bit_rate']
	else:
		audio_bitrate = 0

	print(video_bitrate)
	print(audio_bitrate)
	quit(0)
else:
	quit(1)
