# perceptron.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
import numpy as np
import numpy.linalg as la
"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def classify(train_set, train_labels, dev_set, learning_rate, max_iter):
    """
    train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
                This can be thought of as a list of 7500 vectors that are each
                3072 dimensional.  We have 3072 dimensions because there are
                each image is 32x32 and we have 3 color channels.
                So 32*32*3 = 3072
    train_labels - List of labels corresponding with images in train_set
    example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
             and X1 is a picture of a dog and X2 is a picture of an airplane.
             Then train_labels := [1,0] because X1 contains a picture of an animal
             and X2 contains no animals in the picture.

    dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
              It is the same format as train_set
    """
    # TODO: Write your code here
    # return predicted labels of development set
    weight = np.zeros(len(train_set[0]))
    bias = 0.5

    for i in range(len(train_set)):
        y = train_labels[i]
        for iter in range(max_iter):
            y_prime = np.sign(np.dot(weight, train_set[i]) + bias)
            if ((y_prime == -1 and y == False) or (y_prime == 1 and y == True)):
                break
            else:
                weight = weight + (learning_rate * (y - y_prime) * train_set[i])
                bias = bias + learning_rate * (y - y_prime)
    '''
    for iter in range(max_iter):
        for i in range(len(train_set)):
            y = train_labels[i]
            y_prime = np.sign(np.dot(weight, train_set[i]) + bias)
            if ((y_prime == -1 and y == False) or (y_prime == 1 and y == True)):
                continue
            else:
                if (y == True):
                    y = 1
                else:
                    y = 0
                if (y_prime == -1):
                    y_prime = 0
                weight = weight + (learning_rate * (y - y_prime) * train_set[i])
                bias = bias + learning_rate * (y - y_prime)
    '''
    list = []
    print("------weight------")
    print(weight)
    print("------bias------")
    print(bias)
    for i in range(len(dev_set)):
        val = np.sign(np.dot(weight, dev_set[i]) + bias)
        if (val < 0):
            val = 0
        list.append(val)
    return list

def classifyEC(train_set, train_labels, dev_set,learning_rate,max_iter):
    # Write your code here if you would like to attempt the extra credit
    return classify(train_set, train_labels, dev_set, learning_rate, max_iter)
