class configinfo():
    #输入cookie，例如：cookie='12qhfu3eibzcd...'
    cookie=''
    
    #繁简转换标志：繁转简（输入s）；简转繁（输入t）；不变（不输入），例如：state='s'
    state=''
    
    '''
    标题保存状态(序号 章节名称 内容提要)
    显示则输入1，不显示则输入0，数字之间用空格隔开
    例如：若只显示序号和内容提要，则输入'1 0 1'
    '''
    titleInfo='1 1 1'
        
    #线程池最大容量
    ThreadPoolMaxNum=100
