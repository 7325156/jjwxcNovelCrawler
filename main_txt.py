# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re


#小说主地址，后接小说编号
req_url_base='http://www.jjwxc.net/onebook.php?novelid='

#头文件，可用来登陆，cookie可在浏览器或者client.py中获取
headerss={'cookie': '',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
global aaa
#下载单章
def get_sin(i,headers,chinf,aaa,lll,rosn,rossn,fo):
    tit=i.split('=')
    b=str(tit[2])
    cont=requests.get(i,headers=headers).content
    dot=etree.HTML(cont.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
        
    #tex:标题
    tex=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/text()")
    #he:正文
    he=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[2]/h2/text()")
    #tex1:作话
    tex1=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[@class='readsmall']/text()")
    #sign:作话位置
    sign=dot.xpath("//*[@id='oneboolt']/tr[2]/td[1]/div/div[4]/@class")
    #标题字符串及序号填充
    tl=str(tit[2]).zfill(lll)+"# "

    if len(he)==0:
        print("第"+tit[2]+"章未购买或加载失败")
    else:
        tll=he[0]
        tl=tl+tll
        #chinf:内容提要
        tl=tl.rstrip()+" "+chinf[aaa].strip()
        
        #写入卷标
        if i in rossn:
            fo.write("第"+str(rossn.index(i)+1)+"卷 "+rosn[rossn.index(i)]+"\r\n")
            print("\r\n"+rosn[rossn.index(i)]+"\r\n")

        #写入标题
        fo.write(tl+"\r\n")

        #作话在文前的情况
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
        else:#作话在文后的情况
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
        
        print("    "+tl)
    
def get_txt(txt_id):
    titlem=''
    intro=''
    ids=str(txt_id)
    
    #获取文章网址
    req_url=req_url_base+ids
    #通过cookie获取文章信息
    res=requests.get(req_url,headers=headerss).content
    #对文章进行编码
    ress=etree.HTML(res.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
    
    #获取文案
    intro=ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']//text()")
    #获取标签
    info=ress.xpath("string(/html/body/table[1]/tr/td[1]/div[3])")
    #获取文章信息
    infox=[]
    for i in range(1,7):
        infox.append(ress.xpath("string(/html/body/table[1]/tr/td[3]/div[2]/ul/li["+str(i)+"])"))
     
    #获取标题
    titlem=ress.xpath("//html/head/title/text()")
    print("编号："+ ids + " 小说信息："+ str(titlem[0]) +" 开始下载。\r\n")

    
    #获取所有章节链接
    #非vip
    href_list=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a/@href")
    #vip
    hhr=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a[1]/@rel")

    #每章内容提要
    loc=ress.xpath("//*[@id='oneboolt']//tr/td[2]/span/div[1]/span/ancestor-or-self::tr/td[3]/text()")
    chinf=ress.xpath("//*[@id='oneboolt']//tr/td[3]/text()")
    
    for i in chinf:
        if i.strip()=='[此章节已锁]':
            del chinf[chinf.index(i)]
    for i in chinf:
        if i.strip()=='[此章节已锁]':
            del chinf[chinf.index(i)]
    for i in chinf:
        if i in loc:
            del chinf[chinf.index(i)]
    for i in chinf:
        if i in loc:
            del chinf[chinf.index(i)]
    for i in chinf:
        if i in loc:
            del chinf[chinf.index(i)]

    #获取卷标名称
    rosn=ress.xpath("//*[@id='oneboolt']//tr/td/b[@class='volumnfont']/text()")
    #获取卷标位置
    rossn=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
    rossn+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")

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

    for ix in infox:
        ix=ix.strip()
        ix=re.sub('\r\n','',ix)
        ix=re.sub(' +','',ix)
        fo.write(ix+"\r\n")

    fo.write("文案：\r\n")
    for nx in intro:
        v=re.sub(' +', ' ', str(nx)).rstrip()+"\r\n"
        if v == "\r\n":
            v=""
        fo.write(v)
    info=re.sub(' +', ' ', info).rstrip()
    info=re.sub('\r', '', info)
    info=re.sub('搜索关键字','\r\n搜索关键字',info)
    info=re.sub('\n', '', info)+"\r\n"
    fo.write(info)
    aaa=0
    #获取每一章内容
    for i in href_list:
        aaa=aaa+1
        get_sin(i,headerss,chinf,aaa,lll,rosn,rossn,fo)
    
    for i in hhr:
        aaa=aaa+1
        get_sin(i,headerss,chinf,aaa,lll,rosn,rossn,fo)
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
