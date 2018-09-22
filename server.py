import os
import time

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask import request
app = Flask(__name__)

from azure.storage.blob import BlockBlobService
block_blob_service = BlockBlobService(os.getenv("AZURE_BLOB_ACCOUNT_NAME"), os.getenv("AZURE_BLOB_ACCOUNT_KEY"))
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

have_camera = False
try:
    from picamera import PiCamera
    print("imported")
    camera = PiCamera()
    print("set camera")
    have_camera = True
except:
    print("No camera module")
    
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
        settings = camera._get_camera_settings()
        print("Uploading the photo")
        block_blob_service.create_blob_from_path(container_name, file_name, full_path)
        print("posted the picture")
        return_string = str(settings)

    else:
        file_path = "./pictures/example.png"
        print("about to post the picture")
        block_blob_service.create_blob_from_path(container_name, "example.png", file_path)
        print("posted the picture")
        return_string = 'Uploaded the example image'

    return return_string

@app.route('/test', methods = ['POST'])
def test_read_json():
    body = request.get_json()
    print(type(body))
    print(body['exp_time'])
    return str(body)