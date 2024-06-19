import psycopg2
from consts import Consts
from contextlib import closing

class PostgresDB:
    def __init__(self):
        self.conn = psycopg2.connect(Consts.DATABASE_URL, sslmode='require')

    def GetTCGPlayerSettings(self, serverId):
        try:
            sql = f"SELECT ServerID FROM tcgplayer_server_settings WHERE ServerID = {serverId}"
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(sql)
                return cursor.rowcount
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return -1

    def GetPTCGLPricesSettings(self, serverId):
        try:
            sql = f"SELECT ServerID FROM ptcgoprices_server_settings WHERE ServerID = {serverId}"
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(sql) 
                return cursor.rowcount
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return -1
        
    def InsertTCGPlayerSettings(self, serverId):
        try:
            if(self.GetTCGPlayerSettings(serverId) != 0):
                return True
            sql = f"INSERT INTO tcgplayer_server_settings(ServerID) VALUES({serverId})"
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(sql) 
                self.conn.commit()
                return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def InsertPTCGLPricesSettings(self, serverId):
        try:
            if(self.GetPTCGLPricesSettings(serverId) != 0):
                return True
            sql = f"INSERT INTO ptcgoprices_server_settings(ServerID) VALUES({serverId})"
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(sql) 
                self.conn.commit()
                return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def DeleteTCGPlayerSettings(self, serverId):
        try:
            sql = f"DELETE FROM tcgplayer_server_settings WHERE ServerID = {serverId}"
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(sql) 
                self.conn.commit()
                return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    def DeletePTCGLPricesSettings(self, serverId):
        try:
            sql = f"DELETE FROM ptcgoprices_server_settings WHERE ServerID = {serverId}"            
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(sql) 
                self.conn.commit()
                return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False