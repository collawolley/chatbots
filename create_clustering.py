#!/usr/bin/python
# -*- coding: utf8 -*-
import numpy as np
import jieba
import codecs
from sklearn.decomposition import RandomizedPCA
from sklearn import cluster

f1 = codecs.open("filtertxt.txt","r","utf-8")
f2 = codecs.open("sorted_set_of_vocabulary.txt","r","utf-8")
message = f1.readlines()
setOfVocabulary = f2.readlines()
numberOfMessage = len(message)            #获取消息的数量，也就是样本数量
numberOfSetVocab = len(setOfVocabulary)   #获取词库长度，也就是特征的长度
reducedVocabulary = []                    #存储按频率排序后前N个词汇，最好不超过5000
#numberOfMessage=numberOfMessage-5000
string=[]
s=""
for i in range(0,numberOfMessage):        #去掉样本后面的换行符
   #message[i] = message[i][:-1]
   message[i] = message[i].strip()        #这个函数可以删除所有关于换行符制表符全部删去

for i in range(1,1001):                   #选前5000个词汇,语料库文件第一行是换行符的频率，不需要，
                                          #应为每条消息都会有一个换行，可以用来验证是否统计了所有词汇
   reducedVocabulary.append(setOfVocabulary[i].strip().split('\t')[0])   #通过split可以把一个字符串按'\t'把字符串分成几节存在数组里
                                                                         #这里的[0]就表示第一列也就是所有词汇，[2]表示出现次数[3]平均为值
#print reducedVocabulary[2]


numberOfReducedVocabulary=len(reducedVocabulary)
X = np.zeros((numberOfMessage,numberOfReducedVocabulary))    #X为训练集
Y = np.zeros((numberOfMessage-1,numberOfReducedVocabulary))  #Y为输出，因为上一个的说话算样本，下一个的说话就算输出，一问一答

print "start create X_train....sadasd"

for i in range(0,numberOfMessage):                           #对样本进行分词，并找到这个词在语料库的index，给X相应的位置标1表示存在  
  seg_list = jieba.lcut(message[i], cut_all=False)           #这个函数耗时较长
  for s in seg_list:
    try:                                        #vocabulary.index(seg_list[j]) 如果不存在，会出现异常报错，所以用python的异常机制,所以不能用if
      p=reducedVocabulary.index(s)              #这里要吐槽一下，难道无匹配就不能返回个none，非要抛出异常？？？说不定有这样的函数我没找到
      X[i][p] = 1
    except:
      pass
#print type(X)  numpy.ndarray
print X.shape
print "start Kmeans process......"
k_means = cluster.KMeans(n_clusters=100)
k_means.fit(X)
print "save result....."
for i in range(0,100):
  string.append("======================="+str(i)+"===================\n")
  for j in range(0,numberOfMessage):
    if k_means.labels_[j]==i :
      string[i]+=message[j]+"\n"
     #print k_means.labels_[::10]
  s+=string[i]
f1 = open("clustering.txt","w")
f1.writelines(s.encode('utf-8'))
f1.close

