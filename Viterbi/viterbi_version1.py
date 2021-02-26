"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
def sort(set):
    dataset = {}
    countset = {}

    for sent in set:
        for word, tag in sent:
            if (word not in dataset):
                dataset[word] = {}
            if (tag not in dataset[word]):
                dataset[word][tag] = 1
            else:
                dataset[word][tag] += 1
            if (tag not in countset):
                countset[tag] = 1
            else:
                countset[tag] += 1
    return dataset, countset

def sort2(set):
    dataset = {}
    tagset = {}
    tag_tag_set = {}
    wordwithtagset = {}

    for sent in set:
        prev = 'START'
        for word, tag in sent:
            #data set
            if (word not in dataset):
                dataset[word] = {}
            if (tag not in dataset[word]):
                dataset[word][tag] = 1
                if (tag not in wordwithtagset):
                    wordwithtagset[tag] = 1
                else:
                    wordwithtagset[tag] += 1
            else:
                dataset[word][tag] += 1
            #tag set
            if (tag not in tagset):
                tagset[tag] = 1
            else:
                tagset[tag] += 1

            #tag-tag pairs
            if (tag is not "START"):
                if (prev not in tag_tag_set):
                    tag_tag_set[prev] = {}

                if (tag not in tag_tag_set[prev]):
                    tag_tag_set[prev][tag] = 1
                else:
                    tag_tag_set[prev][tag] += 1
            prev = tag
    return dataset, tagset, tag_tag_set, wordwithtagset

def transition_prob(taglist, tag_tag_set, alpha):
    dict = {}
    V = 17
    '''
    for tag in tag_tag_set:
        V += len(tag_tag_set[tag])
    for prev_tag in taglist:
        dict[prev_tag] = {}
        for curr_tag in taglist:
            if (curr_tag not in tag_tag_set[prev_tag]):
                dict[prev_tag][curr_tag] = alpha / (alpha * (1 + V) + taglist[curr_tag])
            else:
                dict[prev_tag][curr_tag] = tag_tag_set[prev_tag][curr_tag] / taglist[prev_tag]
    '''
    for prev in tag_tag_set:
        if (prev is not 'null'):
            dict[prev] = {}
            for curr in taglist:
                if (curr not in tag_tag_set[prev]):
                    #dict[prev][curr] = alpha / (alpha * (1 + V) + taglist[curr])
                    dict[prev][curr] = 10 ** -10
                else:
                    #dict[prev][curr] = (alpha + tag_tag_set[prev][curr]) / (taglist[prev] + alpha * (1 + V))
                    dict[prev][curr] = tag_tag_set[prev][curr] / taglist[curr]
    return dict

def calculate_emission(dataset, taglist, alpha):
    dict = {}
    V = 0
    '''
    for word in dataset:
        dict[word] = {}
        for tag in taglist:
            total_num = taglist[tag]
            if (tag not in dataset[word]):
                dict[word][tag] = alpha / (taglist[tag] + alpha * (1 + V))
            else:
                dict[word][tag] = (alpha + dataset[word][tag]) / (taglist[tag] + alpha * (1 + V))
    '''

    for word in dataset:
        dict[word] = {}
        for tag in taglist:
            if (tag not in dataset[word]):
                dict[word][tag] = alpha / (taglist[tag] + alpha * (1 + V))
            else:
                num_of_word = sum(dataset[word].values())
                dict[word][tag] = (dataset[word][tag]) / (num_of_word)
    return dict

def initial_prob(taglist, wordwithtagset, alpha):
    dict = {}
    for tag in taglist:
        if (tag == 'START'):
            dict[tag] = 1
            #initial = taglist[tag] + alpha
            #initial = initial / (taglist["START"] + alpha * (1 + wordwithtagset["START"]))
            #dict[tag] = initial
        else:
            dict[tag] = 10 ** -10
            #initial = alpha / (taglist["START"] + alpha * (1 + wordwithtagset["START"]))
            #dict[tag] = initial
    return dict

