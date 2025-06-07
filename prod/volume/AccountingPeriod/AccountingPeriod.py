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
  pcn_list = (sys.argv[1])
  username = (sys.argv[2])
  password = (sys.argv[3])
  username2 = (sys.argv[4])
  password2 = (sys.argv[5])
  username3 = (sys.argv[6])
  password3 = (sys.argv[7])
  mysql_host = (sys.argv[8])
  mysql_port = (sys.argv[9])
  azure_dw = (sys.argv[10])

#%DEV%pcn_list = '123681'
## %DEV%pcn_list = '123681,300758'
    # # pcn_list = '123681,300758,310507,306766,300757'
#%DEV%username = 'mg.odbcalbion'
#%DEV%password = 'Mob3xalbion'
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

  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
  cursor = conn.cursor()
  # accounting_period_dw_import
  cursor.execute("{call sproc300758_11728751_2059406 (?)}", pcn_list)
  rows = cursor.fetchall()
  
  cursor.close()

  fetch_time = datetime.now()
  tdelta = fetch_time - start_time 
  print_to_stdout(f"fetch_time={tdelta}") 

  length = len(rows)
  i = 0
  f = '%Y-%m-%d %H:%M:%S.%f'

  # Convert Plex format to datetime with 3 precision second decimal
  # If DW column was datetime2 no conversion would be necessary
  while i < length:
    if(rows[i][9] is not None):
      r9=rows[i][9]
      if(len(r9)==19):
        ts=r9+'.000'
      else:        
        ts=r9[:-6]
      rows[i][9]=ts
    i += 1

  conn2 = pyodbc.connect('DSN=repsys1;UID='+username2+';PWD='+ password2 + ';DATABASE=repsys1')
  cursor2 = conn2.cursor()

  del_command = f"delete from Plex.accounting_period where pcn in ({pcn_list}) and ordinal = 0"

  rowcount=cursor2.execute(del_command).rowcount
  print_to_stdout(f"{del_command} - rowcount={rowcount}")
  print_to_stdout(f"{del_command} - messages={cursor2.messages}")
  cursor2.commit()

  # set the newest records to the previous records.
  update_command = f"update Plex.accounting_period set ordinal=0 where pcn in ({pcn_list}) and ordinal = 1"
  rowcount=cursor2.execute(update_command).rowcount
  print_to_stdout(f"{update_command} - rowcount={rowcount}")
  print_to_stdout(f"{update_command} - messages={cursor2.messages}")
  cursor2.commit()

  im2='''insert into Plex.accounting_period (pcn,period_key,period,period_display,fiscal_order,quarter_group,begin_date,end_date,period_status,add_date,update_date,ordinal) 
          values (?,?,?,?,?,?,?,?,?,?,?,1)''' 

  cursor2.fast_executemany = True
  cursor2.executemany(im2,rows)
  cursor2.commit()
  cursor2.close()

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
  if 'conn' in globals():
    conn.close()
  if 'conn2' in globals():
    conn2.close()
  sys.exit(ret)
