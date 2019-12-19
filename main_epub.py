# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil
from hanziconv import HanziConv

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
    <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles></container>'''
    epub.writestr('META-INF/container.xml',container_info, compress_type=zipfile.ZIP_STORED)
 
def create_content(epub,path,title,author):
    content_info = '''
<<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<package version="2.0" unique-identifier="uuid_id" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>'''+title+'''</dc:title>
  <dc:creator>'''+author+'''</dc:creator>
</metadata>
<manifest>
          %(manifest)s <item id="ncx" href="toc.ncx" media-type="text/xml"/>
        <item id="content" href="content.html" media-type="application/xhtml+xml"/>
        <item id="css" href="stylesheet.css" media-type="text/css"/>
      </manifest><spine toc="ncx"> %(spine)s <itemref idref="cover" linear="no"/>
        <itemref idref="content"/></spine></package>'''
    manifest = ''
    spine = ''
    for html in os.listdir(path):
        basename = os.path.basename(html)
        if basename.endswith('html')|basename.endswith('jpg'):
            manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (basename, basename) 
            spine += '<itemref idref="%s"/>' % (basename)
    epub.writestr('OEBPS/content.opf',content_info % {'manifest': manifest,'spine': spine,},compress_type=zipfile.ZIP_STORED)

def create_tox(epub,path,index,rosn):
    tox_info='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
   "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">

<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content=""/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>Unknown</text>
  </docTitle>
  <navMap>'''
    sig=0
    for html in os.listdir(path):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            if basename!='C.xhtml':
                while index[sig] in rosn:
                    if index[sig]==rosn[0]:
                        tox_info+='''<navPoint id="'''+str(sig)+'''" playOrder="'''+str(sig)+'''">
                        <navLabel><text>'''+index[sig]+'''</text></navLabel>
                        <content src="'''+basename+'''"/>'''
                    else:
                        tox_info+='''</navPoint><navPoint id="'''+str(sig)+'''" playOrder="'''+str(sig)+'''">
                        <navLabel><text>'''+index[sig]+'''</text></navLabel>
                        <content src="'''+basename+'''"/>'''
                    sig+=1
                tox_info+='''<navPoint id="'''+str(sig)+'''" playOrder="'''+str(sig)+'''">
                <navLabel><text>'''+index[sig]+'''</text></navLabel>
                <content src="'''+basename+'''"/></navPoint>'''
                sig+=1
    tox_info+='''</navPoint></navMap></ncx>'''
    epub.writestr('OEBPS/toc.ncx',tox_info,compress_type=zipfile.ZIP_STORED)
    
    
def create_stylesheet(epub):
    css_info = ''' body {font-family: sans-serif;}'''
    epub.writestr('OEBPS/stylesheet.css',css_info,compress_type=zipfile.ZIP_STORED)

