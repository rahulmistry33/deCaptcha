from django import forms 
from .models import CaptchaImage, CAPTCHA_CHOICES, CrackCaptcha
  
class CaptchaUploadForm(forms.ModelForm): 
    class Meta: 
        model = CaptchaImage
        fields = ['captcha_img','captcha_type']
        widgets = {
               'captcha_type': forms.RadioSelect(attrs={'class': "custom-radio-list"})
           } 

class CrackCaptchaForm(forms.ModelForm): 
    class Meta: 
        model = CrackCaptcha
        fields = ['img_url','captcha_type']