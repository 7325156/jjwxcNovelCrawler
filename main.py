# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re


#小说主地址，后接小说编号
req_url_base='http://www.jjwxc.net/onebook.php?novelid='

#头文件，可用来登陆，cookie可在浏览器或者client.py中获取
headers = {
    'cookie':'',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
#下载单章
def get_sin(i,headers,fo,nn,chinf):
    tit=i.split('=')
    b=str(tit[2])
    cont=requests.get(i,headers=headers).content
    dot=etree.HTML(cont.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
        
    #获取标题及正文
    tex=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/text()")
    he=dot.xpath("string(//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[2]/h2)")
    #获取作话
    tex1=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[@class='readsmall']/text()")

    tl="第 "+str(tit[2])+" 章"
    tll=he
    if he=="":
        tll="$"
    if tl[0] == tll[0]:
        tl=tll
    else:
        tl="第"+str(tit[2])+"章 "+tll
    #写入文件
    fo.write(tl.rstrip())
    fo.write("  "+chinf[nn].strip()+"\r\n")  #如果不想在标题后下载每一章的内容提要，把这行删除或者在行首加‘#’
    for tn in tex:
        v=re.sub(' +', ' ', str(tn)).rstrip()+"\r\n"
        if v == "\r\n":
            v=""
        fo.write(v)
    for m in tex1:
        v=re.sub(' +', ' ', str(m)).rstrip()+"\r\n"
        if v == "\r\n":
            v=""
        fo.write(v)
    print("第"+str(tit[2])+"章下载完成")

def get_txt(txt_id):
    titlem=''
    intro=''
    ids=str(txt_id)
    req_url=req_url_base+ids
    res=requests.get(req_url,headers=headers).content
    ress=etree.HTML(res.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
    
    #获取文案
    intro=ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']/text()")
    if len(intro) == 0:
        intro=ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']//font/text()")
    info=ress.xpath("string(//html/body/table/tr/td[1]/div[3])")
    
    #获取标题
    titlem=ress.xpath("//html/head/title/text()")
    print("编号："+ ids + " 小说信息："+ str(titlem[0]) +" 开始下载。\r\n")

    
    #获取所有章节链接//*[@id="oneboolt"]/tbody/tr[4]/td[2]/span/div[1]/a
    href_list=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a/@href")
    hhr=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a[1]/@rel")
    chinf=ress.xpath("//*[@id='oneboolt']//tr/td[3]/text()")
    section_ct=len(href_list)+len(hhr)
    print("可下载章节数："+str(section_ct)+"\r\n")
    #ti=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[1]/span[1]/h1[1]/span[1]/text()")
    ti=str(titlem[0]).split('_')
    ti=ti[0]+".txt"
    #ti=ids+ti #若将此行行首的“#”删去，可在文件名前加编号
    
    v=""
    #打开小说文件写入小说相关信息
    fo=open(ti,'w',encoding='utf-8')
    for nn in titlem:
        fo.write(str(nn)+"\r\n")
        fo.write("文案：\r\n")
    for nx in intro:
        v=re.sub(' +', ' ', str(nx)).rstrip()+"\r\n"
        if v == "\r\n":
            v=""
        fo.write(v)
    info=re.sub(' +', ' ', info).rstrip()+"\r\n"
    fo.write(info)
    nn=0
    #获取每一章内容
    for i in href_list:
        nn=1+nn
        get_sin(i,headers,fo,nn,chinf)
    
    for i in hhr:
        nn=1+nn
        get_sin(i,headers,fo,nn,chinf)
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
