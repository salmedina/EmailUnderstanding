'''
Created on Jul 14, 2016

@author: zhongzhu
'''
import os
from random import shuffle

from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence, TaggedDocument
import numpy
from sklearn.linear_model import LogisticRegression

import DBUtil


# numpy
# random
# classifier
class LabeledLineSentence(object):
    def __init__(self, emails):
        self.emails = emails
    
    def __iter__(self):
        for email in self.emails:
            yield TaggedDocument(utils.to_unicode(email.one_line).split(), ['email_%s' % email.id])
            
#         for source, prefix in self.sources.items():
#             with utils.smart_open(source) as fin:
#                 for item_no, line in enumerate(fin):
#                     yield TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
    
    def to_array(self):
        self.sentences = []
        for email in self.emails:
            taggedDoc = TaggedDocument(utils.to_unicode(email.one_line).split(), ['email_%s' % email.id])
            self.sentences.append(taggedDoc)
        return self.sentences

#         self.sentences = []
#         for source, prefix in self.sources.items():
#             with utils.smart_open(source) as fin:
#                 for item_no, line in enumerate(fin):
#                     self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
#         return self.sentences
    
    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences
    
def train_model():
    db = DBUtil.initDB()
    emails = db.get_all_brushed_emails()
    sentences = LabeledLineSentence(emails)
    model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)

    model.build_vocab(sentences.to_array())

    for epoch in range(10):
        model.train(sentences.sentences_perm())
    model.save('./trained_model.d2v')

if not os.path.isfile("./trained_model.d2v"):
    print("Model doesn't exist, training...")
    train_model()

model = Doc2Vec.load('./trained_model.d2v')
# print(model.docvecs['email_1'])
# print(model.docvecs.doctags)
# print('email_1' in model.docvecs.doctags.keys())
# print(len(model.docvecs.doctags.keys()))
# print(model['email_1'])

# print model.most_similar('i')


db = DBUtil.initDB()
emails = db.get_all_brushed_emails()

train_arrays = []
train_labels = []
test_arrays = []
test_labels = []

for email in emails:
    i = email.id
    prefix_train_pos = 'email_' + str(i)
    if i % 5 != 0:
        train_arrays.append(model.docvecs[prefix_train_pos])
        train_labels.append(int(email.label))
    else:
        test_arrays.append(model.docvecs[prefix_train_pos])
        test_labels.append(int(email.label))
        
classifier = LogisticRegression()
classifier.fit(numpy.array(train_arrays), numpy.array(train_labels))

print("Overall score is %f." % classifier.score(numpy.array(test_arrays), numpy.array(test_labels)))

corrects = []
wrongs = []
for email in emails:
    i = email.id
    prefix_train_pos = 'email_' + str(i)
    if i % 5 == 0:
        prediction = classifier.predict([model.docvecs[prefix_train_pos]])[0]
        actual = int(email.label)
        if prediction != actual:
            wrongs.append((email.id, prediction, actual))
        else:
            corrects.append(email.id)

print("%i are wrong, %i are correct." % (len(wrongs), len(corrects)))
for w in wrongs:
    print w