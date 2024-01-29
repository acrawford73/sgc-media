#!/bin/python3

import sys
import ffmpeg


def generate_thumbnails(asset_full_path, thumbnail_path):
	probe = ffmpeg.probe(asset_full_path)
	time = float(probe['streams'][0]['duration']) // 2
	width = probe['streams'][0]['width']
	try:
		(
			ffmpeg
			.input(asset_full_path, ss=time)
			.filter('scale', width, -1)
			.output(thumbnail_path, vframes=1)
			.overwrite_output()
			.run(capture_stdout=True, capture_stderr=True)
		)
	except ffmpeg.Error as e:
		log.error(e.stderr.decode(), file=sys.stderr)
		return False


if __name__ == "__main__":
	
	asset_full_path = "media_assets/How to Deal with Past Trauma and Get Past It   Jordan B Peterson.mp4"
	thumbnail_path = "thumb.png"
	
	generate_thumbnails(asset_full_path, thumbnail_path)

	print();print("DONE");print()

	quit(0)