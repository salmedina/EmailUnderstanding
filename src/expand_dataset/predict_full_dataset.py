'''
Created on Aug 1, 2016

@author: zhongzhu
'''
import datetime
import email
from email.utils import parsedate
import os
import re
import string
import time

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from DBWrapper import EnronDB, Email
import multiprocessing as mp


db = EnronDB("email_prediction")
db.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')
db.create_table()

# create classifier
print("Training...")
emails = db.get_all_brushed_emails()
raw_documents = []
targets = []
for e in emails:
    raw_documents.append(e.subject + ' ' + e.one_line)
    targets.append(e.is_scheduling)

text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])

parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
              'tfidf__use_idf': (True, False),
              'clf__alpha': (1e-2, 1e-3, 1e-4)}
gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(raw_documents, targets)

print("Training completed!")

exclude_set = set(string.punctuation)

def clean(body):
    new_body = ""
    lines = body.split("\n")
    for line in lines:
        cleaned_line = re.sub(r"(^.*?(From|Sent|To|Cc):.*$|=20|=09|=\s*$|^.*Original Message.*$|^\s+)", "", line)
        if line.endswith("="):
            new_body += cleaned_line
        else:
            new_body += " " + cleaned_line
    return new_body

def regexp_pos(s, pattern):
    '''Returns -1 if pattern was not found, otherwise it returns the position of the regex'''
    search_res = re.search(pattern, s)
    if search_res is None:
        return -1
    return search_res.start()

def remove_block(s, start_pattern, end_patterns):
    lines = s.split('\n')
    filtered_lines = []
    filtering = False
    for line in lines:
        if regexp_pos(line.lower(), start_pattern) != -1:
            filtering = True
            continue
        for pattern in end_patterns:
            if regexp_pos(line.lower(), pattern) != -1:
                filtering = False
                filtered_lines.append('')
                continue
        if not filtering:
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def replace_weblinks(msg):
    # url_regex = r'[<]?http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@\.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[>]?'
    url_regex = r'[<]?http[s]?://(?:[a-zA-Z]|[0-9]|[_.\-/@&+=$?]|[!\*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[>]?'
    # replace the weblinks with WEBLINK token
    urls = re.findall(url_regex, msg)
    for url in urls:
        msg = msg.replace(url, 'WEBLINK')
    return msg

def remove_original_message(msg):
    return remove_block(msg, r'[- ]{3,}original message', [r'to:.*', r'cc:.*', r'subject:.*'])

def remove_forward_header(msg):
    return remove_block(msg, r'[- ]{3,}forward', [r'to:.*', r'cc:.*', r'subject:.*'])

def remove_reply_header(msg):
    return remove_block(msg, r'\w+ <?\w+@[A-Z]+>?', [r'to:.*', r'cc:.*', r'subject:.*'])

def remove_attachments(msg):
    lines = msg.split('\n')
    filtered_lines = []
    for line in lines:
        if regexp_pos(line.lower(), r'<{1,}[\w -_\':]+.[\w ]+>{1,}') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'- [\w -_\':]+.\w{2,5}$') != -1:
            filtered_lines.append('')
            continue        
        
        filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def remove_confidentiality_notice(msg):
    lines = msg.split('\n')
    filtered_lines = []
    filtering = False
    for line in lines:
        if regexp_pos(line.lower(), r'confidentiality not') != -1:
            filtering = True
            continue
        if len(line) < 1:
            filtering = False
            filtered_lines.append('')
            continue
        if not filtering:
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def remove_misc(msg):
    lines = msg.split('\n')
    filtered_lines = []
    for line in lines:
        # Email like
#         if regexp_pos(line.lower(), r'[\w/]+@\w+') != -1:
#             filtered_lines.append('')
#             continue
        if regexp_pos(line.lower(), r'to:\w*') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'cc:\w*') != -1:
            filtered_lines.append('')
            continue        
        if regexp_pos(line.lower(), r'from:\w*') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'phone:\w*') != -1:
            filtered_lines.append('')    
            continue
        if regexp_pos(line.lower(), r'subject:\w*') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'sent:\w*') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'sent by:\w*') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'importance:\w*') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'tel[:.]?\w*') != -1:
            filtered_lines.append('')
            continue        
        if regexp_pos(line.lower(), r'fax:?\w*') != -1:
            filtered_lines.append('')
            continue
        if regexp_pos(line.lower(), r'facsimile:\w*') != -1:
            filtered_lines.append('')        
            continue
        if regexp_pos(line.lower(), r'\d\d/\d\d/\d\d\d\d[ \t]+\d\d:\d\d( [AP]M)?') != -1:
            filtered_lines.append('')        
            continue
        
        filtered_lines.append(line)
        
    return '\n'.join(filtered_lines)

