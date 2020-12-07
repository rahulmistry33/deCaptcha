from django.shortcuts import render
from .forms import CaptchaUploadForm
import sys,os
from .Math_CNN_RNN_Model import predict_math_cnn_rnn
from .Sina_CNN_Model import predict_sina_cnn
from .WaterRipple_CNN_Model import predict_waterripple_cnn
from .models import Image

filenames = []
def index(request):
    return render(request,'crackCaptcha/index.html')

def crack(request):
    global filenames
    if request.method == 'POST': 
        form = CaptchaUploadForm(request.POST, request.FILES) 
        filenames = []
        if form.is_valid(): 
            # form.save() 
            # img_url = form.cleaned_data['captcha_img']
            files = request.FILES.getlist('captcha_img')
            for f in files:
                instance = Image(image=f)  # match the model.
                filenames.append(instance.filename())
                instance.save()
            
            captcha_type = form.cleaned_data['captcha_type']
            return render(request,'crackCaptcha/crack.html', {'img_url':filenames, 'captcha_type':captcha_type }) 
    else: 
        form = CaptchaUploadForm() 
    return render(request,'crackCaptcha/crack.html', {'form' : form}) 

def crackImage(request):
    if request.method == 'POST': 
        # img_url = request.POST['imgUrl']
        captcha_type = request.POST['captchaType']
        
        #add time param
        text = crack_from_image_list(filenames,captcha_type)
        map = zip(range(1,len(filenames)+1),filenames,text)
    return render(request,'crackCaptcha/crack.html', {'map':map,'captcha_text':text,'img_url':filenames, 'captcha_type':captcha_type }) 

def crack_from_image_list(url_list,type):
    pred_texts = None
    if type == 'Sina':
        pred_texts=predict_sina_cnn(url_list)

    elif type == 'Mathematical':
        pred_texts=predict_math_cnn_rnn(url_list)
        # if(pred_texts[0].find("[UNK]")!=-1):
        #     print("-try wheezy-")

    elif type == 'WaterRipple':
        pred_texts=predict_waterripple_cnn(url_list)

    return pred_texts#,time