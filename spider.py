# -*- coding:utf-8 -*-
# 导包
import time
from selenium import webdriver
import pymysql
from selenium.webdriver.common.keys import Keys

class doubanwlwz_spider():
    def __init__(self):
        # 创建chrome参数对象
        opt = webdriver.ChromeOptions()
        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-gpu')
        opt.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        opt.add_argument('--headless') #浏览器不提供可视化页面. 
        # 用的是谷歌浏览器
        driver = webdriver.Chrome('/data/chromedriver',options=opt)
       
#        driver=webdriver.Chrome('/data/chromedriver')
        self.getInfo(driver)

    def writeMysql(self,userName,userConment,userLocation):
        # 打开数据库连接
        db = pymysql.connect("123.207.35.161", "zhangfan", "N$nIpms1", "hupo_test")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        sql = "insert into userinfo(username,commont,location) values(%s, %s, %s)"
        cursor.execute(sql, [userName, userConment, userLocation])
        db.commit()
        # 关闭数据库连接
        cursor.close()
        db.close()

    def getInfo(self,driver):
    # 切换到登录框架中来
    # 登录豆瓣网
        driver = driver
        driver.get("http://www.douban.com/")
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
        # 点击"密码登录"
        bottom1 = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
        bottom1.click()
        # # 输入密码账号
        input1 = driver.find_element_by_xpath('//*[@id="username"]')
        input1.clear()
        input1.send_keys("18111577822")

        input2 = driver.find_element_by_xpath('//*[@id="password"]')
        input2.clear()
        input2.send_keys("zf13696270344")

        # 登录
        bottom = driver.find_element_by_class_name('account-form-field-submit ')
        bottom.click()

        time.sleep(1)
        #获取全部评论 一共有480页，每个页面20个评论

        for i in range(1, 25):
            driver.get('https://movie.douban.com/subject/3882715/comments?start={}&limit=20&sort=new_score'.format(i*20))
            print("开始抓取第%i页面"%(i))
            search_window = driver.current_window_handle
            # pageSource=driver.page_source
            # print(pageSource)
            #获取用户的名字 每页20个
            for i in range(1,21):
                userName=driver.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a'.format(str(i))).text
                print("用户的名字是:  %s"%(userName))
         #  获取用户的评论
            # print(driver.find_element_by_xpath('//*[@id="comments"]/div[1]/div[2]/p/span').text)
                userConment=driver.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/p/span'.format(str(i))).text
                print("用户的评论是:  %s"%(userConment))
        #获取用户的url然后点击url获取居住地
                userInfo=driver.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a'.format(str(i))).get_attribute('href')
                driver.get(userInfo)
                try:
                    userLocation = driver.find_element_by_xpath('//*[@id="profile"]/div/div[2]/div[1]/div/a').text
                    print("用户的居之地是  %s"%(userLocation))
                except Exception as e:
                    userLocation='NUll'
                self.writeMysql(userName,userConment,userLocation)
                driver.back()

AAA=doubanwlwz_spider()
