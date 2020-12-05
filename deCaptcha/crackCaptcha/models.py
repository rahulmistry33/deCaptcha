from django.db import models

CAPTCHA_CHOICES = (
   ('WaterRipple', 'WaterRipple Captcha'),
   ('Sina', 'Sina Captcha'),
   ('Mathematical', 'Mathematical Captcha')
)

class CaptchaImage(models.Model): 
    captcha_img = models.ImageField(upload_to='images/') 
    captcha_type = models.CharField(max_length=20,choices=CAPTCHA_CHOICES, default=CAPTCHA_CHOICES[0])

class CrackCaptcha(models.Model): 
    img_url = models.CharField(max_length=20, default=None) 
    captcha_type = models.CharField(max_length=20,choices=CAPTCHA_CHOICES, default=CAPTCHA_CHOICES[0])
