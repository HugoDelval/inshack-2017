import requests,time
from requests.auth import HTTPBasicAuth

url = "http://127.0.0.1:5000/"
creds = HTTPBasicAuth('Coffee_Machine', 'Coffee_Password')

def testRequest(method,route,text,code):
    r = requests.request(method, url+route,auth=creds)
    return r.text.rstrip() == text and r.status_code == code

def testCommand(method,text,code,data):
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    r = s.request(method,url+'coffee',data=data,auth=creds)
    return r.text.rstrip() == text and r.status_code == code

#Test basic to all routes
print testRequest('GET','teapot',"I'm a teapot",418)
print testRequest('GET','coffee',"Not acceptable",406)
print testRequest('POST','coffee',"Wrong Content-type",406)
print testRequest('WHEN','coffee',"Not acceptable",406)
print testRequest('PROPFIND','coffee',"Coffee pouring time: 16 seconds\n\r Milk pouring time: beetwen 4 and 7 seconds.",200)

#Test basic with good protocol
print testCommand('POST',"Not acceptable",406,"")
print testCommand('POST',"Available commands: info, start, stop, milk",200,"info")
print testCommand('POST',"Starting to serve coffee",200,"start")
print testCommand('POST',"Not acceptable",406,"stop")
print testCommand('POST',"Not acceptable",406,"milk")

print testCommand('BREW',"Not acceptable",406,"")
print testCommand('BREW',"Available commands: info, start, stop, milk",200,"info")
print testCommand('BREW',"Starting to serve coffee",200,"start")
print testCommand('BREW',"Not acceptable",406,"stop")
print testCommand('BREW',"Not acceptable",406,"milk")

#Test pouring coffee time too short
def early_coffee():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds)
    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "Your Coffee isn't fully served yet, you can wait a little more!" and r.status_code == 200)

    r = s.request('BREW',url+'coffee',data='stop',auth=creds)
    b = (r.text == "Your coffee was not ready, try again!" and r.status_code == 200)
    return a and b

#Test pouring coffee time too short
def late_coffee():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds)

    time.sleep(18)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "Coffee overflow!" and r.status_code == 200)

    r = s.request('BREW',url+'coffee',data='stop',auth=creds)
    b = (r.text == "Coffee overflow, try again!" and r.status_code == 200)
    return a and b

def good_coffee():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds)

    time.sleep(16)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "Your Coffee is quite full, you can stop pouring it." and r.status_code == 200)
    r = s.request('BREW',url+'coffee',data='stop',auth=creds)
    b = (r.text == "Coffee machine is stopped. You can now pour the milk." and r.status_code == 200)
    r = s.request('BREW',url+'coffee',data='milk',auth=creds)
    c = (r.text == "You didn't set the milk type" and r.status_code==406)
    return a and b and c

def early_milk():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds,headers={"milk-type":"Half-and-half","syrup-type":"Raspberry"})

    time.sleep(17)

    s.request('PROPFIND',url+'coffee',auth=creds)
    s.request('BREW',url+'coffee',data='stop',auth=creds)
    s.request('BREW',url+'coffee',data='milk',auth=creds)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "Not enough milk." and r.status_code == 200)

    r = s.request('WHEN',url+'coffee',auth=creds)
    b = (r.text == "Not enough milk, try again!" and r.status_code == 200)
    return a and b

def late_milk():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds,headers={"milk-type":"Half-and-half","syrup-type":"Raspberry"})

    time.sleep(16)

    s.request('PROPFIND',url+'coffee',auth=creds)
    s.request('BREW',url+'coffee',data='stop',auth=creds)
    s.request('BREW',url+'coffee',data='milk',auth=creds)

    time.sleep(9)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "Milk overflow!" and r.status_code == 200)

    r = s.request('WHEN',url+'coffee',auth=creds)
    b = (r.text == "Milk overflow, try again!" and r.status_code == 200)
    return a and b

def good_milk():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds,headers={"milk-type":"Half-and-half","syrup-type":"Raspberry"})

    time.sleep(16)

    s.request('PROPFIND',url+'coffee',auth=creds)
    s.request('BREW',url+'coffee',data='stop',auth=creds)
    s.request('BREW',url+'coffee',data='milk',auth=creds)

    time.sleep(5)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "There is enough milk, you can stop pouring it." and r.status_code == 200)

    r = s.request('WHEN',url+'coffee',auth=creds)
    b = (r.text == "Milk is served." and r.status_code == 200)

    r = s.request('GET',url+'coffee',auth=creds)
    c = (r.text == 'Here is your coffee: INSA{April_Fool_of_Coffee_Machine}' and r.status_code == 200 )
    return a and b and c

def no_syrup():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds,headers={"milk-type":"Half-and-half"})

    time.sleep(16)

    s.request('PROPFIND',url+'coffee',auth=creds)
    s.request('BREW',url+'coffee',data='stop',auth=creds)
    s.request('BREW',url+'coffee',data='milk',auth=creds)

    time.sleep(5)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "There is enough milk, you can stop pouring it." and r.status_code == 200)

    r = s.request('WHEN',url+'coffee',auth=creds)
    b = (r.text == "Milk is served." and r.status_code == 200)

    r = s.request('GET',url+'coffee',auth=creds)
    c = (r.text == "Your coffee is ready but you didn't put syrup in it." and r.status_code == 200 )
    return a and b and c

def wrong_syrup():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds,headers={"milk-type":"Half-and-half","syrup-type":"Chocolate"})

    time.sleep(16)

    s.request('PROPFIND',url+'coffee',auth=creds)
    s.request('BREW',url+'coffee',data='stop',auth=creds)
    s.request('BREW',url+'coffee',data='milk',auth=creds)

    time.sleep(5)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "There is enough milk, you can stop pouring it." and r.status_code == 200)

    r = s.request('WHEN',url+'coffee',auth=creds)
    b = (r.text == "Milk is served." and r.status_code == 200)

    r = s.request('GET',url+'coffee',auth=creds)
    c = (r.text == "Your coffee is ready but you didn't put the right syrup-type." and r.status_code == 200 )
    return a and b and c

def wrong_milk_type():
    s = requests.Session()
    s.headers.update({'content-type': 'message/coffeepot'})
    s.request('BREW',url+'coffee',data='start',auth=creds,headers={"milk-type":"Whole","syrup-type":"Chocolate"})

    time.sleep(16)

    s.request('PROPFIND',url+'coffee',auth=creds)
    s.request('BREW',url+'coffee',data='stop',auth=creds)
    s.request('BREW',url+'coffee',data='milk',auth=creds)

    time.sleep(5)

    r = s.request('PROPFIND',url+'coffee',auth=creds)
    a = (r.text == "There is enough milk, you can stop pouring it." and r.status_code == 200)

    r = s.request('WHEN',url+'coffee',auth=creds)
    b = (r.text == "Milk is served." and r.status_code == 200)

    r = s.request('GET',url+'coffee',auth=creds)
    c = (r.text == "Your coffee is ready but you didn't put the right milk-type." and r.status_code == 200 )
    return a and b and c

print "Early Coffee:", early_coffee()
print "Late Coffee:", late_coffee()
print "Good Coffee:", good_coffee()
print "Early Milk:", early_milk()
print "Late Milk:", late_milk()
print "Flag:", good_milk()
print "No Syrup:",no_syrup()
print "Wrong Syrup:",wrong_syrup()
print "Wrong Milk:",wrong_milk_type()
