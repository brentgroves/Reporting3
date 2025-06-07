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
  ret = 2
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
