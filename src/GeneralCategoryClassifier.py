'''
Created on Jul 12, 2016

@author: zhongzhu
'''
import os

from sklearn import svm

import numpy as np
import DBUtil


def get_doc_vector(filename):
    with open(filename) as f:
        f.readline()  # skip the first line
        raw_content = f.read()

        word_vectors = []
        for line in raw_content.split("\n"):
            if not line:
                continue
            v = []
            for x in line.split(" ")[1:]:
                v.append(float(x))
            word_vectors.append(v)
            
        doc_vector = np.array([0] * len(word_vectors[0]))
        for vector in word_vectors:
#             doc_vector = np.multiply(doc_vector, np.array(vector))
            doc_vector = np.add(doc_vector, np.array(vector))
#         doc_vector = np.power(doc_vector, 1./len(word_vectors))
        doc_vector = np.divide(doc_vector, len(word_vectors))
    return doc_vector

training_set = []
categories = []
db = DBUtil.initDB()
for filename in os.listdir("../training_data"): 
    email_id = int(filename[6:-4])
    if email_id % 5 == 0:  # use 4 in every 5 emails as training set
        continue
    email = db.get_brushed_email(email_id)
    label = int(email.label)
    v = get_doc_vector("../training_data/" + filename)
    training_set.append(v)
    categories.append(label)

# clf = svm.SVC(decision_function_shape='ovo')
print("Training with dataset of " + str(len(training_set)) + " and categories are " + str(categories))
clf = svm.LinearSVC()
clf.fit(training_set, categories)

correct = []
wrong = []
for filename in os.listdir("../training_data"): 
    email_id = int(filename[6:-4])
    if email_id % 5 != 0:  # use the rest as test set
        continue
    email = db.get_brushed_email(email_id)
    label = int(email.label)
    v = get_doc_vector("../training_data/" + filename)
    prediction = clf.predict([v])[0]
#     print("email " + str(email_id) + ": predicting " + str(prediction) + " and actual is " + str(label))
    if prediction == label:
        correct.append((email_id, prediction, label))
    else:
        wrong.append((email_id, prediction, label))
    
print(str(len(correct)) + " are correct, " + str(len(wrong)) + " are wrong.")
# print(correct)
print(wrong)