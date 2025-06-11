#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "zeep",
#     "pyodbc",
# ]
# ///
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport
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
  username = (sys.argv[2])
  password = (sys.argv[3])
  username2 = (sys.argv[4])
  password2 = (sys.argv[5])
  username3 = (sys.argv[6])
  password3 = (sys.argv[7])
  username4 = (sys.argv[8])
  password4 = (sys.argv[9])
  mysql_host = (sys.argv[10])
  mysql_port = (sys.argv[11])
  azure_dw = (sys.argv[12])

#%DEV%pcn = '123681'
#%DEV%username = 'mg.odbcalbion'
#%DEV%password = 'Mob3xalbion'
#%DEV%username2 = 'repsys1' 
#%DEV%password2 = 'WeDontSharePasswords1!' 
#%DEV%username3 = 'root'
#%DEV%password3 = 'password'
#%DEV%username4 = 'MGEdonReportsws@plex.com'
#%DEV%password4 = '9f45e3d-67ed-'
#%DEV%mysql_host = 'reports31'
#%DEV%mysql_port = '30031'
#%DEV%azure_dw = '1'

  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time=}")

  start_period = 0
  end_period = 0
  start_open_period = 0
  end_open_period = 0
  no_update = 9

  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
    # https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc
  cursor = conn.cursor()

  # accounting_period_ranges_dw_import
  obj=cursor.execute("{call sproc123681_11728751_2112421 (?)}", pcn)
  rows = cursor.fetchall()
  print_to_stdout(f"call sproc123681_11728751_2112421 - len={len(rows)}")
  print_to_stdout(f"call sproc123681_11728751_2112421 - messages={cursor.messages}")

  cursor.close()
  fetch_time = datetime.now()
  tdelta = fetch_time - start_time 
  print_to_stdout(f"fetch_time={tdelta}") 

  start_open_period = rows[0][3]
  end_open_period = rows[0][4] 

  period = start_open_period
  year = period // 100

  conn2 = pyodbc.connect('DSN=repsys1;UID='+username2+';PWD='+ password2 + ';DATABASE=repsys1')
  cursor2 = conn2.cursor()

  sql_max = """\
DECLARE @MAX_FISCAL_PERIOD INT;
EXEC Plex.sp_max_fiscal_period @pcn = ?,@year = ?,@max_fiscal_period=@MAX_FISCAL_PERIOD OUT
SELECT @MAX_FISCAL_PERIOD
"""

  cursor2.execute(sql_max, (pcn, year))
  row = cursor2.fetchone()
  max_fiscal_period = row[0]

  session = Session()
  session.auth = HTTPBasicAuth(username4,password4)

  client = Client(wsdl='/home/brent/src/Reporting3/prod/volume/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # prod
#%DEV%client = Client(wsdl='/home/brent/src/Reporting3/prod/volume/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # stand-alone .
  
  e_type = client.get_type('ns0:ExecuteDataSourceRequest')
  a_ip_type = client.get_type('ns0:ArrayOfInputParameter')
  ip_type=client.get_type('ns0:InputParameter')
  ip_pcn = ip_type(Value=pcn,Name='@PCNs',Required=False,Output=False)


  while period <= end_open_period:
    # account_no_from and account_no_to parameters are inclusive
    # Account total from accounting_account_DW_Import on Dec 3,2024 = 4889
    # Try to break accounts into 2 groups of ~ 2500 records
    # to prevent web service call from timing out.

    # Total records = 2209 + 2684 = 4893
    # row_count = 2209 on Dec 3, 2024
    account_no_from = '00000-000-0000'
    account_no_to = '66666-666-6666'

    # # row_count = 2684 on Dec 3, 2024
    # account_no_from = '66666-666-6666'
    # account_no_to = '99999-999-9999'

    for x in range(2):
      ip_period_start = ip_type(Value=period,Name='@Period_Start',Required=True,Output=False)
      ip_period_end = ip_type(Value=period,Name='@Period_End',Required=True,Output=False)
      ip_account_no_from = ip_type(Value=account_no_from,Name='@Account_No_From',Required=False,Output=False)
      ip_account_no_to = ip_type(Value=account_no_to,Name='@Account_No_To',Required=False,Output=False)
      Parameters=a_ip_type([ip_pcn,ip_period_start,ip_period_end,ip_account_no_from,ip_account_no_to])

      e=e_type(DataSourceKey=4814,InputParameters=Parameters,DataSourceName='Account_Activity_Summary_xPCN_Get')

      test=0
      response = client.service.ExecuteDataSource(e)

      # test=0
      # if response.Error == True:
      #   test=1
      # if response.Error == False:
      #   test=2

      # collect desired columns of the result set into a list  
      list = response['ResultSets'].ResultSet[0].Rows.Row
      rec=[]
      row=0
      for i in list:
        # balance = float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value)
        # str(round(float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value),5)),
        rec.append((pcn,period,
        i.Columns.Column[1].Value, # account_no
        i.Columns.Column[4].Value, # beginning balance
        i.Columns.Column[5].Value, # debit
        i.Columns.Column[6].Value, # credit
        str(round(float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value),5)), # balance
        i.Columns.Column[7].Value)) # ending balance
        # debug section
        # print(rec[row])
        # row=row+1

      sql = "delete from Plex.account_activity_summary WHERE pcn = ? and period = ? and account_no BETWEEN ? and ?"
      rowcount=cursor2.execute(sql, (pcn,period,account_no_from,account_no_to)).rowcount
      print_to_stdout(f"delete from Plex.account_activity_summary - rowcount={rowcount}")
      print_to_stdout(f"delete from Plex.account_activity_summary - messages={cursor2.messages}")
      cursor2.commit()

      im2 ='''insert into Plex.account_activity_summary (pcn,period,account_no,beginning_balance,debit,credit,balance,ending_balance)
      values (?,?,?,?,?,?,?,?)'''
      cursor2.fast_executemany = True
      cursor2.executemany(im2,rec) 
      cursor2.commit()

      # row_count = 2684 on Dec 3, 2024
      account_no_from = '66666-666-6667'
      account_no_to = '99999-999-9999'

 
    if (period < max_fiscal_period):
      period = period + 1
    else:
      period = (year+1)*100 + 1
      year = period // 100
      # Get Max fiscal period
      max_fiscal_period = 0
      # The parameters are needed in the call but the output params are not changed but are in result_args.
      cursor2.execute(sql_max, (pcn, year))
      row = cursor2.fetchone()
      max_fiscal_period = row[0]
    # print_to_stdout(f"period={period}")

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

# #python -mzeep Plex_SOAP_test.wsdl
# # https://www.youtube.com/watch?v=JBYEQjg_znI
# # request = '<ExecuteDataSourceRequest xmlns="http://www.plexus-online.com/DataSource"><DataSourceKey>8619</DataSourceKey><InputParameters><InputParameter><Value>4/26/2022</Value><Name>@Report_Date</Name><Required>false</Required><Output>false</Output></InputParameter></InputParameters><DataSourceName>Detailed_Production_Get_New</DataSourceName></ExecuteDataSourceRequest>'

# # request = '''<ExecuteDataSourceRequest xmlns="http://www.plexus-online.com/DataSource">
# #     <DataSourceKey>8619</DataSourceKey>
# #     <InputParameters>
# #       <InputParameter>
# #         <Value>4/26/2022</Value>
# #         <Name>@Report_Date</Name>
# #         <Required>false</Required>
# #         <Output>false</Output>
# #       </InputParameter>
# #     </InputParameters>
# #     <DataSourceName>Detailed_Production_Get_New</DataSourceName>
# #   </ExecuteDataSourceRequest>'''
# # print(request)
# # client.service.ExecuteDataSource(request)