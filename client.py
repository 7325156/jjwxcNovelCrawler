from selenium import webdriver
import time

#此处需要安装chormedriver ，并存放到python路径下
driver=webdriver.Chrome()

driver.delete_all_cookies()
driver.get("http://my.jjwxc.net/login.php")



username=input("请输入用户名：")
passwd=input("请输入密码：")
driver.find_element_by_id("loginname").send_keys(username)
driver.find_element_by_id("loginpassword").send_keys(passwd)
driver.find_element_by_xpath("//*[@id='login_submit_tr']/input").click()

cookies = driver.get_cookies()
cookies_list= []
for cookie_dict in cookies:
     cookie =cookie_dict['name']+'='+cookie_dict['value']
     cookies_list.append(cookie)
header_cookie = ';'.join(cookies_list)
   
headers = {
    'cookie':header_cookie,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

print(headers)

driver.quit()


