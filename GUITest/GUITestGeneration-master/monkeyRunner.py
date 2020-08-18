# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

import os

import re
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import uiautomator2 as Device
from PIL import Image
from imageFactory import getlist

driver=Device.connect_usb('0123456789ABCDEF')

#sess = u.app_start("com.sankuai.meituan.takeoutnew")
print(driver.info)
print("11111")

#页面序号
i=0
#存储页面名称
actiList= []
#存储所有控件
elementLists=[]
backButton=[]
eCutList=[]
#子图编号
k=0
#按钮编号
p=0

currentLen=0
#创建空的网络图
G = nx.MultiDiGraph()


class Test(object):
    def __init__(self, driver):
        self.driver = driver

    #def hasclicked(self,ele):
    def startActivity(self, activity):
        os.system('adb -s %s shell am start %s' % (self.driver, activity))

   #获取屏幕截图
    def get_elem_screenshot(self, element, index):
        location = element.center
        #size = element.size
        name = element.elem.tag
        if str(name) == "android.widget.ImageView":
            name="img"
        elif str(name) == "android.widget.TextView":
            name="text"
        elif str(name) == "android.widget.ImageButton":
            name="button"
        elif str(name) == "android.widget.EditText":
            name="textbox"
        elif str(name) == "android.view.View":
            name="view"
        #TEMP_Elem = 'F:\\pythonProject\\Monkey\\result\\page%s' % index
        TEMP_Elem =  '/Users/xuanliu/PycharmProjects/monkey/result/pages%s' % index
        TEMP_El= TEMP_Elem+ "\\%s" % k
        TEMP_PA=TEMP_El+"_%s.png" %name

        #t = "F:\\pythonProject\\Monkey\\result\\all"
        t = "/Users/xuanliu/PycharmProjects/monkey/result/all"
        to=t+"\\%s" % k
        total=to+"_%s.png" %name
        if not os.path.exists(TEMP_Elem):
           os.makedirs(TEMP_Elem)
        if not os.path.exists(t):
           os.makedirs(t)
        #loca=open("F:\\pythonProject\\Monkey\\result\\page%s\\location.txt" % index , 'a')
        # 先截取整个屏幕，存储至系统临时目录下
        #self.driver.get_screenshot_as_file(TEMP_PA)
        driver.screenshot(TEMP_PA)
         # 获取元素bounds
        bounds = element.elem.attrib.get("bounds")
        lx, ly, rx, ry = map(int, re.findall("\d+", bounds))
        #box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        box=(lx,ly,rx,ry)
        print(box)
        # 截取图片
        image = Image.open(TEMP_PA)
        newImage = image.crop(box)
        newImage.save(TEMP_PA)
        newImage.save(total)
        #loca.write(str(name)+str(box)+"\n")
        return self

    # 对每一个界面保存控件位置、截图
    #def save_screeninfo(self, ac):
    def save_screeninfo(self,driver):
        global i
        global k
        global p
        global G
        global currentLV
        # 旧页面控件位置
        old = []
        eCutList=[]
        print(eCutList)
        time.sleep(3)
        # 保存当前页面至特定文件夹
        #di="F:\\pythonProject\\Monkey\\result\\page%s" % i
        #if not os.path.exists(di):
        #   os.makedirs(di)
        #driver.get_screenshot_as_file(di+"\\total.png" )

        #al="F:\\pythonProject\\Monkey\\result\\whole"
        al="/Users/xuanliu/PycharmProjects/monkey/result/whole"
        if not os.path.exists(al):
           os.makedirs(al)

        destina=al+"\\%s.png" %i
        driver.screenshot(destina)

        #sourcePic=driver
        #dirr = "F:\\pythonProject\\Monkey\\result\\whole\\%s.png" %i
        dirr = "/Users/xuanliu/PycharmProjects/monkey/result/whole/%s.png" %i
        #sourcePic = Image.open(dirr)

        #eCutList=getlist(dirr,"F:\\pythonProject\\Monkey\\invoice.model")
        eCutList=getlist(dirr,"/Users/xuanliu/PycharmProjects/monkey/invoice.model")
        #去掉前面页面的位置信息
        #currentLen=len(eCutList)
        #if currentLen !=0:
          # for iii in range(currentLen):
           #  eCutList.remove(eCutList(iii))
        print(eCutList)

        #将界面加入节点
        G.add_node(i)
        #判断界面内容
        time.sleep(3)
        judgePage=driver.xpath("//android.widget.ImageView").all()
        print(judgePage[1].elem.attrib.get("bounds"))


        old_index=0
        for ju in judgePage:
            #j=ju.location
            #j=ju.info['bounds']
            j=ju.center
            old.insert(old_index,j)
            old_index+=1
        #old=len(judgePage)
        #print(old)

        time.sleep(3)
        # 保存当前页面所有控件
        '''
        eList2 = driver.find_elements_by_class_name("android.widget.EditText")
        eList3 = driver.find_elements_by_class_name("android.widget.ImageView")
        eList1=driver.find_elements_by_class_name("android.widget.TextView")
        eList5=driver.find_elements_by_class_name("android.view.View")
        eList4=driver.find_elements_by_class_name("android.widget.ImageButton")
        eList9=driver.find_elements_by_class_name("android.widget.Button")
        '''
        eList2=driver.xpath("//android.widget.EditText").all()
        eList3 = driver.xpath("//android.widget.ImageView").all()
        eList1 = driver.xpath("//android.widget.TextView").all()
        eList5 = driver.xpath("//android.view.View").all()
        eList4 = driver.xpath("//android.widget.Button").all()
        eList9 = driver.xpath("//android.widget.ImageButton").all()
        #eList5=driver.find_elements_by_class_name("android.widget.SeekBar")
        eList=eList2+eList3+eList1+eList9+eList5+eList4
        elocation=[]
        ind=0
        for ee in eList:
            #elocation=elocation+str(ee.center)
            #nn = ee.center
            boun = ee.elem.attrib.get("bounds")
            lx, ly, rx, ry = map(int, re.findall("\d+", boun))
            nn = (lx, ly, rx, ry)
            elocation.insert(ind, nn)
        '''
        for cut in eCutList:
            if cut[1] in elocation:
                continue
            else:
                eList=eList+cut
        '''
        #保存所有返回按钮
        '''
        ba1=driver.find_elements("id","reader_opt_btn_close_img")
        ba2 = driver.find_elements("id", "titlebar_lefticon_btn")
        ba3 = driver.find_elements("id", "detailspage_btn_back_img")
        ba4=driver.find_elements_by_accessibility_id("转到上一层级")
        '''
        ba1=driver.xpath("//转到上一层级").all()
        ba2=driver.xpath("//navi_back_btn").all()
        ba3=driver.xpath("//iv_back").all()
        ba=ba1+ba2+ba3
        for b in ba:
            l1=b.center
            backButton.insert(p, str(l1))
            p+=1

        for member in eList:
            w.get_elem_screenshot(member, i)
            k=k+1

             # 自己截的控件位置
        for cut in eCutList:
                    try:
                        nametype = cut[0]
                        if nametype == "textbox":
                            print("hh")
                            cut.send_keys("hello")
                            # .send_keys("hello")
                        xStart = cut[1][0]
                        xEnd = cut[1][2]
                        yStart = cut[1][1]
                        yEnd = cut[1][3]
                        xpoint = (xEnd + xStart) / 2
                        ypoint = (yEnd + yStart) / 2
                        #判断是否为返回按钮
                        locationPair=[]
                        #lll='{\'x\': '+str(cut[1][0])+','+'\'y\': '+str(cut[1][1])+'}'
                        lll='('+str(xStart)+','+str(yStart)+','+str(xEnd)+','+str(yEnd)+')'
                        locationPair.insert(0,str(lll))
                        #print(locationPair)
                        #print(backButton)
                        if locationPair in backButton:
                            continue
                        else:
                            #点击当前控件
                            driver.click(xpoint,ypoint)
                            time.sleep(3)
                        # 获取新页面的控件位置
                        # 新页面控件位置
                        new = []
                        newAct=driver.xpath("//android.widget.ImageView").all()
                        new_index = 0
                        for ne in newAct:
                            #n = ne.center
                            boun = ne.elem.attrib.get("bounds")
                            lx, ly, rx, ry = map(int, re.findall("\d+", boun))
                            n = (lx, ly, rx, ry)
                            new.insert(new_index, n)
                            new_index += 1

                        # print(new)
                        # print(actiList)

                        # 判断新页面控件位置列表是否已经初现
                        if new in actiList:
                            if old != new:
                                # driver.get(old)
                                driver.press_keycode(4)
                            continue
                        else:

                            tag = str(cut[0])
                            G.add_edge(i, i + 1, label="%s" % (tag))
                            nx.draw_networkx(G, pos=nx.random_layout(G), node_color='g', edge_color='r',
                                             with_labels=True,
                                             font_size=10, font_color='b', node_size=20)

                            i = i + 1
                            actiList.insert(i, new)
                            # print(actiList)
                            w.save_screeninfo(driver)

                    except Exception:
                        continue

        #driver.press_keycode(4)
        driver.press.back()
        plt.show()
        print(driver.current_activity)


time.sleep(10)
if __name__ == "__main__":
    #Device.connect_usb('5LMNPBCQYSTS5HEM')
    Device.connect_usb('0123456789ABCDEF')
    #w=Test('5LMNPBCQYSTS5HEM')   #记录手机串号，查看方式adb devices
    w=Test('0123456789ABCDEF')
    w.startActivity('com.sankuai.meituan.activity.LaunchActivity')
    time.sleep(5)
    w.save_screeninfo(driver)
#w = UIAutomator(driver)
#w.save_screeninfo(driver)









