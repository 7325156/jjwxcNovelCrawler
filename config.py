class configinfo():
    #输入cookie，例如：cookie='12qhfu3eibzcd...'
    cookie='CNZZDATA30075907=cnzz_eid%3D1630076582-1610849236-http%253A%252F%252Fwww.jjwxc.net%252F%26ntime%3D1629707265; timeOffset_o=536.699951171875; smidV2=2021020523525895c40cb64e2ebc10e61c92bae31ccb8e00880dd4f17c44b40; testcookie=yes; Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1630071429,1630251143,1630543467,1630757902; token=MjAwNzA4OTB8ZTE1YjEyODcxNDJmMmE5OWViYzAzNjgzODdlNzA1OTR8fHwxODMxMjQ3fDI1OTIwMDB8MXzmupDliJ3kuYvngat8fOaZi%2Baxn%2BeUqOaIt3wwfGF1dGhvcm5hbWV8MQ%3D%3D; JJEVER=%7B%22sms_total%22%3A%220%22%2C%22user_signin_days%22%3A%2220210904_20070890_0%22%2C%22desid%22%3A%22XueBhNl4x%2Bgkux41k9s4riM66UOKWXWc%22%2C%22background%22%3A%22%22%2C%22font_size%22%3A%22%22%2C%22isKindle%22%3A%22%22%2C%22fenzhan%22%3A%22by%22%2C%22ispayuser%22%3A%2220070890-1%22%2C%22foreverreader%22%3A%2220070890%22%2C%22nicknameAndsign%22%3A%222%257E%2529%2524%25E9%2587%2591%25E7%259F%25B3%25E4%25B9%258B%25E8%25AA%2593%22%2C%22lastCheckLoginTimePc%22%3A%221630757958%22%2C%22lastCheckLoginTimeWap%22%3A%221630747806%22%7D; JJSESS=%7B%22returnUrl%22%3A%22http%3A//www.jjwxc.net/%22%2C%22clicktype%22%3A%22%22%7D; Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1630758258'

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
