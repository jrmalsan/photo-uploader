import os
import time

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
app = Flask(__name__)

from azure.storage.blob import BlockBlobService
block_blob_service = BlockBlobService(os.getenv("AZURE_BLOB_ACCOUNT_NAME"), os.getenv("AZURE_BLOB_ACCOUNT_KEY"))
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

have_camera = False
try:
    from picamera import PiCamera
    camera = PiCamera()
    have_camera = True

@app.route('/', methods = ['GET'])
def welcome_page():
    return "Post to this endpoint to take a picture and upload it"

@app.route('/', methods = ['POST'])
def hello_world():
    if have_camera:
        cur_time = str(int(time.time()))
        print(cur_time)
        file_name = 'pi-capture-{}.png'.format(cur_time)
        full_path = './pictures/{}'.format(file_name)
        print("Taking the picture")
        camera.capture(full_path)
        print("Uploading the photo")
        block_blob_service.create_blob_from_path(container_name, file_name, full_path)
        print("posted the picture")
        
    else:
        file_path = "./pictures/example.png"
        print("about to post the picture")
        block_blob_service.create_blob_from_path(container_name, "imagepng_0.png", file_path)
        print("posted the picture")

    return "Posted the image"