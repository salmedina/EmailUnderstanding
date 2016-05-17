import email
import flanker
import talon
import sqlalchemy


def import_mails(mail_dir, db):
    # Traverse through all directories recursively
    
    # When no more subdirs...
    # For each file
    # Parse the email 
    # save the email in the DB
    # DB fields:
    #     - Datetime
    #     - From
    #     - To
    #     - Subject
    #     - Type
    #     - Body
    #     - file_path: relative path from source
    pass

if __name__=='__main__':
    # if no config file, create default and exit
    
    # Load config file
    
    # Initialize db object
    
    # Import the final mails into db
    import_mails(mail_dir, db)