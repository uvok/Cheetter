import sqlite3 as sq

class liteDB(object):
    """ Interface for sqlite3 database, used to handle accounts """
    
    def __init__(self):
        """ Opens table and calls _check_table  - autocommit mode """
        
        # TODO: This file in ~/.cheetter 
        self.connection = sq.connect("cheetter.sql", isolation_level=None)
        self.connection.row_factory = sq.Row
        self.cursor = self.connection.cursor()
        self._create_table()

    def __del__(self):
        """ Closes connection - may fail if table is in non-committed state? """
        
        self.cursor.close()
        self.connection.close()

    def _create_table(self):
        """ Creates table accounts if not exists """
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(name TEXT PRIMARY KEY, oauth TEXT, oauth_secret TEXT)""")

    def add_entry(self, name, oauth, oauth_secret):
        """ Add an account to table accounts

        returns 0 if  successful, -1 if error occurred """
        
        tup = (name, oauth, oauth_secret)
        query = """INSERT INTO accounts VALUES(?, ?, ?)"""

        try:
            self.cursor.execute(query, tup)
        except sq.IntegrityError, ex:
            print "Entry already exists. Please delete old entry first"
            print ex
            return -1
        return 0

    def delete_entry(self, name):
        """ Delete account(s) from table - No confirmation prompt, so be careful """
        
        query = "DELETE FROM accounts WHERE name=?"
        self.cursor.execute(query, (name,))

    def modify_entry(self, name, oauth, oauth_secret):
        """ Modifies account by deleting and reading it 

        May actually not be needed at all """

        self.delete_entry(name)
        ret = self.add_entry(name, oauth, oauth_secret)
        return ret

    def howmany(self):
        """ Returns number of entries in the database """

        res = self.dumpTable()
        return len(res)

    def dumpTable(self):
        """ Returns all entries in database using searchEntry() """
        
        res = self.searchEntry("all")
        return res
        

    def searchEntry(self, name):
        """ Search account with specified name 

        returns list of results """

        # There is no twitter account all, so this shouldn't be a problem
        if name is not "all":
            self.cursor.execute("SELECT * FROM accounts WHERE name=?", (name,))
        else:
            self.cursor.execute("SELECT * FROM accounts")
        result = self.cursor.fetchall()
        return result
