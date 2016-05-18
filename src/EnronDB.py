import sys
import sqlalchemy

class Email:
    def __init__(self):
        self.date = ''
        self.mime_type = ''
        self.from_addr = ''
        self.to_addr = ''
        self.subject = ''
        self.body = ''
        self.path = ''
        self.label = -1

class EmailAddress:
    def __init__(self):
        self.address = ''
        self.name = ''

class EnronDB:
    def __init__(self):
        self.engine = None
        self.metadata = ()
        
    def init(self, host, username, password, db_name):
        engine_desc = 'mysql://%s:%s@%s/%s'%(username, password, host, db_name)
        try:
            self.engine = create_engine(engine_desc)
            self.metadata.reflect(self.engine)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        return True    
    
    # RAW_EMAIL table
    def insert_email(self, email):
        if type(email) != Email:
            print 'ERROR: input must be of type Email'
            return
        
        email_table = Table('raw_email', self.metadata)
        ins_stmt = email_table.insert()
        conn = self.engine.connect()
        result = conn.execute(ins_stmt, date = email.date,
                              mime_type = email.mime_type,
                              from_addr = email.from_addr,
                              to_addr = email.to_addr,
                              subject = email.subject,
                              body = email.body,
                              path = email.path,
                              label = email.label)
    
    def get_email(self, email_id):
        email_table = Table('raw_email', self.metadata)
        sel_stmt = select([email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_addr, \
                           email_table.c.subject, email_table.c.body, \
                           email_table.c.path, email_table.c.label]).where(email_table.c.id == email_id)
        rp = self.engine.execute(sel_stmt)
        record = rp.first()
        email = Email()
        if record is not None:
            email.date = record.date
            email.mime_type = record.mime_type
            email.from_addr = record.from_addr
            email.to_addr = record.to_addr
            email.subject = record.subject
            email.body = record.body
            email.path = record.path
            email.label = record.label
        
        return email
        
    def get_emails_from(self, from_addr):
        email_table = Table('raw_email', self.metadata)
        sel_stmt = select([email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_addr, \
                           email_table.c.subject, email_table.c.body, \
                           email_table.c.path, email_table.c.label]).where(email_table.c.id == email_id)
        rp = self.engine.execute(sel_stmt)        
    
    def get_emails_before(self, date):
        pass
        
    # EMAIL_ADDRESS table
    def insert_address(self, email_address):
        if type(email) != EmailAddress:
            print 'ERROR: input must be of type EmailAddress'
            return
        
        email_address_table = Table('email_address', self.metadata)
        ins_stmt = email_address_table.insert()
        conn = self.engine.connect()
        result = conn.execute(ins_stmt, address = email_address.address,
                              name = email_address.name)
    
    # thread table