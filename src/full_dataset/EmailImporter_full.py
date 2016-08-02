import datetime
import email
from email.utils import parsedate
import os
import time

from EmailContentCleaner import clean
from EnronDB import Email
import EnronDB


mail_root = "/Volumes/My Passport/data/maildir/allen-p"

def import_mails(mail_dir, db):
    processed_count = 0
    # Traverse through all directories recursively
    for dirpath, _, filenames in os.walk(mail_dir):
        for filename in filenames:
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
                e.body = clean(raw_email.get_payload())
                e.path = filepath[len(mail_root):]
            db.insert_raw_email_full(e)
            processed_count += 1
    print(str(processed_count) + " emails processed.")

if __name__ == '__main__':
    enron_db = EnronDB.EnronDB()
    enron_db.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')
    
    # Import the final mails into db
    import_mails(mail_root, enron_db)
