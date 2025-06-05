#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyodbc",
# ]
# ///

#!/usr/bin/env python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
# https://docs.python-zeep.org/en/master/
import pyodbc 
from datetime import datetime
# importing date class from datetime module
from datetime import date
# import mysql.connector
#         from mysql.connector import Error

import sys 
import os
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines?view=sql-server-ver16
# remember to source oaodbc64.sh to set env variables.
# https://github.com/mkleehammer/pyodbc/wiki/Calling-Stored-Procedures
# https://thepythonguru.com/fetching-records-using-fetchone-and-fetchmany/
# https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki
def print_to_stdout(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(os.path.basename(__file__)+':',*a, file = sys.stdout)


def print_to_stderr(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(os.path.basename(__file__)+':',*a, file = sys.stderr)

try:
  ret = 0
  # pcn_list = (sys.argv[1])
  # username = (sys.argv[2])
  # password = (sys.argv[3])
  # username2 = (sys.argv[4])
  # password2 = (sys.argv[5])
  # username3 = (sys.argv[6])
  # password3 = (sys.argv[7])
  # mysql_host = (sys.argv[8])
  # mysql_port = (sys.argv[9])
  # azure_dw = (sys.argv[10])
    
  pcn_list = '123681'
  username = 'mg.odbcalbion'
  password = 'Mob3xalbion'
  username2 = 'repsys1'
  password2 = 'WeDontSharePasswords1!'
  username3 = 'root'
  password3 = 'password'
  mysql_host = 'reports31'
  mysql_port = '30031'
  azure_dw = '1'
   
  # print(f"params={params}")
  # print(f"params={params},username={username},password={password},username2={username2},password2={password2}")
  # sys.exit(0)
  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"{current_time}")
  print_to_stdout(f"point 1")


  # https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
  # password = 'wrong' 
  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
  # https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc
  cursor = conn.cursor()
# accounting_year_category_type_dw_import
  rowcount=cursor.execute("{call sproc300758_11728751_1999909 (?)}", pcn_list).rowcount
  print_to_stdout(f"point 2: rowcount={rowcount}")

  rows = cursor.fetchall()
  print_to_stdout(f"point 3")

  print_to_stdout(f"call sproc300758_11728751_1999909 - rowcount={cursor.rowcount}")
  print_to_stdout(f"call sproc300758_11728751_1999909 - messages={cursor.messages}")
  cursor.close()
  fetch_time = datetime.now()
  tdelta = fetch_time - start_time 
  print_to_stdout(f"fetch_time={tdelta}") 

  insertObject = []
  # columnNames = [column[0] for column in cursor.description]
  for record in rows:
    t=tuple(record) 
    i=t[:2]+t[3:] 
    insertObject.append(i)

  print_to_stdout(f"point 4")
  t = len(insertObject)
  print_to_stdout(f"rows={t}")

  # creating the date object of today's date
  # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
  todays_date = date.today()
  this_year = todays_date.year
  next_year = todays_date.year + 1


  conn2 = pyodbc.connect('DSN=repsys1;UID='+username2+';PWD='+ password2 + ';DATABASE=repsys1')
  print_to_stdout(f"point 5")

  cursor2 = conn2.cursor()
  print_to_stdout(f"point 6")

  del_command = f'''delete from Plex.accounting_account_year_category_type 
  where year between {this_year} and {next_year} 
  and pcn in ({pcn_list})'''

  print_to_stdout(f"point 7: del_command={del_command}")

  # del_command = f"delete from Plex.accounting_account_year_category_type where [year] = {todays_date.year} and pcn in ({params})"
  # del_command = f"delete from Scratch.accounting_account_year_category_type where [year] = {todays_date.year} and pcn in ({params})"
  # print_to_stdout(del_command)

  # https://github.com/mkleehammer/pyodbc/wiki/Cursor
  # The return value is always the cursor itself:
  rowcount=cursor2.execute(del_command).rowcount
  print_to_stdout(f"point 8")

  # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
  print_to_stdout(f"{del_command} - rowcount={rowcount}")
  print_to_stdout(f"{del_command} - messages={cursor2.messages}")
  cursor2.commit()
  print_to_stdout(f"point 9")



  # https://github.com/mkleehammer/pyodbc/wiki/Cursor
  # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
  # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
  im2=f'''insert into Plex.accounting_account_year_category_type (pcn,account_no,[year],category_type,revenue_or_expense) 
  values (?,?,{this_year},?,?)''' 
  print_to_stdout(f"point 10: im2={im2}")

  # rec = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]
  cursor2.fast_executemany = True
  cursor2.executemany(im2,insertObject)
  # cursor2.executemany(im2,rows)
  cursor2.commit()

  im2=f'''insert into Plex.accounting_account_year_category_type (pcn,account_no,[year],category_type,revenue_or_expense) 
  values (?,?,{next_year},?,?)''' 
  print_to_stdout(f"point 11: im2={im2}")

  # rec = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]
  cursor2.fast_executemany = True
  cursor2.executemany(im2,insertObject)
  cursor2.commit()
  print_to_stdout(f"point 12")


  cursor2.close()
  print_to_stdout(f"point 20")

except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stderr(error_msg) 

# except Error as e:
#   ret = 1
#   print("MySQL error: ", e)

finally:
  end_time = datetime.now()
  tdelta = end_time - start_time 
  print_to_stdout(f"total time: {tdelta}") 
  if 'conn' in globals():
    conn.close()
  if 'conn2' in globals():
    conn2.close()
  print_to_stdout(f"end point")
 
  sys.exit(ret)
