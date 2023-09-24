#!bin/python3

import os,sys
import ffmpeg

def get_video_metadata(media_path):
	try:
		metadata = ffmpeg.probe(media_path)["streams"]
		if metadata is not None:
			return metadata
	except:
		log.error(error)
		return False

#media_path = "media_assets/drink-one-cup-per-day-as-a.mp4"
media_path = "media_assets/Dr. Cody at Tech for Psych typing with his brain in 2023 sep 24 2023.mp4"
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

quit()