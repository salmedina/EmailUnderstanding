import email
import re
import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.sql.schema import Table, MetaData

labels = {1:"Company business, strategy, alliances etc.",
          2:"Company image, PR, press releases",
          3:"Employment arrangements (hiring etc.)",
          4:"Empty message",
          5:"IT (Information technology)",
          6:"Jokes, humour, fun",
          7:"Legal and regulatory affairs",
          8:"Logistic arrangements (meetings etc.)",
          9:"News and newsletters",
          10:"Other",
          11:"Personal, Friends, Family",
          12:"Political influence and contacts",
          13:"Project work, general collaboration",
          14:"Spam"}

class Email:
    def __init__(self):
        self.id = -1
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
        self.metadata = MetaData()
        
    def init(self, host, username, password, db_name):
        engine_desc = 'mysql://%s:%s@%s/%s' % (username, password, host, db_name)
        try:
            self.engine = create_engine(engine_desc)
            self.metadata.reflect(self.engine)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        return True    
    
    # RAW_EMAIL table
    def insert_email(self, email):
        self.insert_to_table(email, "raw_email")
    
    # RAW_EMAIL table
    def insert_cleaned_email(self, email):
        self.insert_to_table(email, "cleaned_email")

    def insert_to_table(self, email, table_name):
        if not isinstance(email, Email):
            print 'ERROR: input must be of type Email'
            return
        
        email_table = Table(table_name, self.metadata)
        ins_stmt = email_table.insert()
        conn = self.engine.connect()
        result = conn.execute(ins_stmt, date=email.date,
                              mime_type=email.mime_type,
                              from_addr=email.from_addr,
                              to_addr=email.to_addr,
                              subject=email.subject,
                              body=email.body,
                              path=email.path,
                              label=email.label)
    
    def get_all_content(self):
        email_table = Table('raw_email', self.metadata)
        sel_stmt = select([email_table.c.subject, email_table.c.body])
        rp = self.engine.execute(sel_stmt)
        all_content = ""
        for record in rp:
            all_content += record.subject + " "
            all_content += record.body + " "
        return all_content
    
    def add_username(self):
        email_table = Table('brushed_email', self.metadata)
        sel_stmt = select([email_table.c.id, email_table.c.path])
        rp = self.engine.execute(sel_stmt)
        conn = self.engine.connect()
        for record in rp:
#             print(record)
            p = "\/[^\/]*\/([^\/]+)" # match the content between the second / and the third /
            match = re.match(p, record.path)
            if match:
                username = match.group(1)
                stmt = email_table.update().where(email_table.c.id==record.id).values(username=username)
                conn.execute(stmt)
            else:
                print("Error! " + record.path)
                exit(0)
    
    def get_all_dates(self):
        email_table = Table('raw_email', self.metadata)
        sel_stmt = select([email_table.c.date])
        rp = self.engine.execute(sel_stmt)
        dates = []
        for record in rp:
            dates.append(record.date.strftime("%y%m%d"))
        return dates

    def get_all_brushed_emails(self):
        email_table = Table('brushed_email', self.metadata)
        sel_stmt = select([email_table.c.id, email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_adddr, \
                           email_table.c.subject, email_table.c.body, \
                           email_table.c.path, email_table.c.label])
        rp = self.engine.execute(sel_stmt)
        emails = []
        for record in rp:
            email = Email()
            if record is not None:
                email.id = record.id
                email.date = record.date
                email.mime_type = record.mime_type
                email.from_addr = record.from_addr
                email.to_addr = record.to_adddr
                email.subject = record.subject
                email.body = record.body
                email.path = record.path
                email.label = record.label
            emails.append(email)
        return emails
    
    def get_brushed_email(self, email_id):
        email_table = Table('brushed_email', self.metadata)
        sel_stmt = select([email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_adddr, \
                           email_table.c.subject, email_table.c.body, \
                           email_table.c.path, email_table.c.label]).where(email_table.c.id == email_id)
        rp = self.engine.execute(sel_stmt)
        record = rp.first()
        email = Email()
        if record is not None:
            email.date = record.date
            email.mime_type = record.mime_type
            email.from_addr = record.from_addr
            email.to_addr = record.to_adddr
            email.subject = record.subject
            email.body = record.body
            email.path = record.path
            email.label = record.label
        
        return email
    
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
                           email_table.c.path, email_table.c.label]).where(email_table.c.from_addrr == from_addr)
        rp = self.engine.execute(sel_stmt)
        email_list = []
        for record in rp:
            email = Email()
            email.date = record.date
            email.mime_type = record.mime_type
            email.from_addr = record.from_addr
            email.to_addr = record.to_addr
            email.subject = record.subject
            email.body = record.body
            email.path = record.path
            email.label = record.label 
            email_list.append(email)
            
        return email_list
    
    def get_emails_before(self, query_date):
        email_table = Table('raw_email', self.metadata)
        sel_stmt = select([email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_addr, \
                           email_table.c.subject, email_table.c.body, \
                           email_table.c.path, email_table.c.label]).where(email_table.c.date <= query_date)
        rp = self.engine.execute(sel_stmt)
        email_list = []
        for record in rp:
            email = Email()
            email.date = record.date
            email.mime_type = record.mime_type
            email.from_addr = record.from_addr
            email.to_addr = record.to_addr
            email.subject = record.subject
            email.body = record.body
            email.path = record.path
            email.label = record.label 
            email_list.append(email)
            
        return email_list        
        
    # EMAIL_ADDRESS table
    def insert_address(self, email_address):
        if type(email) != EmailAddress:
            print 'ERROR: input must be of type EmailAddress'
            return
        
        email_address_table = Table('email_address', self.metadata)
        ins_stmt = email_address_table.insert()
        conn = self.engine.connect()
        result = conn.execute(ins_stmt, address=email_address.address,
                              name=email_address.name)
    
    def get_address(self, address_id):
        email_address_table = Table('email_address', self.metadata)
        sel_stmt = select([email_address_table.c.name, email_address_table.c.address]).where(email_address_table.c.id == address_id)
        rp = self.engine.execute(sel_stmt)
        record = rp.first()
        email_address = EmailAddress()
        if record is not None:
            email_address.name = record.name
            email_address.address = record.address
        
        return email_address
    
    def get_address_name(self, address_id):
            email_address_table = Table('email_address', self.metadata)
            sel_stmt = select([email_address_table.c.name]).where(email_address_table.c.id == address_id)
            rp = self.engine.execute(sel_stmt)
            record = rp.first()
            email_address = EmailAddress()
            if record is not None:
                email_address.name = record.name
                email_address.address = record.address
            
            return email_address    
    
    # THREAD table
