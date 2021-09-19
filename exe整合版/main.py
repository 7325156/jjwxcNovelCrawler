# -*- coding: UTF-8 -*-
# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
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
from fontTools.ttLib import TTFont
import concurrent.futures
import yaml
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import EPUB2
import EPUB3

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
    fontcss = ''
    fontlist = []

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
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        ico_path = os.path.join(os.path.dirname(__file__), 'jjlogo.ico')
        icon = QIcon()
        icon.addPixmap(QPixmap(ico_path), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        if os.path.exists("config.yml"):
            f = open('config.yml', encoding='utf-8')
            confdict = yaml.load(f.read(), Loader=yaml.FullLoader)
            titleInfo = confdict['titleInfo'].split(' ')
            state = confdict['state']
            if state == 't':
                self.s2t.setChecked(True)
            elif state == 's':
                self.t2s.setChecked(True)
            else:
                self.stremain.setChecked(True)
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
                self.epub2.setChecked(True)
            elif confdict['format'] == 'epub3':
                self.epub3.setChecked(True)
            elif confdict['format'] == 'epub2s':
                self.epub2s.setChecked(True)
            elif confdict['format'] == 'epub3s':
                self.epub3s.setChecked(True)
            elif confdict['format'] == 'txt':
                self.txt.setChecked(True)
            if confdict['cover']:
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        else:
            f = open('config.yml', 'w', encoding='utf-8')
        f.close()

    def saveconfig(self):
        with open('config.yml', encoding='utf-8') as f:
            doc = yaml.load(f.read(), Loader=yaml.FullLoader)
        cookies = self.jjcookie.text().replace("\n", " ")
        doc['cookie'] = str(cookies)
        if self.stremain.isChecked():
            doc['state'] = ""
        elif self.s2t.isChecked():
            doc['state'] = str("t")
        elif self.t2s.isChecked():
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
        if self.epub2.isChecked():
            doc['format'] = 'epub2'
        elif self.epub3.isChecked():
            doc['format'] = 'epub3'
        elif self.epub3s.isChecked():
            doc['format'] = 'epub3s'
        elif self.epub2s.isChecked():
            doc['format'] = 'epub2s'
        elif self.txt.isChecked():
            doc['format'] = 'txt'
        if self.checkBox.isChecked():
            doc['cover'] = 'e'
        else:
            doc['cover'] = ''

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

    def download(self):
        self.textEdit.clear()
        self.textEdit.moveCursor(self.textEdit.textCursor().End)

        cookie = self.jjcookie.text()
        num = self.jjurl.text()
        self.headerss = {'cookie': cookie,
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

        if self.stremain.isChecked():
            self.state = ""
        elif self.s2t.isChecked():
            self.state = str("t")
        elif self.t2s.isChecked():
            self.state = str("s")

        self.get_txt(num, int(self.threadnum.text()))
        QApplication.processEvents()

    def get_sin(self, l):
        titleOrigin = l.split('=')
        i = self.href_list.index(l)

        # dot=etree.HTML(cont.content)
        fontfamily = ''
        cvlist = []
        cvdic = []
        cont = ''
        dot = ''
        codetext = ''
        badgateway = True
        while (badgateway):
            cont = requests.get(l, headers=self.headerss)
            dot = etree.HTML(cont.content.decode('gb18030', "ignore").encode("utf-8").decode('utf-8'))
            codetext = etree.tostring(dot, encoding="utf-8").decode()
            bdw = re.findall('<h1>502 Bad Gateway</h1>', codetext)
            if bdw == []:
                badgateway = False
            else:
                time.sleep(1)

        # 字体反爬虫
        fontsrc = re.findall(r'//static.jjwxc.net/tmp/fonts/.*?woff2.h=my.jjwxc.net', codetext)
        if fontsrc:
            fontsrc = "http:" + fontsrc[0]
            fontname = re.sub('http://static.jjwxc.net/tmp/fonts/', '', fontsrc)
            fontname = re.sub('.h=my.jjwxc.net', '', fontname)
            fontfamily = re.sub('.woff2', '', fontname)
            cvdic = []
            if not os.path.exists(self.path + "/Fonts/" + fontfamily + '.txt'):
                # 解析json文件
                r = requests.get('http://jjwxc.yooooo.us/' + fontfamily + '.json')
                fonttxt = re.sub('{"status": 0, "data": ', '', r.text)
                fonttxt = re.sub('}}', '}', fonttxt)
                cdic = json.loads(fonttxt)
                fonttxt = ''
                f = open(self.path + "/Fonts/" + fontfamily + ".txt", "w", encoding='utf-8')
                for s, v in cdic.items():
                    fonttxt = fonttxt + '&#x' + s + ';-' + v + '\n'
                fonttxt.strip()
                f.write(fonttxt)
                f.close()

                # 若需要下载ttf文件，可运行下方代码
                fontwb = requests.get(re.sub('woff2', 'ttf', fontsrc)).content
                fontf = open(self.path + "/Fonts/" + fontfamily + '.ttf', 'wb')
                fontf.write(fontwb)
                fontf.close()

            try:
                with open(self.path + "/Fonts/" + fontfamily + ".txt", "r", encoding='utf-8') as f:
                    cvlist = f.readlines()
                    for y in range(len(cvlist)):
                        cvdic.append(cvlist[y].split('-'))
                    cvdic = dict(cvdic)
            except:
                t = 1
            if cvlist != []:
                fontfamily += '_c'
            elif fontfamily not in self.fontlist:
                self.fontlist.append(fontfamily)
                self.fontcss += '''@font-face{font-family: "%s";
            src:url("%s") format('woff2'),
            url("../font/%s") format('woff2'),
            url("../font/%s.ttf") format("truetype");}
            .%s{font-family:"%s",serif;}
            ''' % (fontfamily, fontsrc, fontname, fontfamily, fontfamily, fontfamily)

        # tex:正文
        tex = dot.xpath('//*[@id="oneboolt"]/tr[2]/td[1]/div/text()')

        # tex1:作话
        tex1 = dot.xpath("//div[@class='readsmall']/text()")
        # sign:作话位置
        sign = dot.xpath("//*[@id='oneboolt']/tr[2]/td[1]/div/div[4]/@class")

        title = ''
        # 序号填充
        if self.number.isChecked():
            title = str(titleOrigin[2]).zfill(self.fillNum)
            if self.txt.isChecked():
                title += " #"

        # 章节名称
        if self.title.isChecked():
            title = title + " " + self.titleindex[i].strip()

        # 内容提要
        if self.summary.isChecked():
            title = title + " " + self.Summary[i].strip()

        title = title.strip()

        if self.state == 's':
            title = OpenCC('t2s').convert(title)
        elif self.state == 't':
            title = OpenCC('s2t').convert(title)
        if self.href_list[i] in self.rollSignPlace:
            v = self.rollSign[self.rollSignPlace.index(l)]
            if self.state == 's':
                v = OpenCC('t2s').convert(self.rollSign[self.rollSignPlace.index(l)])
            elif self.state == 't':
                v = OpenCC('s2t').convert(self.rollSign[self.rollSignPlace.index(l)])

        # 创建章节文件
        if self.txt.isChecked():
            fo = open("z" + str(titleOrigin[2].zfill(4)) + ".txt", 'w', encoding='utf-8')
        else:
            fo = open("z" + str(titleOrigin[2].zfill(4)) + ".xhtml", 'w', encoding='utf-8')
            fo.write('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>''' + title + '''</title>
<meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/>
</head><body class="''' + fontfamily + '''">''')
        # 写入卷标
        rs = ''
        if self.href_list[i] in self.rollSignPlace:
            if self.txt.isChecked():
                v = re.sub('&amp;', '&', v)
                v = re.sub('&lt;', '<', v)
                v = re.sub('&gt;', '>', v)
                fo.write("\n\n" + v.rstrip() + '\n')
                fo.write(title + '\n')
            else:
                fo.write("<h1>" + v.rstrip() + "</h1>")
                rs = " id='v'"
            self.textEdit.append("\n" + v + "\n")
            self.textEdit.moveCursor(self.textEdit.textCursor().End)

        # 写入标题
        if self.txt.isChecked():
            fo.write("\n\n" + title + "\n")
        else:
            fo.write('<h2' + rs + '>' + title + "</h2>")
        if len(tex) == 0:
            self.failInfo.append(titleOrigin[2].zfill(self.fillNum))
            # self.textEdit.append("第"+titleOrigin[2]+"章未购买或加载失败")
        else:
            # 反爬虫处理，必须把对照表TXT文件下载至Fonts文件夹
            if cvdic:
                for y in range(len(tex)):
                    for s, v in cvdic.items():
                        if not s == '&#x78"/;':
                            s = re.sub(r'&#x', r'\\u', s)
                            s = re.sub(';', '', s).encode('utf-8').decode('unicode_escape')
                            tex[y] = re.sub(s, v.strip(), tex[y])
            cvdic = cvlist = []
            # 作话在文前的情况
            if str(sign) == "['readsmall']":
                if not self.txt.isChecked():
                    fo.write('''<blockquote>''')
                for m in tex1:  # 删除无用文字及多余空格空行
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(m))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&', '&amp;', v)
                    v = re.sub('>', '&gt;', v)
                    v = re.sub('<', '&lt;', v)
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if self.txt.isChecked():
                        v = re.sub('作者有话要说：', '作者有话要说：\n', v)
                    else:
                        v = re.sub('作者有话要说：', '<b>作者有话要说</b>：</p><p>', v)
                    if v != "" and self.txt.isChecked():  # 按行写入正文
                        fo.write(v + "\n")
                    elif v != "":
                        fo.write("<p>" + v + "</p>")
                if not self.txt.isChecked():
                    fo.write("</blockquote>")
                if len(tex1) != 0 and self.txt.isChecked():
                    fo.write("\n*\n")
                elif len(tex1) != 0:
                    fo.write("<hr/>")
                for tn in tex:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(tn))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&', '&amp;', v)
                    v = re.sub('>', '&gt;', v)
                    v = re.sub('<', '&lt;', v)
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if v != "" and self.txt.isChecked():  # 按行写入正文
                        fo.write(v + "\n")
                    elif v != "":
                        fo.write("<p>" + v + "</p>")
            else:  # 作话在文后的情况
                for tn in tex:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(tn))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&', '&amp;', v)
                    v = re.sub('>', '&gt;', v)
                    v = re.sub('<', '&lt;', v)
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if v != "" and self.txt.isChecked():  # 按行写入正文
                        fo.write(v + "\n")
                    elif v != "":
                        fo.write("<p>" + v + "</p>")
                if len(tex1) != 0 and self.txt.isChecked():
                    fo.write("\n*\n")
                elif len(tex1) != 0:
                    fo.write("<hr/>")
                if not self.txt.isChecked():
                    fo.write('''<blockquote>''')
                for m in tex1:
                    vv = re.sub('@无限好文，尽在晋江文学城', '', str(m))
                    v = re.sub('　', '', vv)
                    v = re.sub(' +', ' ', v).strip()
                    v = re.sub('&', '&amp;', v)
                    v = re.sub('>', '&gt;', v)
                    v = re.sub('<', '&lt;', v)
                    if self.state == 's':
                        v = OpenCC('t2s').convert(v)
                    elif self.state == 't':
                        v = OpenCC('s2t').convert(v)
                    if self.txt.isChecked():
                        v = re.sub('作者有话要说：', '作者有话要说：\n', v)
                    else:
                        v = re.sub('作者有话要说：', '<b>作者有话要说</b>：</p><p>', v)
                    if v != "" and self.txt.isChecked():  # 按行写入正文
                        fo.write(v + "\n")
                    elif v != "":
                        fo.write("<p>" + v + "</p>")
                if len(tex1) != 0 and not self.txt.isChecked():
                    fo.write("</blockquote>")
        if not self.txt.isChecked():
            fo.write("</body></html>")
        fo.close()
        self.percent += 1
        QApplication.processEvents()

    def get_txt(self, txt_id, threadnum):
        titlem = ''
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
        self.fontcss = ''
        self.fontlist = []
        self.textEdit.clear()
        section_ct = 9999

        # 获取文章网址
        req_url = ids

        # 通过cookie获取文章信息
        res = requests.get(req_url, headers=self.headerss).content
        # 对文章进行编码
        ress = etree.HTML(res.decode("GB18030", "ignore").encode("utf-8", "ignore").decode('utf-8'))

        # 获取文案
        if self.epub2s.isChecked() or self.epub3s.isChecked():
            intro = ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']")
        else:
            intro = ress.xpath("//html/body/table/tr/td[1]/div[2]/div[@id='novelintro']//text()")

        # 获取标签
        if self.epub2s.isChecked() or self.epub3s.isChecked():
            info = ress.xpath('//html/body/table[1]/tr[1]/td[1]/div[3]')
        else:
            info = ress.xpath("string(/html/body/table[1]/tr/td[1]/div[3])")

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
        self.setWindowTitle("正在下载："+xtitle + '-' + xaut)

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
                if self.txt.isChecked():
                    v = re.sub('</?\w+[^>]*>', '', v)
                else:
                    v = re.sub('<a.*?>', '', v)
                    v = re.sub('</a>', '', v)
                self.titleindex.append(v.strip())
                v = i.xpath('./td[3]')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                if self.txt.isChecked():
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
                if self.txt.isChecked():
                    v = re.sub('</?\w+[^>]*>', '', v)
                else:
                    v = re.sub('<a.*?>', '', v)
                    v = re.sub('</a>', '', v)
                self.titleindex.append(v.strip())
                v = i.xpath('./td[3]')
                v = etree.tostring(v[0], encoding="utf-8").decode().strip()
                if self.txt.isChecked():
                    v = re.sub('</?\w+[^>]*>', '', v)
                    v = re.sub('&#13;', '', v)
                else:
                    v = re.sub('<td>&#13;', '', v)
                    v = re.sub('<td>', '', v)
                    v = re.sub('</td>&#13;', '', v)
                    v = re.sub('</td>', '', v)
                self.Summary.append(v.strip())
            elif i.xpath('./td[2]/span/div[1]/span') != []:
                loc.append(i.xpath('./td[1]/text()')[0].strip())

        # 获取卷标名称
        self.rollSign = ress.xpath("//*[@id='oneboolt']//tr/td/b[@class='volumnfont']")
        # 获取卷标位置
        self.rollSignPlace = []
        # self.rollSignPlace+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
        # self.rollSignPlace+=ress.xpath("//*[@id='oneboolt']//tr/td/b/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")
        self.rollSignPlace += ress.xpath(
            "//*[@class='volumnfont']/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@href")
        self.rollSignPlace += ress.xpath(
            "//*[@class='volumnfont']/ancestor-or-self::tr/following-sibling::tr[1]/td[2]/span/div[1]/a[1]/@rel")

        # 修改卷标格式
        for rs in range(len(self.rollSign)):
            self.rollSign[rs] = etree.tostring(self.rollSign[rs], encoding="utf-8").decode().strip()
            if self.txt.isChecked():
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
            if self.txt.isChecked():
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
        if not os.path.exists('Fonts'):
            os.mkdir('Fonts')
        if os.path.exists(ti):
            os.chdir(ti)
        else:
            os.mkdir(ti)
            os.chdir(ti)
        ppp = os.getcwd()

        self.index = []
        # 保存封面图片
        if img != "0" and self.checkBox.isChecked() and not self.txt.isChecked():
            pic = open("p.jpg", 'wb')
            pic.write(img)
            pic.close()

            # 写入封面
            f = open("C.xhtml", 'w', encoding='utf-8')
            f.write('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Cover</title></head>
<body><div style="text-align: center; padding: 0pt; margin: 0pt;">
<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
<image width="100%" xlink:href="p.jpg"/></svg></div></body></html>''')
            f.close()

        # 写入文章信息页
        if self.txt.isChecked():
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
            if self.href_list[i] in self.rollSignPlace:
                v = self.rollSign[self.rollSignPlace.index(l)]
                if self.state == 's':
                    v = OpenCC('t2s').convert(self.rollSign[self.rollSignPlace.index(l)])
                elif self.state == 't':
                    v = OpenCC('s2t').convert(self.rollSign[self.rollSignPlace.index(l)])
                self.index.append(v)
            self.index.append(title)

        for ix in infox:
            ix = ix.strip()
            ix = re.sub('\n', '', ix)
            ix = re.sub(' +', '', ix)
            ix = re.sub('&', '&amp;', ix)
            ix = re.sub('>', '&gt;', ix)
            ix = re.sub('<', '&lt;', ix)
            if self.txt.isChecked():
                TOC += ix + "\n"
            else:
                TOC += "<p>" + ix + "</p>"
        if self.txt.isChecked():
            TOC += "文案：\n"
        else:
            TOC += "</blockquote>"
            TOC += "<hr/><p><b>文案：</b></p>"
        if self.epub2s.isChecked() or self.epub3s.isChecked():
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
                if v != "" and self.txt.isChecked():
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
        if self.txt.isChecked():
            info = re.sub('搜索关键字', '\n搜索关键字', info)
            info = re.sub(' +一句话简介：', '\n一句话简介：', info)
            info = re.sub('\n +\n +立意：', '\n立意：', info)
            TOC += info
            fo = open("info.txt", 'w', encoding='utf-8')
            fo.write(TOC.strip() + '\n')
            fo.write(lockinfo.strip() + '\n')
            fo.close()
        else:
            if self.epub2s.isChecked() or self.epub3s.isChecked():
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
            fo = open("info.xhtml", 'w', encoding='utf-8')
            fo.write('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title></title><meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/></head>
<body>''' + TOC + lockinfo + '''</body></html>''')
            fo.close()
        tlist = []
        # 获取每一章内容

        with concurrent.futures.ThreadPoolExecutor(max_workers=threadnum) as executor:
            tlist = {executor.submit(self.get_sin, i): i for i in self.href_list}
            for future in concurrent.futures.as_completed(tlist):
                if self.percent < section_ct:
                    self.progressBar.setValue(int(100 * self.percent / section_ct))
                    self.progressBar.update()
                    self.pct.setText(str(self.percent) + '/' + str(section_ct))
                    self.setWindowTitle("正在下载：" + xtitle + '-' + xaut+" ("+self.pct.text()+")")
                    QApplication.processEvents()
            self.progressBar.setValue(int(100 * self.percent / section_ct))
            self.progressBar.update()
            self.textEdit.append('\n 下载完成，总进度：' + str(self.percent) + '/' + str(section_ct))
            self.textEdit.moveCursor(self.textEdit.textCursor().End)
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
        if self.txt.isChecked():
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
            if self.epub2.isChecked() or self.epub2s.isChecked():
                epubfile = EPUB2.epubfile()
            else:
                epubfile = EPUB3.epubfile()
            epubfile.fontcss = self.fontcss
            epubfile.createEpub(epub, xaut, xtitle, ti, self.index, self.rollSign, path)
            self.textEdit.append("\nepub打包完成")
            self.textEdit.moveCursor(self.textEdit.textCursor().End)
        self.setWindowTitle("下载完成：" + xtitle + '-' + xaut + " (" + self.pct.text() + ")")
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
