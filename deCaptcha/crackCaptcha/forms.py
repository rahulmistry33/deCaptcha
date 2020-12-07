from django import forms 
from .models import CaptchaImage, CAPTCHA_CHOICES, CrackCaptcha
CAPTCHA_CHOICES = (
   ('WaterRipple', 'WaterRipple Captcha'),
   ('Sina', 'Sina Captcha'),
   ('Mathematical', 'Mathematical Captcha')
)
class CaptchaUploadForm(forms.Form): 
    # class Meta: 
        # model = CaptchaImage
    captcha_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        # fields = ['captcha_img','captcha_type']
    captcha_type = forms.ChoiceField(choices=CAPTCHA_CHOICES, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
        
        # widgets = {
        #        'captcha_type': forms.RadioSelect(attrs={'class': "custom-radio-list"})
        #    } 

class CrackCaptchaForm(forms.ModelForm): 
    class Meta: 
        model = CrackCaptcha
        fields = ['img_url','captcha_type']