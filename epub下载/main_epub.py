# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil
from opencc import OpenCC
import concurrent.futures
import EPUB3

class noveldl():
    #小说主地址，后接小说编号
    req_url_base='http://www.jjwxc.net/onebook.php?novelid='

    #头文件，可用来登陆，cookie可在浏览器或者client.py中获取
    headerss={'cookie':'',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    count=0
    percent=0
    index=[]#目录
    titleindex=[]#标题
    Summary=[]#内容提要
    fillNum=''#章节填充位数
    rollSign=[]#卷标
    rollSignPlace=[]#卷标位置
    state=''#繁简转换状态
    href_list=[]#章节链接
    td=[]
    
    def clear(self):
        self.count=0
        self.percent=0
        self.index=[]
        self.titleindex=[]
        self.Summary=[]
        self.fillNum=''
        self.rollSign=[]
        self.rollSignPlace=[]
        self.state=''
        self.href_list=[]
        self.td=[]
            

    #下载单章
    def get_sin(self,l):
        titleOrigin=l.split('=')
        i=self.href_list.index(l)
        cont=requests.get(l,headers=self.headerss).content
        dot=etree.HTML(cont.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
        
        #tex:正文
        tex=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/text()")
        #he:标题
        he=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[2]/h2/text()")
        #tex1:作话
        tex1=dot.xpath("//html/body/table[@id='oneboolt']/tr[2]/td[1]/div[@class='noveltext']/div[@class='readsmall']/text()")
        #sign:作话位置
        sign=dot.xpath("//*[@id='oneboolt']/tr[2]/td[1]/div/div[4]/@class")
        
        #序号填充
        title=str(titleOrigin[2]).zfill(self.fillNum)+" "
        
        #章节名称
        title=title+self.titleindex[i].strip()+" "
        
        #内容提要
        title=title+self.Summary[i].strip()
        
        if self.state=='s':
            title=OpenCC('t2s').convert(title)
        elif self.state=='t':
            title=OpenCC('s2t').convert(title)
        if self.href_list[i] in self.rollSignPlace:
            v=self.rollSign[self.rollSignPlace.index(l)]
            if self.state=='s':
                v=OpenCC('t2s').convert(self.rollSign[self.rollSignPlace.index(l)])
            elif self.state=='t':
                v=OpenCC('s2t').convert(self.rollSign[self.rollSignPlace.index(l)])

            
            
        if len(he)==0:
            print("第"+titleOrigin[2]+"章未购买或加载失败")
        else:
            #创建章节文件
            fo=open("z"+str(titleOrigin[2].zfill(self.fillNum))+".xhtml",'w',encoding='utf-8')
                
            fo.write('''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title></title></head><body>''')
            #写入卷标
            if self.href_list[i] in self.rollSignPlace:
                fo.write("<h2>"+v.rstrip()+"</h2>")
                print("\r\n"+v+"\r\n")
                fo.write("<h3 id='v'>"+title+"</h3>")
            #写入标题
            else:
                fo.write("<h3>"+title+"</h3>")
            #作话在文前的情况
            if str(sign) == "['readsmall']":
                fo.write('''<blockquote class="userstuff">''')
                for m in tex1:#删除无用文字及多余空格空行
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                    v=re.sub(' +', ' ', vv).rstrip()
                    v=re.sub('&','&amp;',v).rstrip()
                    v=re.sub('>','&gt;',v)
                    v=re.sub('<','&lt;',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":#按行写入正文
                        fo.write("<p>"+v+"</p>")
                fo.write("</blockquote>")
                if len(tex1)!=0:
                    fo.write("<hr/>")
                for tn in tex:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                    v=re.sub(' +', ' ', vv).rstrip()
                    v=re.sub('&','&amp;',v).rstrip()
                    v=re.sub('>','&gt;',v)
                    v=re.sub('<','&lt;',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write("<p>"+v+"</p>")
            else:#作话在文后的情况
                for tn in tex:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                    v=re.sub(' +', ' ', vv).rstrip()
                    v=re.sub('&','&amp;',v).rstrip()
                    v=re.sub('>','&gt;',v)
                    v=re.sub('<','&lt;',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write("<p>"+v+"</p>")
                if len(tex1)!=0:
                    fo.write("<hr/>")
                fo.write('''<blockquote class="userstuff">''')
                for m in tex1:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                    v=re.sub(' +', ' ', vv).rstrip()
                    v=re.sub('&','&amp;',v).rstrip()
                    v=re.sub('>','&gt;',v)
                    v=re.sub('<','&lt;',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write("<p>"+v+"</p>")
                fo.write("</blockquote>")
            fo.write("</body></html>")
            fo.close()
            self.percent+=1

    def get_txt(self,txt_id,state,threadnum):
        titlem=''
        intro=''
        ids=str(txt_id)
        percent=0
        self.state=state

        #获取文章网址
        req_url=ids
        
        #通过cookie获取文章信息
        res=requests.get(req_url,headers=self.headerss).content
        #对文章进行编码
        ress=etree.HTML(res.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
        
        #获取文案
        intro=ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']//text()")
        #获取标签
        info=ress.xpath("string(/html/body/table[1]/tr/td[1]/div[3])")

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
        if self.state=='s':
            titlem[0]=OpenCC('t2s').convert(titlem[0])
        elif self.state=='t':
            titlem[0]=OpenCC('s2t').convert(titlem[0])
        print("网址："+ ids + "\r\n小说信息："+ str(titlem[0]) +"\r\n")
        
        #获取所有章节网址、标题、内容提要
        self.td=ress.xpath('//*[@id="oneboolt"]//tr')
        
        for i in self.td:
            u=i.xpath('./td[2]/span/div[1]/a/@href')
            x=i.xpath('./td[2]/span/div[1]/a[1]/@rel')
            if len(u)>0:
                self.href_list+=u
                v=i.xpath('./td[2]/span/div[1]/a/text()')[0].strip()
                v=re.sub('&','&amp;',v)
                v=re.sub('>','&gt;',v)
                v=re.sub('<','&lt;',v)
                self.titleindex.append(v)
                v=i.xpath('./td[3]/text()')[0].strip()
                v=re.sub('&','&amp;',v)
                v=re.sub('>','&gt;',v)
                v=re.sub('<','&lt;',v)
                self.Summary.append(v)
            elif len(x)>0:
                self.href_list+=x
                v=i.xpath('./td[2]/span/div[1]/a/text()')[0].strip()
                v=re.sub('&','&amp;',v)
                v=re.sub('>','&gt;',v)
                v=re.sub('<','&lt;',v)
                self.titleindex.append(v)
                v=i.xpath('./td[3]/text()')[0].strip()
                v=re.sub('&','&amp;',v)
                v=re.sub('>','&gt;',v)
                v=re.sub('<','&lt;',v)
                self.Summary.append(v)
            

        #获取卷标名称
        self.rollSign=ress.xpath("//*[@id='oneboolt']//tr/td/b[@class='volumnfont']/text()")
        #获取卷标位置
        self.rollSignPlace=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
        self.rollSignPlace+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")

        section_ct=len(self.href_list)
        
        print("可下载章节数："+str(section_ct)+"\r\n")
        
        #fillNum：填充序号的长度，例如：若全文有1437章，则每章序号有四位，依次为0001、0002……
        self.fillNum=len(str(len(self.td)-4))
        
        #对标题进行操作，删除违规字符等
        ti=str(titlem[0]).split('_')
        ti=ti[0]
        ti=re.sub('/', '_', ti)
        ti=re.sub(r'\\', '_', ti)
        ti=re.sub('\|', '_', ti)
        ti=re.sub('\*','',ti)
        ti=re.sub('&','&amp;',ti)
        

        xaut=ti.split('》')[1]
        xauthref=ress.xpath("//*[@id='oneboolt']//h2/a/@href")[0]
        xtitle=re.sub('《','',ti.split('》')[0])
        

        #若文件名不想加编号，可以将这行删除
        ti=ti+'['+ids.split('=')[1]+']'
        ti=re.sub('\r','',ti)


        
        v=""
        #打开小说文件写入小说相关信息
        path=os.getcwd()
        if os.path.exists(ti):
            os.chdir(ti)
        else:
            os.mkdir(ti)
            os.chdir(ti)
        self.index=[]
        #保存封面图片
        if img!="0":
            pic=open("p.jpg",'wb')
            pic.write(img)
            pic.close()
        
            #写入封面
            f=open("C.xhtml",'w',encoding='utf-8')
            f.write('''<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title></title></head><body><img alt="p" src="p.jpg"/></body></html>''')
            f.close()

        #写入文章信息页 
        fo=open("TOC.xhtml",'w',encoding='utf-8')
        fo.write('''<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title></title></head><body>''')

        fo.write("<h2><center><a href='"+req_url+"'>"+xtitle+"</a></center></h2><p></p>")
        fo.write("<h3 class='sigil_not_in_toc'><center><a href='"+xauthref+"'>"+xaut+"</a></center></h3><p></p>")
        fo.write('''<blockquote class="userstuff">''')
        #self.index.append(titlem[0])
        #生成目录文字
        for l in self.href_list:
            titleOrigin=l.split('=')
            i=self.href_list.index(l)
            title=str(titleOrigin[2]).zfill(self.fillNum)+" "
            title=title+self.titleindex[i].strip()
            title=title+" "+self.Summary[i].strip()
            if self.state=='s':
                title=OpenCC('t2s').convert(title)
            elif self.state=='t':
                title=OpenCC('s2t').convert(title)
            if self.href_list[i] in self.rollSignPlace:
                v=self.rollSign[self.rollSignPlace.index(l)]
                if self.state=='s':
                    v=OpenCC('t2s').convert(self.rollSign[self.rollSignPlace.index(l)])
                elif self.state=='t':
                    v=OpenCC('s2t').convert(self.rollSign[self.rollSignPlace.index(l)])
                v=re.sub('&','&amp;',v).rstrip()#&amp;
                v=re.sub('>','&gt;',v)
                v=re.sub('<','&lt;',v)
                self.index.append(v)
            title=re.sub('&','&amp;',title).rstrip()#&amp;
            title=re.sub('>','&gt;',title)
            title=re.sub('<','&lt;',title)
            self.index.append(title)

        for ix in infox:
            ix=ix.strip()
            ix=re.sub('\r\n','',ix)
            ix=re.sub(' +','',ix)
            ix=re.sub('&','&amp;',ix)
            ix=re.sub('>','&gt;',ix)
            ix=re.sub('<','&lt;',ix)
            fo.write("<p>"+ix+"</p>")

        fo.write("</blockquote>")
        fo.write("<p><b>文案：</b></p>")
        for nx in intro:
            v=re.sub(' +', ' ', str(nx)).rstrip()
            v=re.sub('&','&amp;',v).rstrip()
            v=re.sub('>','&gt;',v)
            v=re.sub('<','&lt;',v)
            if self.state=='s':
                v=OpenCC('t2s').convert(v)
            elif self.state=='t':
                v=OpenCC('s2t').convert(v)
            if v!="":
                fo.write("<p>"+v+"</p>")
        info=re.sub(' +', ' ',info).strip()
        info=re.sub('&','&amp;',info)
        info=re.sub('>','&gt;',info)
        info=re.sub('<','&lt;',info)
        if self.state=='s':
            info=OpenCC('t2s').convert(info)
        elif self.state=='t':
            info=OpenCC('s2t').convert(info)
        info=re.sub('搜索关键字','</p><p>搜索关键字',info)
        fo.write("<p>"+info+"</p>")
        fo.write("</body></html>")
        fo.close()
        count=0
        tlist=[]
        #获取每一章内容
        with concurrent.futures.ThreadPoolExecutor(max_workers=threadnum) as executor:
           tlist = {executor.submit(self.get_sin,i):i for i in self.href_list}
           for future in concurrent.futures.as_completed(tlist):
               print('\r 下载进度：%d/%d\r\n' % (self.percent,section_ct),end='',flush=True)
        #for i in self.href_list:
         #   thread = Thread(target=self.get_sin, args=(i,))
          #  tlist.append(thread)
           # thread.start()
        #for t in tlist:
         #   t.join()
          #  print('\r 下载进度：%d/%d\r\n' % (self.percent,section_ct),end='',flush=True)
        print('\r 下载完成，总进度：%d/%d\r\n' % (self.percent,section_ct),end='',flush=True)


        #input("\r\n请按回车键打包epub：")
        #保存为epub
        os.chdir(path)
        epub_name = ti+".epub"
        epub = zipfile.ZipFile(epub_name, 'w')
        EPUB3.epubfile.create_mimetype(epub)     
        EPUB3.epubfile.create_container(epub)  
        os.chdir(ti)
        ppp=os.getcwd()
        EPUB3.epubfile.create_content(epub,ppp,xtitle,xaut)
        EPUB3.epubfile.create_info(epub,ppp,self.index,self.rollSign,xtitle+"-"+xaut)
        EPUB3.epubfile.create_stylesheet(epub)
        for html in os.listdir('.'):
            basename = os.path.basename(html)
            if basename.endswith('jpg'):
                epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
            if basename.endswith('html'):
                epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
        epub.close()
        os.chdir(path)
        shutil.rmtree(ppp)
        print("\r\nepub打包完成")
n=1
#此处为需要下载小说的编号，编号获取方法在上文中已经讲过，
while 1:
    num =input('\r\n请输入小说主页网址：')
    c=noveldl()
    state=input('\r\n文章内容：\r\n1、繁转简（输入s）\r\n2、简转繁（输入t）\r\n3、不变（直接按回车）\r\n')
    c.get_txt(num,state,50)
    c.clear()
