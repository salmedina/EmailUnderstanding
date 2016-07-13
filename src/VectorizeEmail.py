'''
Created on Jul 10, 2016

@author: zhongzhu
'''
from gensim.models.word2vec import Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize
import DBUtil

db = DBUtil.initDB()
all_emails = db.get_all_brushed_emails()
for email in all_emails:
    try:
        raw = email.body
        sentences = []
        raw_sens = sent_tokenize(raw)
        for raw_sen in raw_sens:
            sentences.append(word_tokenize(raw_sen))

        model = Word2Vec(sentences, size=100, window=5, min_count=1, workers=4)
        model.save_word2vec_format("../training_data/model_" + str(email.id) + ".txt")
    except:
        print("Error processing email " + str(email.id))