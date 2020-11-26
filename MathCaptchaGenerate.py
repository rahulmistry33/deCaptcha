from claptcha import Claptcha
import random

for i in range(0,50):
    operator = random.randint(1,2)
    operand1 = random.randint(10,99)
    operand2 = random.randint(10,99)
    captcha = ""
    if operator == 1:
        captcha = "{}{}{}".format(operand1,'+',operand2)
    elif operator == 2:
        captcha = "{}{}{}".format(operand1,'-',operand2)
    
    c = Claptcha(captcha, "Arial.ttf", noise = 0.15)
    text, image = c.image
    text, file = c.write('.\\MathCaptchaColored\\{}.png'.format(captcha))