# Fingerprint Challenge
## Ins'hack 2017

**To flag this challenge all you have to do is to follow the hints, then just click on the text in the navbar. **

### Required properties

* **User-agent : **
  User-agent must be set to : "xXxGetSecretInfoxXx"
* **Accept-Language : **
  Must includes 'co' (means corsican), can be achieved by addinf it in the language menu in Chrome/chromium
* **Value of str property and associated properties : **
  The str value should be `175949`. Here the step to follow to have this value sent by the js file.
  * Install Hack-bar extension
  * Block cookies and local storage (Chrome : Settings->privacy->content settings->block sites from setting any data)
  * Activate do not track
  * Connect to github but not to your google account. To connect to github while blocking localStorage and cookies you can add an exception
* **Ip address**
  Your local (private) ip address should contains the number `13`
* **Screen resolution**
  When clicking on the navbar text your screen resolution have to be 8000*4578, you can make it using the emulation tool in chrome.
* **Time offset**
  You should use AEST – Australian Eastern Standard Time in your system.
* **Font**
  You have to install the `Original by fnkfrsh` font.
* **WebRTC devices**
  All your devices should be detected with a descrition containing "false". Use these options in the terminal : `--use-fake-device-for-media-stream --use-fake-ui-for-media-stream`. (*Note : Kill the chrome process to launch a new process with these options*)


### Final exploit

````
import requests
headers = {
    'User-Agent': 'xXxGetSecretInfoxXx',
    "Accept-Language": "co"
}
data = {
    'ip':'192.168.1.13',
    'h':4578,
    'w':8000,
    'str':175949,
    'offset':-600,
    'f[]':['Original by fnkfrsh','random'],
    'd[]':['fake1','Fake2','FAKE 3 ze']
}

r=requests.post('https://fingerprint.insecurity-insa.fr/php/handle.php',data=data,headers=headers)
print r.content
````
