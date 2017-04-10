import requests
import re
import json
import hashlib
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
r=requests.get('http://www.ietf.org/rfc/rfc3920.txt',headers)
text=r.text
result= re.compile('\w+').findall(text)
result = result [:300]
requests.put('http://dga.insecurity-insa.fr')
for i in range(10):
    rHeure=requests.get('http://www.convert-unix-time.com/api?timestamp=now&timezone=paris')
    parsed_json = json.loads(rHeure.text)
    currentTime = parsed_json['timestamp']
    hashResult=int(hashlib.sha1(str(currentTime)).hexdigest(), 16) % (10 ** 9)
    posWord1=hashResult//(10**6)
    posWord2=(hashResult % (10**6))//(10**3)
    posWord3=hashResult % (10**3)
    resultDomain = 'http://'+result[posWord1%300].lower()+result[posWord2%300].lower()+result[posWord3%300].lower()+'.fr'
    try:
        requests.get(resultDomain)
    except requests.exceptions.RequestException as e:
        pass
    time.sleep(10)
