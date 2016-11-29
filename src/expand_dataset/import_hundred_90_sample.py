'''
Created on Aug 4, 2016

@author: zhongzhu
'''
import random
from DBWrapper import EnronDB


db = EnronDB.holbox_db()

# all_scheduling = db.get_all_email_predictions_greater_than(0.9)
#  
# print([(e.id, e.probability) for e in all_scheduling])
#  
# seq = range(len(all_scheduling))
# random.shuffle(seq)
#  
# sample_emails = []
# random_hundred = seq[:100]
# for n in random_hundred:
#     sample_emails.append(all_scheduling[n])
#      
# db.create_sample_table("sample_100_email_90")
# for se in sample_emails:
#     db.insert_sample_email("sample_100_email_90", se)

all_sample_emails = db.get_sample_emails("sample_100_email_90")
correct = [e for e in all_sample_emails if e.manual_label == 1]
wrong = [e for e in all_sample_emails if e.manual_label != 1]
 
print("precision is %f." % (len(correct) * 1.0 / len(all_sample_emails)))