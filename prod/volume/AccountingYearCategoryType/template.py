#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyodbc",
# ]
# ///
import pyodbc 
from datetime import datetime
# importing date class from datetime module
from datetime import date

import sys 
import os

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
%PROD%pcn_list = (sys.argv[1])
%PROD%username = (sys.argv[2])
%PROD%password = (sys.argv[3])
%PROD%username2 = (sys.argv[4])
%PROD%password2 = (sys.argv[5])
%PROD%username3 = (sys.argv[6])
%PROD%password3 = (sys.argv[7])
%PROD%mysql_host = (sys.argv[8])
%PROD%mysql_port = (sys.argv[9])
%PROD%azure_dw = (sys.argv[10])
    
%DEV%pcn_list = '123681'
%DEV%username = 'mg.odbcalbion'
%DEV%password = 'Mob3xalbion'
%DEV%username2 = 'repsys1'
%DEV%password2 = 'WeDontSharePasswords1!'
%DEV%username3 = 'root'
%DEV%password3 = 'password'
%DEV%mysql_host = '%MYSQL_HOST%'
%DEV%mysql_port = '%MYSQL_PORT%'
%DEV%azure_dw = '%AZURE_DW%'
   
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"{current_time}")
  print_to_stdout(f"point 1")


  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
  print_to_stdout(f"point 2")
  cursor = conn.cursor()

# accounting_year_category_type_dw_import
  rowcount=cursor.execute("{call sproc300758_11728751_1999909 (?)}", pcn_list).rowcount
  print_to_stdout(f"point 3: rowcount={rowcount}")

  rows = cursor.fetchall()
  print_to_stdout(f"point 4")

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

  rowcount=cursor2.execute(del_command).rowcount
  print_to_stdout(f"point 8")

  print_to_stdout(f"{del_command} - rowcount={rowcount}")
  print_to_stdout(f"{del_command} - messages={cursor2.messages}")
  cursor2.commit()
  print_to_stdout(f"point 9")

  im2=f'''insert into Plex.accounting_account_year_category_type (pcn,account_no,[year],category_type,revenue_or_expense) 
  values (?,?,{this_year},?,?)''' 
  print_to_stdout(f"point 10: im2={im2}")

  cursor2.fast_executemany = True
  cursor2.executemany(im2,insertObject)
  cursor2.commit()

  im2=f'''insert into Plex.accounting_account_year_category_type (pcn,account_no,[year],category_type,revenue_or_expense) 
  values (?,?,{next_year},?,?)''' 
  print_to_stdout(f"point 11: im2={im2}")

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

except:
  ret = 2
  print_to_stdout(f"AccountingYearCategoryType error()")

finally:
  print_to_stdout(f"point 30")
  end_time = datetime.now()
  tdelta = end_time - start_time 
  print_to_stdout(f"total time: {tdelta}") 
  if 'conn' in globals():
    conn.close()
  if 'conn2' in globals():
    conn2.close()
  print_to_stdout(f"point 39: ret={ret}")
  sys.exit(ret)
