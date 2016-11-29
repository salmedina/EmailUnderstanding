import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import select, text
from sqlalchemy.sql.schema import Table, MetaData, Column
from sqlalchemy.sql.sqltypes import Integer, Text, Float


class Email:
    def __init__(self):
        self.id = -1
        self.date = ''
        self.mime_type = ''
        self.from_addr = ''
        self.to_addr = ''
        self.subject = ''
        self.raw_body = ''
        self.cleaned_body = ''
        self.one_line = ''
        self.path = ''
        self.is_scheduling = -1
        self.prediction = -1
        self.probability = -1
        self.label = -1
        self.manual_label = -1
    
    def isScheduling(self):
        return self.is_scheduling == 1 or self.manual_label == 1
    

class EnronDB:
    def __init__(self, table_name):
        self.engine = None
        self.metadata = MetaData()
        self.table_name = table_name
        
    @classmethod
    def holbox_db(cls):
        db = EnronDB("email_prediction")
        db.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')
        return db
        
    def init(self, host, username, password, db_name):
        engine_desc = 'mysql://%s:%s@%s/%s' % (username, password, host, db_name)
        try:
            self.engine = create_engine(engine_desc)
            self.metadata.reflect(self.engine)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        return True    
    
    # sql:
    # create table TABLE_NAME (id INT NOT NULL AUTO_INCREMENT, date DATETIME, mime_type TEXT, from_addr TEXT, 
    # to_addr TEXT, subject TEXT, raw_body TEXT, cleaned_body TEXT, one_line TEXT, path TEXT, prediction INT, PRIMARY KEY(id));
    def create_table(self):
        email_table = Table(self.table_name, self.metadata,
            Column('id', Integer, primary_key=True),
            Column('date', Text),
            Column('mime_type', Text),
            Column('from_addr', Text),
            Column('to_addr', Text),
            Column('subject', Text),
            Column('raw_body', Text),
            Column('cleaned_body', Text),
            Column('one_line', Text),
            Column('path', Text),
            Column('prediction', Integer),
            Column('probability', Float)
        )
        email_table.create(self.engine)

    def create_sample_table(self, sample_table_name):
        if sample_table_name == self.table_name:
            print('Cannon use the same table name')
            return
        email_table = Table(sample_table_name, self.metadata,
            Column('id', Integer, primary_key=True),
            Column('date', Text),
            Column('mime_type', Text),
            Column('from_addr', Text),
            Column('to_addr', Text),
            Column('subject', Text),
            Column('raw_body', Text),
            Column('cleaned_body', Text),
            Column('one_line', Text),
            Column('path', Text),
            Column('prediction', Integer),
            Column('probability', Float),
            Column('manual_label', Integer)
        )
        email_table.create(self.engine)

    def get_all_brushed_emails(self):
        email_table = Table('brushed_email', self.metadata)
        sel_stmt = select([email_table.c.id, email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_adddr, \
                           email_table.c.subject, email_table.c.body, email_table.c.one_line, \
                           email_table.c.path, email_table.c.label, email_table.c.is_scheduling])
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
                email.one_line = record.one_line
                email.path = record.path
                email.label = record.label
                email.is_scheduling = record.is_scheduling or 0
            emails.append(email)
        return emails
    
    def insert_email(self, email):
        if not isinstance(email, Email):
            print 'ERROR: input must be of type Email'
            return
        
        email_table = Table(self.table_name, self.metadata)
        ins_stmt = email_table.insert()
        conn = self.engine.connect()
        conn.execute(ins_stmt, date=email.date,
                              mime_type=email.mime_type,
                              from_addr=email.from_addr,
                              to_addr=email.to_addr,
                              subject=email.subject,
                              raw_body=email.raw_body,
                              cleaned_body=email.cleaned_body,
                              one_line=email.one_line,
                              path=email.path,
                              label=email.label,
                              prediction=email.prediction,
                              probability=email.probability
                              ) 
    
    def get_all_email_predictions(self):
        email_table = Table(self.table_name, self.metadata)
        sel_stmt = select([email_table.c.id, email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_addr, \
                           email_table.c.subject, email_table.c.raw_body, email_table.c.cleaned_body, email_table.c.one_line, \
                           email_table.c.path, email_table.c.prediction, email_table.c.probability])
        rp = self.engine.execute(sel_stmt)
        emails = []
        for record in rp:
            email = Email()
            if record is not None:
                email.id = record.id
                email.date = record.date
                email.mime_type = record.mime_type
                email.from_addr = record.from_addr
                email.to_addr = record.to_addr
                email.subject = record.subject
                email.raw_body = record.raw_body
                email.cleaned_body = record.cleaned_body
                email.one_line = record.one_line
                email.path = record.path
                email.prediction = record.prediction
                email.probability = record.probability
            emails.append(email)
        return emails

    def get_sample_emails(self, sample_table_name):
        email_table = Table(sample_table_name, self.metadata)
        sel_stmt = select([email_table.c.id, email_table.c.date, email_table.c.mime_type, \
                           email_table.c.from_addr, email_table.c.to_addr, \
                           email_table.c.subject, email_table.c.raw_body, email_table.c.cleaned_body, email_table.c.one_line, \
                           email_table.c.path, email_table.c.prediction, email_table.c.probability, email_table.c.manual_label])
        rp = self.engine.execute(sel_stmt)
        emails = []
        for record in rp:
            email = Email()
            if record is not None:
                email.id = record.id
                email.date = record.date
                email.mime_type = record.mime_type
                email.from_addr = record.from_addr
                email.to_addr = record.to_addr
                email.subject = record.subject
                email.raw_body = record.raw_body
                email.cleaned_body = record.cleaned_body
                email.one_line = record.one_line
                email.path = record.path
                email.prediction = record.prediction
                email.probability = record.probability
                email.manual_label = record.manual_label
            emails.append(email)
        return emails

    def get_all_email_predictions_greater_than(self, threshold = 0.7):
        s = text("select * from " + self.table_name + " where probability >= " + str(threshold))
        rp = self.engine.execute(s).fetchall()
