#!/usr/bin/python
import random
import sys
import signal

FLAG='XXX'
signal.alarm(30)

def my_print(to_print):
    sys.stdout.write(to_print)
    sys.stdout.flush()


def handle():
    my_print('Welcome to the Heads or Tails game !\nIf you win at least 90/100 games you\'ll win a gift !\n')
    endConn=False
    while not endConn:
        my_print('1.Play\n2.Hash your input\n3.Help\n4.Exit\n')
        choice = raw_input()
        if choice.isdigit():
            if int(choice)==1:
                endConn=playGame()
            elif int(choice)==2:
                doHash()
            elif int(choice)==3:
                printHelp()
            else:
                endConn=True
        else:
            endConn=True
    my_print('Bye !\n')

def playGame():
    headsTailsList=random.getrandbits(100)
    fails=0
    for playno in range(100):
        my_print('Heads or tails ? Send me the hash of your play !\n')
        playHash=raw_input()
        headsTails=(headsTailsList >> playno) & 1
        expectedPlay = ['heads','tails'][headsTails]
        badPlay=['tails','heads'][headsTails]
        my_print('Now, prove me that you did %s by sending your play\n' % expectedPlay)
        playOrig=raw_input()

        if hashPlay(playOrig)!=playHash:
            fails+=1
            my_print('Hash mismatch. Fail %s/10\n' % fails)
        elif not (expectedPlay in playOrig.lower()) or (badPlay in playOrig.lower()):
            fails+=1
            my_print('Play better next time ! Fail %s/10\n' % fails)
        else:
            my_print('Good job !\n')

        if fails >= 10:
            my_print('You have too many fails. Better luck next time !\n')
            break

    if fails < 10:
        my_print('You\'re good ! Here is your flag : %s' % FLAG)
        return True
    return False

def doHash():
    my_print('Send me what you played, I will give you the hash.\n')
    played=raw_input()
    if not (('heads' in played.lower()) ^ ('tails' in played.lower())):
        my_print('Your play is invalid, but here is your hash :')
    my_print(hashPlay(played)+'\n')

def hashPlay(play):
    play+='A'
    while len(play)%4:
        play+='B'
    state=[2, 2, 0, 0, 2, 1, 0, 2, 0, 1, 0, 1, 1, 1, 1, 2, 1, 0, 0, 2, 1]
    for blockStart in range(0,len(play),4):
        block=play[blockStart:blockStart+4]
        blockSum=ord(block[0])*0x1000000+ord(block[1])*0x10000+ord(block[2])*0x100+ord(block[3])
        blockState=[]
        while blockSum:
            blockState.append(blockSum%3)
            blockSum/=3
        while len(blockState)<21:
            blockState.append(state[(11+5*len(blockState))%21])
        for i in range(21):
            state[i]=[[1,0,0],[1,0,2],[2,2,1]][blockState[i]][state[i]]
        newState=state[14:21]+state[0:7]+state[7:14]
        for i in range(0,21,2):
            state[i]=(state[i]-1)%3
        for i in range(1,21,2):
            state[i]=(state[i]+1)%3
        for i in range(21):
            state[i]=[[1,0,0],[1,0,2],[2,2,1]][newState[i]][state[i]]
        newState=state[3:6]+state[18:21]+state[12:15]+state[6:9]+state[9:12]+state[0:3]+state[15:18]
        for i in range(21):
            state[i]=([[1,0,0],[1,0,2],[2,2,1]][state[i]][newState[i]]+blockState[-i])%3
    return ''.join([['O','0','o'][stateElem] for stateElem in state])
        

def printHelp():
    my_print('This game is a fair & open source heads or tails game where the server cannot cheat you and you cannot cheat the server. You can play at home with a real coin.\nFirst, you toss a coin and hash a phrase containing the result using our hashing function, like "My coin landed on tails !". Your phrase must contain "heads" or "tails".\nAfter sending your hash, the server will ask you to prove that your coin landed on heads/tails.\nYou will have to send the initial phrase that you hashed, proving that your coin indeed landed on the good side.\n')

            
if __name__ == "__main__":
    try:
        if len(sys.argv)>=2:
            FLAG=sys.argv[1]
        handle()
    except:
        my_print("Bye!\n")
        sys.exit(0)
