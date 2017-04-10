import subprocess
import os


def textToWav(letter,value,file_name):
    text="<speak><prosody pitch='" + str(value) + "st'>" + letter +"</prosody><break strength='medium'/></speak>"
    print text
    subprocess.call(["espeak","-m", "-s 80", "-w"+file_name+".wav", text])

if not os.path.exists('audioFiles'):
    os.makedirs('audioFiles')
for i in range(-10,11):
    for letter in 'aeiou':
        textToWav(letter,i,'audioFiles/'+letter+str(i))
