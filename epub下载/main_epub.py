# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil
from opencc import OpenCC
import EPUB

class noveldl():
    #小说主地址，后接小说编号
    req_url_base='http://www.jjwxc.net/onebook.php?novelid='

    #头文件，可用来登陆，cookie可在浏览器或者client.py中获取
    headerss={'cookie': '',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    count=0
    index=0
    Summary=''
    fillNum=''
    rollSign=''
    rollSignPlace=''
    state=''

    #下载单章 
    def get_sin(self,i,headers,sum,fillNum,rollSign,rollSignPlace,index,state):

        titleOrigin=i.split('=')
        b=str(titleOrigin[2])
        cont=requests.get(i,headers=headers).content
        dot=etree.HTML(cont.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
                
        #tex:正文
        tex=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/text()")
        #he:标题
        he=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[2]/h2/text()")
        #tex1:作话
        tex1=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[@class='readsmall']/text()")
        #sign:作话位置
        sign=dot.xpath("//*[@id='oneboolt']/tr[2]/td[1]/div/div[4]/@class")
        #标题字符串及序号填充
        title=str(titleOrigin[2]).zfill(fillNum)+" "

        if len(he)==0:
            print("第"+titleOrigin[2]+"章未购买或加载失败")
        else:
            tll=he[0]
            title=title+tll
            #self.Summary:内容提要
            title=title.rstrip()+" "+sum.strip()
            if state=='s':
                title=OpenCC('t2s').convert(title)
            elif state=='t':
                title=OpenCC('s2t').convert(title)
            #创建章节文件
            fo=open("z"+str(titleOrigin[2].zfill(fillNum))+".xhtml",'w',encoding='utf-8')
            
            fo.write('''<?xml version="1.0" encoding="utf-8"?>
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                            <html xmlns="http://www.w3.org/1999/xhtml">
                            <head><title>'''+title+'''</title></head><body>''')
            #写入卷标
            if i in rollSignPlace:
                v=rollSign[rollSignPlace.index(i)]
                if state=='s':
                    v=OpenCC('t2s').convert(rollSign[rollSignPlace.index(i)])
                elif state=='t':
                    v=OpenCC('s2t').convert(rollSign[rollSignPlace.index(i)])
                fo.write("<h1>"+v+"</h1>")
                print("\r\n"+v+"\r\n")
                index.append(v)

                #写入标题
            fo.write("<h2>"+title+"</h2>")
            index.append(title)

            #作话在文前的情况
            if str(sign) == "['readsmall']":
                for m in tex1:#删除无用文字及多余空格空行
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                    v=re.sub(' +', ' ', vv).rstrip()
                    if state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":#按行写入正文
                        fo.write("<p>"+v+"</p>")
                if len(tex1)!=0:
                    fo.write("<hr/>")
                for tn in tex:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                    v=re.sub(' +', ' ', vv).rstrip()
                    if state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write("<p>"+v+"</p>")
            else:#作话在文后的情况
                for tn in tex:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                    v=re.sub(' +', ' ', vv).rstrip()
                    if state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write("<p>"+v+"</p>")
                if len(tex1)!=0:
                    fo.write("<hr/>")
                for m in tex1:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                    v=re.sub(' +', ' ', vv).rstrip()
                    if state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write("<p>"+v+"</p>")
            fo.write("</body></html>")
            print("    "+title.rstrip())
        
    def get_txt(self,txt_id,state,threadnum):
        titlem=''
        intro=''
        ids=str(txt_id)

        #获取文章网址
        req_url=self.req_url_base+ids
        
        #通过cookie获取文章信息
        res=requests.get(req_url,headers=self.headerss).content
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
        
        if cover!='':
            pres=requests.get(cover)
            img=pres.content
        else:
            img="0"

        #获取标题
        titlem=ress.xpath("//html/head/title/text()")
        if state=='s':
            titlem[0]=OpenCC('t2s').convert(titlem[0])
        elif state=='t':
            titlem[0]=OpenCC('s2t').convert(titlem[0])
        print("编号："+ ids + " 小说信息："+ str(titlem[0]) +" 开始下载。\r\n")
        
        #获取所有章节链接
        #非vip
        href_list=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a/@href")
        #vip
        hhr=ress.xpath("//html/body/table[@id='oneboolt']//tr/td[2]/span/div[1]/a[1]/@rel")
        href_list+=hhr
        #每章内容提要
        #loc:被锁章节
        loc=ress.xpath("//*[@id='oneboolt']//tr/td[2]/span/div[1]/span/ancestor-or-self::tr/td[3]/text()")
        self.Summary=ress.xpath("//*[@id='oneboolt']//tr/td[3]/text()")
        
        for i in self.Summary:
            if i.strip()=='[此章节已锁]':
                del self.Summary[self.Summary.index(i)]
        for i in self.Summary:
            if i.strip()=='[此章节已锁]':
                del self.Summary[self.Summary.index(i)]
        if self.Summary[0].strip()=='内容提要':
            del self.Summary[0]
        for i in self.Summary:
            if i in loc:
                del self.Summary[self.Summary.index(i)]
        for i in self.Summary:
            if i in loc:
                del self.Summary[self.Summary.index(i)]
        for i in self.Summary:
            if i in loc:
                del self.Summary[self.Summary.index(i)]

        #获取卷标名称
        rollSign=ress.xpath("//*[@id='oneboolt']//tr/td/b[@class='volumnfont']/text()")
        #获取卷标位置
        rollSignPlace=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
        rollSignPlace+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")

        section_ct=len(href_list)

        print("可下载章节数："+str(section_ct)+"\r\n")
        
        #fillNum：填充序号的长度，例如：若全文有1437章，则每章序号有四位，依次为0001、0002……
        fillNum=len(str(section_ct))
        
        #对标题进行操作，删除违规字符等
        ti=str(titlem[0]).split('_')
        ti=ti[0]
        ti=re.sub('/', '_', ti)
        ti=re.sub(r'\\', '_', ti)
        ti=re.sub('\|', '_', ti)
        ti=re.sub('\*','',ti)

        

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
        index=[]
        #保存封面图片
        if img!="0":
            pic=open("p.jpg",'wb')
            pic.write(img)
            pic.close()
        
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
            if state=='s':
                v=OpenCC('t2s').convert(v)
            elif state=='t':
                v=OpenCC('s2t').convert(v)
            if v!="":
                fo.write("<p>"+v+"</p>")
        info=re.sub(' +', ' ',info).strip()
        if state=='s':
            info=OpenCC('t2s').convert(info)
        elif state=='t':
            info=OpenCC('s2t').convert(info)
        info=re.sub('搜索关键字','</p><p>搜索关键字',info)
        fo.write("<p>"+info+"</p>")
        fo.write("</body></html>")
        count=0
        #获取每一章内容
        for i,sum in zip(href_list,self.Summary):
            self.get_sin(i,self.headerss,sum,fillNum,rollSign,rollSignPlace,index,state)
            fo.close()

        
        input("\r\n请按回车键打包epub：")
        #保存为epub
        os.chdir(path)
        epub_name = ti+".epub"
        epub = zipfile.ZipFile(epub_name, 'w')
        EPUB.epubfile.create_mimetype(epub)     
        EPUB.epubfile.create_container(epub)  
        os.chdir(ti)
        ppp=os.getcwd()
        EPUB.epubfile.create_content(epub,ppp,xtitle,xaut)
        EPUB.epubfile.create_tox(epub,ppp,index,rollSign)
        EPUB.epubfile.create_stylesheet(epub)
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
    state=input('\r\n文章内容：\r\n1、繁转简（输入s）\r\n2、简转繁（输入t）\r\n3、不变（直接按回车）\r\n')
    c=noveldl()
    c.get_txt(num,state,5)
    n=input("\r\n直接按回车键退出/输入任意值下载新小说：")
    if str(n) == "0":
        exit()
