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

print "start load data......"
f1 = open('./data/X_Train_pca', 'rb')
X_train_PCA = pickle.load(f1)
f1.close
f2 = open('./data/Y1', 'rb')
Y = pickle.load(f2)
f2.close
numberOfExample=Y.shape[0]
numberOfPCA = X_train_PCA.shape[1]
numberOfFeatureY = Y.shape[1]

print "numberOfExample: "+str(numberOfExample)+"  numberOfPCA: "+str(numberOfPCA)+"  numberOfFeatureY: "+str(numberOfFeatureY)

print "load network......."
net = NetworkReader.readFrom('./data/mynetwork1.xml')
print "create data set..."

ds = SupervisedDataSet(numberOfPCA, numberOfFeatureY)
for i in range(0,numberOfExample):
    ds.addSample(X_train_PCA[i], Y[i])
print ds.getLength()
print "start training....."
trainer = BackpropTrainer(net, ds)
trainer.train()

print "save the training modules"
NetworkWriter.writeToFile(net, './data/mynetwork1.xml')
