#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from Crypto.Cipher import AES
import base64
import boulicoin
import json

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
    return base64.b64encode(aes.encrypt(pad(str(data))))

def decrypt(data):
    aes=AES.new(boulicoin.SECRET_KEY, AES.MODE_CBC, boulicoin.AES_IV)
    return unpad(aes.decrypt(base64.b64decode(data)))
    
@app.route('/task')
def getTask():
    items,size,scoreMin = boulicoin.generateTask()
    itemsEnc = encrypt(items)
    sizeEnc = encrypt(size)
    scoreMinEnc = encrypt(scoreMin)
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
        items=json.loads(decrypt(req['itemsEnc']))
        size=int(decrypt(req['sizeEnc']))
        scoreMin=int(decrypt(req['scoreMinEnc']))
        selected=req['selected']
        assert type(selected)==type([])
        assert len(set(selected))==len(selected)
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
