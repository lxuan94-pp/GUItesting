from PIL import Image
import numpy as np
from keras.models import load_model
# import os
import time

norm_size = 32
start_h = 0
po = []  #po为最终子图相对于整图坐标信息list
elist = []
def line_is_same(arry):
    width = len(arry)
    for i in range(width):
        if arry[i] == arry[0]:
            continue
        else:
            return False
    return True

def get_start(arry):
    global start_h
    height = arry.shape[0]
    start1 = 0
    for j in range(start_h,height):
        if line_is_same(arry[j]):  #如果当前横线为背景线
            if j == (height - 1):
                start1 = j
                start_h = j
            continue
        else:
            start_h = j
            start1 = j
            break#控件图块起始点,局部变量
    return start1

def get_end(arry):
    global start_h
    height = arry.shape[0]
    end1 = 0
    for j in range(start_h, height):
        if not line_is_same(arry[j]):
            continue
        else:
            start_h = j
            end1 = j
            break
    return end1

# def mkdir(path):
#     folder = os.path.exists(path)
#     if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
#         os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
#         return path
#     else:
#         return path

def imagefactory1(sourcelist,sourceimage):  #横切
    N = len(sourcelist) #sourcelist为坐标信息数组，sourceimage为切割的单张整图最开始应为单元素
    if N == 0:
        print("切割结束")
    else:
        outlist = [] #输出坐标信息
        w = ()  # 元组，存储（start，end）

        for i in range(N): #在输入坐标列表里面，输入每个子图
            imgsite = sourcelist[i]  #site为单个坐标信息
            im = sourceimage.crop(imgsite) #im为切割出的子图
            img_size = im.size
            height = img_size[1]
            width = img_size[0]
            imA = im.convert('RGB') #图像转RGB
            imB = imA.convert("L")  # 图像转换为灰值图
            iar = np.asarray(imB)   #图像变为矩阵
            global start_h
            start_h = 0# 竖向遍历的起始点
            location = {}  # 字典，存储w ，每张子图都有一个location，存储其子图坐标信息特征
            l = 0

            for m in range(start_h, height): #遍历纵向像素点获取各个可切出的子图纵向开始点，结束点
                if start_h == (height - 1):
                    break
                start = 0
                end = 0
                start = get_start(iar)
                end = get_end(iar)
                if (start < end):
                    if (end - start < 18): #如果开始结束之间距离小于18像素点，则放弃此截子图（大概率为废图）
                        continue
                    else: #否则存储信息
                        w = (start, end)
                        location["w" + str(l)] = w
                        l += 1
                else:
                    break

            if l == 0:  #l == 0即表达location中无元组
                po.append(imgsite) #imgsite即为此最终子图的坐标信息
            else:
                for n in range(l): #location中元组序号应为 0 ···(l-1)恰好为range(l)
                    s = location["w" + str(n)][0]  # 子图开始点Y值
                    h = location["w" + str(n)][1]  # 子图结束点位置Y值
                    a = (0, s, width, h) #(0,s)为此下级子图相对于切后子图的左上角坐标；(width, h)为右下角坐标
                    b = a
                    if sourcelist: #如果位置类有元素
                        x = imgsite[0] #x为上级图的左上点坐标x值
                        y = imgsite[1] #为上级图的左上点坐标y值
                        b = (x, s+y ,width+x, h+y) #计算此下级子图相对于整图的位置信息

                    outlist.append(b)
        imagefactory2(outlist,sourceimage)

def imagefactory2(sourcelist,sourceimage): #竖切
    N = len(sourcelist)  # sourcelist为坐标信息数组，sourceimage为切割的单张整图最开始应为单元素
    if N == 0:
        print("切割结束")
    else:
        outlist = []  # 输出坐标信息
        w = ()  # 元组，存储（start，end）

        for i in range(N):
            imgsite = sourcelist[i]  # site为单个坐标信息
            im = sourceimage.crop(imgsite)  # im为切割出的子图
            img_size = im.size
            height = img_size[1]
            imA = im.convert('RGB')  # 图像转RGB
            imB = imA.convert("L")  # 图像转换为灰值图
            iar_heng = np.asarray(imB)#将图片转为矩阵
            iar = np.transpose(iar_heng)#矩阵变形，使横向变纵向


            global start_h
            start_h = 0  # 竖向遍历的起始点
            start = 0
            end = 0  # 中止点
            w = ()  # 元组，存储（start，end）
            location = {}  # 字典，存储w
            l = 0

            for m in range(start_h, height): #遍历纵向像素点获取各个可切出的子图纵向开始点，结束点
                if start_h == (height - 1):
                    break
                start = 0
                end = 0
                start = get_start(iar)
                end = get_end(iar)
                if (start < end):
                    if (end - start < 18): #如果开始结束之间距离小于18像素点，则放弃此截子图（大概率为空隙废图）
                        continue
                    else: #否则存储信息
                        w = (start, end)
                        location["w" + str(l)] = w
                        l += 1
                else:
                    break

            if l == 0:  #获取最终子图坐标信息
                po.append(imgsite)  # imgsite即为此最终子图的坐标信息
            else:
                for n in range(l):
                    s = location["w" + str(n)][0]  # 子图开始点Y值
                    w = location["w" + str(n)][1]  # 子图结束点位置
                    a = (s, 0, w, height)
                    b = a
                    if sourcelist:  # 如果位置类有元素
                        x = imgsite[0]  # x为上级图的左上点坐标x值
                        y = imgsite[1]  # 为上级图的左上点坐标y值
                        b = (s+x,0+y,w+x, height+y)
                    outlist.append(b)

        imagefactory1(outlist, sourceimage)

