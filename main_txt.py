# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil
from opencc import OpenCC
from fontTools.ttLib import TTFont
import concurrent.futures

class noveldl():
    #小说主地址，后接小说编号
    req_url_base='http://www.jjwxc.net/onebook.php?novelid='

    #头文件，可用来登陆，cookie可在浏览器或者client.py中获取，user-agent为Chrome87，可替换
    headerss={'cookie': '',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

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
    path=''
    failInfo=[]
    titleInfo=[1,1,1]
    fontlist=[]
    
    def clear(self):
        self.percent=0
        self.index=[]
        self.titleindex=[]
        self.Summary=[]
        self.fillNum=0
        self.rollSign=[]
        self.rollSignPlace=[]
        self.state=''
        self.href_list=[]
        self.td=[]
        self.failInfo=[]
        self.path=''
        self.fontlist=[]
            

    #下载单章
    def get_sin(self,l):
        titleOrigin=l.split('=')
        i=self.href_list.index(l)
        cont=requests.get(l,headers=self.headerss).content
        dot=etree.HTML(cont.decode("GB18030","ignore").encode("utf-8","ignore").decode('utf-8'))
        fontfamily=''
        cvlist=[]
        cvdic=[]
        
        #字体反爬虫
        codetext=etree.tostring(dot,encoding="utf-8").decode()
        fontsrc=re.findall(r'//static.jjwxc.net/tmp/fonts/.*?woff2.h=my.jjwxc.net',codetext)
        if fontsrc!=[]:
            fontsrc="http:"+fontsrc[0]
            fontname=re.sub('http://static.jjwxc.net/tmp/fonts/','',fontsrc)
            fontname=re.sub('.h=my.jjwxc.net','',fontname)
            fontfamily=re.sub('.woff2','',fontname)
            try:
                with open(self.path+"/Fonts/"+fontfamily+".txt", "r",encoding='utf-8') as f:
                    cvlist=f.readlines()
                    for i in range(len(cvlist)):
                        cvdic.append(cvlist[i].split('-'))
                    cvdic=dict(cvdic)
            except:
                t=1
            if not os.path.exists(self.path+"/Fonts/"+fontname):
                fontwb=requests.get(fontsrc).content
                fontf=open(self.path+"/Fonts/"+fontname,'wb')
                fontf.write(fontwb)
                fontf.close()
            if cvlist!=[]:
                fontfamily=''
            elif fontfamily not in self.fontlist:
                self.fontlist.append(fontfamily)

        
        #tex:正文
        tex=dot.xpath('//*[@id="oneboolt"]/tr[2]/td[1]/div/text()')

        #tex1:作话
        tex1=dot.xpath("//div[@class='readsmall']/text()")
        #sign:作话位置
        sign=dot.xpath("//*[@id='oneboolt']/tr[2]/td[1]/div/div[4]/@class")

        title=''
        #序号填充
        if self.titleInfo[0]=='1':
            title=str(titleOrigin[2]).zfill(self.fillNum)+"#"
        
        #章节名称
        if self.titleInfo[1]=='1':
            title=title+" "+self.titleindex[i].strip()
        
        #内容提要
        if self.titleInfo[2]=='1':
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

            
            
            #创建章节文件
        fo=open("z"+str(titleOrigin[2].zfill(4))+".txt",'w',encoding='utf-8')
            #写入卷标
        if self.href_list[i] in self.rollSignPlace:
            fo.write("\r\n\r\n"+v.rstrip()+'\r\n')
            print("\r\n"+v+"\r\n")
            fo.write(title+'\r\n')
        #写入标题
        else:
            fo.write("\r\n\r\n"+title+"\r\n")
        if len(tex)==0:
            self.failInfo.append(titleOrigin[2].zfill(self.fillNum))
            fo.write('下载失败！')
        else:
            #反爬虫处理，必须把对照表TXT文件下载至Fonts文件夹
            if cvdic!=[]:
                for i in range(len(tex)):
                    for s,v in cvdic.items():
                        s=re.sub(r'&#x',r'\\u',s)
                        s=re.sub(r';','',s).encode('utf-8').decode('unicode_escape')
                        tex[i]=re.sub(s,v.strip(),tex[i])
            cvdic=cvlist=0
            #作话在文前的情况
            if str(sign) == "['readsmall']":
                for m in tex1:#删除无用文字及多余空格空行
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                    v=re.sub(' +', ' ', vv).strip()
                    v=re.sub('　','',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    v=re.sub('作者有话要说：','作者有话要说：\n',v)
                    if v!="":#按行写入正文
                        fo.write(v+"\n")
                if len(tex1)!=0:
                    fo.write("\n*\r\n")
                for tn in tex:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                    v=re.sub(' +', ' ', vv).strip()
                    v=re.sub('　','',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write(v+"\n")
            else:#作话在文后的情况
                for tn in tex:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(tn))
                    v=re.sub(' +', ' ', vv).strip()
                    v=re.sub('　','',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    if v!="":
                        fo.write(v+"\n")
                if len(tex1)!=0:
                    fo.write("\n*\r\n")
                for m in tex1:
                    vv=re.sub('@无限好文，尽在晋江文学城','',str(m))
                    v=re.sub(' +', ' ', vv).strip()
                    v=re.sub('　','',v)
                    if self.state=='s':
                        v=OpenCC('t2s').convert(v)
                    elif self.state=='t':
                        v=OpenCC('s2t').convert(v)
                    v=re.sub('作者有话要说：','作者有话要说：\n',v)
                    if v!="":
                        fo.write(v+"\n")
        fo.close()
        self.percent+=1

    def get_txt(self,txt_id,state,threadnum):
        titlem=''
        intro=''
        ids=str(txt_id)
        percent=0
        self.state=state
        self.percent=0
        self.index=[]
        self.titleindex=[]
        self.Summary=[]
        self.fillNum=0
        self.rollSign=[]
        self.rollSignPlace=[]
        self.href_list=[]
        self.td=[]
        self.failInfo=[]

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

        #获取标题和作者
        xtitle=ress.xpath('string(//*[@itemprop="articleSection"])').strip()
        xaut=ress.xpath('string(//*[@itemprop="author"])').strip()
        ti=xtitle+'-'+xaut

        if self.state=='s':
            ti=OpenCC('t2s').convert(ti)
        elif self.state=='t':
            ti=OpenCC('s2t').convert(ti)
        print("网址："+ ids + "\r\n小说信息："+ str(ti) +"\r\n")
        
        #获取所有章节网址、标题、内容提要
        self.td=ress.xpath('//*[@id="oneboolt"]//tr')
        loc=[]
        
        for i in self.td:
            u=i.xpath('./td[2]/span/div[1]/a/@href')
            x=i.xpath('./td[2]/span/div[1]/a[1]/@rel')
            if len(u)>0:
                self.href_list+=u
                v=i.xpath('./td[2]/span/div[1]/a')
                v=etree.tostring(v[0],encoding="utf-8").decode().strip()
                v=re.sub('</?\w+[^>]*>','',v)
                self.titleindex.append(v.strip())
                v=i.xpath('./td[3]')
                v=etree.tostring(v[0],encoding="utf-8").decode().strip()
                v=re.sub('</?\w+[^>]*>','',v)
                v=re.sub('&#13;','',v)
                self.Summary.append(v.strip())
            elif len(x)>0:
                self.href_list+=x
                v=i.xpath('./td[2]/span/div[1]/a')
                v=etree.tostring(v[0],encoding="utf-8").decode().strip()
                v=re.sub('</?\w+[^>]*>','',v)
                self.titleindex.append(v.strip())
                v=i.xpath('./td[3]')
                v=etree.tostring(v[0],encoding="utf-8").decode().strip()
                v=re.sub('</?\w+[^>]*>','',v)
                v=re.sub('&#13;','',v)
                self.Summary.append(v.strip())
            elif i.xpath('./td[2]/span/div[1]/span')!=[]:
                    loc.append(i.xpath('./td[1]/text()')[0].strip())
            

        #获取卷标名称
        self.rollSign=ress.xpath("//*[@id='oneboolt']//tr/td/b[@class='volumnfont']")
        #获取卷标位置
        self.rollSignPlace=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
        self.rollSignPlace+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")

        #修改卷标格式
        for rs in range(len(self.rollSign)):
            self.rollSign[rs]=etree.tostring(self.rollSign[rs],encoding="utf-8").decode().strip()
            self.rollSign[rs]=re.sub('</?\w+[^>]*>','',self.rollSign[rs])
            self.rollSign[rs]="§ "+self.rollSign[rs]+" §"
            
        section_ct=len(self.href_list)
        
        print("可下载章节数："+str(section_ct)+"\r\n")
        if loc!=[]:
            i=""
            for x in loc:
                i=i+x+" "
            print("被锁章节："+i+"\r\n")
        
        #fillNum：填充序号的长度，例如：若全文有1437章，则每章序号有四位，依次为0001、0002……
        self.fillNum=len(str(len(self.td)-4))
        
        #对标题进行操作，删除违规字符等
        ti=re.sub('[\/:*?"<>|]','_',ti)
        ti=re.sub('&','&amp;',ti)
        

        xauthref=ress.xpath("//*[@id='oneboolt']//h2/a/@href")[0]

        

        #若文件名不想加编号，可以将这行删除
        ti=ti+'.'+ids.split('=')[1]
        ti=re.sub('\r','',ti)


        
        v=""
        #打开小说文件写入小说相关信息
        path=os.getcwd()
        self.path=path
        if not os.path.exists('Fonts'):
            os.mkdir('Fonts')
        if os.path.exists(ti+'_txt'):
            os.chdir(ti+'_txt')
        else:
            os.mkdir(ti+'_txt')
            os.chdir(ti+'_txt')
        ppp=os.getcwd()
        self.index=[]
        #写入文章信息页 
        TOC=xtitle+'\n'
        TOC+='作者：'+xaut+"\r\n"
        #生成目录文字
        for l in self.href_list:
            titleOrigin=l.split('=')
            i=self.href_list.index(l)
            #
            title=str(titleOrigin[2]).zfill(self.fillNum)+" "
            #
            title=title+self.titleindex[i].strip()+" "
            #
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
                self.index.append(v)
            self.index.append(title)

        for ix in infox:
            ix=ix.strip()
            ix=re.sub('\r\n','',ix)
            ix=re.sub(' +','',ix)
            TOC+=ix+"\r\n"

        TOC+="文案：\r\n"
        for nx in intro:
            v=re.sub(' +', ' ', str(nx)).strip()
            if self.state=='s':
                v=OpenCC('t2s').convert(v)
            elif self.state=='t':
                v=OpenCC('s2t').convert(v)
            if v!="":
                TOC+=v+"\n"
        info=re.sub(' +', ' ',info).strip()
        if self.state=='s':
            info=OpenCC('t2s').convert(info)
        elif self.state=='t':
            info=OpenCC('s2t').convert(info)
        info=re.sub('搜索关键字','\r\n搜索关键字',info)
        info=re.sub(' 一句话简介：','一句话简介：',info)
        info=re.sub('\r\n \r\n 立意：','\r\n立意：',info)
        TOC+=info+"\n"
        fo=open("TOC.txt",'w',encoding='utf-8')
        fo.write(TOC)
        fo.close()
        tlist=[]
        #获取每一章内容
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threadnum) as executor:
            tlist = {executor.submit(self.get_sin,i):i for i in self.href_list}
            for future in concurrent.futures.as_completed(tlist):
                if self.percent < section_ct:
                    print('\r 下载进度：%d/%d' % (self.percent,section_ct),end='',flush=True)
            print('\r 下载完成，总进度：%d/%d\r\n' % (self.percent,section_ct),end='',flush=True)
        '''
        for i in self.href_list:
            self.get_sin(i)
        '''
        if self.failInfo != []:
            self.failInfo.sort()
            vs=""
            for ss in self.failInfo:
                vs=vs+ss+"|"
            print("\r\n未购买或加载失败章节：")
            print(vs[:-1]+"\r\n")

        #整合
        os.chdir(path)
        f=open(ti+".txt",'w',encoding='utf-8')
        filenames=os.listdir(ppp)
        i=0
        for filename in filenames:
            filepath = ppp+'\\'+filename
            for line in open(filepath,encoding='utf-8', errors='ignore'):
                f.writelines(line)
        f.close()
        shutil.rmtree(ppp)

        print("\r\ntxt文件整合完成")

if __name__ == '__main__':
    #print('请输入cookie：')
    #cookie=input()
    #此处为需要下载小说的编号，编号获取方法在上文中已经讲过，
    while 1:
        num =input('\r\n请输入小说主页网址：')
        c=noveldl()
        
        #c.headerss={'cookie':cookie,
        #          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

        state=input('\r\n文章内容：\r\n1、繁转简（输入s）\r\n2、简转繁（输入t）\r\n3、不变（直接按回车）\r\n')
        
        titleInfo=input('\r\n请输入标题保存状态(序号 章节名称 内容提要)\r\n显示则输入1，不显示则输入0，数字之间用空格隔开\r\n例如：若只显示序号和内容提要，则输入[1 0 1](方括号不输入)\r\n若全部显示，可以直接按回车，若不显示标题，可以直接输入0\r\n若输入的数字个数小于3，则空缺的数字与最后输入的数字相同\r\n')
        if titleInfo=='':
            titleInfo='1 1 1'
        titleInfo=titleInfo.split(' ')
        while len(titleInfo)<3:
            titleInfo.append(titleInfo[len(titleInfo)-1])
        c.titleInfo=titleInfo
        
        c.get_txt(num,state,50)
