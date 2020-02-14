import  requests
from lxml import etree
import sys
import re
import os
import zipfile
import shutil
class epubfile():
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
            if basename.endswith('html'):
                manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (basename, basename) 
            if basename.endswith('jpg'):
                manifest += '<item id="%s" href="%s" media-type="image/jpeg"/>' % (basename, basename)
            if basename.endswith('html')|basename.endswith('jpg'):
                spine += '<itemref idref="%s"/>' % (basename)
        epub.writestr('OEBPS/content.opf',content_info % {'manifest': manifest,'spine': spine,},compress_type=zipfile.ZIP_STORED)

    def create_tox(epub,path,index,rollSign):
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
                    while index[sig] in rollSign:
                        if index[sig]==rollSign[0]:
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
    
