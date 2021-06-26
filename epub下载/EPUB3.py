path.basename(html)
            if basename.endswith('html'):
                manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (basename, basename)
                if basename != 'C.xhtml' and basename != 'info.xhtml':
                    spine += '<itemref idref="%s"/>' % (basename)
        spine+='''<guide>
    <reference type="cover" title="封面" href="C.xhtml"/>
  </guide>'''
        epub.writestr('OEBPS/content.opf',content_info % {'manifest': manifest,'spine': spine,},compress_type=zipfile.ZIP_STORED)

    def create_info(self,epub,path,index,rollSign):
        nav_info='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head><title></title>
<meta charset="utf-8"/>
<link href="sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<nav epub:type="toc" id="toc"><h1>目录</h1>
    <ol>
    '''
        sig=0
        nav_info+='''<li><a href="info.xhtml">'''+self.title+'-'+self.author+'''</a>
<ol>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename!='C.xhtml' and basename!='info.xhtml':
                    iii=0
                    while index[sig] in rollSign:
                        index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                        nav_info+='''</ol></li>
<li><a href="'''+basename+'''">
'''+index[sig]+'''</a>
<ol>'''
                        sig+=1
                        iii=1
                    if iii==1:
                        basename+='#v'
                    index[sig]=re.sub('</?\w+[^>]*>','',index[sig])
                    nav_info+='''<li><a href="'''+basename+'''">'''+index[sig]+'''</a></li>
'''
                    sig+=1
        nav_info+='''</ol></li></ol></nav></body></html>'''
        epub.writestr('OEBPS/nav.xhtml',nav_info,compress_type=zipfile.ZIP_STORED)
    def create_toc(self,epub,path,index,rollSign):
        tox_info='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="" />
    <meta name="dtb:depth" content="2" />
    <meta name="dtb:totalPageCount" content="0" />
    <meta name="dtb:maxPageNumber" content="0" />
</head><docTitle><text>'''+self.title+'''</text></docTitle><navMap>'''
        sig=0
        tox_info+='''<navPoint id="0" playOrder="0">
<navLabel><text>'''+self.title+'''</text></navLabel><content src="info.xhtml"/>'''
        for html in os.listdir(path):
            basename = os.path.basename(html)
            if basename.endswith('html'):
                if basename!='C.xhtml' and basename!='info.xhtml' and sig<len(index):
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
        css_info = '''nav#landmarks {
    display:none;
}

nav#page-list {
    display:none;
}

ol {
    list-style-type: none;
}
h1{font-size:1.4em;text-align:center;}h2{font-size:1.24em;text-align:center;}
.title{
text-align:center;
}
'''+self.fontcss
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
        self.create_toc(epub,ppp,index,rollSign)
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