#         email_table = Table(self.table_name, self.metadata)
#         sel_stmt = select([email_table.c.id, email_table.c.date, email_table.c.mime_type, \
#                            email_table.c.from_addr, email_table.c.to_addr, \
#                            email_table.c.subject, email_table.c.raw_body, email_table.c.cleaned_body, email_table.c.one_line, \
#                            email_table.c.path, email_table.c.prediction, email_table.c.probability]).where(email_table.c.probability >= 0.7)
#         rp = self.engine.execute(sel_stmt)
        emails = []
        for record in rp:
            email = Email()
            if record is not None:
                email.id = record.id
                email.date = record.date
                email.mime_type = record.mime_type
                email.from_addr = record.from_addr
                email.to_addr = record.to_addr
                email.subject = record.subject
                email.raw_body = record.raw_body
                email.cleaned_body = record.cleaned_body
                email.one_line = record.one_line
                email.path = record.path
                email.prediction = record.prediction
                email.probability = record.probability
            emails.append(email)
        return emails
        
    def insert_sample_email(self, sample_table_name, email):
        if not isinstance(email, Email):
            print 'ERROR: input must be of type Email'
            return
        
        if sample_table_name == self.table_name:
            print('Cannot use the same table name')
            return
        
        email_table = Table(sample_table_name, self.metadata)
        ins_stmt = email_table.insert()
        conn = self.engine.connect()
        conn.execute(ins_stmt, date=email.date,
                              mime_type=email.mime_type,
                              from_addr=email.from_addr,
                              to_addr=email.to_addr,
                              subject=email.subject,
                              raw_body=email.raw_body,
                              cleaned_body=email.cleaned_body,
                              one_line=email.one_line,
                              path=email.path,
                              label=email.label,
                              prediction=email.prediction,
                              probability=email.probability,
                              ) 