from django.shortcuts import render
from django.core.files.storage import default_storage
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
import random
import string
import PIL
from claptcha import Claptcha
import re
from django.forms import ModelForm
from django import forms
from .models import *
from .claptcha import Claptcha


filenames = []
def index(request):
    return render(request,'crackCaptcha/index.html')
def home(request):
    # check if the request is post 
    if request.method =='POST':  
 
        # Pass the form data to the form class
        details = LoginForm(request.POST)
 
        # In the 'form' class the clean function 
        # is defined, if all the data is correct 
        # as per the clean function, it returns true
        if details.is_valid():  
 
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database   
            post = details.save(commit = False)
 
            # Finally write the changes into database
            post.save()  
 
            # redirect it to some another page indicating data
            # was inserted successfully
            return HttpResponse("data submitted successfully")
             
        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "crackCaptcha/login.html", {'form':details})  
    else:
 
        # If the request is a GET request then,
        # create an empty form object and 
        # render it into the page
        form = LoginForm(None)   
        return render(request, 'crackCaptcha/login.html', {'form':form})

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


def generate(request):
    if request.method == 'GET': 
        return render(request,'generateCaptcha/generate.html') 
    else:
        print(request.POST)
        captchaType = request.POST['captchaType']
        captchaLength = int(request.POST['captchaLength'])
        captchaTextType = request.POST['captchaTextType']
        noiseLevel = float(request.POST['noiseLevel'])
        captchaText = None
        if 'captchaText' in request.POST:
            captchaText = request.POST['captchaText']
        addRandomArc = False
        fontfile = None
        if 'addRandomArc' in request.POST: addRandomArc = True
        if 'fontfile' in request.FILES: fontfile = request.FILES['fontfile']
        color=[0,0,0]
        fontColor=[0,0,255]
        lineColor=[255,255,255]
        if request.POST['bg1'] != '':
            color = [int(request.POST['bg1']),int(request.POST['bg2']),int(request.POST['bg3'])]
        if request.POST['f1'] != '':
            fontColor = [int(request.POST['f1']),int(request.POST['f2']),int(request.POST['f3'])]
        if request.POST['a1'] != '':
            lineColor = [int(request.POST['a1']),int(request.POST['a2']),int(request.POST['a3'])]
        img_url = generateParamterisedCaptcha(captchaType,captchaLength, captchaTextType ,captchaText ,noiseLevel, addRandomArc, fontfile,color,fontColor,lineColor)
        
        return render(request, 'generateCaptcha/generate.html', {'img_url' : img_url})
        

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

def generateParamterisedCaptcha(captchaType, captchaLength, captchaTextType ,captchaText, noiseLevel, addRandomArc=False, fontfile=None,color=[0,0,0],fontColor=[0,0,255],lineColor=[255,255,255]):
    file_name = "C:\\Users\\vinod\\Desktop\\New folder\\deCaptcha\\crackCaptcha\\Arial.ttf"
    if(fontfile != None):
        file_name = default_storage.save(fontfile.name, fontfile)
        file_name = "C:\\Users\\vinod\\Desktop\\New folder\\deCaptcha\\deCaptcha\\media\\" + file_name
        

    if captchaTextType == 'auto':
        if captchaType == 'alphanumeric':
            rndLetters = (random.choice(string.ascii_uppercase) for _ in range(captchaLength))
            captchaText = "".join(rndLetters)
        else:
            
            fno = random.randint(11,100)
            op1 =  '+' if random.randint(1,3) == 1 else '-'
            sno = random.randint(11,100)
            captchaText = str(fno) + op1 + str(sno)

            
            
            


    c = Claptcha(captchaText,file_name, color=color,textColor=fontColor,lineColor = lineColor,resample=PIL.Image.BICUBIC, noise=noiseLevel)
    c.size = (170,90)
    c.margin = (25,25)
    text, _ = c.write("C:\\Users\\vinod\\Desktop\\New folder\\deCaptcha\\deCaptcha\\media\\generated\\captcha.png")
    img_url = '/media/generated/captcha.png'
    return img_url
    

# define the class of a form
class LoginForm(ModelForm):
    class Meta:
        # write the name of models for which the form is made
        model = Login
        # Custom fields
        fields =["mobile", "password"]

    # this function will be used for the validation
    def clean(self):
        # data from the form is fetched using super function
        super(LoginForm, self).clean()
        # extract the mobile and password field from the data
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')

        # conditions to be met for the username length
        if len(mobile) != 10:
            self._errors['mobile'] = self.error_class([
                'Mobile number should be 10 digits'])
        if len(password) != 10:
            pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
            result = re.findall(pattern, password)
            if not(result):
                self._errors['password'] = self.error_class([
                'Password invalid'])
        # return any errors if found
        return self.cleaned_data