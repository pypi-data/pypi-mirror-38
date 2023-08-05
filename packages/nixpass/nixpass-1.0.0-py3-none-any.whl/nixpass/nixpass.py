#!VE/bin/python3.6
#Your virtual environment here
#######################
# NixPass   -   [@]   #
#  v.1.0     -    \   #
#             -   =\  #
#######################
#  -   gatovato   -   #
#######################

#Crypto library for encryption of password workspace file, for generation of IV and 32 byte key, respectively
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256

#Used for writing AES to file, prevent special characters from being lost
import base64

#Obtain password from user as securely as possible
from getpass import getpass

#Used for storing usernames/passwords in each password workspace file
import json

#Get cwd and use cwd to safely remove files
import os

#Used for generating random password
import random


def encrypt_data(key,msg):
    iv = Random.get_random_bytes(16)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    if len(msg) % 16 != 0:
        msg += '\x00' * (16 - len(msg) % 16)
    tmp = iv + cipher.encrypt(msg.encode('UTF-8'))
    secret = base64.b64encode(tmp)
    return secret

def decrypt_data(key,msg):
    aes_decode = base64.b64decode(msg)
    iv = aes_decode[:AES.block_size]
    decipher = AES.new(key,AES.MODE_CBC,iv)
    plain_text = decipher.decrypt(aes_decode)
    return plain_text

def gen_passwd(passLen):
    caps = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    lower = []
    for i in caps:
    	lower.append(i.lower())
    nums = [1,2,3,4,5,6,7,8,9,0]
    syms = ['[','<','>','@','!','$','%','^','&','(',')','+','-','_','+','?','~']

    tmpList = []
    passList = []

    tmp = 0
    while tmp < passLen:
        tmpList = []
        tmpList.append(random.choice(caps))
        tmpList.append(random.choice(lower))
        tmpList.append(random.choice(nums))
        tmpList.append(random.choice(syms))
        passList.append(random.choice(tmpList))
        tmp += 1

    myPass = ''
    for i in passList:
    	myPass = myPass + str(i)
    return myPass

def notInList(myList,name):
    for i in myList:
        if i == name:
            return False
    return True

def createFile(masterList,stordir):
    running = True
    key = ['0','1']
    tmpDict = {}
    newDict = json.dumps(tmpDict)

    while running == True:
        name = input('File Name: ')
        goodName = notInList(masterList,name)
        while goodName == False:
            print('File Name already exists, please enter variant')
            name = input('File Name: ')
            goodName = notInList(masterList,name)

        hash0 = SHA256.new()
        hash0.update(getpass('Password: ').encode('UTF-8'))
        key[0] = hash0.digest()

        hash1 = SHA256.new()
        hash1.update(getpass('Confirm Password: ').encode('UTF-8'))
        key[1] = hash1.digest()

        while key[0] != key[1]:
            print('Passwords don\'t match, please re-enter')
            key = ['0','1']

            hash0 = SHA256.new()
            hash0.update(getpass('Password: ').encode('UTF-8'))
            key[0] = hash0.digest()

            hash1 = SHA256.new()
            hash1.update(getpass('Confirm Password: ').encode('UTF-8'))
            key[1] = hash1.digest()

        new_file = open(stordir + name,'wb')
        new_file.write(encrypt_data(key[0],newDict))
        new_file.close()
        key = ['0','1']
        running = False
    return name

def listFiles(masterList):
    for i in masterList:
        print(i)

