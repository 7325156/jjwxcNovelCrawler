import requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil
class epubfile():
    #创建epub文件格式信息
    author=''
    title=''
    description=''
    TOC=''
    path=''
    def create_mimetype(self,epub):
        epub.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
     
    def create_container(self,epub):
        container_info = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
</rootfiles></container>'''
        epub.writestr('META-INF/container.xml',container_info, compress_type=zipfile.ZIP_STORED)
     
    def create_content(self,epub,path):
        content_info = '''<?xml version="1.0" encoding="utf-8"?>
<package version="3.0" unique-identifier="BookId" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'''
        if self.title!='':
            content_info+="<dc:title>"+self.title+"</dc:title>"
        if self.author!='':
            content_info+="<dc:creator>"+self.author+"</dc:creator>"
        if self.description!='':
            content_info+="<dc:description>"+self.description+"</dc:description>"
        content_info+='''<meta name="cover" content="p.jpg" />
</metadata><manifest>
<item id="sgc-nav.css" href="sgc-nav.css" media-type="text/css"/>
<item id="TOC.xhtml" href="TOC.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="p.jpg" href="p.jpg" media-type="image/jpeg" properties="cover-image"/>
%(manifest)s
</manifest><spine>
<itemref idref="C.xhtml" />
<itemref idref="TOC.xhtml" />
%(spine)s
</spine></package>'''
        manifest = ''
        spine = ''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (basename, basename)
                if basename != 'C.xhtml':
                    spine += '<itemref idref="%s"/>' % (basename)
        epub.writestr('OEBPS/content.opf',content_info % {'manifest': manifest,'spine': spine,},compress_type=zipfile.ZIP_STORED)

    def create_info(self,epub,path,index,rollSign):
        nav_info='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head><title></title>
<meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>'''+self.TOC+'''
<nav epub:type="toc" id="toc"><h1>目录</h1>
    <ol>
    '''
        sig=0
        nav_info+='''<li><a href="TOC.xhtml">'''+self.title+'-'+self.author+'''</a>
<ol>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename!='C.xhtml' and basename!='TOC.xhtml':
                    iii=0
                    while index[sig] in rollSign:
                        nav_info+='''</ol></li>
<li><a href="'''+basename+'''">
'''+index[sig]+'''</a>
<ol>'''
                        sig+=1
                        iii=1
                    if iii==1:
                        basename+='#v'
                    nav_info+='''<li><a href="'''+basename+'''">'''+index[sig]+'''</a></li>
'''
                    sig+=1
        nav_info+='''</ol></li></ol></nav></body></html>'''
        epub.writestr('OEBPS/TOC.xhtml',nav_info,compress_type=zipfile.ZIP_STORED)
 
        
    def create_stylesheet(self,epub):
        css_info = '''nav#landmarks {
    display:none;
}

nav#page-list {
    display:none;
}

ol {
    list-style-type: none;
}
h1{
font-size:1.4em;
}
h2{
font-size:1.2em;
}
.title{
text-align:center;
}
'''
        epub.writestr('OEBPS/sgc-nav.css',css_info,compress_type=zipfile.ZIP_STORED)

