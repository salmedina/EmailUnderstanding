import os
import re
import nltk
import collections
import EnronDB
from nltk.stem.wordnet import WordNetLemmatizer
import multiprocessing as mp
import cPickle as pickle


def flatten_list(inList):
    return [item for sublist in inList for item in sublist]

def extract_pos_of_sentence(sentence):
    sentencesTokens = nltk.word_tokenize(sentence)  # Converts into list of words
    posTokens = nltk.pos_tag(sentencesTokens)       # Return list of tuples (word, POS)
    return posTokens

def get_verbs_from_sentence_pos(posSentence):
    verbs = []
    return [word for word,pos in posSentence if re.match(r'VB.*', pos)]

def lemmatize_verb(verbs):
    lemmatizer = WordNetLemmatizer()
    return map(lambda x:lemmatizer.lemmatize(x, 'v'),verbs)

def mp_lemmatize_verbs(verbs):
    return mp_process_iterable(lemmatize_verb, verbs)

def mp_get_verbs(posSentences):
    return mp_process_iterable(get_verbs_from_sentence_pos, posSentences)
    
def mp_extract_pos(sentences):
    return mp_process_iterable(extract_pos_of_sentence, sentences)

def mp_lemmatize_verbs(verbs):
    return mp_process_iterable(lemmatize_verb, verbs)

def mp_process_iterable(func, iterable):
    numThreads = mp.cpu_count()-1
    pool = mp.Pool(numThreads)
    
    res = pool.map(func, iterable)
    
    pool.close()
    pool.join()
    
    return res

def extract_lemmatized_verbs(sentence):
    sentence_pos = extract_pos_of_sentence(sentence)
    sentence_verbs = get_verbs_from_sentence_pos(sentence_pos)
    lemma_verbs = lemmatize_verb(sentence_verbs)

    return lemma_verbs

def get_brushed_lines_from_db():
    '''Gets a list of the email body from the database'''
    edb = EnronDB.EnronDB()
    edb.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo','enron_experiment')
    body_list = edb.get_all_brushed_lines_with_id()
    return body_list

def update_verbs(email_id, verb_list):
    edb = EnronDB.EnronDB()
    edb.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo','enron_experiment')
    verbs = ', '.join(verb_list)
    edb.update_brushed_verbs(email_id, verbs)

def extract_all_verbs():
    # Get all the bodies from the emails and their respective id's
    emails = get_brushed_lines_from_db()
    
    # For each of the emails
    for email_id, email_body in emails:
        print 'PROCESSING EMAIL: %d'%(email_id)
        # get all the lines
        lines = email_body.split('\n')
        
        # extract the sentences
        sentences = []
        for line in lines:
            sentences.append(nltk.sent_tokenize(line))
        sentences = flatten_list(sentences)
        
        # calculate the POS
        posSentences = mp_extract_pos(sentences)
        # extract the verbs
        verbs = mp_get_verbs(posSentences)
        # lemmative the verbs
        lemmatizedVerbs = mp_lemmatize_verbs(verbs)
        # get a full list of verbs
        lemmatizedVerbs = flatten_list(lemmatizedVerbs)
        # store in the db
        update_verbs(email_id, lemmatizedVerbs)
        

if __name__=='__main__':
    extract_all_verbs()