def predict(image_arr,model):
    # 分类
    result = model.predict(image_arr)[0]
    # 得到最大概率的数值
    proba = np.max(result) #概率例如0.7624
    #得到类别，为数字
    label = str(np.where(result == proba)[0])
    if label == '[1]':
        label = "button"
    elif label == '[2]':
        label = "icon"
    elif label == '[3]':
        label = "menuitem"
    elif label == '[4]':
        label = "picturelink"
    elif label == '[5]':
        label = "textbox"
    elif label == '[6]':
        label = "textlink"
    else:
        label = "Rubbish"
    #label = "{}: {:.2f}%".format(label, proba * 100)
    label = label
    return label

# def predictImage(sourceImagepath,outpath,modelpath):
#
#     model = load_model(modelpath)
#
#     im = Image.open(sourceImagepath)
#     img_size = im.size
#     height = img_size[1]
#     width = img_size[0]
#
#     site = (0, 0, width, height)
#     sorcelist = [site]
#
#     imagefactory1(sorcelist,im)
#
#     #检验是否是正确的坐标信息
#     f = open(outpath,'w')
#     #预测图片信息
#
#     for i in range(len(po)):
#         aa = po[i]
#         souceimage = im.crop(aa)
#
#         # path1 = "E:\PyWork\Predict\FinalImage"
#         # path = path1 + '/Image%d.jpg' % (i)
#         # souceimage.save(path)
#
#         resize_image = souceimage.resize((norm_size, norm_size), Image.ANTIALIAS)
#         imA = resize_image.convert('RGB')  # 图像转RGB
#         iar = np.asarray(imA)  # 图像变为矩阵
#         iarB = iar / 255.0
#         image_arr = np.expand_dims(iarB, axis=0)
#
#         label = predict(image_arr,model)
#
#         str2 = str(i) + ":" + str(aa) + "--" + label
#         f.write(str2 + "\n")
#
#     f.close()

def predictImage(sourceImagepath, modelpath):
    model = load_model(modelpath)

    im = Image.open(sourceImagepath)
    img_size = im.size
    height = img_size[1]
    width = img_size[0]

    site = (0, 0, width, height)
    sorcelist = [site]

    imagefactory1(sorcelist, im)

    # 检验是否是正确的坐标信息
    # 预测图片信息

    for i in range(len(po)):
        aa = po[i]
        souceimage = im.crop(aa)

        # path1 = "E:\PyWork\Predict\FinalImage2"
        # path = path1 + '/Image%d.jpg' % (i)
        # souceimage.save(path)

        resize_image = souceimage.resize((norm_size, norm_size), Image.ANTIALIAS)
        imA = resize_image.convert('RGB')  # 图像转RGB
        iar = np.asarray(imA)  # 图像变为矩阵
        iarB = iar / 255.0
        image_arr = np.expand_dims(iarB, axis=0)

        label = predict(image_arr, model)

        e = (label,aa)
        elist.append(e)

    return elist



def getlist(imagepath,modlepath):
    list = predictImage(imagepath,modlepath)
    return list

if __name__ == "__main__":
    start_time = time.time()
    #参数：需要识别的图片路径，识别结果输出文件路径，引用模型的路径
    # predictImage("./SourceImage/4"
    #              ".jpg",
    #              "./predict/type2.txt",
    #              "./predict/model2.model")
    LIST  = getlist("./SourceImage/4.jpg","./predict/model2.model")
    for i in LIST:
        print(i)
    end_time = time.time()
    time = end_time - start_time
    print("timeCost: ",time,"s")
