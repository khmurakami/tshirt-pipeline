#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python Default Libraries
import os
import json

# Third Party Libraries
from google.cloud import storage
from PIL import Image, ImageDraw, ImageFont

import cv2
import numpy as np
import requests

# Personal Libraries
from printfulpy import PrintfulPy
from style_transfer import style_image

class GCPBucket():

    def __init__(self):

        self.bucket_client = storage.Client()

    def bucket_exists(self, bucket_name):
        """Check if a bucket exists with name
        Args:
            bucket_name (string): The name of the bucket you want to check
        Return:
            status (bool): True if the bucket exists. False if not
        """

        bucket = self.bucket_client.get_bucket(bucket_name)
        print(bucket)
        return bucket

    def create_bucket(self, bucket_name):

        # The name for the new bucket
        bucket_name = bucket_name

        if self.bucket_exists:
            # Creates the new bucket
            bucket = self.bucket_client.create_bucket(bucket_name)
            print('Bucket {} created.'.format(bucket.name))
        else:
            print("Bucket already exists")

    def upload_file(self, bucket_name, bucket_file_path, local_file_path):

        """Upload a file to a specified bucket
        Args:
            bucket_name (string): The name of the bucket
            bucket_file_path (string): The file location you want to upload the file to in the bucket
            local_file_path (string): The location of the file on your system that you want to upload
        Return:
            None
        """

        bucket = self.bucket_client.get_bucket(bucket_name)
        blob = bucket.blob(bucket_file_path)
        blob.upload_from_filename(local_file_path)
        print("uploaded file")

    def list_bucket_files(self, bucket_name, bucket_file_path):

        """List all of the files in a bucket by a specific path

        Args:
            bucket_name (string): Name of the bucket
            bucket_file_path (string): The folder(s) you want to list the contents of

        Return
            blobs (list of Strings) The contents of the bucket in a list

        """

        bucket = self.bucket_client.bucket('my_project')
        blobs = list(bucket.list_blobs(prefix='data/'))
        return blobs

    def create_public_url(self, bucket_name, bucket_path):

        """Create downloadable bucket url. Based on this: http(s)://storage.googleapis.com/[bucket]/[object]

        Args:
            bucket_name (string): Name of the bucket
            bucket_path (string): Name to the object you want to create a public url of

        """

        url = "https://storage.googleapis.com/{0}/{1}".format(bucket_name, bucket_path)
        return url


def remove_style_background(image_file, output_file):

    """Remove the background generated from style transfer

    Args:
        image_file (string): The name of the input file created by style transfer
        output_file (string): The name of the output file

    Return:
        None

    """

    img = Image.open(image_file)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []

    # Hard coded to get rid of style transfer background
    for item in datas:
        if 80 <= item[0] <= 120 and 85 <= item[1] <= 101 and 100 <= item[2] <= 122:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            print(item)


    img.putdata(newData)
    img.save(output_file, "PNG")

def create_text_image(input_string, font_path, output_file):

    """Input text to create image from it. Creates a PNG file

    Args:
        input_string (string): The string you want drawn
        font_path (string): Path to the font path
        output_file (string): Name of the output file

    Return:
        None

    """

    # sample text and font
    unicode_text = u'{0}'.format(input_string)
    font = ImageFont.truetype(font_path, 100, encoding="unic")

    # get the line size
    text_width, text_height = font.getsize(unicode_text)

    # create a blank canvas with extra space between lines
    canvas = Image.new('RGB', (text_width + 100, text_height + 100), "white")

    # draw the text onto the text canvas, and use black as the text color
    draw = ImageDraw.Draw(canvas)
    draw.text((5,5), u'Beautiful', 'black', font)

    # save the blank canvas to a file
    canvas.save(output_file, "PNG")
    #canvas.show()

def remove_text_background(image_text, output_file):

    """Remove the white space behind a text. Saved as png

    Args: 
        image_text (string): Path the text image
        output_file (string): Name of the file you want created

    Return:
        None

    """

    img = Image.open(image_text)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []

    # Hard coded to get rid of style transfer background
    for item in datas:
        if item[0] <= 255 and item[1] <= 255 and item[2] ==255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            print(item)


    img.putdata(newData)
    img.save(output_file, "PNG")

def download_printful_designs(raw_json, folder_path):

    """Download all images that are in the json result of a mockup design

    Args:
        raw_json (dict): The raw json from the mock up design
        folder_path (string): Folder in which you want to store the designs

    Return:
        None

    """

    # Get the task id of the job in queue to create t shirt mock ups
    task_id = raw_json["result"]["task_key"]

    # Create a folder named by the task id to store the images
    dirName = os.path.join(folder_path, task_id)

    # Create target Directory if don't exist
    if not os.path.exists(dirName):
        try: 
            os.makedirs(dirName)
            print("Directory {0} Created ".format(dirName))
        except:
            print("Director already exists")

    # Iterate through the json and append the json fields as the image name and download them
    for i in raw_json["result"]["mockups"]:
        for j in i["extra"]:

            # Get the options name and clean out spaces and special charcters to name the file
            option_lower = j['option']
            option_lower = ''.join(e for e in option_lower if e.isalnum()).lower()

            option_group_lower = j['option_group']
            option_group_lower = ''.join(e for e in option_group_lower if e.isalnum()).lower()
            
            file_name = os.path.join(dirName, "{0}_{1}.jpg".format(option_lower, option_group_lower))
            print(file_name)

            # Create the file and save the content to that file
            f = open(file_name, 'wb')

            f.write(requests.get(j["url"]).content)

            f.close()

    print("Finished Downloading Images")

