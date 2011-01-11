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
                    re=self.AddAccount()
                    if re!=-1:
                        break
                    else:
                        pass
                elif answ.lower()=='n':
                    print "Using client not possible w/o account, quitting"
                    exit()
                else:
                    print "Invalid answer"
                    pass
            
    def AddAccount(self):
        # get this stupid token thingie
        # Validate this thing
        # Validate User - user object -> name for database
        return

    def DeleteAccount(self):
        sel=self.SelectAccount()
        self.db.delete_entry(self.result[sel]['name'])
        self._NoAccounts()
        return

    def ReauthAccount(self):
        # 2 possibilities:
        # 1st: Deleting account and adding account
        # 2nd: Somehow use sq.modify_entry
        return

    def ListAccounts(self):
        self.result=self.db.dumpTable()
        for num, res in enumerate(self.result):
            print "%i) %s" % (num, res['name'])
        return

    def SelectAccount(self):
        selection=None
        self.ListAccounts()
        if len(self.result) != 0:
            while True:
                selection=int(raw_input("Which account? "))
                if 0<=selection<len(self.result):
                    break
                else:
                    pass

        return selection    

    def GetAccount(self):
        sel=self.SelectAccount()
        return self.result[sel]
