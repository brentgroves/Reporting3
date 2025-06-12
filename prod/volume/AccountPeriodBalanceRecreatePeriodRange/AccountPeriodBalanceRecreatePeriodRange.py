#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyodbc",
# ]
# ///
import pyodbc 
from datetime import datetime
import sys
import os

def print_to_stdout(*a):
    print(os.path.basename(__file__)+':',*a, file = sys.stdout)

def print_to_stderr(*a):
    print(os.path.basename(__file__)+':',*a, file = sys.stderr)

try:
  ret = 0
  pcn = (sys.argv[1])
  username2 = (sys.argv[2])
  password2 = (sys.argv[3])
  username3 = (sys.argv[4])
  password3 = (sys.argv[5])
  mysql_host = (sys.argv[6])
  mysql_port = (sys.argv[7])
  azure_dw = (sys.argv[8])

#%DEV%pcn = '123681'
#%DEV%username2 = 'repsys1'
#%DEV%password2 = 'WeDontSharePasswords1!'
#%DEV%username3 = 'root'
#%DEV%password3 = 'password'   
#%DEV%mysql_host = 'reports31'
#%DEV%mysql_port = '30031'
#%DEV%azure_dw = '1'

  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time}")


  # https://www.pythonfixing.com/2022/02/fixed-how-to-set-db-connection-timeout.html
  conn2 = pyodbc.connect('DSN=repsys1;UID='+username2+';PWD='+ password2 + ';DATABASE=repsys1',timeout=30)
  cursor2 = conn2.cursor()
  print_to_stdout(f"Point 1")

  rowcount=cursor2.execute("{call Plex.account_period_balance_delete_period_range (?)}",pcn).rowcount
  print_to_stdout(f"call Plex.account_period_balance_delete_period_range - rowcount={rowcount}")
  print_to_stdout(f"call Plex.account_period_balance_delete_period_range - messages={cursor2.messages}")
  cursor2.commit()
  print_to_stdout(f"Point 2")


  rowcount=cursor2.execute("{call Plex.account_period_balance_recreate_period_range (?)}",pcn).rowcount
  print_to_stdout(f"call Plex.account_period_balance_recreate_period_range - rowcount={rowcount}")
  print_to_stdout(f"call Plex.account_period_balance_recreate_period_range - messages={cursor2.messages}")
  cursor2.commit()
  cursor2.close()
  print_to_stdout(f"Point 3")

except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stderr(f"error {error_msg}") 
  print_to_stderr(f"error {ex.args}") 

except Exception as e:
  ret = 2
  print_to_stderr(e) 

finally:
  end_time = datetime.now()
  tdelta = end_time - start_time 
  print_to_stdout(f"total time: {tdelta}") 
  if 'conn2' in globals():
    conn2.close()
  sys.exit(ret)