def openFile(name,stordir):
    running = True
    key = [None]
    try:
        myFile = open(stordir + name,'rb')
    except:
        print('File not made yet, use the \'c\' option to make it')
        running = False
    if running == True:
        hash0 = SHA256.new()
        hash0.update(getpass('Password: ').encode('UTF-8'))
        key[0] = hash0.digest()

        encodeTxt = myFile.read()
        myFile.close()

        plain_text = [None]
        msg = [None]
        plain_text[0] = decrypt_data(key[0],encodeTxt)
        try:
            msg[0] = plain_text[0][AES.block_size:].decode('ascii')
            plain_text[0] = None
            msg[0] = msg[0].replace('\x00','')
            myDict = json.loads(msg[0])
            msg[0] = None
        except:
            print('decryption failed')
            running = False

    while running == True:
        start = input('\n'+'Password File Command (h for help): ')

        if start == 'h':
            print('a'+'\t\t'+'add a new entry' + '\n' +
            'l'+'\t\t'+'list entry names'+'\n'+
            'entry name'+'\t' + 'display username and password' + '\n'
            + 'e' +'\t\t'+'edit entry'+'\n'+
            'r'+'\t\t'+'remove entry'+'\n'+
            'm'+'\t\t'+'main menu')

        elif start == 'a':
            entry_name = input('Entry Name: ')
            entry_username = input('Entry Username: ')
            give_or_gen = input('(e)nter password or (g)enerate password? ')
            if give_or_gen == 'e' or give_or_gen == 'E':
                entrypass = [None,None]
                entrypass[0] = getpass('Entry Password: ')
                entrypass[1] = getpass('Confirm Entry Password: ')
                while entrypass[0] != entrypass[1]:
                    entrypass[0] = getpass('Entry Password: ')
                    entrypass[1] = getpass('Confirm Entry Password: ')
                myDict[entry_name] = {}
                myDict[entry_name][entry_username] = entrypass[0]
                entrypass=[None,None]
            elif give_or_gen == 'g' or give_or_gen == 'G':
                passLen = int(input('Password Length? '))
                genPass = gen_passwd(passLen)
                myDict[entry_name] = {}
                myDict[entry_name][entry_username] = genPass

        elif start == 'l':
            for x,y in myDict.items():
                print(x)

        elif start == 'e':
            entry_name = input('Entry name to edit? ')
            task = input('Edit (u)sername or (p)assword? ')
            if task == 'u' or task == 'U':
                username = input('Existing Username? ')
                new_user = input('What should it be changed too? ')
                print('updating username')
                try:
                    myDict[entry_name][new_user] = myDict[entry_name].pop(username)
                    print('updated username to '+new_user)
                except:
                    print('unable to edit username, please confirm spelling')
            if task == 'p' or task == 'P':
                username = input('Which user is it for? ')
                new_pass = getpass('What shoud the new password be? ')
                confirm_pass = getpass('Confirm password: ')
                while new_pass != confirm_pass:
                    print('Passwords don\'t match, please re-enter')
                    new_pass = getpass('What shoud the new password be? ')
                    confirm_pass = getpass('Confirm password: ')
                print('changing password for '+username)
                try:
                    myDict[entry_name][username] = new_pass
                    print('password changed for username ' + username)
                except:
                    print('unable to edit password, please check username\'s spelling')
        elif start == 'r':
            rm = input('Which entry to remove? ')
            confirm_rm = input('Are you sure you want to remove' + rm + '?(y/n) ')
            if confirm_rm == 'y' or confirm_rm == 'Y':
                print('removing ' + rm)
                try:
                    del myDict[rm]
                    print('removed ' + rm +' successfully')
                except:
                    print('unable to remove' + rm + 'please confirm the spelling')
        elif start == 'm':
            new_file = open(stordir + name,'wb')
            new_file.write(encrypt_data(key[0],json.dumps(myDict)))
            new_file.close()
            key = ['0']
            msg = ['0']
            running = False
        else:
            if start in myDict:
                for x,y in myDict.items():
                    if x == start:
                        for a,b in myDict[x].items():
                            print(a,'\n'+b)
            else:
                print('command or entry not found')

