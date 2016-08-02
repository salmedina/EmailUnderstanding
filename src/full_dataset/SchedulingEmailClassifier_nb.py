'''
Created on Jul 22, 2016

@author: zhongzhu
'''
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import EnronDB

def save_scheduling_emails_prediction():
    db = EnronDB.EnronDB()
    db.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')
    emails = db.get_all_brushed_emails()
    raw_documents = []
    targets = []
    for email in emails:
        raw_documents.append(email.subject + ' ' + email.one_line)
        targets.append(email.is_scheduling)

    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])

    parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
                  'tfidf__use_idf': (True, False),
                  'clf__alpha': (1e-2, 1e-3, 1e-4)}
    gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(raw_documents, targets)

    test_documents = []
    test_emailids = []
    for email in db.get_all_brushed_email_more():
        test_documents.append(email.subject + ' ' + email.one_line)
        test_emailids.append(int(email.id))

    predicted = gs_clf.predict(test_documents)
    predicted_scheduling = []
    for i in range(len(predicted)):
        if predicted[i] == 1:
            predicted_scheduling.append(test_emailids[i])
            
    with open("final_result.txt", "w+") as f:
        f.write(predicted_scheduling)

def print_scheduling_emails_prediction():
    db = EnronDB.EnronDB()
    db.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')
    emails = db.get_all_brushed_emails()
    raw_documents = []
    targets = []
    for email in emails:
        raw_documents.append(email.subject + ' ' + email.one_line)
        targets.append(email.is_scheduling)

    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])

    parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
                  'tfidf__use_idf': (True, False),
                  'clf__alpha': (1e-2, 1e-3, 1e-4)}
    gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(raw_documents, targets)

    test_documents = []
    test_emailids = []
    for email in db.get_all_brushed_emails_full():
        test_documents.append(email.subject + ' ' + email.one_line)
        test_emailids.append(int(email.id))

    predicted = gs_clf.predict(test_documents)
    predicted_scheduling = []
    for i in range(len(predicted)):
        if predicted[i] == 1:
            predicted_scheduling.append(test_emailids[i])
            
    print(predicted_scheduling)