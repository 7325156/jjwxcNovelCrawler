from fontTools.ttLib import TTFont
import os
import re
import concurrent.futures

global nnn
nnn=''
def convertXML(name):
    font = TTFont(name+'.woff2')
    font.saveXML(name+'.xml')
    font.close()
def createLIST(name):
    tlist=[]
    print(name)
    with open(name+'.xml','r') as f:
        c=f.readlines()
        for l in c:
            y=re.search(r'GlyphID.*?uni....',l)
            if not y==None:
                y=re.sub(r'GlyphID id.*?name..uni','&#x',y.group())
                y=y+';-'
                tlist.append(y)
    fo=open(name+'.empty.txt','w',encoding='utf-8')
    for y in tlist:
        fo.write(y+'\n')
    fo.close()
    
def conf(name):
    if name.endswith('woff2'):
        name=re.sub('.woff2','',name)
        nnn=name
        if not os.path.exists(name+'.xml'):
            convertXML(name)
        if not os.path.exists(name+'.empty.txt'):
            createLIST(name)

if __name__ == '__main__':
    list=os.listdir()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        tlist = {executor.submit(conf,i):i for i in list}
        concurrent.futures.as_completed(tlist)
