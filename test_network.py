#!/usr/bin/python
# -*- coding: utf8 -*-
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml.networkwriter import NetworkWriter 
from pybrain.tools.customxml.networkreader import NetworkReader
from numpy import ndarray
import numpy as np
import pickle
import codecs
from sklearn.decomposition import RandomizedPCA
from sklearn.externals import joblib
import jieba
def loadAllData():
  print "load network......."
  net = 0#NetworkReader.readFrom('./data/mynetwork1.xml')
  print "load X and PCA......."
  f1 = open('./data/X_Train_pca', 'rb')
  X_train_PCA = pickle.load(f1)
  f1.close
  pca = joblib.load('./data/filename.pkl')
  print "load Vocabulary......."
  f2 = codecs.open("./data/sorted_set_of_vocabulary.txt","r","utf-8")
  setOfVocabulary = f2.readlines()
  f2.close

  print "create reducedVocabulary......."
  reducedVocabulary={}
  #print len(setOfVocabulary)
  for i in range(1,3001):                   #选前3000个词汇,语料库文件第一行是换行符的频率，不需要，
                                          #应为每条消息都会有一个换行，可以用来验证是否统计了所有词汇
    reducedVocabulary[i]=[setOfVocabulary[i].strip().split('\t')[0],setOfVocabulary[i].strip().split('\t')[2]]   
                                          #通过split可以把一个字符串按'\t'把字符串分成几节存在数组里
                                          #这里的[0]就表示第一列也就是所有词汇，[2]表示出现次数[3]平均为值
  d={"net":net,"X_train_PCA":X_train_PCA,"reducedVocabulary":reducedVocabulary,"pca":pca}
  return d 

def wordHypothesis(inputExample,net,pca,reducedVocabulary,a,X_train_PCA):
  seg_list = jieba.lcut(inputExample, cut_all=False)           #这个函数耗时较长
  X=np.zeros((1,len(reducedVocabulary)))
  for s in seg_list:
    try:                                        #vocabulary.index(seg_list[j]) 如果不存在，会出现异常报错，所以用python的异常机制,所以不能用if
      p=reducedVocabulary.index(s)              #这里要吐槽一下，难道无匹配就不能返回个none，非要抛出异常？？？说不定有这样的函数我没找到
      X[0][p] = 1
    except:
      pass
  Z = pca.transform(X)                          #通过PCA转化X为Z
  #print Z[0][:10]
  #print X_train_PCA[0][:10]
  h = net.activate(Z)
  print sum(h)
  dicts={}
  for i in range(0,len(h)):      #把神经网络反馈结果返回到一个键为序号，值为结果的字典里
    dicts[i] = h[i]

  print "sort hypothposi......."

  sortedDicts = sorted(dicts.iteritems(),reverse=True,key=lambda d:d[1])   #按字典的值从大到小排序，返回的不是数组，是一个一个的元祖

  #print sortedDicts[:50]

  hWord={}
  for i in range(0,len(sortedDicts)):
    if(sortedDicts[i][1]>=a):           #如果该值到达一个阈值
      pos=sortedDicts[i][0]             #返回该值的序号
      word=reducedVocabulary[pos][0]    #所在序号代表的词汇
      hWord[word]= reducedVocabulary[pos][1] #把这个词汇，以词语做键，词语出现的一般位置做值

  sortedhWord = sorted(hWord.iteritems(),reverse=False,key=lambda d:int(d[1]))  #排序返回的是元祖
  #print sortedhWord
  s=""
  for i in range(0,len(sortedhWord)):
    s+=sortedhWord[i][0]                #返回字符串
  return s
if __name__ == "__main__":
  d=loadAllData()
  s=wordHypothesis("黄黄你的电脑弄好了没？",d['net'],d['pca'],d['reducedVocabulary'],0.5)
