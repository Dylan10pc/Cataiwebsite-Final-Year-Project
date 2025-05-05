from django.shortcuts import render
import os
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.conf import settings
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from .forms import catimageformforupload
from django.http import JsonResponse
from .models import catimage
from django.shortcuts import get_object_or_404, redirect
import requests
# Create your views here.

#these are paths to the model and csv file
pathtomodel = os.path.join(settings.BASE_DIR, "catbreedmodel1.keras")
pathtocsv = os.path.join(settings.BASE_DIR, "cat_breeds.csv")

#path to the image directory
imgpath = os.path.join(settings.BASE_DIR, "CatBreedsRefined-7k")
breedsfromimg = set(os.listdir(imgpath))

#load the model 
model = load_model(pathtomodel)
#read breed info from csv file and sets breed name as the index
breedinfos = pd.read_csv(pathtocsv)

#filter the breed info to only include breeds that are in the image directory
filteredinfobreed = breedinfos[breedinfos["name"].isin(breedsfromimg)]
#set the index of the filtered breed info to the breed name
breedinfos = filteredinfobreed.set_index("name")

#create a mapping from model output index to breed name
class_indices = {i: breed for i, breed in enumerate(breedinfos.index)}

#view for the about page
def about(request):
    return render(request, 'about.html')

#a function to predict the breed of a cat from an image
def predictcatbreed(image_path):
    try:
        #load the image and preprocess it
        #resizes image then converts it to an array
        img = load_img(image_path, target_size=(299, 299))
        #convert the image to an array and normalize it to [0, 1]
        imgarray = img_to_array(img) / 255.0
        #expand the dimensions of the image array to match the input shape of the model
        imgarray = np.expand_dims(imgarray, axis=0)


        #make a prediction with the model 
        predictions = model.predict(imgarray)
        #confidence prediction and get the index of the highest confidence
        confidence = np.max(predictions) * 100
        #get the index of the highest confidence prediction
        predictedindex = np.argmax(predictions)
        #get the breed name from the index
        predictedbreedname = class_indices[predictedindex]

        #get the breed details from the csv file
        breed_details = breedinfos.loc[predictedbreedname]
        facts = {
            "Length": breed_details.get("length", "Unknown"),
            "Children Friendly": breed_details.get("children_friendly", "Unknown"),
            "General Health": breed_details.get("general_health", "Unknown"),
        }
        
        #convert the facts to integers if they are integers
        facts = {k: v.item() if hasattr(v, 'item') else v for k, v in facts.items()}
        #return the predicted breed name, confidence and facts
        return predictedbreedname, confidence, facts

    #if there is an error print the error
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Unknown", 0, {}
    
#home view that handles the image and predictions
def home(request):
    #if the request is a post request
    if request.method == "POST":
        #get the image from the form
        form = catimageformforupload(request.POST, request.FILES)
        if form.is_valid():
            #get the image from the form
            imagefromform = form.cleaned_data["image"]

            #check if the image is a png, jpg or jpeg file and if not return an error
            if not imagefromform.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                return JsonResponse({"error": "Only PNG, JPG, or JPEG files are supported."}, status=400)

            #save the image to the uploads directory and get the full path of the image
            dirupload = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(dirupload, exist_ok=True) 
            #save the image to the uploads directory
            pathtoimage = os.path.join(dirupload, imagefromform.name)
            with open(pathtoimage, "wb+") as f:
                for chunk in imagefromform.chunks():
                    f.write(chunk)

            #predict the breed of the cat from the image
            predictedbreed, confidence, facts = predictcatbreed(pathtoimage)
            
            #an cat image obj to save the image and prediction to the database
            try:
                catimage.objects.create(
                #save the image to the database
                image="uploads/" + imagefromform.name,
                predictedbreed1=predictedbreed,
                confidence=confidence,
                facts=facts
            )
            except Exception as e:
             print(f"Database save error: {e}")
             
            #get the url path to the image in the media folder 
            trueurlpath = os.path.join(settings.MEDIA_URL, "uploads", imagefromform.name).replace("\\", "/")
            #get the absolute url path to the image in the media folder
            image_url = request.build_absolute_uri(trueurlpath)

            #this is the prediction of the cat response 
            dataresponse = {
                #predicted breed
                "predicted_breed": predictedbreed,
                #confidence of the prediction
                "confidence": float(confidence),
                #facts about the breed turn and convert the facts to integers and run a for loop to get the facts
                "facts": {k: (int(v) if isinstance(v, (np.integer, np.int64)) else v) for k, v in facts.items()},
                #image url of the image
                "image_url": image_url,
            }
            #return the prediction of the cat response as a json response
            return JsonResponse(dataresponse)
        #if the form is invalid return an error
        return JsonResponse({"error": "Invalid form submission."}, status=400)
    #render the home page with the form
    return render(request, "home.html", {"form": catimageformforupload()})

#view for the history page that shows all the images and predictions
def history(request):
    #get all the images and predictions from the database and order them by the uploaded time
    predall = catimage.objects.order_by("-uploadedwhen") 
    return render(request, "history.html", {"history": predall})

#this view is called when the delete button is clicked in the history page
def delete_image(request, image_id):
    #if the request is a post request delete the image from the database and the media folder
    if request.method == "POST":
        image_entry = get_object_or_404(catimage, id=image_id)
        image_entry.delete()
        return redirect('history')
    return JsonResponse({'error': 'Invalid request'}, status=400)

#view for the facts page that shows all the cat breeds and their facts
def facts(request):
    #fetch cat facts from the API
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {
        "x-api-key": "live_4RfE2YHv4kht1TpFyEdRIfctrNxfRuihWIpHB7PRr8HUHVgKAmApLIeajZgT7jfF"
    }
    #get the cat facts from the API and convert it to a json object
    try:
        response = requests.get(url, headers=headers)
        breedsinfo = response.json()
    except Exception as e:
        print("Error fetching cat facts:", e)
        breedsinfo = []

    return render(request, "facts.html", {"cat_breeds": breedsinfo})

