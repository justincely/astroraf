
__all__ = ['unpickle','progress_bar','send_email']

def unpickle(pickled_object):
    import pickle
    return pickle.load( open(pickled_object,'r') )


class Logger(object):
    def __init__(self,filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()


def progress_bar(iteration, total):
    """
    Print progress bar to stdout

    Call progress bar while in a loop, passing the int value
    of the current interation and the total number of iterations.
    A progress bar in % will be written to stdout.

    Parameters
    ----------
    iteration : int
        Integer value of current iteration in loop
    total : int
        Integer value of total # of loops

    Example
    -------
    >>> progress_bar( i, 100 )
    [===                 ] 17%

    """

    import sys
    
    bar_length = 20
    frac_done = (iteration + 1) / float(total)
    percent_done = int(100 * frac_done)
    bar_done = int(bar_length * frac_done)

    #Write to initial stdout, incase stdout was redirected in program
    #fixes writing each step of the bar to log files.
    sys.__stdout__.write('\r')
    sys.__stdout__.write("[%-20s] %d%%" % ('='* bar_done, percent_done))
    sys.__stdout__.flush()

    if percent_done == 100:
        sys.__stdout__.write('\n')
        sys.__stdout__.flush()


def send_email(subject=None,message=None,from_addr=None,to_addr=None):
    '''
    Send am email via SMTP server.
    This will not prompt for login if you are alread on the internal network.
    '''
    import os
    import getpass
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    users_email=getpass.getuser()+'@stsci.edu'

    if not subject:
	subject='Message from %s'%(__file__)
    if not message:
	message='You forgot to put a message into me'
    if not from_addr:
        from_addr=users_email
    if not to_addr:
        to_addr=users_email

    svr_addr='smtp.stsci.edu'
    msg = MIMEMultipart()
    msg['Subject']=subject
    msg['From']=from_addr
    msg['To']=to_addr
    msg.attach(MIMEText(message))
    s = smtplib.SMTP(svr_addr)
    s.sendmail(from_addr, to_addr, msg.as_string())
    s.quit()
    print '\nEmail sent to %s \n' %(from_addr)