def concat_paragraph_lines(msg):
    lines = msg.split('\n')
    
    cat_lines = []
    tmp_line = lines[0] + ' '
    i = 1
    while i < len(lines):
        if len(lines[i].strip()) < 1:
            cat_lines.append(tmp_line)
            tmp_line = ''
        else:
            tmp_line += lines[i] + ' '
        i += 1
    if len(tmp_line) > 0:
        cat_lines.append(tmp_line)
    
    return '\n'.join(cat_lines)

    
def process_email(msg):
    lines = msg.split('\n')
    stripped_lines = []
    for line in lines:
        # Remove the empty spaces, tabs and > of forwarded or replied messages
        strpd_line = line.lstrip(' >\t')
        # Replace lines that only contain '?' with empty space
        if strpd_line == '?':
            strpd_line = ''
        stripped_lines.append(strpd_line)
    brushed_body = '\n'.join(stripped_lines)

    # REPLACE weblinks
    brushed_body = replace_weblinks(brushed_body)

    # REMOVE the forwarding/replying blocks
    # ORIGINAL MESSAGE
    filt_1_body = remove_original_message(brushed_body)
    # FORWARDED BY
    filt_2_body = remove_forward_header(filt_1_body)
    # REPLY no separating line header
    filt_3_body = remove_reply_header(filt_2_body)
    # ATTACHMENT placeholders i.e. <file_name>
    filt_4_body = remove_attachments(filt_3_body)
    # CONFIDENTIALITY NOTICE paragraphs from the company
    filt_5_body = remove_confidentiality_notice(filt_4_body)
    # EXTRAS any other eleemnt that could not be removed 
    final_body = remove_misc(filt_5_body)

    # Replace more than two new lines into two newlines
    if re.search('\n{3,}', final_body, re.IGNORECASE):
        r = re.compile(r'\n{3,}', re.IGNORECASE)
        final_body = r.sub(r'\n\n', final_body)  # substitute string        

    # remove the empty spaces at the beginning and the end
    strip_body = final_body.strip()

    # cat_body = concat_paragraph_lines(strip_body)
    return strip_body


def import_and_clean_email_in_folder(mail_dir):
    start = datetime.datetime.now()
    processed_emails = []
    processed_count = 0
    # Traverse through all directories recursively
    for dirpath, _, filenames in os.walk(mail_dir):
        for filename in filenames:
            try:
                if filename in [".DS_Store", ".gitignore"]:
                    continue
                filepath = os.path.abspath(os.path.join(dirpath, filename))
                with open(filepath) as f:
                    raw_email = email.message_from_file(f)
                    e = Email()
                    if raw_email['Date']:
                        e.date = datetime.datetime.fromtimestamp(time.mktime(parsedate(raw_email['Date'])))
                    e.mime_type = raw_email['Content-Type']
                    e.from_addr = raw_email['From']
                    e.to_addr = raw_email['To']
                    e.subject = raw_email['Subject']
                    # TODO use the actual raw_body 
                    e.raw_body = raw_email.get_payload()
                    # Process the email body
                    e.cleaned_body = process_email(clean(e.raw_body))
                    e.all_lines = concat_paragraph_lines(e.cleaned_body)
                    e.path = filepath
                    # To lower case and remove unwanted chars 
                    e.one_line = ''.join(ch for ch in e.cleaned_body.lower().translate(None, '\n\t\r') if ch not in exclude_set)
                    e.prediction = gs_clf.predict([e.subject + ' ' + e.one_line])[0]
                    e.probability = gs_clf.predict_proba([e.subject + ' ' + e.one_line])[0][1]
                    # Store in DB
                # insert later
                processed_emails.append(e)
#                 db.insert_email(e)
                processed_count += 1
            except:
                print("Error processing %s." % filename)
    end = datetime.datetime.now()
    
    print("%i emails processed in %ss in %s." % (processed_count, (end - start).seconds, mail_dir))
    return processed_emails

def mp_process_iterable(func, iterable):
    '''
    This function launches into N-1 threads the current action, where N is the number of cores
    '''
    numThreads = mp.cpu_count() - 1
    pool = mp.Pool(numThreads)
    
    res = pool.map(func, iterable)
    
    pool.close()
    pool.join()
    
    return res
    
if __name__ == '__main__':
    root_dir = "../maildir/"
    if not root_dir.endswith('/'):
        print("root_dir should end with '/', otherwise it won't work.")
        exit(1)
    all_dirs = os.listdir(root_dir)
    if ".DS_Store" in all_dirs:
        all_dirs.remove(".DS_Store")
    folders = [(root_dir + d) for d in all_dirs]
    all_emails = mp_process_iterable(import_and_clean_email_in_folder, folders)
    count = 0
    print("Processing completed! Inserting...")
    for sublist in all_emails:
        for em in sublist:
            db.insert_email(em)
            count += 1
        print("%i emails are inserted successfully!" % len(sublist))
    print("Totally %i emails are inserted successfully from %i folders!" % (count, len(all_emails)))
#     import_and_clean_email_in_folder("../maildir/allen-p/discussion_threads/")
