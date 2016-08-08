'''
Created on Jun 4, 2016

@author: zhongzhu
'''
import ConfigParser
import os

import EnronDB


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

def initDB():
    db = EnronDB.EnronDB()
    db.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')
    return db