from django.shortcuts import render
from .forms import CaptchaUploadForm
import sys,os
from .Math_CNN_RNN_Model import predict_math_cnn_rnn



def index(request):
    return render(request,'crackCaptcha/index.html')


def crack(request):
    
    if request.method == 'POST': 
        form = CaptchaUploadForm(request.POST, request.FILES) 

        if form.is_valid(): 
            form.save() 
            img_url = form.cleaned_data['captcha_img']
            captcha_type = form.cleaned_data['captcha_type']
            return render(request,'crackCaptcha/crack.html', {'img_url':img_url, 'captcha_type':captcha_type }) 
    else: 
        form = CaptchaUploadForm() 
    return render(request,'crackCaptcha/crack.html', {'form' : form}) 

def crackImage(request):
    if request.method == 'POST': 
        img_url = request['imgUrl']
        captcha_type = request['captchaType']
        text,time = crack_from_image_list([img_url],[captcha_type])
    return render(request,'crackCaptcha/crack.html', {'captcha_text':text[0],'img_url':img_url, 'captcha_type':captcha_type }) 

def crack_from_image_list(url_list,type):
    pred_texts=[]
    for i,url in url_list:

        if type[i] == 'Sina':
            return [''],0
        elif type[i] == 'Mathematical':
            pred_texts.append(predict_math_cnn_rnn(url))
        elif type[i] == 'WaterRipple':
            return [''],0
    return pred_texts,0