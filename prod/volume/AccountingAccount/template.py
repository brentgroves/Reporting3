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

%DEV%pcn_list = '123681,300758'
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
  print_to_stdout(f"Current Time: {current_time=}")

  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
  cursor = conn.cursor()
# accounting_account_DW_Import
  cursor.execute("{call sproc300758_11728751_1978024 (?)}", pcn_list)
  rows = cursor.fetchall()

  cursor.close()
  fetch_time = datetime.now()
  tdelta = fetch_time - start_time 
  print_to_stdout(f"fetch_time={tdelta}") 

  conn2 = pyodbc.connect('DSN=repsys1;UID='+username2+';PWD='+ password2 + ';DATABASE=repsys1')
  cursor2 = conn2.cursor()

  txt = "delete from Plex.accounting_account where pcn in ({dellist:s})"

  rowcount=cursor2.execute(txt.format(dellist = pcn_list)).rowcount
  print_to_stdout(f"{txt} - rowcount={rowcount}")
  print_to_stdout(f"{txt} - messages={cursor2.messages}")
  cursor2.commit()

  im2='''insert into Plex.accounting_account
  values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''' 
  # rec = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]
  cursor2.fast_executemany = True
  cursor2.executemany(im2,rows)
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
  if 'conn' in globals():
      conn.close()
  if 'conn2' in globals():
      conn2.close()
  sys.exit(ret)
