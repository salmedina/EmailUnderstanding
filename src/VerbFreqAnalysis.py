import Table
import EnronDB
import matplotlib.pyplot as plt

def flatten_list(inList):
    return [item for sublist in inList for item in sublist]

def get_verbs_from_db():
    '''Gets a list of verbs from the database'''
    edb = EnronDB.EnronDB()
    edb.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo','enron_experiment')
    verbs_list = edb.get_all_brushed_verbs_with_id()
    return verbs_list

def get_verbs_per_label(label):
    '''Gets a list of verbs from the database per class'''
    edb = EnronDB.EnronDB()
    edb.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo','enron_experiment')
    verbs_list = edb.get_all_brushed_verbs_per_label(label)
    return verbs_list

def calc_verb_freq(verbs_list):
    # 1. Get the overall frequency
    
    # Create flattened verb list
    all_verbs = [email_verbs.split(',') for email_id,email_verbs in verbs_list]
    all_verbs = flatten_list(all_verbs)
    all_verbs = [x.strip() for x in all_verbs]
    
    verb_set = set(all_verbs)
    print len(verb_set)

    verb_freq = []
    for verb in verb_set:
        verb_freq.append((verb, all_verbs.count(verb)))
    
    verb_freq = sorted(verb_freq, key=lambda x: x[1], reverse=True)
    
    print max(verb_freq, key=lambda x:x[1])
    print min(verb_freq, key=lambda x:x[1])
    
    return verb_freq
    
def table_test():
    fout = open('mytable.tex','w')
    t = Table.Table(2, justs='cc', caption='Awesome results', label="tab:label")
    t.add_header_row(['obj', 'X'])
    col1 = ['obj1','obj2','obj3']
    col2 = [0.001,0.556,10.56]   # just numbers
    col3 = [[0.12345,0.1],[0.12345,0.01],[0.12345,0.001]]
    t.add_data([col1,col2], sigfigs=2)
    t.print_table(fout)
    fout.close()
    
def analyze_verbs(verb_freq, table_filename):
    vfl = [list(x) for x in zip(*verb_freq)]    
    verbs = vfl[0]
    freq = vfl[1]
    '''
    # Plot the histogram of relevant verbs
    print 'Plotting histogram'
    cbar = plt.bar(range(len(freq)-2),freq[2:], color='orange', edgecolor='none')
    #plt.bar(range(len(freq)),freq, color='red', edgecolor='none')
    plt.xlabel('Verb ID')
    plt.ylabel('Count')
    plt.title('Verb Frequency')
    plt.show()'''
    
    # Plot print 
    print 'Printing table'
    t = Table.Table(2, justs='cc', caption='', label='')
    t.add_header_row(['Verb', 'Count'])
    t.add_data([verbs[:13], freq[:13]], sigfigs=2)
    fout = open(table_filename, 'w')
    t.print_table(fout)
    fout.close()
    
    return verbs[2:13]
    
def plot_class_histogram():
    edb = EnronDB.EnronDB()
    edb.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo','enron_experiment')    

    class_tags = ['Strategy', 'PR', 'Employment','Empty','IT','Jokes','Legal','Logistic','News','Other','Personal','Political','Project','Spam']
    class_labels = range(1,15)
    ind_labels = [x+0.4 for x in class_labels]
    class_count = []
    for label in class_labels:
        class_count.append(edb.count_per_label(label))
        
    plt.bar(class_labels, class_count, color='lightblue', edgecolor='none')
    plt.xticks(ind_labels, class_tags, rotation=90)
    plt.xlabel('Class ID')
    plt.ylabel('Count')

    plt.show()
    
    
if __name__=='__main__':
    #plot_class_histogram()
    
    print 'Obtaining data'
    verbs_list = get_verbs_from_db()
    print 'Calculating verb frequency'
    verb_freq = calc_verb_freq(verbs_list)
    print 'Analyzing verbs'
    analyze_verbs(verb_freq, 'verbs_freq_all.tex')
    
    
    table_cols = []
    for label in range(1,15):
        print 'Analyzing label %d'%(label)
        verb_list = get_verbs_per_label(label)
        verb_freq = calc_verb_freq(verb_list)
        save_filename = 'verbs_freq_%d.tex'%(label)
        label_verbs=analyze_verbs(verb_freq, save_filename)
        table_cols.append(label_verbs)

    class_tags = ['Strategy', 'PR', 'Employment','Empty','IT','Jokes','Legal','Logistic','News','Other','Personal','Political','Project','Spam']
    
    
    t = Table.Table(len(class_tags), justs='c'*len(class_tags), caption='', label='')
    t.add_header_row(class_tags)
    t.add_data(table_cols, sigfigs=2)
    fout = open('top_class_verbs.tex', 'w')
    t.print_table(fout)
    fout.close()    
    