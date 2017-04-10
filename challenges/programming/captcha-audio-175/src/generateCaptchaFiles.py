import random
import subprocess
import os

if not os.path.exists('captchaFiles'):
    os.makedirs('captchaFiles')
for j in range (2000) :
    initString='sox '
    resultString=''
    for i in range(45):
        letter = random.choice('aeiou')
        resultString+=letter
        initString+="audioFiles/"+letter+str(random.randint(-10,10))+".wav ";

    initString+='captchaFiles/'+resultString+'.wav'
    subprocess.call(initString,shell=True)
