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
  pcn = 123681
  username2 = 'mgadmin' 
  password2 = 'WeDontSharePasswords1!' 
  username3 = 'repsys1'
  password3 = 'WeDontSharePasswords1!' 

  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time}")

  conn = pyodbc.connect('DSN=mgsqlmi;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')
  cursor = conn.cursor()
  print_to_stdout(f"point 1")

  sql = """
  select pcn,account_no,period,period_display,debit,ytd_debit,credit,ytd_credit,balance,ytd_balance 
  from Plex.account_period_balance 
  where pcn = 123681 
  and period between 202409 and 202412
  order by period desc, account_no
    """

  rowcount=cursor.execute(sql).rowcount
  print_to_stdout(f"select from Plex.account_period_balance - rowcount={rowcount}")
  print_to_stdout(f"select from Plex.account_period_balance - messages={cursor.messages}")
  print_to_stdout(f"point 2")

  rows = cursor.fetchall()
  print_to_stdout(f"point 3")

  cursor.close()
  print_to_stdout(f"rows={len(rows)}")

  conn2 = pyodbc.connect('DSN=repsys1;UID='+username3+';PWD='+ password3 + ';DATABASE=repsys1')
  cursor2 = conn2.cursor()
  print_to_stdout(f"point 4")

#   INSERT INTO Mgslqmi.account_period_balance
# (pcn, account_no, period, period_display, debit, ytd_debit, credit, ytd_credit, balance, ytd_balance)
# VALUES(0, '', 0, '', 0, 0, 0, 0, 0, 0)

  im2 = """
  INSERT INTO Mgslqmi.account_period_balance
(pcn, account_no, period, period_display, debit, ytd_debit, credit, ytd_credit, balance, ytd_balance)
VALUES(?,?,?,?,?,?,?,?,?,?)
"""
  cursor2.fast_executemany = True
  cursor2.executemany(im2,rows)
  cursor2.commit()
  cursor2.close()



except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stdout(error_msg) 

except Exception as e:
  ret = 2
  print_to_stdout(e) 

finally:
  print_to_stdout(f"point 90")
  end_time = datetime.now()
  tdelta = end_time - start_time 
  print_to_stdout(f"total time: {tdelta}") 
  if 'conn' in globals():
    conn.close()
  if 'conn2' in globals():
    conn2.close()
  print_to_stdout(f"point 99")
  sys.exit(ret)