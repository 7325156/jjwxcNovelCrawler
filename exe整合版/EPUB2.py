import requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil


class epubfile():
    # 创建epub文件格式信息
    author = ''
    title = ''
    description = ''
    TOC = ''
    csstext = ''
    htmlvol = 0

    def create_vol(self, epub, path, index, rollSign):
        nav_info = '''<?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
    <head><title></title>
    <meta charset="utf-8"/>
    <link href="sgc-nav.css" rel="stylesheet" type="text/css"/>
    </head>
    <body>
    <nav epub:type="toc" id="toc" role="doc-toc"><h1>目录</h1>
        <ol>
        '''
        sig = 0
        sigr = 0
        nav_info += '''<li><a href="info.xhtml">''' + self.title + '-' + self.author + '''</a>
    <ol>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename != 'C.xhtml' and basename != 'info.xhtml':
                    if sig < len(index) or sigr < len(rollSign):
                        if "vol" in basename:
                            # rollSign[sigr] = re.sub('</?\w+[^>]*>', '', rollSign[sigr])
                            nav_info += '''</ol></li>
        <li><a href="''' + basename + '''">
        ''' + rollSign[sigr] + '''</a>
        <ol>'''
                            sigr += 1
                        else:
                            # index[sig] = re.sub('</?\w+[^>]*>', '', index[sig])
                            nav_info += '''<li><a href="''' + basename + '''">''' + index[sig] + '''</a></li>
        '''
                            sig += 1
        nav_info += '''</ol></li></ol></nav></body></html>'''
        epub.writestr('OEBPS/nav.xhtml', nav_info, compress_type=zipfile.ZIP_STORED)

    def create_mimetype(self, epub):
        epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)

    def create_container(self, epub):
        container_info = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
</rootfiles></container>'''
        epub.writestr('META-INF/container.xml', container_info, compress_type=zipfile.ZIP_STORED)

    def create_content(self, epub, path):
        content_info = '''<?xml version="1.0" encoding="utf-8"?>
<package version="2.0" unique-identifier="uuid_id" xmlns="http://www.idpf.org/2007/opf">
<metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>''' + self.title + '''</dc:title>
<dc:creator>''' + self.author + '''</dc:creator>
<meta name="cover" content="p.jpg" />
</metadata><manifest>
%(manifest)s <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
<item id="content" href="content.html" media-type="application/xhtml+xml"/>
<item id="css" href="sgc-nav.css" media-type="text/css"/>
</manifest><spine toc="ncx"> %(spine)s <itemref idref="cover" linear="no"/>
<itemref idref="content"/></spine></package>'''
        manifest = ''
        spine = ''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (basename, basename)
            if basename.endswith('jpg'):
                manifest += '<item id="%s" href="%s" media-type="image/jpeg"/>' % (basename, basename)
            if basename.endswith('html') | basename.endswith('jpg'):
                spine += '<itemref idref="%s"/>' % (basename)
        spine += '''<guide>
    <reference type="cover" title="封面" href="C.xhtml"/>
  </guide>'''
        if self.htmlvol:
            manifest += '<item id="nav.xhtml" href="nav.xhtml" media-type="application/xhtml+xml"/>'
            spine += '<itemref idref="nav.xhtml"/>'
        epub.writestr('OEBPS/content.opf', content_info % {'manifest': manifest, 'spine': spine, },
                      compress_type=zipfile.ZIP_STORED)

    def create_info(self, epub, path, index, rollSign):
        tox_info = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="" />
<meta name="dtb:depth" content="2" />
<meta name="dtb:totalPageCount" content="0" />
<meta name="dtb:maxPageNumber" content="0" />
</head><docTitle><text>''' + self.title + '''</text></docTitle><navMap>'''
        sig = 0
        sigr = 0
        count = 0
        tox_info += '''<navPoint id="0" playOrder="0">
            <navLabel><text>''' + self.title + '-' + self.author + '''</text></navLabel><content src="info.xhtml"/>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename != 'C.xhtml' and basename != 'info.xhtml':
                    iii = 0
                    if sig < len(index) or sigr < len(rollSign):
                        if "vol" in basename:
                            rollSign[sigr] = re.sub('</?\w+[^>]*>', '', rollSign[sigr])
                            tox_info += '''</navPoint><navPoint id="''' + str(count) + '''" playOrder="''' + str(
                                count) + '''">
                <navLabel><text>''' + rollSign[sigr] + '''</text></navLabel><content src="''' + basename + '''"/>'''
                            sigr += 1
                            count += 1
                        else:
                            index[sig] = re.sub('</?\w+[^>]*>', '', index[sig])
                            tox_info += '''<navPoint id="''' + str(count) + '''" playOrder="''' + str(count) + '''">
                                            <navLabel><text>''' + index[
                                sig] + '''</text></navLabel><content src="''' + basename + '''"/></navPoint>'''
                            sig += 1
                            count += 1
        tox_info += '''</navPoint></navMap></ncx>'''
        epub.writestr('OEBPS/toc.ncx', tox_info, compress_type=zipfile.ZIP_STORED)

    def create_stylesheet(self, epub):
        css_info = self.csstext
        epub.writestr('OEBPS/sgc-nav.css', css_info, compress_type=zipfile.ZIP_STORED)

    def createEpub(self, epub, xaut, xtitle, ti, index, rollSign, path):
        self.author = xaut
        self.title = xtitle
        self.create_mimetype(epub)
        self.create_container(epub)
        os.chdir(ti)
        ppp = os.getcwd()
        if self.htmlvol:
            self.create_vol(epub, ppp, index, rollSign)
        self.create_content(epub, ppp)
        self.create_info(epub, ppp, index, rollSign)
        self.create_stylesheet(epub)
        for html in os.listdir('.'):
            basename = os.path.basename(html)
            if basename.endswith('jpg'):
                epub.write(html, "OEBPS/" + basename, compress_type=zipfile.ZIP_DEFLATED)
            if basename.endswith('html'):
                epub.write(html, "OEBPS/" + basename, compress_type=zipfile.ZIP_DEFLATED)
        epub.close()
        os.chdir(path)
        shutil.rmtree(ppp)
