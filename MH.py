import secrets
import math
import time
import matplotlib.pyplot as plt
import random as rm

def getpriv(numofitems, bits):
    seq=[]
    #random = secrets.randbits(bits)
    random=rm.randint(1,2**bits - 1)
    for i in range(numofitems):
        seq.append(random << 1)
        random = seq[i]
    return seq

def relativeprime(q):
    for i in range(2 , q):
        if (math.gcd(q,i)==1):
            return i
            
def inverse(s,q):
    for i in range(1,q):
        if ((s*i)%q == 1):
            return i

def generatepubkey(r,q,privatesequence):
    pubseq=[]
    for i in range(len(privatesequence)):
        pubseq.append((r*privatesequence[i])%q)
    return pubseq
    
def encryption(msg , pubsequence):
    cipher=0
    for i in range(len(msg)):
        cipher+=msg[i]*pubsequence[i]
    return cipher

def decryption(cipher , s ,q, privatesequence):
    temp = (cipher%q * s%q)%q
    originalmsg = [0] * len(privatesequence)
    for i in range(len(privatesequence)-1 , -1 , -1):
        if privatesequence[i]<=temp :
            originalmsg[i]=1
            temp=temp - privatesequence[i]
            if(temp == 0):
                break
    return originalmsg

def modinverse(A, M):
    m0 = M
    y = 0
    x = 1
 
    if (M == 1):
        return 0
 
    while (A > 1):
        q = A // M
        t = M
        M = A % M
        A = t
        t = y
        y = x - q * y
        x = t
 
    # Make x positive
    if (x < 0):
        x = x + m0
 
    return x

def MH_Knapscak(numofitems, bits):
    tim=[]
    start = time.time()
    privatesequence = getpriv(numofitems , bits)
    q = sum(privatesequence)*2; #Greater than sum of all elements in private sequence
    print("priv seq = ", privatesequence ,"Q value= ",q)
    #choosing random r suchh that gcd(r,q)=1
    r=relativeprime(q)
    print("r value= ",r)
    #Find s which is multiplicative inverse of r mod q
    #s=inverse(r,q)
    #print("s value= ",s)
    pubsequence=generatepubkey(r,q,privatesequence)
    print("Pub sequence = ",pubsequence)
    end = time.time()
    print("The time  for key generation is :",(end-start) * 10**3, "ms")
    tim.append((end-start) * 10**3)
    #Generating a random message m
    msg=[]
    for i in range(numofitems):
        msg.append(secrets.randbits(1))
    print("Message m is ",msg)
    #Encryption
    start = time.time()
    cipher=encryption(msg , pubsequence)
    print("Cipher text= ",cipher)
    end = time.time()
    print("The time for encryption is :",(end-start) * 10**3, "ms")
    tim.append((end-start) * 10**3)
    #Decryption
    start = time.time()
    #Find s which is multiplicative inverse of r mod q
    #s=inverse(r,q)
    #s= math.pow(r, -1, q)
    s=modinverse(r,q)
    print("s value= ",s)
    res=decryption(cipher , s ,q, privatesequence)
    print("Original Message:",res)
    end = time.time()
    print("The time for decryption is :",(end-start) * 10**3, "ms")
    tim.append((end-start) * 10**3)
    return tim

keygentime=[]
encryptiontime=[]
decryptiontime=[]
size=[]
for i in range(1,11):
    numofitems = i
    bits = 5
    tim=MH_Knapscak(numofitems, bits)
    size.append(i)
    keygentime.append(tim[0])
    encryptiontime.append(tim[1])
    decryptiontime.append(tim[2])
print(keygentime)
print(encryptiontime)
print(decryptiontime)
plt.plot(size, keygentime, marker ="o",label="Key generation")
plt.plot(size, encryptiontime,marker ="o",label="Encryption")
plt.plot(size, decryptiontime,marker ="o",label="Decryption")
plt.xlabel("Sequence size")
plt.ylabel("Time(milliseconds)")
plt.title("Knapsack cryptographic system Performance graph")
plt.legend()
plt.show()
