import datetime
import email
from email.utils import parsedate
import os
import re
import time

from DBUtil import initDB
from EnronDB import Email


mail_root = "/Users/zhongzhu/Documents/code/EmailUnderstanding/data/Emails_with_label"

def import_mails(mail_dir, db):
    # Traverse through all directories recursively
    for dirpath, _, filenames in os.walk(mail_dir):
        match = re.search(r"Emails_with_label/(?P<label>\d+)/", dirpath)
        if match:
            label = match.group("label")
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
                e.body = raw_email.get_payload()
                e.path = filepath[len(mail_root):]
                e.label = int(label)
            db.insert_email(e)

if __name__ == '__main__':
    enron_db = initDB()
    
    # Import the final mails into db
    import_mails(mail_root, enron_db)