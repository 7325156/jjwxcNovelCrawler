# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import json
from io import BytesIO
import base64
import pyDes
def decrypt_str(data):
    Key = "KW8Dvm2N"  # 加密的key
    Iv = "1ae2c94b"  # 偏移量
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    k = base64.b64decode(data)
    return method.decrypt(k)
headerss = {'cookie': 'cookieofcommentusername=%25E5%258F%25A4%25E9%25BE%2599%25E9%25A1%25B6%25E7%259F%25B3%25E8%259C%25A5%25E8%259C%25B4%25E7%2590%2583%25E8%25B5%259B;  timeOffset_o=-831.800048828125; bbsnicknameAndsign=2%257E%2529%2524%25E5%258F%25A4%25E9%25BE%2599%25E9%25A1%25B6%25E7%259F%25B3%25E8%259C%25A5%25E8%259C%25B4%25E7%2590%2583%25E8%25B5%259B;  smidV2=2022072009415232651494365beeffbe0acbc1a89861c900a72cda9be98d3e0; testcookie=yes;  Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1696152377; token=MjAwNzA4OTB8MzI0MzI1NWI1MjZhNzIzNDE2ZTUxMGQwMTkwNTQ0ZTJ8fGJpZyoqKioqQDE2My5jb218MTgzMTI0N3w0MzIwMHwxfOa6kOWIneS5i%2BeBq3x85pmL5rGf55So5oi3fDB8ampyZWFkZXJ8MXwwfHw%3D;  bbstoken=MjAwNzA4OTBfMF9iYWYyNDRhYWM5N2I5YjFjNGVjNGI3YjRiZjdhZDQ3OF8xX18xTFN6OWRhdXUvQT1fMQ%3D%3D;  JJSESS=%7B%22sidkey%22%3A%22DZSCysTt8XBfuiLv5RGVa762pNQlmHke1Mw%22%2C%22clicktype%22%3A%22%22%7D;  Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1696425463; JJEVER=%7B%22shumeideviceId%22%3A%22WC39ZUyXRgdFGwImE1SAEXIKRZc+ekIHAD9OcL6dI1BKr5DQljF1yPE16xA25LpxtJ4ahb280Ic9xFjK1l0bxSqnK/0w3xOMItL/WmrP2Tav+DYF2YqyHq+76XDFMP+Mz3fVLMpg6KnLRSiimUmMxhJ4mCbdPQ1BRajW7hxiYtqOGduzx9VSOoUCqgMwPBHjV0JSgM/vzIa0G7wWr0zokqy0niiV7IOsveTGRfTb8IVDRcZXOIFnyYAZlZvkF7JuG2eDSNFSlDac%3D1487577677129%22%2C%22nicknameAndsign%22%3A%222%257E%2529%2524%25E5%258F%25A4%25E9%25BE%2599%25E9%25A1%25B6%25E7%259F%25B3%25E8%259C%25A5%25E8%259C%25B4%25E7%2590%2583%25E8%25B5%259B%22%2C%22foreverreader%22%3A%2220070890%22%2C%22desid%22%3A%223nmH0guS8cE4jN0ftnaczX7MD0ole3dk%22%2C%22sms_total%22%3A%220%22%2C%22lastCheckLoginTimePc%22%3A%221696422642%22%7D',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
chlink='https://app.jjwxc.net/androidapi/chapterContent?novelId=5795330&chapterId=45&versionCode=453&token=20070890_c1498e5498bb59811aefe5449cb5a95b'
chcot = requests.get(chlink, headers=headerss)
print(chcot.text.strip())
chcont = {'chapterSize': '', 'chapterDate': '', 'sayBody': '', 'upDown': '', 'content': chcot.text.strip()}
print(chcont)
tex = chcont['content']
tex = decrypt_str(tex).decode('utf-8')
print(tex)
