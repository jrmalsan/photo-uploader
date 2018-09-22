import os
import time
import src.camera_helper as ch

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask import request
app = Flask(__name__)

from azure.storage.blob import BlockBlobService
block_blob_service = BlockBlobService(os.getenv("AZURE_BLOB_ACCOUNT_NAME"), os.getenv("AZURE_BLOB_ACCOUNT_KEY"))
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

have_camera = False
camera = 0
try:
    from picamera import PiCamera
    print("imported")
    camera = PiCamera()
    print("set camera - taking warmup")
    full_path = './pictures/startup.png'
    print("Taking the picture")
    camera.capture(full_path)
    have_camera = True
except:
    print("No camera module")
    
@app.route('/', methods = ['GET'])
def welcome_page():
    return "Post to this endpoint to take a picture and upload it"

@app.route('/', methods = ['POST'])
def hello_world():
    if have_camera:
        settings = request.get_json()
        ch.set_settings(camera, settings)

        cur_time = str(int(time.time()))
        print(cur_time)
        file_name = 'pi-capture-{}.png'.format(cur_time)
        full_path = './pictures/{}'.format(file_name)
        print("Taking the picture")
        camera.capture(full_path)
        settings = ch.get_settings(camera)

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