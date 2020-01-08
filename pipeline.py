#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Default Libraries
import json
import os

# Third Party Libraries
from PIL import Image

import cv2
import numpy

# Company Libraries. Can be found in the lib folder
from tshirt_pipeline.gcp_client import GCPBucket
from printfulpy import PrintfulPy
from style_transfer import style_image, load_img
from background_helper import BackgroundRemoval

def convert_jpg_to_png(input_image_folder):

    """Convert all jpg images to png properly. Deletes jpg's after its done

    Args:
        input_image_folder (string): Path to jpgs

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
    
    def tensor_to_image(tensor):

        """Convert a Tensor output to a Image using PIl

        Args:
            tensor (int):

        Return:
            image (PIL Image)

        """

        tensor = tensor*255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
            img = PIL.Image.fromarray(tensor)
        return img

    blah = tensor_to_image(load_img(input_image))
    print(type(blah))
    #cv2.imshow("blah", blah)
    #cv2.waitKey(0)
    model_path = background_nn_model
    extract_client = BackgroundRemoval(model_path)
    cropped_area = extract_client.run_visualization(input_image, "temp_image.png", save_image=False)
    print("here")
    print(type(cropped_area))
    convert = numpy.asarray(cropped_area)
    style_image(input_image, input_style, "temp_output.png")
    style_input = cv2.imread("temp_output.png")
    print(type(style_input))
    print("cropped {0}".format(convert.shape))
    print("style {0}".format(style_input.shape))

    cv2.imshow("window", convert)
    cv2.imshow("style", style_input)
    cv2.waitKey(0)
    # replaced_image = cv2.bitwise_and(style_input, convert)
    # cv2.imwrite("example.png", replaced_image)
    # print("applied mask")
    

if __name__ == "__main__":

    # Convert all jpgs to pngs and delete pngs
    #convert_jpg_to_png("input_images")
    #convert_jpg_to_png("input_styles")

    # Go through all the permutatiosn within these folders
    #style_permutations("input_images", "input_styles", "output_folder")
    model_path = "/home/kmurakami/tshirt/tshirt-airflow/lib/background_removal/mobile_net_model/frozen_inference_graph.pb"
    apply_mask("input_images/photo_girl.png", "input_styles/graffiti.png", model_path)
    #style_image(os.path.join("input_images", "photo_girl.png"), os.path.join("input_styles", "graffiti.png"), "temp_output.png")

    

    #create_text_image("Beautiful", "Lintsec.ttf", "text_creation.png")
    #remove_text_background("text_creation.png", "remove_text.png")
    #print("im done")
    #style_image("input_matrix.jpg", "matrix_style.jpg", "matrix_output.png")
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
