#!/usr/bin/python
# -*- coding: utf8 -*-
import re 
import numpy as np
import time
f = open("testmsg.txt")             # 返回一个文件对象
lines = f.readlines()             # 调用文件的 readline()方法
numberOfLines=len(lines)
"""
for i in range(0,numberOfLines):
  print lines[i]
"""
pattern1 = re.compile(r'\d\d\d\d-\d\d-\d\d \d:\d\d:\d\d')   #match两种不同的时间方式
pattern2 = re.compile(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d')
txt = []
i=0
name=""
for i in range(0,numberOfLines):
    #print line,                 # 后面跟 ',' 将忽略换行符
    # print(line, end = '')　　　# 在 Python 3中使用
    match1 = pattern1.match(lines[i])
    match2 = pattern2.match(lines[i]) 
    #time.sleep(1)
    if match1 :
      if(lines[i+1]!="\n"):                          #这个表示当消息的发起人那一行匹配后，下一行一定是写的话，但是也有可能是发了个回车的空消息
       if name == lines[i][len(match1.group()):]:    
          #考虑到真正聊天并不是你一句我一句，有可能一个人发了好多句，所以在另一个人回复之前，把所有同样人发的消息合并为一句。
          txt[len(txt)-1]+=lines[i+1][:-1]  #去除最后的换行符
       else:
          name = lines[i][len(match1.group()):]     #如果名字不再是上一个人的，表示另外一个人回复了，所以消息另外添加一行
          txt.append(lines[i+1][:-1])        
    if match2 :                                    #同理本来可以写简单写，犯懒直接粘贴
      if(lines[i+1]!="\n"):
       if name == lines[i][len(match2.group()):]:
          txt[len(txt)-1]+=lines[i+1][:-1]
       else:
          name = lines[i][len(match2.group()):]  
          txt.append(lines[i+1][:-1]) 
f.close()

f1 = open("filtertxt.txt","w")
for i in range(0,len(txt)):
    txt[i]=txt[i]+"\n"     #要写入文件每行加入一个换行符
   
f1.writelines(txt)
f1.close
