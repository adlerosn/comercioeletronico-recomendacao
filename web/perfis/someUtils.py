#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import isfile as isfile
from os.path import isdir as isdir
import sys
from os import popen as system
import os
import json

encodings = [
    'utf-8', #common unicode
    'iso-8859-1','cp1252', #latin-1
    'shift_jis','shift_jisx0213', #japanese
    'utf-16-le','utf-16-be' #last permissive unicode
]

def readAllFile(loc,permissive=False):
    encTry=0
    f=open(loc,'rb')
    a=f.read()
    while(isinstance(a,bytes)):
        try:
            a = a.decode(encodings[encTry])
        except UnicodeError:
            encTry+=1
        except IndexError:
            if not permissive:
                raise IndexError('No encoding found to decode this file')
            else:
                a = a.decode('utf-8','ignore')
    f.close()
    return a

def saveFile(loc,cnt):
    f=open(loc,'wt',encoding='utf-8')
    f.write(cnt)
    f.close()

def appendFile(loc,cnt):
    f=open(loc,'at')
    f.write(cnt)
    f.close()

def readObject(loc):
    a=json.loads(readAllFile(loc))
    return a

def saveObject(loc,obj):
    saveFile(loc,json.dumps(obj))

def listDirectory(where='.'):
    return [f for f in os.listdir(where) if isfile(where+os.sep+f)]

def listSubdirectories(where='.'):
    return [f for f in os.listdir(where) if isdir(where+os.sep+f)]

def fileListExists(lst):
    return [f for f in lst if isfile(f)]

def readList(loc):
    return [a for a in readAllFile(loc).strip('\n').strip(' ').strip('\n').split('\n')]

def saveList(loc,lst):
    s = ''
    for t in lst:
        s+=(t+'\n')
    saveFile(loc,s)
    return s

def openObjectList(loc):
    t = readAllFile(loc)
    l=[]
    for ln in t.split('\n'):
        l.append(json.loads(ln))
    return l

def saveObjectList(loc, lst:list):
    t = '\n'.join([json.dumps(e) for e in lst])
    saveFile(loc,t)
    return t

def appendObjectList(loc,item):
    if not isfile(loc):
        return saveObjectList(loc,[item])
    else:
        return appendFile(loc,'\n'+json.dumps(item))

def delFile(loc):
    if isfile(loc):
        os.remove(loc)

def run(cmd):
    return system('bash -c "'+cmd+'"').read()

def quietRun(cmd):
    return system('bash -c "'+cmd+'" 2>/dev/null'
    ).read()

def runbkg(cmd):
    return system('bash -c "'+cmd+'"')

def cp(f,p):
    run('cp '+f+' '+p)

def mv(f,p):
    run('mv '+f+' '+p)

def mkdir(a):
    if not isdir(a):
        run('mkdir '+'./%s/'%a)

def mkdirp(a):
    if not isdir(a):
        run('mkdir -p '+'%s'%a)

def rm(f):
    if isfile(f):
        run('rm '+f)

def rmf(f):
    if isfile(f):
        run('rm -f '+f)

def stdoutflush():
    sys.stdout.flush()
    return