def removeFile(masterList,rm,stordir):
    removing = True
    goodName = False
    for i in masterList:
        if i == rm:
            goodName = True

    if goodName == True:
        try:
              myFile = open(stordir + rm,'rb')
        except:
              print('error opening file, verify if it\'s in .nixpass')
              removing = False
        if removing == True:
            key = [None]
            hash0 = SHA256.new()
            hash0.update(getpass('Password: ').encode('UTF-8'))
            key[0] = hash0.digest()

            encodeTxt = myFile.read()
            myFile.close()
            plain_text = [None]
            msg = [None]
            plain_text[0] = decrypt_data(key[0],encodeTxt)
            try:
                #using openFile()'s decrypt code to make sure file can be decrypted, if it can, password must be good, and authorized for removal
                #error will be thrown on the .decode('ascii') if not decrypted text after [AES.block_size:]
                #in the offchance something after [AES.block_size:] doesn't exceed 128 (decode('ascii') error), it will fail for sure on the
                #.replace() method as obj will = byte obj not str
                msg[0] = plain_text[0][AES.block_size:].decode('ascii')
                plain_text[0] = None
                msg[0] = msg[0].replace('\x00','')
                msg[0] = None

                try:
                    masterList.pop(masterList.index(rm))
                    os.remove(stordir + rm)
                except:
                    print('Unable to remove pass file, check file in .nixpass directory')
                tmpStr = ''
                for i in masterList:
                    if i != '':
                        tmpStr = tmpStr + i + ','
                myFile = open(stordir+'master-list','w')
                myFile.write(tmpStr)
                myFile.close()

            except:
                print('Password Failure, unable to remove')
                myFile.close()
    else:
        print('name not found in master-list')

def main():
    running = True

    intro = '''
    #######################
    # NixPass   -   [@]   #
    #  v.1.0     -    \   #
    #             -   =\  #
    #######################'''+'\n'
    print(intro)

    usr = os.environ.get('USER')
    stordir = '/home/'+usr+'/.nixpass/'
    if os.path.isdir(stordir):
        pass
    else:
        os.mkdir('/home/'+usr+'/.nixpass')

    masterList = open(stordir+'master-list','a').close()

    while running == True:

        start = input('\n'+'Command (h for help): ')

        if start == 'h':
            print('C'+'\t\t'+'create a new pass file' + '\n' +
            'l'+'\t\t'+'list pass files'+'\n'+
            'filename'+'\t' + 'enter file name to open pass file' + '\n'
            + 'r' +'\t\t'+'remove pass file'+'\n'+
            'q'+'\t\t'+'quit NixPass'+'\n'+
            'abt'+'\t\t'+'about NixPass')

        elif start == 'c':
            myFile = open(stordir +'master-list','r')
            tmpStr = myFile.read()
            masterList = tmpStr.split(',')
            name = createFile(masterList,stordir)
            myFile.close()

            myFile = open(stordir +'master-list','a')
            myFile.write(name+',')
            myFile.close()

        elif start == 'r':

            rm = input('Which File to remove? ')

            myFile = open(stordir+'master-list','r')
            tmpStr = myFile.read()
            masterList = tmpStr.split(',')
            myFile.close()

            removeFile(masterList,rm,stordir)

        elif start == 'l':
            myFile = open(stordir+'master-list','r')
            tmpStr = myFile.read()
            masterList = tmpStr.split(',')
            myFile.close()
            listFiles(masterList)

        elif start == 'q':
            running = False

        elif start == 'abt':
            about = '''
            NixPass was created to help organize, generate, and store
            passwords. It allows password workspaces to be encrypted
            with AES-256 and decrypted with a single password, giving
            access to all entered credentials within that workspace.
            ''' + '\n'
            print(about)

        else:
            myFile = open(stordir+'master-list','r')
            tmpStr = myFile.read()
            masterList = tmpStr.split(',')
            myFile.close()
            nameFound = False
            for i in masterList:
                if i == start:
                    nameFound = True

            if nameFound == True:
                print('opening '+start)
                openFile(start,stordir)
            else:
                print('File not found, choose \'c\' to create it')
