#!bin/python3

import requests
from requests.auth import HTTPBasicAuth

endpoint = 'https://api.imagga.com/v2'
api_key = 'acc_6dee3c0c4464145'
api_secret = '357d4450497e3cbd1b8bb40ceed7ccb5'

auth = HTTPBasicAuth(api_key, api_secret)

# Open the desired file
with open('media_assets/2021/06/20/0c9a87c973126d35eb2d3e3c9cebcf42ef589f8e.jpg', 'r') as image_file:
    filename = image_file.name
    print(filename)

    # Upload the multipart-encoded image with a POST
    # request to the /content endpoint
    content_response = requests.post('%s/content' % endpoint, auth=auth, files={filename: image_file})

    # Example /content response:
    # {'status': 'success',
    #  'uploaded': [{'id': '8aa6e7f083c628407895eb55320ac5ad',
    #                'filename': 'example_image.jpg'}]}
    uploaded_files = content_response.json()['uploaded']

    # Get the content id of the uploaded file
    content_id = uploaded_files[0]['id']

# Using the content id and the content parameter,
# make a GET request to the /tagging endpoint to get
# image tags
tagging_query = {'content': content_id}
tagging_response = requests.get('%s/tagging' % endpoint, auth=auth, params=tagging_query)

results = tagging_response.json()
print(results)
