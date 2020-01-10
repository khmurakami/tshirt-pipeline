#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Default Libraries
import json
import os
import time

# Third Party Libraries
from PIL import Image

import cv2
import numpy

# Company Libraries. Can be found in the lib folder
from tshirt_pipeline.gcp_client import GCPBucket
from tshirt_pipeline.image_processing import download_printful_designs, load_json
from printfulpy import PrintfulPy
from style_transfer import file_style_image, load_img, tensor_to_image
from background_helper import BackgroundRemoval

def convert_jpg_to_png(input_image_folder):

    """Convert all jpg images to png properly. Deletes jpg's after its done

    Args:
        input_image_folder (string): Path to folder of jpgs

    Return:
        None

    """

    for filename in os.listdir(input_image_folder):
        if filename.endswith(".jpg"):
            im = Image.open(os.path.join(input_image_folder, filename))
            name = os.path.splitext(os.path.basename(filename))[0] +'.png'
            rgb_im = im.convert('RGB')
            rgb_im.save(os.path.join(input_image_folder, name))
            os.remove(os.path.join(input_image_folder, filename))

    print("Finished Converting")

def style_permutations(input_image_folder, input_style_folder, output_folder):

    """Test function to go through all the input images and input styles for evaluating

    Args:
        input_image_folder (string): Path to the input folder of images
        input_style_folder (string): Path to the styles you want to use
        output_folder (string): Path to the folder you want to output the images to

    Return:
        None

    """

     # Create target Directory if don't exist
    if not os.path.exists(output_folder):
        try: 
            os.makedirs(output_folder)
            print("Directory {0} Created ".format(output_folder))
        except:
            print("Director already exists")

    # Get all the images in the directories
    input_image_list = os.listdir(input_image_folder)
    input_style_list = os.listdir(input_style_folder)

    # Go through all the permutations of the images and styles
    for image in input_image_list:
        for style in input_style_list:
            if image.endswith(".png") and style.endswith(".png"):

                # Get the file base name to name the output
                input_image_base = os.path.splitext(os.path.basename(image))[0]
                input_style_base = os.path.splitext(os.path.basename(style))[0]

                # Name the output image and create path to output location
                output_image = input_image_base + "_" + input_style_base + '.png'
                output_location = os.path.join(output_folder, output_image)

                # Apply the style transfer
                style_image(os.path.join(input_image_folder, image), os.path.join(input_style_folder, style), output_location)
                print(output_location)

    print("Finished all style permutations")

def apply_mask(input_image, input_style, background_nn_model):

    model_path = background_nn_model
    new_input = tensor_to_image(load_img(input_image))
    extract_client = BackgroundRemoval(model_path)
    cropped_area = extract_client.run_visualization(new_input)

    # Stylize the Original Image and conver
    style_input = file_style_image(input_image, input_style)
    style_input = style_input.convert("RGBA")
    style_input = numpy.asarray(style_input)
    style_copy = style_input[:,:-3,:]
    cropped_array = numpy.asarray(cropped_area)
    height, width = cropped_array.shape[:2]
    cropped_copy = cropped_array.copy()

    for i in range(width):
        for j in range(height):
            pixel = cropped_copy[j, i]
            if numpy.all(pixel != [255, 255, 255, 0]):
                cropped_copy[j, i] = style_copy[j, i] 

    #cv2.imwrite("final.png", cropped_copy)
    return cropped_copy

