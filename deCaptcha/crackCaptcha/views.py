from django.shortcuts import render
from .forms import CaptchaUploadForm
import sys,os,time
from .Math_CNN_RNN_Model import predict_math_cnn_rnn
from .Sina_CNN_Model import predict_sina_cnn
from .WaterRipple_CNN_Model import predict_waterripple_cnn
from .Math_CNN_Wheezy_Model import predict_math_cnn_wheezy
from .Shadow_CNN_RNN_Model import predict_shadow_cnn_rnn
from .FishEye_CNN_RNN_Model import predict_fisheye_cnn_rnn
from .Classification_Model import get_captcha_type
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
            
            captcha_type = request.POST['options']
            return render(request,'crackCaptcha/crack.html', {'img_url':filenames, 'captcha_type':captcha_type }) 
    else: 
        form = CaptchaUploadForm() 
    return render(request,'crackCaptcha/crack.html', {'form' : form}) 

def crackImage(request):
    if request.method == 'POST': 
        captcha_type = request.POST['captchaType']
        
        timeToCrack = time.time()

        #assuming batch-image mode, all images of same type
        texts = None
        type_list = None
        if captcha_type == "Unknown":
            # captcha_type = get_captcha_type(filenames)
            type_list = get_captcha_type(filenames)
            texts = crack_from_image_list(filenames,None,isUnknown=True, type_list= type_list)
            print(texts)
        else:
            texts = crack_from_image_list(filenames,captcha_type,isUnknown=False)
            print(texts)

        # texts = crack_from_image_list(filenames,captcha_type)
        
        timeToCrack = (time.time() - timeToCrack)
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
        elif captcha_type == "Unknown":
            map = zip(range(1,len(filenames)+1),filenames,texts, type_list)
        else:
            map = zip(range(1,len(filenames)+1),filenames,texts)

    return render(request,'crackCaptcha/crack.html', {'map':map,'timeToCrack':timeToCrack,'math':math_bool,'captcha_text':texts,'img_url':filenames, 'captcha_type':captcha_type, 'type_list': type_list }) 

def crack_from_image_list(url_list,type,isUnknown=False,type_list=None):
    pred_texts = None
    if isUnknown:
        pred_texts = [] 
        for i,url in enumerate(url_list):
            type = type_list[i]
            if type == 'Sina':
                pred_texts.append(predict_sina_cnn([url])[0])

            elif type == 'Mathematical':
                pred_texts.append(predict_math_cnn_rnn([url])[0])

            elif type == 'Shadow':
                pred_texts.append(predict_shadow_cnn_rnn([url])[0])

            elif type == 'FishEye':
                pred_texts.append(predict_fisheye_cnn_rnn([url])[0])
                
            elif type == "WheezyMath":
                pred_texts.append(predict_math_cnn_wheezy([url])[0])

            elif type == 'WaterRipple':
                pred_texts.append(predict_waterripple_cnn([url])[0])

    else:

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

    return pred_texts