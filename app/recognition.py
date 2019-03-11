import ffmpeg
import glob
import io
import os
import sys

from google.cloud import vision
from google.cloud.vision import types
from pytube import *
from threading import Thread

GOOGLE_APPLICATION_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS"
YOUTUBE_URL_PREFIX = "http://youtube.com/watch?v="
KEY_RESOLUTION = "resolution"
FILE_EXTENSION = "mp4"
OUTPUT_FILENAME = "summarize_output"
NUMBER_OF_HIGHLIGHTS = 5
WORKING_DIRECTORY = "/tmp/"
CREDENTIALS_PATH = "credentials/credentials.json"
WILDCARD = "*"

current_directory = os.path.dirname(os.path.realpath(__file__))
os.environ[GOOGLE_APPLICATION_CREDENTIALS] = os.path.join(current_directory, CREDENTIALS_PATH)

client = vision.ImageAnnotatorClient()

def fetch_label_for_image(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if len(labels) == 0:
        return None
    else:
        return labels[0].description

def download_youtube_video(video_id):
    video_url = YOUTUBE_URL_PREFIX + video_id
    youtube = YouTube(video_url)
    youtube \
        .streams \
        .filter(progressive=True, file_extension=FILE_EXTENSION) \
        .order_by(KEY_RESOLUTION) \
        .first() \
        .download(filename=OUTPUT_FILENAME)
    return int(str(youtube.length))

def fetch_labels(number_of_highlights, video_length, output_dictionary):
    for index in range(0, number_of_highlights):
        time = index * (video_length / 5)
        jpg_filename = OUTPUT_FILENAME + str(index) + ".jpg"
        stream = ffmpeg \
            .input(OUTPUT_FILENAME + "." + FILE_EXTENSION, ss=time) \
            .output(jpg_filename, vframes=1)
        ffmpeg.overwrite_output(stream).run()
        full_jpg_path = WORKING_DIRECTORY + jpg_filename
        output_dictionary[time] = fetch_label_for_image(full_jpg_path)

def remove_temporary_files():
    for filename in glob.glob(WORKING_DIRECTORY + OUTPUT_FILENAME + WILDCARD):
        os.remove(filename) 
        pass

def fetch_highlights(video_id, output_dictionary, number_of_highlights):
    print("Fetching highlights.")
    cwd = os.getcwd()
    os.chdir(WORKING_DIRECTORY)
    video_length = download_youtube_video(video_id)
    fetch_labels(number_of_highlights, video_length, output_dictionary)
    remove_temporary_files()
    os.chdir(cwd)

def fetch_highlights_thread(video_id, output_dictionary, number_of_highlights=NUMBER_OF_HIGHLIGHTS):
    return Thread(target=fetch_highlights, args=(video_id, output_dictionary, number_of_highlights))
