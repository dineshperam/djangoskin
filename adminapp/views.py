from django.shortcuts import render,redirect
from mainapp.models import*
from userapp.models import*
from adminapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
import pandas as pd
import numpy as np
import numpy as np


# Create your views here.

def admin_dashboard(req):
    all_users_count =  UserModel.objects.all().count()
    pending_users_count = UserModel.objects.filter(User_Status = 'pending').count()
    rejected_users_count = UserModel.objects.filter(User_Status = 'removed').count()
    accepted_users_count = UserModel.objects.filter(User_Status = 'accepted').count()
    Feedbacks_users_count= Feedback.objects.all().count()
    prediction_count = UserModel.objects.all().count()
    return render(req,'admin/admin-dashboard.html',{'a' : all_users_count, 'b' : pending_users_count, 'c' : rejected_users_count, 'd' : accepted_users_count,'e':Feedbacks_users_count,'f' : prediction_count,})


def adminlogout(req):
    return redirect('main/admin-login.html')


def pending_users(req):
    pending = UserModel.objects.filter(User_Status='pending')
    paginator = Paginator(pending, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,'admin/pending-users.html', { 'user' : post})


def all_users(req):
    all_users = UserModel.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,'admin/all-users.html', {"allu" : all_users, 'user' : post})

def delete_user(req, id):
    UserModel.objects.get(user_id = id).delete()
    messages.warning(req, 'User was Deleted..!')
    return redirect('all_users')

# Acept users button
def accept_user(req, id):
    status_update = UserModel.objects.get(user_id = id)
    status_update.User_Status = 'accepted'
    status_update.save()
    messages.success(req, 'User was accepted..!')
    return redirect('pending_users')

# Remove user button
def reject_user(req, id):
    status_update2 = UserModel.objects.get(user_id = id)
    status_update2.User_Status = 'removed'
    status_update2.save()
    messages.warning(req, 'User was Rejected..!')
    return redirect('pending_users')

def adminlogout(req):
    messages.info(req, 'You are logged out successfully.')
    return redirect('admin_login')



def admin_feedback(req):
    feed =Feedback.objects.all()
    return render(req,'admin/admin-feedback.html',{'back':feed})

def sentiment_analysis(req):
    fee = Feedback.objects.all()
    return render(req,'admin/sentiment-analysis.html', {'cat':fee})

def sentiment_analysis_graph(req):
    positive = Feedback.objects.filter(Sentiment = 'positive').count()
    very_positive = Feedback.objects.filter(Sentiment = 'very positive').count()
    negative = Feedback.objects.filter(Sentiment = 'negative').count()
    very_negative = Feedback.objects.filter(Sentiment = 'very negative').count()
    neutral = Feedback.objects.filter(Sentiment = 'neutral').count()
    context ={
        'vp': very_positive, 'p':positive, 'neg':negative, 'vn':very_negative, 'ne':neutral
    }
    return render(req,'admin/sentiment-analysis-graph.html',context)
    
    

def comparision_graph(req):
    cnn = Cnn_model.objects.last()
    result=cnn.model_accuracy
    efficientnet = Efficientnet_model.objects.last()
    result2=efficientnet.model_accuracy
    inception= Inception_model.objects.last()
    result3=inception.model_accuracy
    
    context ={
        'cnn': result, 'efficientnet':result2, 'inception':result3,
    }
    return render(req,'admin/comparision-graph.html',context)


def efficient(req):
    return render(req,'admin/efficientnet.html')

from .models import Efficientnet_model

def efficient_btn(req):
    result=Efficientnet_model.objects.last()
    messages.success(req, 'Efficientnet Model executed successfully')
    return render(req, 'admin/efficientnet-btn.html', {'result': result})


def cnn(req):
    return render(req,'admin/cnn.html')

def cnn_btn(req):
    result=Cnn_model.objects.last()
    messages.success(req, ' CNN Model executed successfully')   
    return render(req,'admin/cnn-btn.html', {'result': result})

def Train_Test_Split(req):   
    return render(req,'admin/Train-Test-Split.html')

def Train_Test_Split_Result(req):
    result = Train_test_split_model.objects.last()
    return render(req, 'admin/Train Test Split-result.html',{'result':result})


def inception(req):
    return render(req,'admin/inception.html')

def inception_btn(req):
    result=Inception_model.objects.last()
    messages.success(req, ' Inception Model executed successfully') 
    return render(req,'admin/inception-btn.html', {'result': result})




