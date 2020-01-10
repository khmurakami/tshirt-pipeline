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


def remove_style_background(image_file, output_file):

    """Remove the background generated from style transfer

    Args:
        image_file (string): The name of the input file created by style transfer
        output_file (string): The name of the output file

    Return:
        None

    """

    # Convert image to add another channel for removing tranparency
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

        variant_id = str(i["variant_ids"])

        for j in i["extra"]:

            # Get the options name and clean out spaces and special charcters to name the file
            option_lower = j['option']
            option_lower = ''.join(e for e in option_lower if e.isalnum()).lower()

            option_group_lower = j['option_group']
            option_group_lower = ''.join(e for e in option_group_lower if e.isalnum()).lower()
            
            file_name = os.path.join(dirName, "{0}_{1}_{2}.jpg".format(option_lower, option_group_lower, variant_id))
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