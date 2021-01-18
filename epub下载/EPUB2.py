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
<package version="2.0" unique-identifier="uuid_id" xmlns="http://www.idpf.org/2007/opf">
<metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>'''+self.title+'''</dc:title>
<dc:creator>'''+self.author+'''</dc:creator>
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
            if basename.endswith('html')|basename.endswith('jpg'):
                spine += '<itemref idref="%s"/>' % (basename)
        epub.writestr('OEBPS/content.opf',content_info % {'manifest': manifest,'spine': spine,},compress_type=zipfile.ZIP_STORED)

    def create_info(self,epub,path,index,rollSign):
        tox_info='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content=""/>
<meta name="dtb:depth" content="2"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head><docTitle><text>'''+self.title+'''</text></docTitle><navMap>'''
        sig=0
        tox_info+='''<navPoint id="0" playOrder="0">
<navLabel><text>'''+self.title+'''</text></navLabel><content src="TOC.xhtml"/>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename!='C.xhtml' and basename!='TOC.xhtml':
                    iii=0
                    while index[sig] in rollSign:
                        index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                        tox_info+='''</navPoint><navPoint id="'''+str(sig)+'''" playOrder="'''+str(sig)+'''">
<navLabel><text>'''+index[sig]+'''</text></navLabel><content src="'''+basename+'''"/>'''
                        sig+=1
                        iii=1
                    if iii==1:
                        basename+='#v'
                    index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                    tox_info+='''<navPoint id="'''+str(sig)+'''" playOrder="'''+str(sig)+'''">
<navLabel><text>'''+index[sig]+'''</text></navLabel><content src="'''+basename+'''"/></navPoint>'''
                    sig+=1
        tox_info+='''</navPoint></navMap></ncx>'''
        epub.writestr('OEBPS/toc.ncx',tox_info,compress_type=zipfile.ZIP_STORED)
 
        
    def create_stylesheet(self,epub):
        css_info = '''h1{font-size:1.4em;text-align:center;}h2{font-size:1.24em;text-align:center;}
.title{
text-align:center;
}
@font-face{font-family: 'jjwxcfont_0004v';src:url('../font/jjwxcfont_0004v.woff2') format('woff2'),url('../font/jjwxcfont_0004v.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_00070';src:url('../font/jjwxcfont_00070.woff2') format('woff2'),url('../font/jjwxcfont_00070.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_00091';src:url('../font/jjwxcfont_00091.woff2') format('woff2'),url('../font/jjwxcfont_00091.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000bl';src:url('../font/jjwxcfont_000bl.woff2') format('woff2'),url('../font/jjwxcfont_000bl.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000dz';src:url('../font/jjwxcfont_000dz.woff2') format('woff2'),url('../font/jjwxcfont_000dz.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000ib';src:url('../font/jjwxcfont_000ib.woff2') format('woff2'),url('../font/jjwxcfont_000ib.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000m4';src:url('../font/jjwxcfont_000m4.woff2') format('woff2'),url('../font/jjwxcfont_000m4.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000mn';src:url('../font/jjwxcfont_000mn.woff2') format('woff2'),url('../font/jjwxcfont_000mn.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000qt';src:url('../font/jjwxcfont_000qt.woff2') format('woff2'),url('../font/jjwxcfont_000qt.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000t5';src:url('../font/jjwxcfont_000t5.woff2') format('woff2'),url('../font/jjwxcfont_000t5.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000wi';src:url('../font/jjwxcfont_000wi.woff2') format('woff2'),url('../font/jjwxcfont_000wi.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_000xw';src:url('../font/jjwxcfont_000xw.woff2') format('woff2'),url('../font/jjwxcfont_000xw.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_0012a';src:url('../font/jjwxcfont_0012a.woff2') format('woff2'),url('../font/jjwxcfont_0012a.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_00147';src:url('../font/jjwxcfont_00147.woff2') format('woff2'),url('../font/jjwxcfont_00147.ttf') format('truetype');}
@font-face{font-family: 'jjwxcfont_0015q';src:url('../font/jjwxcfont_0015q.woff2') format('woff2'),url('../font/jjwxcfont_0015q.ttf') format('truetype');}
.jjwxcfont_0004v{font-family:"jjwxcfont_0004v",serif;}
.jjwxcfont_00070{font-family:"jjwxcfont_00070",serif;}
.jjwxcfont_00091{font-family:"jjwxcfont_00091",serif;}
.jjwxcfont_000bl{font-family:"jjwxcfont_000bl",serif;}
.jjwxcfont_000dz{font-family:"jjwxcfont_000dz",serif;}
.jjwxcfont_000ib{font-family:"jjwxcfont_000ib",serif;}
.jjwxcfont_000m4{font-family:"jjwxcfont_000m4",serif;}
.jjwxcfont_000mn{font-family:"jjwxcfont_000mn",serif;}
.jjwxcfont_000qt{font-family:"jjwxcfont_000qt",serif;}
.jjwxcfont_000t5{font-family:"jjwxcfont_000t5",serif;}
.jjwxcfont_000wi{font-family:"jjwxcfont_000wi",serif;}
.jjwxcfont_000xw{font-family:"jjwxcfont_000xw",serif;}
.jjwxcfont_0012a{font-family:"jjwxcfont_0012a",serif;}
.jjwxcfont_00147{font-family:"jjwxcfont_00147",serif;}
.jjwxcfont_0015q{font-family:"jjwxcfont_0015q",serif;}
'''
        epub.writestr('OEBPS/sgc-nav.css',css_info,compress_type=zipfile.ZIP_STORED)
    def createEpub(self,epub,xaut,xtitle,ti,index,rollSign,path):
        self.author=xaut
        self.title=xtitle
        self.create_mimetype(epub)     
        self.create_container(epub)  
        os.chdir(ti)
        ppp=os.getcwd()
        self.create_content(epub,ppp)
        self.create_info(epub,ppp,index,rollSign)
        self.create_stylesheet(epub)
        for html in os.listdir('.'):
            basename = os.path.basename(html)
            if basename.endswith('jpg'):
                epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
            if basename.endswith('html'):
                epub.write(html, "OEBPS/"+basename, compress_type=zipfile.ZIP_DEFLATED)
        epub.close()
        os.chdir(path)
        shutil.rmtree(ppp)
