import email
import flanker
import talon
import sqlalchemy
import ConfigParser
import EnronDB

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

def build_init_file(filename):
    ''' Builds the empty config file for the importer '''
    config = ConfigParser.ConfigParser()
    config.add_section('Database')
    
    config.set('Database', 'ip', '')
    config.set('Database', 'username', '')
    config.set('Database', 'password', '')
    config.set('Database', 'name', '')
    
    config.write(open(filename, 'w'))        
    return config    

def load_init_file(init_filename):
    ''' Loads the initfile that has the same name as the script, if not found -> generates an empty one '''
    config = ConfigParser.ConfigParser()
    
    if os.path.isfile(init_filename):    
        config.read(init_filename)
    else:
        config = build_init_file(init_filename)
    
    return config

if __name__=='__main__':
    # Load config file
    cfg = load_init_file('emailimporter.ini')
    
    # Initialize db object
    enron_db = EnronDB()
    enron_db.init(cfg.get('Database', 'ip'),
                  cfg.get('Database', 'username'),
                  cfg.get('Database', 'password'),
                  cfg.get('Database', 'name'),)
    
    # Import the final mails into db
    import_mails(mail_dir, enron_db)