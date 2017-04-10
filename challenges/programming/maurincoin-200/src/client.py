import requests
import random
import sys

def solve(items,scoreMin,size):
    bestScore=-1
    while True:
        selected=[]
        score=0
        occupiedSize=0
        for i in range(len(items)):
            if random.getrandbits(1):
                selected.append(i)
        for item in selected:
            score+=items[item][0]
            occupiedSize+=items[item][1]
        
        if occupiedSize<=size and score>bestScore:
            bestScore=score
            print '%s/%s' % (score,scoreMin)
            if score>=scoreMin:
                return selected

def work(host):
    req=requests.get('https://'+host+'/task').json()
    selected=solve(req['items'],req['scoreMin'],req['size'])
    req['selected']=selected
    coin=requests.post('https://'+host+'/coin',json=req).json()
    if coin['status']!='success':
        print 'Something wrong happened'
        sys.exit(1)
    return coin['boulicoin']

if __name__=='__main__':
    if len(sys.argv)!=2:
        print 'Usage: python2 client.py host'
        sys.exit(1)
    wallet=[]
    coin=work(sys.argv[1])
    wallet.append(coin)
    print 'New coin added : '+coin
