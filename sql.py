import sqlite3 as sq

class liteDB( object ):
    def __init__(self):
        self.connection=sq.connect("cheetter.sql")
        self.cursor=self.connection.cursor()
        self._check_table()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def _check_table(self):
        self.cursor.execute("""SELECT * FROM sqlite_master WHERE name='accounts'""")
        result=self.cursor.fetchall()

        if len(result)==0: # create table
            print "Account table doesn't exist yet, creating..."
            self._create_table()

    def _create_table(self):
        self.cursor.execute("""CREATE TABLE accounts(name TEXT, oauth TEXT, oauth_secret TEXT)""")
        self.connection.commit()

    def add_entry(self, name, oauth, oauth_secret):
        ret=self._chk_alr_exist(name)
        if ret==-1:
            print "Adding Account unsuccessful!"
            return -1
        tup=(name, oauth, oauth_secret)
        query="""INSERT INTO accounts VALUES(?, ?, ?)"""
        self.cursor.execute(query, tup)
        self.connection.commit()

    def _chk_alr_exist(self, name):
        self.cursor.execute("SELECT * FROM accounts WHERE name=?", (name, ))
        res=self.cursor.fetchall()
        if len(res)>=1:
            answ=raw_input("Account already exists! [D]elete already existing or [C]ancel?")
            answ=answ.lower()
            if answ=='d':
                self.delete_entry(name)
                return 0
            elif answ=='c':
                return -1
            else:
                print "None allowed Input >:( Cancelling"
                return -1

    def delete_entry(self, name):
        query="DELETE FROM accounts WHERE name=?"
        self.cursor.execute(query, (name, ))
        self.connection.commit()
