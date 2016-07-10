'''
Created on Jun 13, 2016

@author: zhongzhu
'''
import summarize

from DBUtil import initDB
import DBUtil
from EnronDB import labels


def summarize_and_filter_all():
    sum_ratio = 4
    db = DBUtil.initDB()

    emails = db.get_all_brushed_emails()
    files = []
    for i in range(1, 15):
        files.append(open("label" + str(i) + ".log", "w+"))
    for email in emails:
        f = files[email.label - 1]
        if "=" in email.body:
            continue
        try:
            summaries = summarize.summarize_text(email.body).summaries
            if len(summaries) > 7:  # TLDR
                continue

            summary_cat = ""
            for summary in summaries:
                summary_cat += summary + "\n"
            
            if len(summary_cat) == 0 or len(email.body) / len(summary_cat) < sum_ratio:  # not really summarizing
                continue
            f.write("-" + str(email.id) + "-\n\n")
            f.write(summary_cat.encode('utf8'))
            f.write("\n")
        except:
            continue

    for f in files:
        f.close()

def samples():
    with open("samples.txt", "w+") as f:
        email_ids = [247, 334, 382, 480, 558, 664, 718, 785, 834, 887, 1022]
        db = initDB()
        for id in email_ids:
            email = db.get_brushed_email(id)
            f.write(">>> raw data <<<\n")
            f.write("\tID: \t\t" + str(id) + "\n")
            f.write("\tLabel: \t\t" + labels[email.label] + "\n")
            f.write("\tSubject: \t" + email.subject + "\n")
            f.write("\tBody: \n" + email.body)
            f.write("\n\n>>> summary <<<\n")
            
            summaries = summarize.summarize_text(email.body).summaries
            for summary in summaries:
                f.write(summary.encode('utf8') + "\n")
            
            f.write("\n\n------\n\n")
        
samples()