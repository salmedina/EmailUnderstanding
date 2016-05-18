'''
Created on May 17, 2016

@author: zhongzhu
'''

import email

def parse_from_file(email_file):
    ''' return_type: message.Message '''
    with open(email_file) as f:
        e = email.message_from_file(f)
        print(e["Message-ID"])
        print(e["Date"])
        print(e["From"])
        print(e["To"])
        print(e["Subject"])
        print(e["Mime-Version"])
        print(e["Content-Type"])
        print(e["Content-Transfer-Encoding"])
        print(e["X-From"])
        print(e["X-To"])
        print(e["X-cc"])
        print(e["X-bcc"])
        print(e["X-Folder"])
        print(e["X-Origin"])
        print(e["X-FileName"])
        print(e.get_payload())
        if e.is_multipart():
            for payload in e.get_payload():
                # if payload.is_multipart(): ...
                print payload.get_payload()
        else:
            print e.get_payload()
            
    
parse_from_file("../data/testemail")