# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

import math
import operator

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
'''
def get_key(dict, val):
    for key, value in dict.items():
         if val == value:
             return key
    return -1
'''

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)
    """
    # TODO: Write your code here
    # return predicted labels of development set

    #count the words
    negative_set = {}
    positive_set = {}
    n_p = 0
    n_n = 0

    for i in range(len(train_set)):
        list = train_set[i]
        for j in range(len(list)):
            word = list[j]
            if (train_labels[i] == 1): #positive
                n_p += 1
                if (word in positive_set):
                    positive_set[word] += 1
                else:
                    positive_set[word] = 1
            else: #negative
                n_n += 1
                if (word in negative_set):
                    negative_set[word] += 1
                else:
                    negative_set[word] = 1

    ps = dict(sorted(positive_set.items(), key=operator.itemgetter(1)))
    ns = dict(sorted(negative_set.items(), key=operator.itemgetter(1)))

    positive_set = {}
    negative_set = {}

    if (len(ps) < len(ns)):
        #cut ns
        positive_set = ps.copy()
        n_n = 0
        for word in ns:
            if(ns[word] != 1):
                negative_set[word] = ns[word]
                n_n += ns[word]
            elif (len(positive_set) > len(negative_set)):
                negative_set[word] = ns[word]
                n_n += ns[word]
    else:
        negative_set = ns.copy()
        n_p = 0
        for word in ps:
            if (ps[word] != 1):
                positive_set[word] = ps[word]
                n_p += ps[word]
            elif (len(negative_set) > len(positive_set)):
                positive_set[word] = ps[word]
                n_p += ps[word]
    print(len(positive_set))
    print(len(negative_set))
    print(n_p)

    '''
    val = 1
    while(len(negative_set) > 2500):
        key = get_key(negative_set, val)
        if (key == -1):
            val += 1
        else:
            n_n -= negative_set[key]
            del negative_set[key]

    val = 1
    while(len(positive_set) > 2500):
        key = get_key(positive_set, val)
        if (key == -1):
            val += 1
        else:
            n_p -= positive_set[key]
            del positive_set[key]

    val = 1

    while(len(negative_set) > 2500):
        for word in negative_set:
            if (negative_set[word] == val):
                n_n -= val
                del negative_set[word]
            if (len(negative_set) <= 2500):
                break
    val = 1
    while(len(positive_set) > 2500):
        for word in positive_set:
            if (positive_set[word] == val):
                n_p -= val
                del positive_set[word]
            if (len(negative) <= 2500):
                break

    n_set = {}
    p_set = {}
    cnt = 0
    for word in negative_set:
        if (cnt < 2500):
            n_set[word] = negative_set[word]
            cnt += 1
            n_n += negative_set[word]
        else:
            break
    cnt = 0
    for word in positive_set:
        if (cnt < 2500):
            p_set[word] = positive_set[word]
            cnt += 1
            n_p += positive_set[word]
        else:
            break
    '''
    #probability calculation
    positive_prob = {}
    negative_prob = {}
    cnt = 0
    for word in positive_set:
        #word = positive_set[i]
        #if (cnt < 2500):
        prob = (smoothing_parameter + positive_set[word]) / (n_p + smoothing_parameter * (1 + len(positive_set)))
        positive_prob[word] = prob
        #    cnt += 1
        #else:
        #    break

    cnt = 0
    for word in negative_set:
        #word = negative_set[i]
        #if (cnt < 2500):
        prob = (smoothing_parameter + negative_set[word]) / (n_n + smoothing_parameter * (1 + len(negative_set)))
        negative_prob[word] = prob
            #cnt += 1
        #else:
        #    break

    result = []
    for i in range(len(dev_set)):
        list = dev_set[i]

        positive_sum = 0
        negative_sum = 0
        for j in range(len(list)):
            word = list[j]

            if (word not in positive_prob):
                prob = smoothing_parameter / (n_p + smoothing_parameter * (1 + len(positive_set)))
                positive_sum += math.log(prob)
            else:
                positive_sum += math.log(positive_prob[word])

            if (word not in negative_prob):
                prob = smoothing_parameter / (n_n + smoothing_parameter * (1 + len(negative_set)))
                negative_sum += math.log(prob)
            else:
                negative_sum += math.log(negative_prob[word])

        pos = positive_sum + math.log(pos_prior)
        neg = negative_sum + math.log(1 - pos_prior)
        '''
        if (math.log(pos) < math.log(neg)):
            result.append(0)
        else:
            result.append(1)
        '''
        if (pos < neg):
            result.append(0)
        else:
            result.append(1)

    return result
