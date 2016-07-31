import re
import summarize
import EnronDB

def remove_invalid_unicode(inStr):
    return re.sub(r'[^\x00-\x7f]',r' ',inStr)

def store_summary_in_db(edb, email_id, text):
    edb.update_brushed_summary(email_id, text)

def main():
    '''Summarize emails and store in DB'''
    # Initialize the DB
    edb = EnronDB.EnronDB()
    edb.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo','enron_experiment')
    # Read all the bodies from the brushed table
    emails = edb.get_all_brushed_bodies_with_id()

    # For each of the emails 
    for email_id, body in emails:
        if email_id == 736:
            continue
        print 'Summarizing email %d '%(email_id)
        body = remove_invalid_unicode(body)
        # Summarize the email
        email_summary = summarize.summarize_text(body)
        # Transform list to text
        email_summary_text = '\n'.join(email_summary.summaries)
        # Store in DB
        store_summary_in_db(edb, email_id, email_summary_text)

if __name__=='__main__':
    main()