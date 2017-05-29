#!/usr/bin/env python
# -*- coding: utf8 -*-
import mailbox 
import os
import datetime
import pwd

#adjust those parameters do you need
maildir = "/var/spool/mail/"
days_to_keep=30

if __name__ == '__main__' :
    mailfiles = os.listdir("/var/spool/mail/")
    for mailfile in mailfiles :
        filename = '/var/spool/mail/%s' % mailfile
        mbox = mailbox.mbox( '/var/spool/mail/%s' % mailfile )
        to_delete = False
        today =  datetime.datetime.now()
        to_remove = []
        for key, msg in mbox.iteritems() :
            datemsg = datetime.datetime.strptime(msg['Date'][0:16],'%a, %d %b %Y')
            if (today - datemsg).days > days_to_keep :
                to_remove.append(key)
        for key in to_remove:
            mbox.discard(key)
        try : 
            mbox.close()
        except :
            to_delete = True
        #  delete empty mailbox
        if os.stat(filename).st_size == 0 : 
            to_delete = True

        if to_delete : 
            os.system("rm -f %s"  % filename)
        else :
            try : 
                #make sur the mailfile is correctly owned
                os.system("chown %s %s"  % (mailfile,filename))
            except : 
                pass
