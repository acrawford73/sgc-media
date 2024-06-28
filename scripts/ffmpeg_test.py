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
#media_path = "af3.ts"
#media_path = "todd.ts"
media_path = "todd.mp4"

metadata = get_video_metadata(media_path)
print(metadata)


audio_bitrate = 0
video_bitrate = 0


if metadata != False:
	print()
	print("Metadata Indexes:")

	index_count = 0
	while index_count < len(metadata):

		if 'codec_type' in metadata[index_count]:
			if metadata[index_count]['codec_type'] == "video":
				print("Video index " + str(index_count))
				if 'bit_rate' in metadata[index_count]:
					video_bitrate = metadata[index_count]['bit_rate']
				else:
					print("*** Video bit rate missing from metadata")
		
			elif metadata[index_count]['codec_type'] == "audio":
				print("Audio index " + str(index_count))
				if 'bit_rate' in metadata[index_count]:
					audio_bitrate = metadata[index_count]['bit_rate']
				else:
					print("*** Audio bit rate missing from metadata")
		
			elif metadata[index_count]['codec_type'] == "data":
				print("Data index " + str(index_count))
			
			else:
				print("*** Unknown codec_type")
		else:
			print("*** codec_type field missing in metadata")
		
		index_count += 1


	print()
	print("Video Bitrate = " + str(video_bitrate))
	print("Audio Bitrate = " + str(audio_bitrate))
	print()
	quit(0)
else:
	quit(1)
