import base64
import requests
import urllib.request
import os 
from snapshot import counter
import json
import base64
from roboflow import Roboflow



# check if the 'prediction' folder is already created in 'inference iot' folder otherwise you're fucked up
# change the 'prediction folder'path related to its path in your PC
# Set the path to the prediction folder
# image_folder = 'C:/Users/39379/Desktop/iot_project/inference iot/image'
#prediction_folder = 'C:/Users/39379/Desktop/iot_project/inference iot/prediction'

image_folder = os.path.join(os.getcwd(), 'image')
prediction_folder = os.path.join(os.getcwd(), 'prediction')

if not os.path.exists(prediction_folder):
    print('funziona')
    os.makedirs(prediction_folder)
# Read the image from the file in the image folder
image_filename = 'image{}.jpg'.format(counter)
image_filepath = os.path.join(image_folder, image_filename)
with open(image_filepath, 'rb') as f:
    image_data = f.read()

# # URL dell'immagine da importare
# image_url = "https://best5.it/b5/wp-content/uploads/2019/07/ape-2-800x400.jpg"

# # Scarica l'immagine
# with urllib.request.urlopen(image_url) as url:
#     image_data = url.read()

# # Salva l'immagine in un file
# with open("image.jpg", "wb") as f:
#     f.write(image_data)


#inferenza su image0 per ottenere predict0
#!pip install Roboflow
def prediction():
    global counter
    print(counter)
    filename = os.path.join(image_folder, 'image{}.jpg'.format(counter))
    print(filename)
        
    rf = Roboflow(api_key="YswyoRwpN8l4oas9n0qJ")
    project = rf.workspace("iotinsectdetectionproject").project("insects-detection-hndll")
    model = project.version(6).model

    # infer on a local image
    print(model.predict(filename, confidence=40, overlap=30).json())

    # visualize your prediction
    # generate unique filename using the counter
    prediction_filename = os.path.join(prediction_folder, 'prediction{}.jpg'.format(counter))
    model.predict(filename, confidence=40, overlap=30).save(prediction_filename)
    # generate prediction's json for db, broh
    # Convert the predicted image to binary data
    # Create a path to the 'json' folder if it doesn't already exist
    dictionary_folder = os.path.join(os.getcwd(), 'dictionary')
    if not os.path.exists(dictionary_folder):
        os.makedirs(dictionary_folder)

    with open(prediction_filename, 'rb') as f:
        binary_data = base64.b64encode(f.read())

    # Save the binary data as a dictionary in a JSON file with a unique name based on the counter value
    binary_data_filename = os.path.join(dictionary_folder, 'prediction_binary_data{}.json'.format(counter))    
    binary_data_dict = {"binary_image": binary_data.decode()}
    #add nel dizionario le seguenti voci
    # "datetime": "2023-02-02T21:41:38.739Z",
    # "contents": "string",
    # "species": "string",
    # "binaryimage": "string",
    # "micro_id": 0
    
    
    
    # with open(binary_data_filename, "w") as f:
    #     f.write(json.dumps(binary_data_dict))

    counter += 1  # increment the counter
    print(counter)

# if __name__ == '__main__':
#     try:
#         prediction()
#     except Exception as e:
#         print('You cannot make a prediction!', e)