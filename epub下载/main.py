# -*- coding: UTF-8 -*-
import sys
import jjurl
import requests
from lxml import etree
import time
import sys
import re
import os
import zipfile
import shutil
from opencc import OpenCC
import concurrent.futures
import yaml
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import EPUB2
import EPUB3
import ctypes
import ico


class MyWindow(QMainWindow, jjurl.Ui_MainWindow):
    # 小说主地址，后接小说编号
    req_url_base = 'http://www.jjwxc.net/onebook.php?novelid='

    # 头文件，可用来登陆，cookie可在浏览器或者client.py中获取
    headerss = {'cookie': '',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

    percent = 0
    index = []  # 目录
    titleindex = []  # 标题
    Summary = []  # 内容提要
    fillNum = ''  # 章节填充位数
    rollSign = []  # 卷标
    rollSignPlace = []  # 卷标位置
    state = ''  # 繁简转换状态
    href_list = []  # 章节链接
    td = []
    path = ''
    failInfo = []
    titleInfo = [1, 1, 1]
    currentTitle = ''

    def __init__(self, parent=None):
        # self._thread = MyThread(self)
        # self._thread.updated.connect(self.download)
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # 限制lineEdit编辑框只能输入数字
        intValidator = QIntValidator(self)
        intValidator.setRange(1, 999)
        self.threadnum.setValidator(intValidator)
        self.jjurl.setText("")
        self.configsave.clicked.connect(self.saveconfig)
        self.start.clicked.connect(self.download)
        self.cssbutton.clicked.connect(self.setDefaultCss)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.setWindowIcon(QIcon(':/jjlogo.ico'))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("jjjwxcdownload")

        if os.path.exists("config.yml"):
            f = open('config.yml', encoding='utf-8')
            confdict = yaml.load(f.read(), Loader=yaml.FullLoader)
            titleInfo = confdict['titleInfo'].split(' ')
            state = confdict['state']
            if state == 't':
                self.stch.setCurrentIndex(2)
            elif state == 's':
                self.stch.setCurrentIndex(1)
            else:
                self.stch.setCurrentIndex(0)
            self.jjcookie.setText(confdict['cookie'])
            self.threadnum.setText(str(confdict['ThreadPoolMaxNum']))

            while len(titleInfo) < 3:
                titleInfo.append(titleInfo[len(titleInfo) - 1])
            if titleInfo[0] == '0':
                self.number.setChecked(False)
            if titleInfo[1] == '0':
                self.title.setChecked(False)
            if titleInfo[2] == '0':
                self.summary.setChecked(False)
            if confdict['format'] == 'epub2':
                self.format.setCurrentIndex(1)
                self.cssedit.setPlainText(confdict['css'])
            elif confdict['format'] == 'epub3':
                self.format.setCurrentIndex(2)
                self.cssedit.setPlainText(confdict['css'])
            elif confdict['format'] == 'txt':
                self.format.setCurrentIndex(0)
            if confdict['special']:
                self.special.setChecked(True)
            else:
                self.special.setChecked(False)
            if confdict['cover']:
                self.cover.setChecked(True)
            else:
                self.cover.setChecked(False)
            if confdict['chinfo']:
                self.chInfo.setChecked(True)
            else:
                self.chInfo.setChecked(False)

        else:
            f = open('config.yml', 'w', encoding='utf-8')
            f.close()

    def setDefaultCss(self):
        if self.format.currentText() == "epub2" or self.format.currentText() == "epub3":
            self.cssedit.setPlainText('''nav#landmarks {display:none;}
nav#page-list {display:none;}
ol {list-style-type: none;}/*epub3目录格式*/
h1{font-size:1.4em;text-align:center;}/*一级标题*/
h2{font-size:1.24em;text-align:center;}/*二级标题*/
.title{text-align:center;}/*文章名*/
.note{font-size:0.8em;text-align:right;}/*章节信息*/
body{}/*全局格式*/''')

    def saveconfig(self):
        with open('config.yml', encoding='utf-8') as f:
            doc = yaml.load(f.read(), Loader=yaml.FullLoader)
        cookies = self.jjcookie.text().replace("\n", " ")
        doc['cookie'] = str(cookies)
        if self.stch.currentIndex() == 0:
            doc['state'] = ""
        elif self.stch.currentIndex() == 2:
            doc['state'] = str("t")
        elif self.stch.currentIndex() == 1:
            doc['state'] = str("s")
        titleinfo = ""
        if self.number.isChecked():
            titleinfo += "1"
        else:
            titleinfo += "0"
        if self.title.isChecked():
            titleinfo += " 1"
        else:
            titleinfo += " 0"

        if self.summary.isChecked():
            titleinfo += " 1"
        else:
            titleinfo += " 0"
        doc['titleInfo'] = str(titleinfo)
        if self.format.currentText() == "epub2":
            doc['format'] = 'epub2'
            doc['css'] = self.cssedit.toPlainText()
        elif self.format.currentText() == "epub3":
            doc['format'] = 'epub3'
            doc['css'] = self.cssedit.toPlainText()
        elif self.format.currentText() == "txt":
            doc['format'] = 'txt'
        if self.special.isChecked():
            doc['special'] = 1
        else:
            doc['special'] = 0
        if self.cover.isChecked():
            doc['cover'] = 'e'
        else:
            doc['cover'] = ''
        if self.chInfo.isChecked():
            doc['chinfo'] = 1
        else:
            doc['chinfo'] = 0

        try:
            if 0 < int(self.threadnum.text()) < 1000:
                doc['ThreadPoolMaxNum'] = int(self.threadnum.text())
            else:
                QMessageBox.warning(self, '警告', '最大线程数超出范围！', QMessageBox.Yes)
        except NameError:
            QMessageBox.warning(self, '警告', 'python库错误！，请提交给7325156的GitHub', QMessageBox.Yes)
        except:
            QMessageBox.warning(self, '警告', '其他错误！请提交给7325156的GitHub', QMessageBox.Yes)

        with open('config.yml', 'w', encoding='utf-8') as f:
            yaml.dump(doc, f)
        self.setWindowTitle("晋江小说下载-配置保存完成！")

    def download(self):
        self.textEdit.clear()
        self.textEdit.moveCursor(self.textEdit.textCursor().End)
        time.sleep(0.1)

        cookie = self.jjcookie.text()
        num = self.jjurl.text()
        self.headerss = {'cookie': cookie,
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

        if self.stch.currentIndex() == 0:
            self.state = ""
        elif self.stch.currentIndex() == 2:
            self.state = str("t")
        elif self.stch.currentIndex() == 1:
            self.state = str("s")
        if re.findall(r'http\://www.jjwxc.net/onebook.php\?novelid=[0-9]+', num):
            self.get_txt(num, int(self.threadnum.text()))
        else:
            QMessageBox.warning(self, '警告', '网址格式错误！请使用网页版网址', QMessageBox.Yes)

    def get_sin(self, l):
        titleOrigin = l.split('=')
        i = self.href_list.index(l)
        self.currentTitle = ''
        # 获取app源
        chlink = re.sub(r'http.*?novelid=', 'https://app.jjwxc.net/androidapi/chapterContent?novelId=', l)
        chlink = re.sub('chapterid', 'chapterId', chlink)
        chcot = requests.get(chlink, headers=self.headerss)
        try:
            chcont = json.loads(chcot.text)
        except:
            chcont = {'chapterSize': '', 'chapterDate': '', 'sayBody': '', 'upDown': '', 'content':''}



        if 'content' in chcont.keys():
            tex = chcont['content']
            tex = re.sub('&lt;br&gt;', '\n', tex).splitlines()
            # tex1:作话
            tex1 = chcont['sayBody'].splitlines()
            # sign:作话位置
            sign = chcont['upDown']
        else:
            tex=''
            tex1=''
            sign=''

        if str(i) in self.rollSignPlace:
            v = self.rollSign[self.rollSignPlace.index(str(i))]
            if self.state == 's':
                v = OpenCC('t2s').convert(self.rollSign[self.rollSignPlace.index(l)])
            elif self.state == 't':
                v = OpenCC('s2t').convert(self.rollSign[self.rollSignPlace.index(l)])
            self.textEdit.append('\n' + v + '\n')
            self.textEdit.moveCursor(self.textEdit.textCursor().End)
            time.sleep(0.1)

        title = ''
        # 序号填充
        if self.number.isChecked():
            title = str(titleOrigin[2]).zfill(self.fillNum)
            if self.format.currentText() == "txt":
                title += " #"

        # 章节名称
        if self.title.isChecked():
            title = title + " " + self.titleindex[i].strip()

        # 内容提要
        if self.summary.isChecked():
            title = title + " " + self.Summary[i].strip()

        title = title.strip()
        self.currentTitle = title

        if self.state == 's':
            title = OpenCC('t2s').convert(title)
        elif self.state == 't':
            title = OpenCC('s2t').convert(title)

        # 创建章节文件
        content = ''

        # 写入标题
        if self.format.currentText() == "txt":
            content += "\n\n" + title + "\n"
        else:
            content += '<h2>' + title + "</h2>"
        if len(tex) == 0:
            self.failInfo.append(titleOrigin[2].zfill(self.fillNum))
            # self.textEdit.append("第"+titleOrigin[2]+"章未购买或加载失败")
        else:
            if self.chInfo.isChecked() and self.format.currentText() == "txt":
                content += "字数：" + chcont['chapterSize'] + '\n日期：' + chcont['chapterDate'] + '\r\n'
            elif self.chInfo.isChecked():
                content += "<p class='note'>字数：" + chcont['chapterSize'] + '<br/>日期：' + chcont['chapterDate'] + '</p>'

            # 作话在文前的情况
            if not sign:
                if not self.format.currentText() == "txt" and len(tex1):
                    content += "<p><b>作者有话要说</b>：</p><blockquote>"
                elif len(tex1):
                    content += "作者有话要说：\n"
                for m in tex1:  # 删除无用文字及多余空格空行
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(m))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if v != "" and self.format.currentText() == "txt":  # 按行写入正文
                        content += v + "\n"
                    elif v != "":
                        content += "<p>" + v + "</p>"
                if not self.format.currentText() == "txt":
                    content += "</blockquote>"
                if len(tex1) and self.format.currentText() == "txt":
                    content += "\n*\n"
                elif len(tex1):
                    content += "<hr/>"
                for tn in tex:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(tn))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if v != "" and self.format.currentText() == "txt":  # 按行写入正文
                        content += v + "\n"
                    elif v != "":
                        content += "<p>" + v + "</p>"
            else:  # 作话在文后的情况
                for tn in tex:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(tn))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if v != "" and self.format.currentText() == "txt":  # 按行写入正文
                        content += v + "\n"
                    elif v != "":
                        content += "<p>" + v + "</p>"
                if len(tex1) and self.format.currentText() == "txt":
                    content += "\n*\n"
                elif len(tex1):
                    content += "<hr/>"
                if not self.format.currentText() == "txt" and len(tex1):
                    content += "<p><b>作者有话要说</b>：</p><blockquote>"
                elif len(tex1):
                    content += "作者有话要说：\n"
                for m in tex1:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(m))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if v != "" and self.format.currentText() == "txt":  # 按行写入正文
                        content += v + "\n"
                    elif v != "":
                        content += "<p>" + v + "</p>"
                if len(tex1) != 0 and not self.format.currentText() == "txt":
                    content += "</blockquote>"
        if not self.format.currentText() == "txt":
            content += "</body></html>"

        if self.format.currentText() == "txt":
            with open("z" + str(titleOrigin[2].zfill(4)) + ".txt", 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open("z" + str(titleOrigin[2].zfill(4)) + ".xhtml", 'w', encoding='utf-8') as f:
                f.write('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>''' + title + '''</title>
<meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/>
</head><body>''')
                f.write(content)
        self.percent += 1

    def get_txt(self, txt_id, threadnum):
        intro = ''
        ids = str(txt_id)
        self.percent = 0
        self.index = []
        self.titleindex = []
        self.Summary = []
        self.fillNum = 0
        self.rollSign = []
        self.rollSignPlace = []
        self.state = ''
        self.href_list = []
        self.td = []
        self.failInfo = []
        self.path = ''
        self.textEdit.clear()
        section_ct = 9999

        # 获取文章网址
        req_url = ids

        # 通过cookie获取文章信息
        res = requests.get(req_url, headers=self.headerss)
        # 对文章进行编码
        ress = etree.HTML(res.content.decode("GB18030", "ignore").encode("utf-8", "ignore").decode('utf-8'))
        res.close()

        # 获取文案
        if self.special.isChecked():
            intro = ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']")
            info = ress.xpath('//html/body/table[1]/tr[1]/td[1]/div[3]')
        else:
            intro = ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']//text()")
            info = ress.xpath("string(/html/body/table[1]/tr/td[1]/div[3])")
        # 获取标签

        infox = []
        for i in range(1, 7):
            infox.append(ress.xpath("string(/html/body/table[1]/tr/td[3]/div[2]/ul/li[" + str(i) + "])"))

        # 获取封面
        cover = ress.xpath("string(/html/body/table[1]/tr/td[1]/div[2]/img/@src)")

        if cover != '':
            try:
                pres = requests.get(cover)
            except Exception:
                img = "0"
                self.textEdit.append("【封面下载失败！请检查网络或尝试科学上网。】\n")
                self.textEdit.moveCursor(self.textEdit.textCursor().End)

            else:
                img = pres.content
        else:
            img = "0"

        fpi = re.findall(r'static.jjwxc.net/novelimage.php.novelid', cover)
        if fpi:
            img = '0'
        # 获取标题和作者
        xtitle = ress.xpath('string(//*[@itemprop="articleSection"])').strip()
        xaut = ress.xpath('string(//*[@itemprop="author"])').strip()
        ti = xtitle + '-' + xaut

        if self.state == 's':
            ti = OpenCC('t2s').convert(ti)
        elif self.state == 't':
            ti = OpenCC('s2t').convert(ti)
        self.textEdit.append("网址：" + ids + "\n小说信息：" + str(ti) + "\n")
        self.textEdit.moveCursor(self.textEdit.textCursor().End)
        self.setWindowTitle("正在下载：" + xtitle + '-' + xaut)

        # 获取所有章节网址、标题、内容提要
        self.td = ress.xpath('//*[@id="oneboolt"]//tr')
        loc = []

        for i in self.td:
            u = i.xpath('./td[2]/span/div[1]/a/@href')
            x = i.xpath('./td[2]/span/div[1]/a[1]/@rel')
            if len(u) > 0:
                self.href_list += u
                v = i.xpath('./td[2]/span/div[1]/a')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                v = re.sub('  +', ' ', v)
                if self.format.currentText() == "txt":
                    v = re.sub('</?\w+[^>]*>', '', v)
                else:
                    v = re.sub('<a.*?>', '', v)
                    v = re.sub('</a>', '', v)
                self.titleindex.append(v.strip())
                v = i.xpath('./td[3]')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                if self.format.currentText() == "txt":
                    v = re.sub('</?\w+[^>]*>', '', v)
                    v = re.sub('&#13;', '', v)
                else:
                    v = re.sub('<td>&#13;', '', v)
                    v = re.sub('<td>', '', v)
                    v = re.sub('</td>&#13;', '', v)
                    v = re.sub('</td>', '', v)
                self.Summary.append(v.strip())
            elif len(x) > 0:
                self.href_list += x
                v = i.xpath('./td[2]/span/div[1]/a')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                if self.format.currentText() == "txt":
                    v = re.sub('</?\w+[^>]*>', '', v)
                else:
                    v = re.sub('<a.*?>', '', v)
                    v = re.sub('</a>', '', v)
                self.titleindex.append(v.strip())
                v = i.xpath('./td[3]')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                if self.format.currentText() == "txt":
                    v = re.sub('</?\w+[^>]*>', '', v)
                    v = re.sub('&#13;', '', v)
                else:
                    v = re.sub('<td>&#13;', '', v)
                    v = re.sub('<td>', '', v)
                    v = re.sub('</td>&#13;', '', v)
                    v = re.sub('</td>', '', v)
                self.Summary.append(v.strip())
            elif i.xpath('./td[2]/span/div[1]/span'):
                loc.append(i.xpath('./td[1]/text()')[0].strip())

        # 获取卷标名称
        self.rollSign = ress.xpath("//*[@id='oneboolt']//tr/td/b[@class='volumnfont']")
        # 获取卷标位置
        self.rollSignPlace = []
        # self.rollSignPlace+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
        # self.rollSignPlace+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")
        self.rollSignPlace += ress.xpath(
            "//*[@class='volumnfont']/ancestor-or-self::tr/following-sibling::tr[1]/td[1]/text()")

        # 修改卷标格式
        for rs in range(len(self.rollSign)):
            self.rollSign[rs] = etree.tostring(self.rollSign[rs], encoding="utf-8").decode().strip()
            if self.format.currentText() == "txt":
                self.rollSign[rs] = re.sub('</?\w+[^>]*>', '', self.rollSign[rs])
            else:
                self.rollSign[rs] = re.sub('<b.*?>', '', self.rollSign[rs])
                self.rollSign[rs] = re.sub('</b>', '', self.rollSign[rs])
            self.rollSign[rs] = "§ " + self.rollSign[rs] + " §"

        section_ct = len(self.href_list)
        lockinfo = ''

        self.textEdit.append("可下载章节数：" + str(section_ct) + "\n")
        self.textEdit.moveCursor(self.textEdit.textCursor().End)
        if loc != []:
            i = ""
            for x in loc:
                i = i + x + " "
            self.textEdit.append("被锁章节：" + i + "\n")
            self.textEdit.moveCursor(self.textEdit.textCursor().End)
            if self.format.currentText() == "txt":
                lockinfo = "被锁章节：" + i + "\n"
            else:
                lockinfo = "<p><em>被锁章节：" + i + "</em></p>"

        # fillNum：填充序号的长度，例如：若全文有1437章，则每章序号有四位，依次为0001、0002……
        self.fillNum = len(str(len(self.td) - 4))

        # 对标题进行操作，删除违规字符等
        ti = re.sub('[\/:*?"<>|]', '_', ti)
        ti = re.sub('&', '&amp;', ti)

        xauthref = ress.xpath('//*[@id="oneboolt"]//h2/a/@href')[0]

        # 若文件名不想加编号，可以将这行删除
        ti = ti + '.' + ids.split('=')[1]
        ti = re.sub('\r', '', ti)

        v = ""
        # 打开小说文件写入小说相关信息
        path = os.getcwd()
        self.path = path
        if os.path.exists(ti):
            os.chdir(ti)
        else:
            os.mkdir(ti)
            os.chdir(ti)
        ppp = os.getcwd()
        for vol in range(len(self.rollSignPlace)):
            self.rollSignPlace[vol] = self.rollSignPlace[vol].strip()
            volt = self.rollSignPlace[vol]
            ros = self.rollSign[vol]
            nm = 'z' + str(int(volt) - 1).zfill(4) + '_vol.xhtml'
            if self.state == 's':
                ros = OpenCC('t2s').convert(ros)
            elif self.state == 't':
                rose = OpenCC('s2t').convert(ros)
            with open(nm, 'w', encoding='utf-8') as f:
                f.write(('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>''' + ros + '''</title><meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/></head>
<body><h1>''' + ros + '''</h1></body></html>'''))
        self.index = []
        # 保存封面图片
        if img != "0" and self.cover.isChecked() and not self.format.currentText() == "txt":
            with open("p.jpg", 'wb') as pic:
                pic.write(img)

            # 写入封面
            with open("C.xhtml", 'w', encoding='utf-8') as f:
                f.write('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Cover</title></head>
<body><div style="text-align: center; padding: 0pt; margin: 0pt;">
<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
<image width="100%" xlink:href="p.jpg"/></svg></div></body></html>''')

        # 写入文章信息页
        if self.format.currentText() == "txt":
            TOC = xtitle + '\n'
            TOC += '作者：' + xaut + "\n"
            TOC += '源网址：' + req_url + '\n'
        else:
            TOC = "<h1 class='title' title='" + xtitle + "-" + xaut + "'><a href='" + req_url + "'>" + xtitle + "</a></h1>"
            TOC += "<h2 class='sigil_not_in_toc title'>作者：<a href='" + xauthref + "'>" + xaut + "</a></h2>"
            TOC += '''<blockquote>'''

        # 生成目录文字
        for l in self.href_list:
            titleOrigin = l.split('=')
            i = self.href_list.index(l)
            #
            title = str(titleOrigin[2]).zfill(self.fillNum) + " "
            #
            title = title + self.titleindex[i].strip() + " "
            #
            title = title + self.Summary[i].strip()
            if self.state == 's':
                title = OpenCC('t2s').convert(title)
            elif self.state == 't':
                title = OpenCC('s2t').convert(title)
            self.index.append(title)

        for ix in infox:
            ix = ix.strip()
            ix = re.sub('\n', '', ix)
            ix = re.sub(' +', '', ix)
            ix = re.sub('&', '&amp;', ix)
            ix = re.sub('>', '&gt;', ix)
            ix = re.sub('<', '&lt;', ix)
            if self.format.currentText() == "txt":
                TOC += ix + "\n"
            else:
                TOC += "<p>" + ix + "</p>"
        if self.format.currentText() == "txt":
            TOC += "文案：\n"
        else:
            TOC += "</blockquote>"
            TOC += "<hr/><p><b>文案：</b></p>"
        if self.special.isChecked():
            v = etree.tostring(intro[0], encoding="utf-8").decode()
            if self.state == 's':
                v = OpenCC('t2s').convert(v)
            elif self.state == 't':
                v = OpenCC('s2t').convert(v)
            TOC += v
        else:
            for nx in intro:
                v = re.sub(' +', ' ', str(nx)).rstrip()
                v = re.sub('&', '&amp;', v).rstrip()
                v = re.sub('>', '&gt;', v)
                v = re.sub('<', '&lt;', v)
                if self.state == 's':
                    v = OpenCC('t2s').convert(v)
                elif self.state == 't':
                    v = OpenCC('s2t').convert(v)
                if v != "" and self.format.currentText() == "txt":
                    TOC += v + "\n"
                elif v:
                    TOC += "<p>" + v + "</p>"
        if type(info) == str:
            info = re.sub(' +', ' ', info).strip()
            info = re.sub('&', '&amp;', info)
            info = re.sub('>', '&gt;', info)
            info = re.sub('<', '&lt;', info)
            if self.state == 's':
                info = OpenCC('t2s').convert(info)
            elif self.state == 't':
                info = OpenCC('s2t').convert(info)
        if self.format.currentText() == "txt":
            info = re.sub('搜索关键字', '\n搜索关键字', info)
            info = re.sub(' +一句话简介：', '\n一句话简介：', info)
            info = re.sub('\n +\n +立意：', '\n立意：', info)
            info = re.sub(' +', ' ', info)
            TOC += info
            fo = open("info.txt", 'w', encoding='utf-8')
            fo.write(TOC.strip() + '\n')
            fo.write(lockinfo.strip() + '\n')
            fo.close()
        else:
            if self.special.isChecked():
                info = etree.tostring(info[0], encoding="utf-8").decode()
                if self.state == 's':
                    info = OpenCC('t2s').convert(info)
                elif self.state == 't':
                    info = OpenCC('s2t').convert(info)
                TOC += '<hr/><br/>' + info
            else:
                info = re.sub('内容标签', '<b>内容标签</b>', info)
                info = re.sub('搜索关键字', '</p><p><b>搜索关键字</b>', info)
                info = re.sub('一句话简介：', '</p><p><b>一句话简介</b>：', info)
                info = re.sub('立意：', '</p><p><b>立意</b>：', info)
                TOC += "<hr/><p>" + info + "</p>"
            with open("info.xhtml", 'w', encoding='utf-8') as fo:
                fo.write('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title></title><meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/></head>
<body>''' + TOC + lockinfo + '''</body></html>''')
        tlist = []
        # 获取每一章内容

        with concurrent.futures.ThreadPoolExecutor(max_workers=threadnum) as executor:
            tlist = {executor.submit(self.get_sin, i): i for i in self.href_list}
            for future in concurrent.futures.as_completed(tlist):
                if self.percent < section_ct:
                    self.progressBar.setValue(int(100 * self.percent / section_ct))
                    self.progressBar.update()
                    self.pct.setText(str(self.percent) + '/' + str(section_ct))
                    self.setWindowTitle("正在下载：" + xtitle + '-' + xaut + " (" + self.pct.text() + ")")
                    QApplication.processEvents()
            if self.percent < section_ct:
                QMessageBox.warning(self, '警告', '请检查cookie是否正确！\n章节：' + self.currentTitle, QMessageBox.Yes)
            self.progressBar.setValue(int(100 * self.percent / section_ct))
            self.progressBar.update()
            self.textEdit.append('\n 下载完成，总进度：' + str(self.percent) + '/' + str(section_ct))
            self.textEdit.moveCursor(self.textEdit.textCursor().End)
            time.sleep(0.1)
            self.pct.setText(str(self.percent) + '/' + str(section_ct))
        '''
        for i in self.href_list:
            self.get_sin(i)
        '''
        if self.failInfo:
            self.failInfo.sort()
            vs = ""
            for ss in self.failInfo:
                vs = vs + ss + "|"
            self.textEdit.append("\n未购买或加载失败章节：")
            self.textEdit.append(vs[:-1] + "\n")
            self.textEdit.moveCursor(self.textEdit.textCursor().End)

        if self.format.currentText() == "txt":
            # txt整合
            os.chdir(path)
            f = open(ti + ".txt", 'w', encoding='utf-8')
            filenames = os.listdir(ppp)
            i = 0
            for filename in filenames:
                filepath = ppp + '\\' + filename
                for line in open(filepath, encoding='utf-8', errors='ignore'):
                    f.writelines(line)
            f.close()
            shutil.rmtree(ppp)
            self.textEdit.append("\ntxt文件整合完成")
            self.textEdit.moveCursor(self.textEdit.textCursor().End)

        else:
            # 保存为epub
            os.chdir(path)
            epub_name = ti + ".epub"
            epub = zipfile.ZipFile(epub_name, 'w')
            if self.format.currentText() == "epub2":
                epubfile = EPUB2.epubfile()
            else:
                epubfile = EPUB3.epubfile()
            epubfile.csstext = self.cssedit.toPlainText()
            epubfile.createEpub(epub, xaut, xtitle, ti, self.index, self.rollSign, path)
            self.textEdit.append("\nepub打包完成")
            self.textEdit.moveCursor(self.textEdit.textCursor().End)
        self.setWindowTitle("下载完成：" + xtitle + '-' + xaut + " (" + self.pct.text() + ")")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
