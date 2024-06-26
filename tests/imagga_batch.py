#!bin/python3

import os
import requests
from requests.auth import HTTPBasicAuth

###
# API Credentials
API_KEY = os.environ.get('IMAGGA_API_KEY', 'acc_6dee3c0c4464145')  # Set API key here
API_SECRET = os.environ.get('IMAGGA_API_SECRET', '357d4450497e3cbd1b8bb40ceed7ccb5')  # Set API secret here
###

ENDPOINT = 'https://api.imagga.com/v2'

FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


class ArgumentException(Exception):
    pass

if API_KEY == 'YOUR_API_KEY' or API_SECRET == 'YOUR_API_SECRET':
    raise ArgumentException('You haven\'t set your API credentials. '
                            'Edit the script and set them.')

auth = HTTPBasicAuth(API_KEY, API_SECRET)


def upload_image(image_path):
    if not os.path.isfile(image_path):
        raise ArgumentException('Invalid image path')

    # Open the desired file
    with open(image_path, 'rb') as image_file:
        filename = image_file.name

        # Upload the multipart-encoded image with a POST
        # request to the /uploads endpoint
        content_response = requests.post(
            '%s/uploads' % ENDPOINT,
            auth=auth,
            files={'image': image_file})

        # Example /uploads response:
        #    {
        #      "result": {
        #        "upload_id": "i05e132196706b94b1d85efb5f3SaM1j"
        #      },
        #      "status": {
        #        "text": "",
        #        "type": "success"
        #      }
        #    }
        uploaded_file = content_response.json()['result']

        # Get the upload id of the uploaded file
        upload_id = uploaded_file['upload_id']

    return upload_id


def tag_image(image, upload_id=False, verbose=False, language='en'):
    # Using the content id and the content parameter,
    # make a GET request to the /tagging endpoint to get
    # image tags
    tagging_query = {
        'image_upload_id' if upload_id else 'image_url': image,
        'verbose': verbose,
        'language': language
    }
    tagging_response = requests.get(
        '%s/tags' % ENDPOINT,
        auth=auth,
        params=tagging_query)

    return tagging_response.json()


def extract_colors(image, upload_id=False):
    colors_query = {
        'image_upload_id' if upload_id else 'image_url': image,
    }

    colors_response = requests.get(
        '%s/colors' % ENDPOINT,
        auth=auth,
        params=colors_query)

    return colors_response.json()


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Tags images in a folder')

    parser.add_argument(
        'input',
        metavar='<input>',
        type=str,
        nargs=1,
        help='The input - a folder containing images')

    parser.add_argument(
        'output',
        metavar='<output>',
        type=str,
        nargs=1,
        help='The output - a folder to output the results')

    parser.add_argument(
        '--language',
        type=str,
        default='en',
        help='The language of the output tags')

    parser.add_argument(
        '--verbose',
        type=int,
        default=0,
        help='Whether to use verbose mode')

    parser.add_argument(
        '--merged-output',
        type=int,
        default=0,
        help='Whether to generate a single output file')

    parser.add_argument(
        '--include-colors',
        type=int,
        default=0,
        help='Whether to do color exctraction on the images too')

    args = parser.parse_args()
    return args


def main():
    import json
    args = parse_arguments()

    tag_input = args.input[0]
    tag_output = args.output[0]
    language = args.language
    verbose = args.verbose
    merged_output = args.merged_output
    include_colors = args.include_colors

    print('Tagging images started...')

    results = {}
    if os.path.isdir(tag_input):
        images = [filename for filename in os.listdir(tag_input)
                  if os.path.isfile(os.path.join(tag_input, filename)) and
                  filename.split('.')[-1].lower() in FILE_TYPES]

        images_count = len(images)
        for iterator, image_file in enumerate(images):
            image_path = os.path.join(tag_input, image_file)
            print('[%s / %s] %s uploading...' % (iterator + 1, images_count, image_path))
            #try:
            upload_id = upload_image(image_path)
            #except IndexError:
            #    continue
            #except KeyError:
            #    continue
            #except ArgumentException:
            #    continue

            tag_result = tag_image(upload_id, True, verbose, language)
			
            if not include_colors:
                results[image_file] = tag_result
            else:
                colors_result = extract_colors(upload_id, True)
                results[image_file] = {
                    'tagging': tag_result,
                    'colors': colors_result
                }
            print('[%s / %s] %s tagged' % (iterator + 1, images_count, image_path))
    else:
        raise ArgumentException('The input directory does not exist: %s' % tag_input)

    if not os.path.exists(tag_output):
        os.makedirs(tag_output)
    elif not os.path.isdir(tag_output):
        raise ArgumentException('The output folder must be a directory.')

    if merged_output:
        with open(os.path.join(tag_output, 'results.json'), 'wb') as results_file:
            results_file.write(json.dumps(results, ensure_ascii=False, indent=4).encode('utf-8'))
    else:
        for image, result in results.items():
            with open(os.path.join(tag_output, 'result_%s.json' % image), 'wb') as results_file:
                results_file.write(json.dumps(result, ensure_ascii=False, indent=4).encode('utf-8'))

    print;print('Image Recognition Completed.');print


if __name__ == '__main__':
    main()
