'''
Created on Jun 4, 2016

@author: zhongzhu
'''
import operator
from EnronDB import EnronDB
from DBUtil import initDB

def getTopWords(num, doc):
    word_freq = {}
    for word in doc.split():
        word = word.lower()
        if not word.isalnum():
            continue
        if word not in word_freq:
            word_freq[word] = 1
            continue
        word_freq[word] += 1
    sorted_word_freq = sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_word_freq[:num]

def getEmailTop10000Words():
    db = initDB()
    top_words = getTopWords(10000, db.get_all_content())
    return top_words