def baseline(train, test):
    '''
    TODO: implement the baseline algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    dataset,countset = sort(train)
    '''
    for sent in train:
        for word, tag in sent:
            if (word not in dataset):
                dataset[word] = {}
            if (tag not in dataset[word]):
                dataset[word][tag] = 1
            else:
                dataset[word][tag] += 1
            if (tag not in countset):
                countset[tag] = 1
            else:
                countset[tag] += 1
    '''
    predicts = []
    for sent in test:
        temp = []
        for word in sent:
            if (word not in dataset):
                temp.append([word, 'NOUN'])
            else:
                max = 0
                final_tag = ''
                for tag in dataset[word]:
                    if (dataset[word][tag] > max):
                        max = dataset[word][tag]
                        final_tag = tag
                temp.append([word, final_tag])
        predicts.append(temp)


    #raise Exception("You must implement me")
    return predicts


def viterbi(train, test):
    '''
    TODO: implement the Viterbi algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    alpha = 1
    V = 17
    dataset, tagset, tagtagset, wordwithtagset = sort2(train)
    transition_p = transition_prob(tagset, tagtagset, alpha)
    initial_p = initial_prob(tagset, wordwithtagset, alpha)
    emission_p = calculate_emission(dataset, tagset, alpha)

    total_num = 0
    for tag in tagset:
        total_num += tagset[tag]
    predicts = []
    for sent in test:
        prev_prev = 'null'
        prev = 'START'
        temp = []

        for word in sent:
            if (word == 'START'):
                temp.append(('START', 'START'))
                continue
            pos_prob = {}
            max_prob = -math.inf
            final_tag = ''


            for possible_tag in tagset:
                emission = 10 ** -10
                if (word in dataset):
                    emission = emission_p[word][possible_tag]
                transition = transition_p[prev][possible_tag]
                initial = initial_p[possible_tag]

                prob = math.log(emission) * math.log(transition) * initial
                if (max_prob < prob):
                    max_prob = prob
                    final_tag = possible_tag


            '''
            if (prev_prev is not 'null'):
                for pos_prev in tagset:
                    emission1 = alpha / (tagset[tag] + alpha * (1 + V))
                    if (word in dataset):
                        emission1 = emission_p[word][pos_prev]
                    transition1 = transition_p[prev_prev][pos_prev]
                    initial1 = initial_p[pos_prev]

                    for pos_curr in tagset:
                        emission = alpha / (tagset[tag] + alpha * (1 + V))
                        if (word in dataset):
                            emission = emission_p[word][pos_curr]
                        transition = transition_p[pos_prev][pos_curr]
                        initial = initial_p[pos_curr]

                        prob = math.log(emission + emission1) * math.log(transition + transition1) * initial
                        if (max_prob < prob):
                            max_prob = prob
                            final_tag = possible_tag

            else: #null second word
                for possible_tag in tagset:
                    emission = alpha / (tagset[tag] + alpha * (1 + V))
                    if (word in dataset):
                        emission = emission_p[word][possible_tag]
                    transition = transition_p[prev][possible_tag]
                    initial = initial_p[possible_tag]
                    prob = math.log(emission ) * math.log(transition )
                    if (max_prob < prob):
                        max_prob = prob
                        final_tag = possible_tag

            '''

            '''
            #version2
            for possible_tag in tagset:
                emission = alpha / (tagset[possible_tag] + alpha * (1 + wordwithtagset[possible_tag]))
                transition = transition_p[prev][possible_tag]
                initial = initial_p[possible_tag]
                if (word in dataset):
                    #emission = emission_p[word][possible_tag]
                    if (possible_tag in dataset[word]):
                        emission = dataset[word][possible_tag] + alpha
                        emission = emission / (tagset[possible_tag] + alpha * (1 + wordwithtagset[possible_tag]))
                    #if (prev in tagtagset[possible_tag]):
                    #    transition = tagtagset[possible_tag][prev] + alpha
                    #    transition = transition / (tagset[prev] + alpha * (1 + wordwithtagset[prev]))
                    #initial = alpha / (tagset["START"] + alpha * (1 + wordwithtagset["START"]))
                prob = math.log(emission + transition)
                if (max_prob < prob):
                    max_prob = prob
                    final_tag = possible_tag
            '''
            #version1
            '''
            if (word not in dataset):
                #do laplace

                for possible_tag in tagset:
                    emission = alpha / (tagset[possible_tag] + alpha * (1 + wordwithtagset[possible_tag]))
                    #transition = alpha / (tagset[prev] + alpha * (1 + wordwithtagset[prev]))
                    transition = transition_p[prev][possible_tag]
                    #initial = alpha / (tagset["START"] + alpha * (1 + wordwithtagset["START"]))
                    initial = initial_p[possible_tag]
                    #prob = math.log(transition) + math.log(emission) + math.log(initial)
                    prob = math.log(transition + emission + initial)
                    #prob = transition * emission * initial
                    if (max_prob < prob):
                        max_prob = prob
                        final_tag = possible_tag
                #print("hi")
                #inal_tag = "NOUN"

                emission = alpha / (tagset[possible_tag] + alpha * (1 + wordwithtagset[possible_tag]))
                transition = transition_p[prev][possible_tag]
                initial = initial_p[possible_tag]
                prob = math.log(emission + transition + initial)
                prob = math.log(transition) + math.log(emission) + math.log(initial)
                if (max_prob < prob):
                    max_prob = prob
                    final_tag = possible_tag
            else:
                for possible_tag in dataset[word]:
                    transition = 0
                    emission = 0
                    if (possible_tag in dataset[word]): #smooth emission
                        emission = dataset[word][possible_tag] + alpha
                        emission = emission / (tagset[possible_tag] + alpha * (1 + wordwithtagset[possible_tag]))
                    else:
                        #emission = alpha / (tagset[possible_tag] + alpha * (1 + wordwithtagset[possible_tag]))
                        emission = 10 ** -6
                    transition = transition_p[prev][possible_tag]

                    if (prev in tagtagset[possible_tag]):
                        transition = tagtagset[possible_tag][prev] + alpha
                        transition = transition / (tagset[prev] + alpha * (1 + wordwithtagset[prev]))
                    else:
                        #transition = alpha / (tagset[prev] + alpha * (1 + wordwithtagset[prev]))
                        transition = 10 ** -6

                    #transition = tagtagset[possible_tag][prev]
                    #transition = transition / tagset[prev]
                    #emission = dataset[word][possible_tag] / tagset[possible_tag]

                    initial = tagset[possible_tag] / total_num
                    if (word == "START"):
                        initial = tagset[word] + alpha
                        initial = initial / (tagset["START"] + alpha * (1 + wordwithtagset["START"]))
                    else:
                        #initial = alpha / (tagset["START"] + alpha * (1 + wordwithtagset["START"]))
                        initial = 10 ** -6

                    initial = initial_p[possible_tag]
                    prob = math.log(transition) + math.log(emission) + math.log(initial)
                    #prob = math.log(transition + emission + initial)
                    #prob = transition * emission * initial

                    if (max_prob < prob):
                        max_prob = prob
                        final_tag = possible_tag
            '''

            #print(max_prob)
            prev_prev = prev
            prev = final_tag
            temp.append((word, final_tag))
        predicts.append(temp)
    #raise Exception("You must implement me")
    return predicts
