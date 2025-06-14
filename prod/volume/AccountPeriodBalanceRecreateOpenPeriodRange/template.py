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
%PROD%pcn = (sys.argv[1])
%PROD%username2 = (sys.argv[2])
%PROD%password2 = (sys.argv[3])
%PROD%username3 = (sys.argv[4])
%PROD%password3 = (sys.argv[5])
%PROD%mysql_host = (sys.argv[6])
%PROD%mysql_port = (sys.argv[7])
%PROD%azure_dw = (sys.argv[8])

%DEV%pcn = 123681
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
  print_to_stdout(f"Current Time: {current_time}")

  conn2 = pyodbc.connect('DSN=repsys1;UID='+username2+';PWD='+ password2 + ';DATABASE=repsys1',timeout=30)
  cursor2 = conn2.cursor()

  rowcount=cursor2.execute("{call Plex.account_period_balance_delete_open_period_range (?)}",pcn).rowcount
  print_to_stdout(f"call Plex.account_period_balance_delete_open_period_range - rowcount={rowcount}")
  print_to_stdout(f"call Plex.account_period_balance_delete_open_period_range - messages={cursor2.messages}")
  cursor2.commit()

  rowcount=cursor2.execute("{call Plex.account_period_balance_recreate_open_period_range (?)}",pcn).rowcount

  print_to_stdout(f"call Plex.account_period_balance_recreate_open_period_range - rowcount={rowcount}")
  print_to_stdout(f"call Plex.account_period_balance_recreate_open_period_range - messages={cursor2.messages}")
  cursor2.commit()
  cursor2.close()

except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stderr(error_msg) 

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