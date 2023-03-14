import time
import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from pymysql import Error

from lxml import html

etree = html.etree
sleep = time.sleep


class CsgoSkins():

    def __init__(self):
        while True:
            print("输入1查询buff\n输入2查询uu(未完成)")
            self.__id = input()
            if self.__id == '1':
                self.__url = 'https://buff.163.com/'
                break
            elif self.__id == '2':
                self.__url = 'https://www.youpin898.com/'
                break
        print(self.__url)

    # 基础函数列表：
    # --cursor()：建立和mysql联系，返回cursor
    # --mysql_Insert(): 获得数据后在mysql中建表并插入数据
    # --buff_login_using_verification_code(): 验证码登录
    # --buff_login_using_keyword(): 密码登录
    # --actionchains_detector(): 通过拖动图像的验证码（未完成）

    def __cursor(self,db_name):
        global db
        db = pymysql.connect(host='localhost', user='root', password='33455433', port=3306, db=f'{db_name}',charset='utf8')
        cursor = db.cursor()
        return cursor

    def __dr_all(self,db_name):
        cursor = self.__cursor(db_name)
        sql = "CALL DupRemove_All()"
        cursor.execute(sql)
        db.commit()

    def __mysql_insert(self,name,skin_float_type,data,db_name,stock):  # data格式[skin_name,prices,stock]
        cursor = self.__cursor(db_name)
        sql = f"CALL CreateNewTable('{name}')"
        cursor.execute(sql)
        sql = f"""
            INSERT INTO {name}
            (
                skin_name,
                skin_float_type,
                skin_float,
                prices,
                store_name,
                stock,
                date
            ) 
            VALUES("{name}","{skin_float_type}",%s,%s,%s,"{stock}",CURRENT_DATE())
        """
        cursor.executemany(sql,data)
        db.commit()

    def __actionchains_detector(self):    #滑块验证码识别处理
        img_url = '//*[@class="yidun_bgimg"]/img[1]/@src'
        pass

    def __skin_name(self,skin_name):
        if len(skin_name) > 7:
            skin_float_type = skin_name[-5:-1]
            skin_name = skin_name[:-7]
            skin_name = skin_name.replace('（★ StatTrak™）', '_暗金')
            skin_name = skin_name.replace("（★）", "")
            skin_name = skin_name.replace(" | ", "_")
            skin_name = skin_name.replace(" ", "_")
        else:
            skin_float_type = '原版'
            skin_name = skin_name[:-3]
        return [skin_name,skin_float_type]

    def __buff_login_using_verification_code(self,account,wait):
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="pcbtn f-fl"]')))
        account_number = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="phoneipt"]')))  # 账号输入定位
        account_key = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="u-input"]/input')))  # 验证码输入定位
        account_enter = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="f-cb loginbox"]/a')))  # 确定登录按钮
        account_number.send_keys(account)
        print("请拖动验证码，完成后输入ok")  # 处理滑动验证码（暂时）
        input()
        key_poster = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="pcbtn f-fl"]')))  # 获取验证码
        key_poster.click()
        print("请输入验证码")
        account_key.send_keys(input())
        account_enter.click()

    def __buff_login_using_keyword(self,account,keyword,wait):
        keyword_enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="tab0"]')))
        keyword_enter_button.click()
        account_number = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="phoneipt"]')))
        account_key = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="j-inputtext dlemail"]')))
        account_enter = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitBtn"]')))
        account_number.send_keys(account)
        account_key.send_keys(keyword)
        print("请拖动验证码，完成后输入ok")  # 处理滑动验证码（暂时）
        input()
        account_enter.click()

    def __uu_login_using_verification_code(self,account,wait):
        account_number = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/span[1]/input')))
        account_key = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/span[2]/span/input')))
        key_poster = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/span[2]/span/span/button')))
        account_number.send_keys(account)
        key_poster.click()
        print("请输入验证码")
        account_key.send_keys(input())
        account_enter = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/button')))
        account_enter.click()

    def __uu_login_using_keyword(self,account,keyword,wait):
        keyword_enter_button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/div[2]/span[1]')))
        keyword_enter_button.click()
        account_number = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/span[1]/input')))
        account_key = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/input')))
        account_enter = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/div/button')))
        account_number.send_keys(account)
        account_key.send_keys(keyword)
        account_enter.click()




    def skin_data_collector(self):
        start = time.perf_counter()
        bro = webdriver.Edge()
        wait = WebDriverWait(bro,10)
        bro.get(url=self.__url)
        sleep(1)

        if self.__id == '1':
            db_name = 'csgo_skins_buff'
            account_enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[3]/ul/li/a')))  # 进入登录界面
            account_enter_button.click()

            account_sure = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="agree-checkbox"]/span/i')))  # 同意用户协议
            account_sure.click()
            bro.switch_to.frame('')  # 切换至登录界面
            print("请输入手机账号")
            account = '18896938962'

            print("验证码登录输入1\n密码登录输入2")
            key = input()
            if key == '1':
                self.__buff_login_using_verification_code(account,wait)
            elif key == '2':
                print("请输入密码")
                keyword = '334554331035Ab'
                self.__buff_login_using_keyword(account,keyword,wait)
            bro.switch_to.default_content()                                                             #切换至原页面

            print("输入最小库存")    #库存数量
            stock_num = int(input())

            sleep(5)
            csgo_button = bro.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/ul/li[2]/a')
            csgo_button.click()
            sleep(0.5)
            knife_button = bro.find_element(By.XPATH, '//*[@id="j_h1z1-selType"]/div[1]/p')
            knife_button.click()
            sleep(1)
            page_num = 1

            while True:   #while True:  检测不到//*[@id="j_market_card"]/div[2]/ul/li[last()]/a  (下一页按钮)节点后停止
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="j_market_card"]/div[2]/ul/li[last()]/a')))
                    print(f"第{page_num}页")
                    sleep(1)
                    page_source = bro.page_source
                    tree = etree.HTML(page_source)
                    for num in range(1,21):
                        wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="j_list_card"]/ul/li[{num}]/p/span')))
                        stock = tree.xpath(f'//*[@id="j_list_card"]/ul/li[{num}]/p/span/text()')[0]
                        stock = stock.strip()
                        stock = stock[:-3]
                        if stock == '1000+':
                            stock = 9999
                        else:
                            stock = int(stock)
                        if stock >= stock_num:
                            wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="j_list_card"]/ul/li[{num}]/h3/a')))
                            skin_name = tree.xpath(f'//*[@id="j_list_card"]/ul/li[{num}]/h3/a/text()')[0]
                            skin_name,skin_float_type = self.__skin_name(skin_name)

                            # 进入详情页
                            wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="j_list_card"]/ul/li[{num}]/h3/a')))
                            detailed_info_url = 'https://buff.163.com' + tree.xpath(f'//*[@id="j_list_card"]/ul/li[{num}]/h3/a/@href')[0]
                            bro.execute_script('window.open()')
                            bro.switch_to.window(bro.window_handles[1])
                            bro.get(detailed_info_url)
                            wait = WebDriverWait(bro,10)

                            #加载页面代码
                            button0 = 1
                            while button0 == 1:
                                try:
                                    wait.until(EC.presence_of_element_located((By.XPATH,'//*[contains(@class,"selling")]/td[4]/a')))
                                    button0 = 0
                                except WebDriverException:
                                    button0 += 1
                                    bro.refresh()
                                    if button0 > 3:
                                        print("网络异常")
                                        return


                            detailed_page_source = bro.page_source
                            detailed_tree = etree.HTML(detailed_page_source)

                            # 获取磨损
                            button1 = 1
                            while button1 == 1:
                                try:
                                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"selling")]/td[3]/div/div[1]/div[1]')))
                                    button1 = 0
                                except WebDriverException:
                                    button1 += 1
                                    bro.refresh()
                                    if button1 > 3:
                                        print("网络异常")
                                        return
                            skin_float = detailed_tree.xpath('//*[@class="selling"]/td[3]/div/div[1]/div[1]/text()')
                            skin_float = [float(i[3:]) for i in skin_float]

                            # 获取价格
                            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"selling")]/td[5]/div[1]/strong')))
                            prices = detailed_tree.xpath('//*[@class="selling"]/td[5]/div[1]/strong/text()')
                            prices = [int(i[2:]) for i in prices]

                            # 获取商店名
                            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"selling")]/td[4]/a')))
                            store_name = detailed_tree.xpath('//*[contains(@class,"selling")]/td[4]/a/text()')
                            store_name = [i.strip() for i in store_name]
                            store_name = [i for i in store_name if i]


                            data = list(zip(skin_float,prices,store_name))
                            print(skin_name)
                            print(data)
                            bro.close()
                            bro.switch_to.window(bro.window_handles[0])

                            try:
                                self.__mysql_insert(skin_name,skin_float_type, data, db_name, stock)
                                print("成功")
                            except Error:
                                print("出现问题")
                                continue

                    next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_market_card"]/div[2]/ul/li[last()]/a')))  # 下一页按钮
                    next_page.click()
                    page_num += 1
                    sleep(1)
                except WebDriverException:
                    break

        elif self.__id == '2':
            db_name = 'csgo_skins_uu'
            account_enter_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/div/div[1]')))
            account_enter_button.click()

            print("请输入手机账号")
            account = '15984879717'

            print("验证码登录输入1\n密码登录输入2")
            key = input()
            if key == '1':
                self.__uu_login_using_verification_code(account,wait)
            elif key == '2':
                print("请输入密码")
                keyword = '334554331035gao'
                self.__uu_login_using_keyword(account,keyword,wait)

            bro.maximize_window()
            csgo_enter = bro.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/ul/li[3]/a/span')
            csgo_enter.click()

            mouse = ActionChains(bro)
            knife_location = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__layout"]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[1]')))
            mouse.move_to_element(knife_location).perform()
            knife_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__layout"]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/ul/li[1]')))
            knife_button.click()

            print("租赁市场查询输入1\n交易市场查询输入2")
            key = input()
            if key == '1':
                pass
            else:
                enter_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__layout"]/div/div[3]/div[1]/div/div[2]/div[2]/div[1]/label[2]')))
                enter_button.click()

                bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                page_source = bro.page_source
                print(page_source)                          #!!! 错误 !!!
                tree = etree.HTML(page_source)              #!!! page_source非源码 !!!
                skin_num = 1
                sleep(1)

                while skin_num <= 1985:
                    try:
                        stock = tree.xpath(f'//*[@id="__layout"]/div/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div[{skin_num}]/span/div[2]/div[2]/span/sub/text()')
                    except WebDriverException:
                        bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                        sleep(1)
                        page_source = bro.page_source
                        tree = etree.HTML(page_source)
                        continue

                    stock = stock[0]
                    stock = stock.strip()
                    stock = stock[:-3]
                    if stock == '1000+':
                        stock = 9999
                    else:
                        stock = int(stock)

                    if stock >= 20:
                        wait.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="__layout"]/div/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div[{skin_num}]/span/div[2]/div[1]')))
                        skin_name = tree.xpath(f'//*[@id="__layout"]/div/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div[{skin_num}]/span/div[2]/div[1]/text()')
                        skin_name,skin_float_type = self.__skin_name(skin_name)

                        # 进入详情页
                        detailed_info_button = wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="__layout"]/div/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div[{skin_num}]/span/div[2]/div[1]')))
                        detailed_info_button.click()
                        bro.switch_to.window(bro.window_handles[1])
                        sleep(2)
                        detailed_page_source = bro.page_source
                        detailed_tree = etree.HTML(detailed_page_source)
                        skin_sale_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__layout"]/div/div[3]/div[1]/div[4]/div[1]/div[1]/div/div/div/div/div[1]/div[2]')))
                        skin_sale_button.click()

                        # 获取磨损
                        try:
                            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__layout"]/div/div[3]/div[1]/div[9]/ul[1]/li/div[2]/div[1]')))
                        except WebDriverException:
                            bro.refresh()
                        skin_float = detailed_tree.xpath('//*[@id="__layout"]/div/div[3]/div[1]/div[9]/ul[1]/li/div[2]/div[1]/text()')
                        skin_float = [int(i[3:]) for i in skin_float]

                        # 获取价格
                        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__layout"]/div/div[3]/div[1]/div[9]/ul[1]/li/div[5]/span/span')))
                        prices = detailed_tree.xpath('//*[@id="__layout"]/div/div[3]/div[1]/div[9]/ul[1]/li/div[5]/span/span/text()')

                        # 获取商店名
                        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__layout"]/div/div[3]/div[1]/div[9]/ul[1]/li/div[4]/span/text()')))
                        store_name = detailed_tree.xpath('//*[@id="__layout"]/div/div[3]/div[1]/div[9]/ul[1]/li/div[4]/span/text()')
                        data = list(zip(skin_float, prices, store_name))
                        print(skin_name)
                        print(data)

                        self.__mysql_insert(skin_name, skin_float_type, data, db_name, stock)
                        print("成功")
                        bro.close()
                        bro.switch_to.window(bro.window_handles[0])

                    skin_num += 1
        self.__dr_all(db_name)
        print("去重成功")
        end = time.perf_counter()
        time_sum = int(end-start)
        print(f"爬取成功\n用时：{time_sum//60}分钟{time_sum%60}秒")


skin = CsgoSkins()
skin.skin_data_collector()
