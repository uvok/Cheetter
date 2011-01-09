import sqlite3 as sq

class liteDB( object ):
    def __init__(self):
        """ Opens table and calls _check_table  """
        
        self.connection=sq.connect("cheetter.sql")
        self.cursor=self.connection.cursor()
        self._check_table()

    def __del__(self):
        """ Closes connection - may fail if table is in uncommited state """
        
        self.cursor.close()
        self.connection.close()

    def _check_table(self):
        """ Checks if table accounts is in database """
        
        self.cursor.execute("""SELECT * FROM sqlite_master WHERE name='accounts'""")
        result=self.cursor.fetchall()

        if len(result)==0:
            print "Account table doesn't exist yet, creating..."
            self._create_table()

    def _create_table(self):
        """ Creates table accounts - don't call yourself """
        
        self.cursor.execute("""CREATE TABLE accounts(name TEXT, oauth TEXT, oauth_secret TEXT)""")
        self.connection.commit()

    def add_entry(self, name, oauth, oauth_secret):
        """ Add an account to table accounts

        Includes check if account with specified name already exists """
        
        ret=self._chk_alr_exist(name)
        if ret==-1:
            print "Adding Account unsuccessful!"
            return -1
        tup=(name, oauth, oauth_secret)
        query="""INSERT INTO accounts VALUES(?, ?, ?)"""
        self.cursor.execute(query, tup)
        self.connection.commit()

    def delete_entry(self, name):
        """ Delete account(s) from table - No asking, so be careful """
        
        query="DELETE FROM accounts WHERE name=?"
        self.cursor.execute(query, (name, ))
        self.connection.commit()

    def _chk_alr_exist(self, name):
        """ Checks if account w/ name already exists - called by add_entry """
        
        self.cursor.execute("SELECT * FROM accounts WHERE name=?", (name, ))
        res=self.cursor.fetchall()
        if len(res)>=1:
            while True:
                answ=raw_input("Account already exists! [D]elete already existing or [C]ancel? ")
                answ=answ.lower()
                if answ=='d':
                    self.delete_entry(name)
                    state=0
                    break
                elif answ=='c':
                    state=-1
                    break
                else:
                    print "No allowed Input >:( "
        return state

    def howmany(self):
        self.cursor.execute("SELECT * FROM accounts")
        len=(self.cursor.fetchall())
        return 0
