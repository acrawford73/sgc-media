#!bin/python3

"""
Example usage:
    python organize.py <input_folder> <output_folder>

input_folder - the folder with images to organize
output_folder - the output folder to put the organized images

Requirements:
 requests (http://docs.python-requests.org/en/master/)
"""

import os
import sys
import shutil
import requests

try:
    input_folder = sys.argv[1]
except IndexError:
    print('No input folder has been provided')
    sys.exit(0)

try:
    output_folder = sys.argv[2]
except IndexError:
    print('No output folder has been provided')
    sys.exit(0)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

endpoint = 'https://api.imagga.com/v1'
api_key = 'acc_d24c845d460bc9e'
api_secret = '12ea701b5a10922224589ea50e8da667'


def upload_image(image_path):
    with open(image_path, 'r') as image_file:
        filename = image_file.name

        content_response = requests.post(
            '%s/content' % endpoint,
            auth=(api_key, api_secret),
            files={filename: image_file})

        uploaded_files = content_response.json()['uploaded']

        content_id = uploaded_files[0]['id']

    return content_id


def process_image(content_id, api_path):
    query = {'content': content_id}
    response = requests.get(
        '%s/%s' % (endpoint, api_path),
        auth=(api_key, api_secret),
        params=query)

    return response.json()


images = filter(lambda x: x.endswith('jpg'),
                map(lambda x: os.path.join(input_folder, x),
                    os.listdir(input_folder)))

for image in images:
    content_id = upload_image(image)
    tagging_result = process_image(
        content_id, 'tagging')
    categorization_result = process_image(
        content_id, 'categorizations/personal_photos')
    try:
        image_category = categorization_result[
            'results'][0]['categories'][0]['name']
    except KeyError, IndexError:
        continue
    try:
        image_tag = tagging_result[
            'results'][0]['tags'][0]['tag']
    except KeyError, IndexError:
        continue

    category_path = os.path.join(output_folder, image_category)
    tag_path = os.path.join(category_path, image_tag)
    if not os.path.exists(tag_path):
        os.makedirs(tag_path)

    shutil.copyfile(
        image, os.path.join(tag_path, os.path.basename(image)))
