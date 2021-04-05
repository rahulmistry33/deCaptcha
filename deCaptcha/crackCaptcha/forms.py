from django import forms 
from .models import CaptchaImage, CAPTCHA_CHOICES, CrackCaptcha
from django.utils.safestring import mark_safe


class CustomChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return mark_safe("<img src='%s'/>" % obj)

CAPTCHA_CHOICES = (
   ('Unknown', 'Unknown Type/Different Types'),
   ('WaterRipple', 'WaterRipple Captcha'),
   ('Sina', 'Sina Captcha'),
   ('Shadow', 'Shadow Captcha'),
   ('FishEye','FishEye Captcha'),
   ('Mathematical', 'Mathematical Captcha'),
   ('WheezyMath', 'Wheezy-Math Captcha')
)
class CaptchaUploadForm(forms.Form): 
   
    captcha_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # captcha_type = forms.ChoiceField(choices=CAPTCHA_CHOICES, initial="Unknown", widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
       

class CrackCaptchaForm(forms.ModelForm): 
    class Meta: 
        model = CrackCaptcha
        fields = ['img_url','captcha_type']


