from django.shortcuts import render
from .forms import CaptchaUploadForm
import sys,os
from .Math_CNN_RNN_Model import predict_math_cnn_rnn
from .Sina_CNN_Model import predict_sina_cnn
from .WaterRipple_CNN_Model import predict_waterripple_cnn
from .Math_CNN_Wheezy_Model import predict_math_cnn_wheezy
from .Shadow_CNN_RNN_Model import predict_shadow_cnn_rnn
from .FishEye_CNN_RNN_Model import predict_fisheye_cnn_rnn
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
        captcha_type = request.POST['captchaType']
        
        #add time param
        texts = crack_from_image_list(filenames,captcha_type)
        
        math_bool = False
        if(captcha_type == "Mathematical" or captcha_type == "WheezyMath"):
            math_bool = True
            solved = []
            for t in texts:
                c=0
                if(t.find('+')!=-1):
                    a,b = t.split('+')
                    c=int(a)+int(b)
                elif(t.find('-')!=-1):
                    a,b = t.split('-')
                    c=int(a)-int(b)
                else:
                    c = "error"
                solved.append(c)
            map = zip(range(1,len(filenames)+1),filenames,texts, solved)

        else:
            map = zip(range(1,len(filenames)+1),filenames,texts)

    return render(request,'crackCaptcha/crack.html', {'map':map,'math':math_bool,'captcha_text':texts,'img_url':filenames, 'captcha_type':captcha_type }) 

def crack_from_image_list(url_list,type):
    pred_texts = None
    if type == 'Sina':
        pred_texts=predict_sina_cnn(url_list)

    elif type == 'Mathematical':
        pred_texts=predict_math_cnn_rnn(url_list)

    elif type == 'Shadow':
        pred_texts=predict_shadow_cnn_rnn(url_list)

    elif type == 'FishEye':
        pred_texts=predict_fisheye_cnn_rnn(url_list)
        
    elif type == "WheezyMath":
        pred_texts = predict_math_cnn_wheezy(url_list)

    elif type == 'WaterRipple':
        pred_texts=predict_waterripple_cnn(url_list)

    return pred_texts#,time