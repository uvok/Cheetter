""" Account management """

import sql

class AccountManager( object ):
    def __init__(self):
        self.db=sql.liteDB()
        self.result=None
        self._NoAccounts()
    def __del__(self):
        del self.db
    def _NoAccounts(self):
        if self.db.howmany()==0:
            while True:
                print "You have no acounts configured yet!\n" \
                      "Would you like to create one now? "
                answ=raw_input()

                if answ.lower()=='y':
                    self.AddAccount()
                    break
                elif answ.lower()=='n':
                    print "Using client not possible w/o account, quitting"
                    exit()
                else:
                    print "Invalid answer"
                    pass
            
