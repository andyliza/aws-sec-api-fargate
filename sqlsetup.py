import os 
import mysql.connector
import time


Database_Endpoint = os.environ['DB_Endpoint']
Username = os.environ['User']
Pass = os.environ['Password']
Database = os.environ['DB']

conn = mysql.connector.connect(user=Username, password=Pass, host=Database_Endpoint, database=Database)
cmd = 'mysql '+'-h '+Database_Endpoint+' -u '+Username+' -p'+Pass+' -D '+Database+' < script.sql'
print(cmd)
def checkTableExists(conn, tablename):
    dbcur = conn.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

dbcur = conn.cursor()
if checkTableExists(conn,'unicorn'):
    dbcur = conn.cursor()
    dbcur.close()
else:
    os.system(cmd)

print('DB setup complete')
time.sleep(30)