# -*- coding: utf-8 -*-
#!/usr/bin/env python

import random,base64
from hashlib import sha1

SECRET_KEY = "ctmj#&amp;8hrgow_^sj$ejt@9fzsmh_o)-=(byt5jmg=e3#foya6u"

#RC4 algorithm
def crypt(data,key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i],box[x] = box[x],box[i]

    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x],box[y] = box[y],box[x]
        out = []
        for char in data:
            x = (x + 1 ) % 256
            y = (y + box[x]) % 256
            box[x], box[y] = box[y], box[x]
            out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
        return ''.join(out)


def encrpyt(data,key, encode=base64.b64encode,salt_length=16):
    salt = ''
    for n in range(salt_length):
        salt += chr(random.randrange(256))
    data = salt + crypt(data,sha1(key + salt).digest())
    if encode:
        data = encode(data)
    return data

def decrpyt(data,key,decode=base64.b64decode,salt_length=16):
    if decode:
        data = decode(data)
    salt = data[:salt_length]
    return crypt(data[salt_length:], sha1(key + salt).digest())
