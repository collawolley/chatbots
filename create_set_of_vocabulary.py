#!/usr/bin/python
# -*- coding: utf8 -*-
import re 
import numpy as np
import time
import jieba
import codecs
f = codecs.open("filtertxt.txt","r","utf-8")     # 返回一个文件对象
lines = f.readlines()                            # 调用文件的 readlines()方法
numberOfLines = len(lines)
vocabulary = []                                  #存储每个出现的词
frequence = []                                   #每个词出现的频率
position = []                                    #每个词出现的位置总和，与出现平率想除可得到这个词一般在一个句子里的平均位置，
                                                 #用于后面神经网络分析出输出词后进行组合成句
dictory = []
string =""
'''
for i in range(0,numberOfLines):
   seg_list = jieba.lcut(lines[i], cut_all=False)
   for s in seg_list:
     vocabulary.append(s)

#setOfVocabulary = set(vocabulary)         #把重复的全部去掉，这里也可以改进为统计每个词汇的出现平率，这里用set简单处理而已
#单纯的set算出来的矩阵X为（10000+，9500+）,发现如此庞大的数据集sklt—learen库和pybrain不支持5000+以上的feature
#错误为mamory error 连库里的PCA都无法使用，所以首先自己先剔除一些词汇，剔除办法为去除一些使用频率较低的词汇

#listOfVocabulary = list(setOfVocabulary)  #因为set函数并不支持index取值
'''
for i in range(0,numberOfLines):
   seg_list = jieba.lcut(lines[i], cut_all=False)
   for j in range(0,len(seg_list)):
     try:                                         #vocabulary.index(seg_list[j]) 如果不存在，会出现异常报错，所以用python的异常机制
       p = vocabulary.index(seg_list[j])          #获取所在位置
       frequence[p]+=1                            #出现一次加一次
       position[p]+=j                             #存入所处的位置和之前的累加
     except:                                      #出现异常就表示不存在，所以添加新的词
       vocabulary.append(seg_list[j])
       frequence.append(1)
       position.append(j)

frequenceArray = np.array(frequence)              #应为list不支持除法，所以先转化为np的array
positionArray = np.array(position)
positionList =list(positionArray/frequenceArray)  #计算出每个词所在的平均位置

for i in range(0,len(vocabulary)):
    dictory.append([vocabulary[i],frequence[i],positionList[i]])      #把这三样东西封装起来，用于排序   

sortedVocabulary=sorted(dictory,reverse = True,key=lambda x:x[:][1])  #lambda x:x[:][1] ===> def output(x):  return x[:][1]
                                                                      #通过第二行每个词的出现频率进行排序

f1 = open("sorted_set_of_vocabulary.txt","w")
for i in range(0,len(sortedVocabulary)):
    string += sortedVocabulary[i][0]+"\t"+str(sortedVocabulary[i][1])+"\t"+str(sortedVocabulary[i][2])+"\n"     #要写入文件每行加入一个换行符
#print listOfVocabulary[0] 
f1.writelines(string.encode('utf-8'))
f1.close
