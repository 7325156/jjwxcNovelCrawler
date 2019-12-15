# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil

#小说主地址，后接小说编号
req_url_base='http://www.jjwxc.net/onebook.php?novelid='

#头文件，可用来登陆，cookie可在浏览器或者client.py中获取
headerss={'cookie': '',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
global aaa

#创建epub文件格式信息
def create_mimetype(epub):
    epub.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
 
def create_container(epub):
    container_info = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>
    '''
    epub.writestr('META-INF/container.xml',container_info, compress_type=zipfile.ZIP_STORED)
 
def create_content(epub,path,title,author):
    content_info = '''
    <?xml version="1.0" encoding="utf-8"?>
    <package version="2.0" unique-identifier="BookId" xmlns="http://www.idpf.org/2007/opf">
      <metadata>
        <dc:title>'''+title+'''</dc:title>
        <dc:creator>'''+author+'''</dc:creator>
        <meta name="cover" content="cover-image" />
      </metadata>
      <manifest>
          %(manifest)s
        <item id="ncx" href="toc.ncx" media-type="text/xml"/>
        <item id="content" href="content.html" media-type="application/xhtml+xml"/>
        <item id="css" href="stylesheet.css" media-type="text/css"/>
      </manifest>
      <spine toc="ncx">
          %(spine)s
        <itemref idref="cover" linear="no"/>
        <itemref idref="content"/>
      </spine>
    </package>
    '''
    manifest = ''
    spine = ''
    for html in os.listdir(path):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (basename, basename) 
            spine += '<itemref idref="%s"/>' % (basename)
    epub.writestr('OEBPS/content.opf',content_info % {
                                'manifest': manifest,
                                'spine': spine,},
                                compress_type=zipfile.ZIP_STORED)
 
def create_stylesheet(epub):
    css_info = '''
        body {
          font-family: sans-serif;     
        }

    '''
    epub.writestr('OEBPS/stylesheet.css',css_info,compress_type=zipfile.ZIP_STORED)


#下载单章
def get_sin(i,headers,chinf,aaa,lll):
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
    tl=tl.rstrip()+" "+chinf[aaa].strip()
    fo=open("z"+str(tit[2].zfill(3))+".xhtml",'w',encoding='utf-8')
    fo.write("<?xml version='1.0' encoding='utf-8'?>\r\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'\r\n  http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\r\n<html xmlns='http://www.w3.org/1999/xhtml'>\r\n<head>\r\n<title>"+tl+"</title>\r\n</head><body>")
    fo.write("<h2>"+tl+"\r\n</h2>")
    if str(sign) == "['readsmall']":
        for m in tex1:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
            v=re.sub(' +', ' ', vv).rstrip()
            if v!="":
                fo.write("<p>"+v+"</p>")
        if len(tex1)!=0:
            fo.write("<p>----------</p>")
        for tn in tex:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
            v=re.sub(' +', ' ', vv).rstrip()
            if v!="":
                fo.write("<p>"+v+"</p>")
    else:
        for tn in tex:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
            v=re.sub(' +', ' ', vv).rstrip()
            if v!="":
                fo.write("<p>"+v+"</p>")
        if len(tex1)!=0:
            fo.write("<p>----------</p>")
        for m in tex1:
            vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
            v=re.sub(' +', ' ', vv).rstrip()
            if v!="":
                fo.write("<p>"+v+"</p>")
    fo.write("</body></html>")
    print(tl.rstrip())
    
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
    xtitle=ress.xpath("string(//*[@id='oneboolt']/tr[1]/td/div/span/h1/span)")
    xaut=ress.xpath("string(//*[@id='oneboolt']/tr[1]/td/div/h2/a/span)")

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
    
    #ti=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[1]/span[1]/h1[1]/span[1]/text()")
    ti=str(titlem[0]).split('_')
    ti=ti[0]
    ti=re.sub('/', '_', ti)
    ti=re.sub(r'\\', '_', ti)
    ti=re.sub('\|', '_', ti)
    
    #ti=ids+ti#若文件名不想加编号，可以将这行删除
    
    v=""
    #打开小说文件写入小说相关信息
    path=os.getcwd()
    if os.path.exists(ti):
        os.chdir(ti)
    else:
        os.mkdir(ti)
        os.chdir(ti)
    fo=open("TOC.xhtml",'w',encoding='utf-8')
    fo.write("<?xml version='1.0' encoding='utf-8'?>\r\n<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN'\r\n  http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\r\n<html xmlns='http://www.w3.org/1999/xhtml'>\r\n<head>\r\n<title>"+ti+"</title>\r\n</head><body>")
    for nn in titlem:
        fo.write("<h2><a href='"+req_url+"'>"+str(nn)+"</a></h2>")
    for nx in intro:
        v=re.sub(' +', ' ', str(nx)).rstrip()
        if v!="":
            fo.write("<p>"+v+"</p>")
    info=re.sub(' +', ' ', info).rstrip()
    info=re.sub('\r', '', info)
    info=re.sub('\n', '', info)+"\r\n"
    fo.write("<p>"+info+"</p>")
    fo.write("</body></html>")
    aaa=0
    #获取每一章内容
    for i in href_list:
        aaa=aaa+1
        get_sin(i,headerss,chinf,aaa,lll)
    
    for i in hhr:
        aaa=aaa+1
        get_sin(i,headerss,chinf,aaa,lll)
    
    fo.close()
    #保存为epub
    os.chdir(path)
    epub_name = ti+".epub"
    epub = zipfile.ZipFile(epub_name, 'w')
    create_mimetype(epub)     
    create_container(epub)  
    os.chdir(ti)
    ppp=os.getcwd()
    create_content(epub,ppp,xtitle,xaut)
    create_stylesheet(epub)
    for html in os.listdir('.'):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
    epub.close()
    os.chdir(path)
    shutil.rmtree(ppp)
    print("\r\n所有章节下载完成")
n=1
#此处为需要下载小说的编号，编号获取方法在上文中已经讲过，
while n:
    num =input('请输入小说编号：')
    get_txt(num)
    n=input("继续下载（输入1）/退出程序（输入0）:")
    if str(n) == "0":
        exit()
