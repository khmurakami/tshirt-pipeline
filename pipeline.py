#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Default Libraries
import json
import os

# Company Libraries. Can be found in the lib folder
from gcp_client import GCPBucket
from printfulpy import PrintfulPy
from style_transfer import style_image

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