def file_generate_tshirt(input_file, input_style, background_model_path, output_folder, printful_api_key):

    """Generate a tshirt

    Args: 

    Return:
        None

    """

     # Create target Directory if don't exist
    if not os.path.exists(output_folder):
        try: 
            os.makedirs(output_folder)
            print("Directory {0} Created ".format(output_folder))
        except:
            print("Director already exists")

    # Create and get a mask
    model_path = background_model_path
    img = apply_mask(input_file, input_style, model_path)

     # Get the file base name to name the output
    input_image_base = os.path.splitext(os.path.basename(input_file))[0]
    input_style_base = os.path.splitext(os.path.basename(input_style))[0]

    # Name the output image and create path to output location
    output_image = input_image_base + "_" + input_style_base

    # Save for debugging and uploading to google bucket. dont remove
    temp_image = "{0}/{1}_test.png".format(output_folder, output_image)

    cv2.imwrite(temp_image, img)

    gcp_client = GCPBucket()
    printful_client = PrintfulPy(
        api_key=printful_api_key)

    bucket_name = "tshirt_pictures"

    status = gcp_client.bucket_exists(bucket_name)
    if status is False:
        gcp_client.create_bucket(bucket_name)

    gcp_client.upload_file(bucket_name, "input/{0}".format(temp_image), temp_image)
    google_download_link = "https://storage.googleapis.com/tshirt_pictures/input/{0}".format(temp_image)
    raw_json = printful_client.create_mockup_gen_task(variant_ids=[4012, 4172, 4142, 4112], image_url=google_download_link)
    with open("{0}/mock_up_json.json".format(output_folder), "w") as data_file:
       json.dump(raw_json, data_file, indent=4, sort_keys=True)

    task_key = raw_json['result']['task_key']

    status_print = False

    while(status_print==False):
        time.sleep(30)
        result = printful_client.get_mockup_gen_task_result(task_key)
        if result['result']['status'] == "completed":
            status_print = True
            print("Completed Mockup")
            with open("{0}/mock_up_json_result.json".format(output_folder), "w") as data_file:
                json.dump(result, data_file, indent=4, sort_keys=True)

    #os.remove("{0}_test.png")
    download_printful_designs(result, output_folder)

def file_generate_tshirt_permutations(input_image_folder, input_style_folder, background_model_path, output_folder, printful_api_key):

     # Create target Directory if don't exist
    if not os.path.exists(output_folder):
        try: 
            os.makedirs(output_folder)
            print("Directory {0} Created ".format(output_folder))
        except:
            print("Director already exists")

    # Get all the images in the directories
    input_image_list = os.listdir(input_image_folder)
    input_style_list = os.listdir(input_style_folder)

    # Go through all the permutations of the images and styles
    for image in input_image_list:
        for style in input_style_list:
            if image.endswith(".png") and style.endswith(".png"):

                # Get the file base name to name the output
                input_image_base = os.path.splitext(os.path.basename(image))[0]
                input_style_base = os.path.splitext(os.path.basename(style))[0]

                folder_name = input_image_base + "_" + input_style_base
                generate_output_folder = os.path.join(output_folder, folder_name)

                # Create target Directory if don't exist
                if not os.path.exists(generate_output_folder):
                    try: 
                        os.makedirs(generate_output_folder)
                        print("Directory {0} Created ".format(generate_output_folder))
                    except:
                        print("Director already exists")

                file_generate_tshirt(os.path.join(input_image_folder, image), os.path.join(input_style_folder, style), background_model_path, generate_output_folder, printful_api_key)

    

    

