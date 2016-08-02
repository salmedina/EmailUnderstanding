'''
Created on Aug 1, 2016

@author: zhongzhu
'''
import EnronDB
from EmailImporter_full import import_mails
from BrushEmails_full import brush_emails
from SchedulingEmailClassifier_nb import print_scheduling_emails_prediction


enron_db = EnronDB.EnronDB()
enron_db.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')

# Import the final mails into db
import_mails("/Volumes/My Passport/data/maildir/allen-p", enron_db)
import_mails("/Volumes/My Passport/data/maildir/arnold-j", enron_db)
import_mails("/Volumes/My Passport/data/maildir/arora-h", enron_db)
import_mails("/Volumes/My Passport/data/maildir/badeer-r", enron_db)
# result: [3097, 3686, 4281, 4316, 4477, 4480, 4484, 4563, 4622, 4656, 5070, 5159, 6281, 6692, 7087, 7153, 7353, 7354, 7817, 7846, 7959, 7960, 8040, 8153, 8207, 8922, 9069, 9136, 9168, 9172, 9226, 9289, 9605, 10016, 10307, 10568, 11297, 11691, 11790, 11851, 11922, 12031, 12049, 12144, 12209, 12278, 12331, 12434]

brush_emails()

print_scheduling_emails_prediction()