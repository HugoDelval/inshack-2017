#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from Crypto.Cipher import AES
import base64
import boulicoin
import json
import random

app = Flask(__name__)

def pad(data):
    length = 16 - (len(data) % 16)
    data += chr(length)*length
    return data

def unpad(data):
    assert data[-ord(data[-1]):]==ord(data[-1])*data[-1]
    return data[:-ord(data[-1])]

def encrypt(data):
    aes=AES.new(boulicoin.SECRET_KEY, AES.MODE_CBC, boulicoin.AES_IV)
    return base64.b64encode(aes.encrypt(pad(data)))

def decrypt(data):
    aes=AES.new(boulicoin.SECRET_KEY, AES.MODE_CBC, boulicoin.AES_IV)
    return unpad(aes.decrypt(base64.b64decode(data)))
    
@app.route('/task')
def getTask():
    items,size,scoreMin = boulicoin.generateTask()
    token=str(random.getrandbits(64))
    itemsEnc = encrypt(token+'|items:'+str(items))
    sizeEnc = encrypt(token+'|size:'+str(size))
    scoreMinEnc = encrypt(token+'|score:'+str(scoreMin))
    return jsonify({'items':items,
                    'size':size,
                    'scoreMin':scoreMin,
                    'itemsEnc':itemsEnc,
                    'sizeEnc':sizeEnc,
                    'scoreMinEnc':scoreMinEnc})

@app.route('/coin', methods=['POST'])
def getCoin():
    req=request.json
    if ('itemsEnc' not in req) or ('sizeEnc' not in req) or ('scoreMinEnc' not in req) or ('selected' not in req):
        return jsonify({'status':'error','message':'JSON attributes missing'})
    items=[]
    size=-1
    try:
        itemsEnc1,itemsEnc2=decrypt(req['itemsEnc']).split(':')
        sizeEnc1,sizeEnc2=decrypt(req['sizeEnc']).split(':')
        scoreMinEnc1,scoreMin2=decrypt(req['scoreMinEnc']).split(':')
        items=json.loads(itemsEnc2)
        size=int(sizeEnc2)
        scoreMin=int(scoreMin2)
        selected=req['selected']
        print selected
        assert type(selected)==type([])
        assert len(set(selected))==len(selected)
        print itemsEnc1,sizeEnc1,scoreMinEnc1
        if not itemsEnc1.split('|')[0]==sizeEnc1.split('|')[0]==scoreMinEnc1.split('|')[0] or not '|items' in itemsEnc1 or not '|score' in scoreMinEnc1 or not '|size' in sizeEnc1:
            return jsonify({'status':'error','message':'Encrypted data mismatch.'})
    except:
        return jsonify({'status':'error','message':'Failed to decode data.'})

    score=0
    weight=0
    try:
        for it in selected:
            if it<0 or it>=len(items):
                return jsonify({'status':'error','message':'Invalid item index.'})
            score+=items[it][0]
            weight+=items[it][1]
    except:
        return jsonify({'status':'error','message':'Invalid proof of work.'})
    
    if score>=scoreMin and weight<=size:
        coin=boulicoin.generateCoin()
        assert coin.startswith('INSA{')
        return jsonify({'status':'success','boulicoin':coin})
    return jsonify({'status':'error','message':'Invalid proof of work.'})
    
        
    
if __name__ == '__main__':
    app.run("0.0.0.0")
