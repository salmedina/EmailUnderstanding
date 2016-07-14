'''
Created on Jul 12, 2016

@author: zhongzhu
'''
from document2vec.corpora import SeriesCorpus
from document2vec.document2vec import Document2Vec

from gensim.models.word2vec import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize

import DBUtil
import pandas as pd


db = DBUtil.initDB()
email = db.get_brushed_email(1)
raw = email.body
sentences = []
raw_sens = sent_tokenize(raw)
for raw_sen in raw_sens:
    sentences.append(word_tokenize(raw_sen))

model = Word2Vec(sentences, size=100, window=5, min_count=1, workers=4)
model.save_word2vec_format("model.txt")

# This must be a gensim Word2Vec or Doc2Vec pickle
d2v = Document2Vec("model.txt")
sentences = pd.Series(['i love jackets', 'blue is my favorite color'])
corpus = SeriesCorpus(sentences)
doc_vectors = d2v.transform(corpus)