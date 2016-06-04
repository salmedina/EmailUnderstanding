import datetime
import email
from email.utils import parsedate
import os
import time

from DBUtil import initDB
from EnronDB import Email


mail_root = "/Users/zhongzhu/Documents/code/EmailUnderstanding/data/"

# import flanker
# import talon
def import_mails(mail_dir, db):
    # Traverse through all directories recursively
    for dirpath, dirnames, filenames in os.walk(mail_dir):
        for dirname in dirnames:
            import_mails(os.path.abspath(os.path.join(dirpath, dirname)), db)
        for filename in filenames:
            if filename == ".DS_Store":
                continue
            filepath = os.path.abspath(os.path.join(dirpath, filename))
            with open(filepath) as f:
                print(filepath)
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
            db.insert_email(e)

if __name__ == '__main__':
    enron_db = initDB()
    
    # Import the final mails into db
    import_mails(mail_root, enron_db)