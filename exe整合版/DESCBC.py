# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import json
from io import BytesIO
import base64
import pyDes
import hashlib

headers={"User-Agent": "Dalvik/2.1.0"}

def md5_encrypt(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()

def decrypt_str(data):
    Key = "KW8Dvm2N"  # 加密的key
    Iv = "1ae2c94b"  # 偏移量
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    k = base64.b64decode(data)
    return method.decrypt(k)

def decrypt_str1(data,Key,Iv):
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    k = base64.b64decode(data)
    return method.decrypt(k)

def decrypt_content(res):
    accesskey=res.headers.get('Accesskey')
    keyString=res.headers.get('Keystring')
    content=res.text
    accesskeyLen = len(accesskey);
    v9 =0;
    v6 = str(ord(accesskey[accesskeyLen-1]))

    for i in range(accesskeyLen):
        v9 += ord(accesskey[i])
    v15 = v9 % len(keyString)

    v17 = int(v9 / 65)
    v18 = len(keyString)
    if v17 + v15 > v18:
        v43 = keyString[v15:(v18-v15)+v15]
    else:
        v43 = keyString[v15:v17+v15]

    v32 = len(content)
    dest=''
    if int(v6)&1:
        v38 = content[v32-12:v32]
        dest = content[0:v32-12]

    else:
        v38 = content[0:12]
        dest = content[12:len(content)]

    key = md5_encrypt(v43+v38)[0:8]
    iv = md5_encrypt(v38)[0:8]
    content = decrypt_str1(dest,key,iv).decode()
    return content
