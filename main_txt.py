# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re

global aaa
#小说主地址，后接小说编号
req_url_base='http://www.jjwxc.net/onebook.php?novelid='

#头文件，可用来登陆，cookie可在浏览器或者client.py中获取
headerss={'cookie': 'CNZZDATA30075907=cnzz_eid%3D939945612-1573890182-%26ntime%3D1574667782; testcookie=yes; token=MjAwNzA4OTB8YzkxZmE2Mzg3ODI3ZjU4ZDhhY2ZiZGU1OThlZDBiOWF8fHwxODMxMjQ3fDI1OTIwMDB8MXzliJfosaHlpKnlnqN8fOasoui%2FjuaCqO%2B8jOaZi%2Baxn%2BeUqOaIt3wwfGF1dGhvcm5hbWU%3D; JJSESS=%7B%22referer%22%3A%22/book2/1975581%22%2C%22clicktype%22%3A%22%22%2C%22nicknameAndsign%22%3A%222%257E%2529%2524%25E9%25BB%258E%25E6%2598%258E%22%7D; JJEVER=%7B%22background%22%3A%22%22%2C%22font_size%22%3A%22%22%2C%22isKindle%22%3A%22%22%2C%22ispayuser%22%3A%2220070890-1%22%2C%22foreverreader%22%3A%2220070890%22%2C%22sms_total%22%3A0%7D; UM_distinctid=16eb57cfc5c536-029610602420b1-2393f61-144000-16eb57cfc5d72f; __gads=ID=015f3ae1b0bb2e24:T=1575002897:S=ALNI_MbWjHfBA_i-QcMQOYBYLYSq7ER0Nw', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

#下载单章
def get_sin(i,headers,fo,chinf,aaa,lll):
    tit=i.split('=')
    b=str(tit[2])
    cont=requests.get(i,headers=headers).content
    dot=etree.HTML(cont.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
        
        #获取标题及正文
    tex=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/text()")
    he=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[2]/h2/text()")
        #获取作话
    tex1=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[@class='readsmall']/text()")
    sign=dot.xpath("//*[@id='oneboolt']/tr[2]/td[1]/div/div[4]/@class")
    tl=str(tit[2]).zfill(lll)+"#"
    if he==[]:
        tll="$"
    else:
        tll=he[0]
    tl=tl+tll
        #写入文件
    fo.write(tl.rstrip())
    fo.write(" "+chinf[aaa].strip()+"\r\n")
    if str(sign) == "['readsmall']":
        for m in tex1:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
            v=re.sub(' +', ' ', vv).rstrip()+"\r\n"
            if v == "\r\n":
                v=""
            fo.write(v)
        fo.write("----------\r\n")
        for tn in tex:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
            v=re.sub(' +', ' ', vv).rstrip()+"\r\n"
            if v == "\r\n":
                v=""
            fo.write(v)
    else:
        for tn in tex:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
            v=re.sub(' +', ' ', vv).rstrip()+"\r\n"
            if v == "\r\n":
                v=""
            fo.write(v)
        if len(tex1)!=0:
            fo.write("----------\r\n")
        for m in tex1:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
            v=re.sub(' +', ' ', vv).rstrip()+"\r\n"
            if v == "\r\n":
                v=""
            fo.write(v)
    
    print(tl.rstrip()+" "+chinf[aaa].strip())
    
def get_txt(txt_id):
    titlem=''
    intro=''
    ids=str(txt_id)
    req_url=req_url_base+ids
    res=requests.get(req_url,headers=headerss).content
    ress=etree.HTML(res.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
    
    #获取文案
    intro=ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']//text()")
    info=ress.xpath("string(//html/body/table/tr/td[1]/div[3])")
    
    #获取标题
    titlem=ress.xpath("//html/head/title/text()")
    print("编号："+ ids + " 小说信息："+ str(titlem[0]) +" 开始下载。\r\n")

    
    #获取所有章节链接
    #非vip
    href_list=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a/@href")
    #vip
    hhr=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a[1]/@rel")
    chinf=ress.xpath("//*[@id='oneboolt']//tr/td[3]/text()")
    for i in chinf:
        if i.strip()=='':
            chinf.remove(i)
    for i in chinf:
        if i.strip()=='':
            chinf.remove(i)

    section_ct=len(href_list)+len(hhr)
    print("可下载章节数："+str(section_ct)+"\r\n")
    lll=len(str(section_ct))
    
    ti=str(titlem[0]).split('_')
    ti=ti[0]+".txt"
    ti=re.sub('/', '_', ti)
    ti=re.sub(r'\\', '_', ti)
    ti=re.sub('\|', '_', ti)
    
    #ti=ids+ti#若文件名不想加编号，可以将这行删除
    
    v=""
    #打开小说文件写入小说相关信息
    fo=open(ti,'w',encoding='utf-8')
    for nn in titlem:
        fo.write(str(nn)+"\r\n")
    fo.write(req_url+"\r\n")
    fo.write("文案：\r\n")
    for nx in intro:
        v=re.sub(' +', ' ', str(nx)).rstrip()+"\r\n"
        if v == "\r\n":
            v=""
        fo.write(v)
    info=re.sub(' +', ' ', info).rstrip()
    info=re.sub('\r', '', info)
    info=re.sub('\n', '', info)+"\r\n"
    fo.write(info)
    aaa=0
    #获取每一章内容
    for i in href_list:
        aaa=aaa+1
        get_sin(i,headerss,fo,chinf,aaa,lll)
    
    for i in hhr:
        aaa=aaa+1
        get_sin(i,headerss,fo,chinf,aaa,lll)
    print("\r\n所有章节下载完成")
    fo.close()
n=1
#此处为需要下载小说的编号，编号获取方法在上文中已经讲过，
while n:
    num =input('请输入小说编号：')
    get_txt(num)
    n=input("继续下载（输入1）/退出程序（输入0）:")
    if str(n) == "0":
        exit()