if __name__ == "__main__":

    #create_text_image("Beautiful", "Lintsec.ttf", "text_creation.png")
    #remove_text_background("text_creation.png", "remove_text.png")

    # Convert all jpgs to pngs and delete pngs
    #convert_jpg_to_png("input_images")
    #convert_jpg_to_png("input_styles")

    # Go through all the permutatiosn within these folders
    #style_permutations("input_images", "input_styles", "output_folder")

    model_path = "/home/kmurakami/tshirt/tshirt-airflow/lib/background_removal/mobile_net_model/frozen_inference_graph.pb"
    file_generate_tshirt_permutations("input_images", "input_styles", model_path, "permutations", "8naldv9l-3gyz-cl2g:yv7r-pwgnxg8e5bjr")


    # Create and get a mask
    # model_path = "/home/kmurakami/tshirt/tshirt-airflow/lib/background_removal/mobile_net_model/frozen_inference_graph.pb"
    # img = apply_mask("input_images/photo_girl.png", "input_styles/graffiti.png", model_path)
    # cv2.imwrite("test.png", img)

    # gcp_client = GCPBucket()
    # printful_client = PrintfulPy(
    #     api_key="8naldv9l-3gyz-cl2g:yv7r-pwgnxg8e5bjr")

    # bucket_name = "tshirt_pictures"

    # status = gcp_client.bucket_exists(bucket_name)
    # if status is False:
    #     gcp_client.create_bucket(bucket_name)

    # gcp_client.upload_file(bucket_name, "input/{0}".format("test.png"), "test.png")
    # google_download_link = "https://storage.googleapis.com/tshirt_pictures/input/{0}".format("test.png")
    # raw_json = printful_client.create_mockup_gen_task(variant_ids=[4012, 4172, 4142, 4112], image_url=google_download_link)

    # task_key = raw_json['result']['task_key']

    # status_print = False

    # while(status_print==False):
    #     time.sleep(10)
    #     result = printful_client.get_mockup_gen_task_result(task_key)
    #     if result['result']['status'] == "completed":
    #         status_print = True
    #         print("Completed Mockup")


    # download_printful_designs(result, "test_folder_2")    

    # data = load_json("mock_up_get_result.json")
    # download_printful_designs(data, "test_folder")

    #http(s)://storage.googleapis.com/[bucket]/[object]

    # google_download_link = "https://storage.googleapis.com/tshirt_pictures/input/tiffany_test.png"
    # raw_json = printful_client.create_mockup_gen_task(variant_ids=[4012, 4013], image_url=google_download_link)
    # with open("mock_up_json.json", "w") as data_file:
    #    json.dump(raw_json, data_file, indent=4, sort_keys=True)
    # print(raw_json)


    
    # https://storage.cloud.google.com/tshirt_pictures/input/output.png
    # raw_json = printful_client.create_mockup_gen_task(variant_ids=[4012, 4013], image_url="https://00e9e64bac9dbd245f6147731ff46d838650047fa0f15e3881-apidata.googleusercontent.com/download/storage/v1/b/tshirt_pictures/o/input%2Fupload_text.png?qk=AD5uMEs6gztqmNZdnKkn3xdv6qNJidvGs--XH0yxEJP7t7hlVgclwNTRPg5SM6d-LahbZucalZCjVRWqihB1vqEUxFF7VwYEvBXwx7lH7G936ziaNpvF0r8xAFWs4G9qXq19bWWXKcEHUd1AIoaLCiTNnPdJBkbPWYXAjL7mzPSKnYeSDbKx2rj73BMg1J8IYo1KtcGtvgBaTodwisbcWZ9_qv3ix4rvkEjAnxp7yy79tn7PKZbRdhRtcGJZDByLD0W5phZdMI8AP72WHsEA2PN9LjODHrNmOYbtIhc2_MPcxDmV923ZUeu-y-8fQJnwqe8EcEaL0RwHCPPSbLEiMCgHgiT_iD8K2D-v_h85g1fqg7N3FXMHJkj43vgv6pLD7e3rKsQVXsX6udEu9vozLdSfI1T_tOR6pwggD6Wm-nCkE7pI5mvXuyVasN6kEnlGI_uZeQdhnejKhJ_rJDgAZVuQgoj635RLUQNJknJsDhI-JJEpK0Tk4vhYe-2xMSUHb_4ogHnFTZruSlXD6kcnM_BDb5cG-qfZTWKaDeH3_kQsPiv0EQYsWf6cIbXLlAxO_UEawFKyzyjscpSiJ1k0yPIf6nVIuJevxozSkvYFzlUhNpFpmN5_1CzVxc1pfMG8TkvFRuKVSslX-9Nhq60BWu3DbDexxX2NZ3dlCqihwRNPsuz2eOPbJ868s0tqJuvGyBUHS3LP7hj5eTx7wNrqfiQsPCbRKyD-48M_HFxmPy9tKEdnlLhVnEfoVsIkwiFYb4wHkunQJ8lVfCVnFsqWFJyAPooGC3-9N8H_YixJVrExFxsvIv_4uIE")
    # print(raw_json)
    # with open("mock_up_json.json", "w") as data_file:
    #    json.dump(raw_json, data_file, indent=4, sort_keys=True)
    # raw_json = printful_client.get_mockup_gen_task_result("z9c4300ab4af3819370472523b9309fd")
    # with open("mock_up_get_result.json", "w") as data_file:
    #    json.dump(raw_json, data_file, indent=4, sort_keys=True)
