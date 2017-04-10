# DGA Challenge
## Ins'hack 2017

#### Analysing the pcap

##### First downloaded file

The fist downloaded file is pure text and seems to be the XMPP specification, direclty requested from a common website. Refering to the challenge title, it may be related to a technique used by botnet to communicate with their C&C server, download a file and send request to randomly generated domain name, created via the words included in the text.

##### Site web request
The second part of the pcap is an HTTP PUT request to http://dga.insecurity-insa.fr. It seems to be redirected due to HTTPS  configuration. When making a PUT request to https://dga.insecurity-insa.fr here is the result :
`Meeting Date : Wed, 08 Nov 2017 12:00:00 CET
hashResult=int(hashlib.sha1(str(currentTime)).hexdigest(), 16) % (10 ** 9)
posWord1=hashResult//(10**6)
posWord2=(hashResult % (10**6))//(10**3)
posWord3=hashResult % (10**3)
resultDomain = 'http://'+result[posWord1%300].lower()+....`

##### Iterative pattern
You can notice that the end of the pcap is a repetitive pattern, with a GET request to this address `http://www.convert-unix-time.com/api?timestamp=now&timezone=paris` followed by try to GET to a non-existent website. Once again it seems to concord with a botnet behavior.
Here is the pattern analysis :
* ###### http://www.convert-unix-time.com/api?timestamp=now&timezone=paris
  There is first a GET request to this URL, it seems that give the timestamp of the moment of the request, which is confirmed by the response, in JSON containing the following property : `"timestamp":1488020928`
* ###### Non-existent site request
  The previous request is always followed by a request to a non-existent domain name. However this domain name does not seems to weird, it's composed of common words and figures. The domain name always end in `.fr`, for example : `building7standards.fr` or `networkprotocolp.fr`

#### Analysing the website
The pcap access to `https://dga.insecurity-insa.fr` with a PUT request, but obviously there is a different result with a GET request. After a curl request it appears that the website may be accessible through a classic browser too.
Indeed, it is a simple website with a title and a text input.
The text input is actually expecting an input and return a link to a screen of this url. This link indicates that the picture is stored on the server, with a unique id name : `https://dga.insecurity-insa.fr/cbd5f084-8313-4bdf-b5f8-4866e53dd33b.png`.
Trying to pass invalid url to the php script does not seem to be working : ` curl --data "name=<script>alert('aa')</script>"  https://dga.insecurity-insa.fr/screen
Nice try`
And with a domain  name found in the pcap you get a nice blue screen picture.
Trying to access to the php page does not bring any result.
Because of the nature of the pcap request (PUT) it seems interesting to see if there is other supported requests, trying with OPTION return an error page, but with DELETE there is an interesting result : `DGA uses sha1 function and I prefer 9 figures in a row`

#### Exploit
First we have to extract all words from the XMPP specification document.
With the DELETE indication, we convert the timestamp to sha1 to see the result. When printing the result of the hash, it appears that hexa won't help us to find words, we cast it in int : 1487766749 -> 4e60b48400aead5d692a5bbd9ec2b58f3bcdf7dc -> 447457876792965549031058960611595930904445188060
It seems we have to keep 9 figures of the result. The positions of the words composing the domain name are 145 188 and 35.
After investigating it seems that it corresponds to the 9 last figures modulo 300.

We then get the timestamp of the time given in the PUT request : 1510138800.
Here is the final Exploit :
```python
import requests
import re
import hashlib

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
r=requests.get('https://www.ietf.org/rfc/rfc3920.txt',headers)
text=r.text
result= re.compile('\w+').findall(text)
currentTime = 1510138800
hashResult=int(hashlib.sha1(str(currentTime)).hexdigest(), 16)% (10 ** 9)
posWord1=hashResult//(10**6)
posWord2=(hashResult % (10**6))//(10**3)
posWord3=hashResult % (10**3)
resultDomain = 'http://'+result[posWord1%300].lower()+result[posWord2%300].lower()+result[posWord3%300].lower()+'.fr'
print resultDomain
```
Result : `http://protocolunlimited14.fr`
And finally : `curl --data "name=http://protocolunlimited14.fr" https://dga.insecurity-insa.fr/screen `
