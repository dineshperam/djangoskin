from django.shortcuts import render,redirect
from django.contrib import messages
import time
import pandas as pd
from userapp.models import *
from adminapp.models import *
from mainapp.models import *
import pytz
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from userapp.views import *
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
import matplotlib
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.paginator import Paginator
import numpy as np
import os
import matplotlib.pyplot as plt
import io
import base64

# Create your views here.
def user_dashboard(req):
    prediction_count = UserModel.objects.all().count()
    print(prediction_count)
    user_id = req.session["user_id"]
    user = UserModel.objects.get(user_id = user_id)
    Feedbacks_users_count= Feedback.objects.all().count()
    all_users_count =  UserModel.objects.all().count()
    if user.Last_Login_Time is None:
        IST = pytz.timezone('Asia/Kolkata')
        current_time_ist = datetime.now(IST).time()
        user.Last_Login_Time = current_time_ist
        user.save()
        return redirect('user_dashboard')
    return render(req,'user/user-dashboard.html', {'predictions' : prediction_count, 'la' : user,'a':Feedbacks_users_count,'a':all_users_count})



def user_profile(req):
    user_id = req.session["user_id"]
    user = UserModel.objects.get(user_id = user_id)
    if req.method == 'POST':
        user_name = req.POST.get('username')
        user_age = req.POST.get('age')
        user_phone = req.POST.get('mobile number')
        user_email = req.POST.get('email')
        user_password = req.POST.get('Password')
        user_address = req.POST.get("address")
        
        #user_img = req.POST.get("userimg")

        user.user_name = user_name
        user.user_age = user_age
        user.user_address = user_address
        user.user_contact = user_phone
        user.user_email=user_email
        user.user_password=user_password
       
       

        if len(req.FILES) != 0:
            image = req.FILES['profilepic']
            user.user_image = image
            user.user_name = user_name
            user.user_age = user_age
            user.user_contact = user_phone
            user.user_email=user_email
            user.user_address = user_address
            user.user_password = user_password
            user.save()
            messages.success(req, 'Updated SUccessfully...!')
        else:
            user.user_name = user_name
            user.user_age = user_age
            user.save()
            messages.success(req, 'Updated SUccessfully...!')
            
    context = {"i":user}
    return render(req,'user/user-profile.html',context)


from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
import numpy as np
from tensorflow.keras.models import load_model
from .models import Skin_cancer_dataset

def predict_image_class(image_path):
    # Load the pre-trained EfficientNetB0 model
    model = load_model('effifix.hdf5')

    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make prediction
    predictions = model.predict(img_array)
    return np.argmax(predictions)

def Classification(req):
    if req.method == 'POST' and req.FILES['image']:
        uploaded_file = req.FILES['image']
        model_type = req.POST.get('model_type')
        
        # Save the uploaded image using default storage
        image_name = default_storage.save(uploaded_file.name, uploaded_file)
        image_path = default_storage.url(image_name)

        # Perform classification
        predicted_label = predict_image_class(default_storage.path(image_name))

        # Map predicted label to disease type
        disease_types = {
            0: 'Actinic keratoses',
            1: 'Basal cell carcinoma',
            2: 'Benign keratosis',
            3: 'Dermatofibroma',
            4: 'Melanoma',
            5: 'Melanocytic nevi',
            6: 'Vascular lesions'
        }
        predicted_disease = disease_types.get(predicted_label, 'Unknown')
        print(predicted_disease)
        if model_type == 'CNN':
            model_info = All_model.objects.get(model_Name='CNN')
        elif model_type == 'Efficientnet':
            model_info = All_model.objects.get(model_Name='Efficientnet')
        elif model_type == 'Inception':
            model_info = All_model.objects.get(model_Name='Inception')
        else:
            # Handle invalid model type
            model_info = None
        print(model_info,"asdsasadasdassdsasd")
        # Save the image path, predicted disease, and accuracy to the session
        req.session['image_path'] = image_path
        req.session['predicted_disease'] = predicted_disease
        if model_info:
            req.session['model_name'] = model_info.model_Name
            req.session['model_accuracy'] = model_info.model_accuracy

        # Redirect to Classification_result view
        return redirect('Classification_result')
    else:
        # Render the Classification template
        return render(req, 'user/classification.html')


from django.http import HttpResponse

def Classification_result(req):
    # Retrieve image path, predicted disease, and accuracy from session
    image_path = req.session.get('image_path', None)
    predicted_disease = req.session.get('predicted_disease', 'Unknown')
    model_accuracy = req.session.get('model_accuracy', None)
    model_name=req.session.get('model_name',None)

    # Check if image_path is available
    if image_path:
        # Pass the image path, predicted disease, and accuracy to the template
        return render(req, 'user/classification-result.html', {'image_path': image_path, 'predicted_disease': predicted_disease, 'model_accuracy': model_accuracy, 'model_name': model_name})
    else:
        # Handle the case where image_path is not available
        return HttpResponse("Error: Image not found")


def user_feedback(req):   
    id=req.session["user_id"]
    uusser=UserModel.objects.get(user_id=id)
    if req.method == "POST":
        rating=req.POST.get("rating")
        review=req.POST.get("review")
        # print(sentiment)        
        # print(rating)
        sid=SentimentIntensityAnalyzer()
        score=sid.polarity_scores(review)
        sentiment=None
        if score['compound']>0 and score['compound']<=0.5:
            sentiment='positive'
        elif score['compound']>=0.5:
            sentiment='very positive'
        elif score['compound']<-0.5:
            sentiment='negative'
        elif score['compound']<0 and score['compound']>=-0.5:
            sentiment=' very negative'
        else :
            sentiment='neutral'
        Feedback.objects.create(Rating=rating,Review=review,Sentiment=sentiment,Reviewer=uusser)
        messages.success(req,'Feedback recorded')
        return redirect('user_feedback')
    return render(req,'user/user-feedback.html')


def user_logout(req):
    view_id = req.session["user_id"]
    user = UserModel.objects.get(user_id = view_id) 
    t = time.localtime()
    user.Last_Login_Time = t
    current_time = time.strftime('%H:%M:%S', t)
    user.Last_Login_Time = current_time
    current_date = time.strftime('%Y-%m-%d')
    user.Last_Login_Date = current_date
    user.save()
    messages.info(req, 'You are logged out..')
    return redirect('user_login')

#--------------------------------------------------------------------------
import tkinter as tk

def update_label(label, text):
    label.config(text=text)

def main():
    root = tk.Tk()
    label = tk.Label(root, text="Initial Text")
    label.pack()

    def update_text():
        # This function is called from the main thread
        update_label(label, "Updated Text")

    # Schedule the update_text function to be called from the main thread
    root.after(1000, update_text)

    root.mainloop()

if __name__ == "__main__":
    main()

#----------------------------------------------------------------



