""" Account management """

import sql

class AccountManager( object ):
    def __init__(self):
        self.db=sql.liteDB()
        self._NoAccounts()
    def __del__(self):
        del self.db
    def _NoAccounts(self):
        if self.db.howmany()==0:
            print "You have no acounts configured yet!" \
                  "Would you like to create one now? "
            ## TODO
    
