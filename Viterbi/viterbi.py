"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
import operator

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


def baseline(train, test):
    '''
    TODO: implement the baseline algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    dataset,countset = sort(train)
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

def sort2(train):

    word_tag_pair = {} #2D
    tag_count = {} #1D
    tag_given_prev = {}#2D
    tag_word_pair = {}
    total_num_word = 0

    for sentence in train:
        prev_tag = ''
        for word, tag in sentence:
            total_num_word += 1

            # set word_tag_pair
            if (word not in word_tag_pair):
                word_tag_pair[word] = {}
            if (tag not in word_tag_pair[word]):
                word_tag_pair[word][tag] = 1
            else:
                word_tag_pair[word][tag] += 1

            #set tag_count
            if (tag not in tag_count):
                tag_count[tag] = 1
            else:
                tag_count[tag] += 1

            #tag_word_pair
            if (tag not in tag_word_pair):
                tag_word_pair[tag] = {}

            if (word not in tag_word_pair[tag]):
                tag_word_pair[tag][word] = 1
            else:
                tag_word_pair[tag][word] += 1


            #set tag_given_prev
            if (tag is not 'START'):
                if (prev_tag not in tag_given_prev):
                    tag_given_prev[prev_tag] = {}

                if (tag not in tag_given_prev[prev_tag]):
                    tag_given_prev[prev_tag][tag] = 1
                else:
                    tag_given_prev[prev_tag][tag] += 1
            prev_tag = tag

    return word_tag_pair, tag_count, tag_given_prev, total_num_word, tag_word_pair

def calculate_probability(word_tag_pair, tag_count, tag_given_prev, total_num_word, tag_word_pair, train):
    emission_probability = {}
    transition_probability = {}
    initial_probability = {}
    alpha = 0.001
    #set emission_probability
    '''
    for word in word_tag_pair:
        emission_probability[word] = {}
        for possible_tag in tag_count:
            num_of_word = sum(word_tag_pair[word].values())
            #if the word had this possible tag tagged
            if (possible_tag in word_tag_pair[word]):
                #emission_probability[word][possible_tag] = math.log(word_tag_pair[word][possible_tag] / num_of_word)
                emission_probability[word][possible_tag] = math.log((word_tag_pair[word][possible_tag] + alpha) / (tag_count[possible_tag] + alpha * 18))
                #emission_probability[word][possible_tag] = math.log((tag_word_pair[possible_tag][word] + alpha) / (tag_count[possible_tag] + alpha * 18))
            else:
                #what do i do?
                emission_probability[word][possible_tag] = math.log(alpha / (alpha * 18 + total_num_word))
    '''
    #set transition_probability
    for possible_prev_tag in tag_count:
        transition_probability[possible_prev_tag] = {}
        for possible_tag in tag_count:
            probability = 0
            #if possible_prev_tag-possible_tag pair have occured in training
            if (possible_tag in tag_given_prev[possible_prev_tag]):
                probability = (tag_given_prev[possible_prev_tag][possible_tag] + alpha )/(tag_count[possible_prev_tag]  + alpha * 18)
                #probability = tag_given_prev[possible_prev_tag][possible_tag] / (tag_count[possible_prev_tag])
            else:
                #what do i do?
                probability = alpha / (tag_count[possible_prev_tag] + alpha * 18)
            transition_probability[possible_prev_tag][possible_tag] = math.log(probability)



    #set initial probability
    for tag in tag_count:
        if (tag is 'START'):
            initial_probability[tag] = math.log(0.999999999999999999999999999999999)
        else:
            initial_probability[tag] = math.log(10 ** -30)
    return emission_probability, transition_probability, initial_probability

def calculate_emission(word, possible_tag, tag_word_pair, tag_count, total_num_word, alpha):

    temp = tag_count[possible_tag] / total_num_word
    emission = alpha * temp / (alpha * 18 + total_num_word)

    if (word in tag_word_pair[possible_tag]):

        emission = (tag_word_pair[possible_tag][word] + alpha * temp) / (18 * alpha + tag_count[possible_tag])

    return math.log(emission)

def viterbi(train, test):
    '''
    TODO: implement the Viterbi algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    word_tag_pair, tag_count, tag_given_prev, total_num_word, tag_word_pair = sort2(train)
    emission_probability, transition_probability, initial_probability = calculate_probability(word_tag_pair, tag_count, tag_given_prev, total_num_word, tag_word_pair, train)
    predicts = []
    unseen = {}
    alpha = 0.001
    cnt = 1
    for sentence in test:
        cnt += 1
        prev_prob = {}
        table = {}
        words = []
        word_idx = 0
        for word in sentence:
            if (word not in word_tag_pair):
                if (word not in unseen):
                    unseen[word] = 1
                else:
                    unseen[word] += 1
            #table[word] = {}
            table[word_idx] = {}
            probability_table = {}
            words.append(word)
            if (word == 'START'):
                for possible_tag in tag_count:
                    emission = calculate_emission(word, possible_tag, tag_word_pair, tag_count, total_num_word, alpha)
                    probability_table[possible_tag] = initial_probability[possible_tag] + emission
            else:
                for possible_tag in tag_count:
                    max = -math.inf
                    max_tag = ''
                    for prev_tag in prev_prob:
                        prob = prev_prob[prev_tag] + transition_probability[prev_tag][possible_tag]
                        if (max <= prob):
                            max = prob
                            max_tag = prev_tag
                    emission = calculate_emission(word, possible_tag, tag_word_pair, tag_count, total_num_word, alpha)
                    probability_table[possible_tag] = max + emission
                    #table[word][possible_tag] = max_tag
                    table[word_idx][possible_tag] = max_tag
            word_idx += 1
            prev_prob = probability_table

        curr_tag = 'START'
        for key in prev_prob:
            if (prev_prob[key] > prev_prob[curr_tag]):
                curr_tag = key
        temp = []
        #words.reverse()
        for i in range(len(words)):
            curr_word = words[len(words) - 1 - i]
            temp.append((curr_word, curr_tag))
            if (i < len(words) - 1):
                curr_tag = table[len(words) - 1 - i][curr_tag]

        temp.reverse()
        if (cnt == 50):
            print(temp)
        predicts.append(temp)

    #print(predicts)
    #raise Exception("You must implement me")
    predicts2 = []
    for sentence in predicts:
        list = []
        for word in sentence:
            if (word[0] in unseen):
                list.append((word[0], "NOUN"))
            else:
                list.append(word)
        predicts2.append(list)
    return predicts2