def load_folder(folder_path):

    """Read in folder of images

    """

    pass

def load_image(image_path):

    pass

def load_json(json_file_path):

    """Load Json File into a dict. Used for saved json results from printful

    Args:
        json_file_path (String): The path to the json file

    Return:
        data (dict): The json loaded from the file

    """

    with open(json_file_path) as json_file:
        data = json.load(json_file)

    return data


if __name__ == "__main__":
    #create_text_image("Beautiful", "Lintsec.ttf", "text_creation.png")
    #remove_text_background("text_creation.png", "remove_text.png")
    #print("im done")
    style_image("input_matrix.jpg", "matrix_style.jpg", "matrix_output.png")
    #gcp_client = GCPBucket()
    # printful_client = PrintfulPy(
    #     api_key="8naldv9l-3gyz-cl2g:yv7r-pwgnxg8e5bjr")

    # data = load_json("mock_up_get_result.json")
    # download_printful_designs(data, "test_folder")

    #http(s)://storage.googleapis.com/[bucket]/[object]

    # google_download_link = "https://storage.googleapis.com/tshirt_pictures/input/tiffany_test.png"
    # raw_json = printful_client.create_mockup_gen_task(variant_ids=[4012, 4013], image_url=google_download_link)
    # with open("mock_up_json.json", "w") as data_file:
    #    json.dump(raw_json, data_file, indent=4, sort_keys=True)
    # print(raw_json)


    #remove_style_background("style_dog_background.png", "style_dog_processed.png")
    #style_image("pre_text.png", "style.jpg", "text_style_example.png")
    # gcp_client.create_bucket("tshirt_pictures")
    # gcp_client.bucket_exists("tshirt_pictures")
    #gcp_client.upload_file("tshirt_pictures", "input/{0}".format("upload_text.png"), "upload_text.png")
    # https://storage.cloud.google.com/tshirt_pictures/input/output.png
    # raw_json = printful_client.create_mockup_gen_task(variant_ids=[4012, 4013], image_url="https://00e9e64bac9dbd245f6147731ff46d838650047fa0f15e3881-apidata.googleusercontent.com/download/storage/v1/b/tshirt_pictures/o/input%2Fupload_text.png?qk=AD5uMEs6gztqmNZdnKkn3xdv6qNJidvGs--XH0yxEJP7t7hlVgclwNTRPg5SM6d-LahbZucalZCjVRWqihB1vqEUxFF7VwYEvBXwx7lH7G936ziaNpvF0r8xAFWs4G9qXq19bWWXKcEHUd1AIoaLCiTNnPdJBkbPWYXAjL7mzPSKnYeSDbKx2rj73BMg1J8IYo1KtcGtvgBaTodwisbcWZ9_qv3ix4rvkEjAnxp7yy79tn7PKZbRdhRtcGJZDByLD0W5phZdMI8AP72WHsEA2PN9LjODHrNmOYbtIhc2_MPcxDmV923ZUeu-y-8fQJnwqe8EcEaL0RwHCPPSbLEiMCgHgiT_iD8K2D-v_h85g1fqg7N3FXMHJkj43vgv6pLD7e3rKsQVXsX6udEu9vozLdSfI1T_tOR6pwggD6Wm-nCkE7pI5mvXuyVasN6kEnlGI_uZeQdhnejKhJ_rJDgAZVuQgoj635RLUQNJknJsDhI-JJEpK0Tk4vhYe-2xMSUHb_4ogHnFTZruSlXD6kcnM_BDb5cG-qfZTWKaDeH3_kQsPiv0EQYsWf6cIbXLlAxO_UEawFKyzyjscpSiJ1k0yPIf6nVIuJevxozSkvYFzlUhNpFpmN5_1CzVxc1pfMG8TkvFRuKVSslX-9Nhq60BWu3DbDexxX2NZ3dlCqihwRNPsuz2eOPbJ868s0tqJuvGyBUHS3LP7hj5eTx7wNrqfiQsPCbRKyD-48M_HFxmPy9tKEdnlLhVnEfoVsIkwiFYb4wHkunQJ8lVfCVnFsqWFJyAPooGC3-9N8H_YixJVrExFxsvIv_4uIE")
    # print(raw_json)
    # with open("mock_up_json.json", "w") as data_file:
    #    json.dump(raw_json, data_file, indent=4, sort_keys=True)
    # raw_json = printful_client.get_mockup_gen_task_result("z9c4300ab4af3819370472523b9309fd")
    # with open("mock_up_get_result.json", "w") as data_file:
    #    json.dump(raw_json, data_file, indent=4, sort_keys=True)