global index
#下载单章
def get_sin(i,headers,chinf,aaa,lll,rosn,rossn,index):
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
    tl=str(tit[2]).zfill(lll)+" "

    if len(he)==0:
        print("第"+tit[2]+"章未购买或加载失败")
    else:
        tll=he[0]
        tl=tl+tll
        #chinf:内容提要
        tl=tl.rstrip()+" "+chinf[aaa].strip()
        tl=HanziConv.toSimplified(tl)
        #创建章节文件
        fo=open("z"+str(tit[2].zfill(3))+".xhtml",'w',encoding='utf-8')
        
        fo.write('''<?xml version="1.0" encoding="utf-8"?>
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml">
                    <head><title>'''+tl+'''</title></head><body>''')
        #写入卷标
        if i in rossn:
            v=HanziConv.toSimplified(rosn[rossn.index(i)])
            fo.write("<h1>"+v+"</h1>")
            print("\r\n"+v+"\r\n")
            index.append(v)

        #写入标题
        fo.write("<h2>"+tl+"</h2>")
        index.append(tl)

        #作话在文前的情况
        if str(sign) == "['readsmall']":
            for m in tex1:#删除无用文字及多余空格空行
                vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                v=re.sub(' +', ' ', vv).rstrip()
                v=HanziConv.toSimplified(v)
                if v!="":#按行写入正文
                    fo.write("<p>"+v+"</p>")
            if len(tex1)!=0:
                fo.write("<hr/>")
            for tn in tex:
                vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                v=re.sub(' +', ' ', vv).rstrip()
                v=HanziConv.toSimplified(v)
                if v!="":
                    fo.write("<p>"+v+"</p>")
        else:#作话在文后的情况
            for tn in tex:
                vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                v=re.sub(' +', ' ', vv).rstrip()
                v=HanziConv.toSimplified(v)
                if v!="":
                    fo.write("<p>"+v+"</p>")
            if len(tex1)!=0:
                fo.write("<hr/>")
            for m in tex1:
                vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                v=re.sub(' +', ' ', vv).rstrip()
                v=HanziConv.toSimplified(v)
                if v!="":
                    fo.write("<p>"+v+"</p>")
        fo.write("</body></html>")
        print("    "+tl.rstrip())
    
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
    #获取封面
    cover=ress.xpath("string(/html/body/table[1]/tr/td[1]/div[2]/img/@src)")

    pres=requests.get(cover)
    img=pres.content

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
    #获取填充序号的长度，例如：若全文有1437章，则每章序号有四位，依次为0001、0002……
    lll=len(str(section_ct))
    
    #对标题进行操作，删除违规字符等
    ti=str(titlem[0]).split('_')
    ti=ti[0]
    ti=re.sub('/', '_', ti)
    ti=re.sub(r'\\', '_', ti)
    ti=re.sub('\|', '_', ti)

    #若文件名不想加编号，可以将这行删除
    #ti=ids+ti

    xxx=ti.split('》')
    xaut=xxx[1].strip()
    xtitle=re.sub('《','',xxx[0]).strip()
    
    v=""
    #打开小说文件写入小说相关信息
    path=os.getcwd()
    if os.path.exists(ti):
        os.chdir(ti)
    else:
        os.mkdir(ti)
        os.chdir(ti)
    
    #保存封面图片
    pic=open("p.jpg",'wb')
    pic.write(img)
    pic.close()

    index=[]
    #写入封面
    f=open("C.xhtml",'w',encoding='utf-8')
    f.write('''<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml"><head><title>cover</title></head><body><img src="p.jpg"/></body></html>''')
    f.close()

    #写入文章信息页 
    fo=open("TOC.xhtml",'w',encoding='utf-8')
    fo.write('''<?xml version="1.0" encoding="utf-8"?>
             <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml"><head><title>'''+ti+'''</title></head><body>''')


    fo.write("<h2><a href='"+req_url+"'>"+titlem[0]+"</a></h2><p></p>")
    index.append(titlem[0])

    for ix in infox:
        ix=ix.strip()
        ix=re.sub('\r\n','',ix)
        ix=re.sub(' +','',ix)
        fo.write("<p>"+ix+"</p>")

    fo.write("<p><b>文案：</b></p>")
    for nx in intro:
        v=re.sub(' +', ' ', str(nx)).rstrip()
        v=HanziConv.toSimplified(v)
        if v!="":
            fo.write("<p>　　"+v+"</p>")
    info=re.sub(' +', ' ',info).strip()
    info=HanziConv.toSimplified(info)
    info=re.sub('搜索关键字','</p><p>搜索关键字',info)
    fo.write("<p>"+info+"</p>")
    fo.write("</body></html>")
    aaa=0
    #获取每一章内容
    for i in href_list:
        aaa=aaa+1
        get_sin(i,headerss,chinf,aaa,lll,rosn,rossn,index)
    
    for i in hhr:
        aaa=aaa+1
        get_sin(i,headerss,chinf,aaa,lll,rosn,rossn,index)
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
    create_tox(epub,ppp,index,rosn)
    create_stylesheet(epub)
    for html in os.listdir('.'):
        basename = os.path.basename(html)
        if basename.endswith('jpg'):
            epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
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
    n=input("直接按回车键退出/输入任意值下载新小说：")
    if str(n) == "0":
        exit()
