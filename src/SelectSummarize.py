import EnronDB
import sys

def ask_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": "yes", "y": "yes", "ye": "yes",
             "no": "no", "n": "no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " \
                             "(or 'y' or 'n').\n")

def main():
    edb = EnronDB.EnronDB()
    edb = EnronDB.EnronDB()
    edb.init('holbox.lti.cs.cmu.edu', 'inmind', 'yahoo', 'enron_experiment')
    # Read all the bodies from the brushed table
    emails = edb.get_all_brushed_body_summary_with_id()

    # Output files
    border_str = '============================================================================='
    body_display_fname = 'body_disp.txt'
    summary_display_fname = 'summary_disp.txt'
    selected_fname = 'selected_id.txt'
    selected_email_ids = []

    for email_id, subject, body, summary in emails:
        print 'Email ID:        %d'%(email_id)
        with open(body_display_fname,'w') as f:
            f.write(body)
            f.close()
            
        with open(summary_display_fname, 'w') as f:
            f.write(summary)
            f.close()

        if ask_yes_no('Keep email?') == 'yes':            
            selected_email_ids.append(email_id)
            with (open(selected_fname, 'a')) as f:
                email_input = border_str + '\n'
                email_input += 'ID:          %d\n'%(email_id)
                email_input += 'SUBJECT:     %s\n'%(subject)
                email_input += '<<<<<<<<<<<<<<<<<<<<<<<<<<<< BODY >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n%s\n\n'%(body)
                email_input += '<<<<<<<<<<<<<<<<<<<<<<<<<< SUMMARY >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n%s\n\n'%(summary)
                f.write('%s\n'%(email_input))
                f.close()

if __name__=='__main__':
    main()