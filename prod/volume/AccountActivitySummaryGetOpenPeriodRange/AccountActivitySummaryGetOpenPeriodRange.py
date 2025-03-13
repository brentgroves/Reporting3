#!/usr/bin/env python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging

# https://docs.python-zeep.org/en/master/
#import xmltodict
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport
import pyodbc
from datetime import datetime
import sys 
import mysql.connector
from mysql.connector import Error
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
## %DEV%sys.path.insert(1, '/home/brent/src/Reporting/prod/volume/modules')   
#   sys.path.insert(1, '/volume/modules')   

#%DEV%pcn = '123681'
  # # pcn = '300758'
#%DEV%username = 'mg.odbcalbion'
#%DEV%password = 'Mob3xalbion'
#%DEV%username2 = 'mgadmin' 
#%DEV%password2 = 'WeDontSharePasswords1!' 
#%DEV%username3 = 'root'
#%DEV%password3 = 'password'
#%DEV%username4 = 'MGEdonReportsws@plex.com'
#%DEV%password4 = '9f45e3d-67ed-'
#%DEV%mysql_host = 'reports31'
  # # mysql_host = 'reports13'
#%DEV%mysql_port = '30031'
#%DEV%azure_dw = '1'


  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time=}")

  start_period = 0
  end_period = 0
  start_open_period = 0
  end_open_period = 0
  no_update = 9

  # https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
    # password = 'wrong' 
  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
    # https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc
  cursor = conn.cursor()

  # accounting_period_ranges_dw_import
  rowcount=cursor.execute("{call sproc123681_11728751_2112421 (?)}", pcn)
  rows = cursor.fetchall()
  print_to_stdout(f"call sproc123681_11728751_2112421 - rowcount={rowcount}")
  print_to_stdout(f"call sproc123681_11728751_2112421 - messages={cursor.messages}")

  cursor.close()
  fetch_time = datetime.now()
  tdelta = fetch_time - start_time 
  print_to_stdout(f"fetch_time={tdelta}") 

  # start_period = rows[0][1] #param 2
  # end_period = rows[0][2] #param 3
  start_open_period = rows[0][3] #param 4
  end_open_period = rows[0][4] #param 5
  # no_update = rows #param 6

  period = start_open_period

  year = period // 100

  # Get Max fiscal period
  # max_fiscal_period = 0

  # https://stackoverflow.com/questions/50750101/pyodbc-read-output-parameter-of-stored-procedure-sql-server
  # https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html
  # elf-contained driver. Connector/Python does not require the MySQL client library or any Python modules outside the standard library.
  # https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
  conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')
  cursor2 = conn2.cursor()

  # DECLARE @out nvarchar(max);
  # SET NOCOUNT ON;
  # EXEC [dbo].[storedProcedure] @x = ?, @y = ?, @z = ?,@param_out = @out OUTPUT;
  # SELECT @out AS the_output;

  sql_max = """\
DECLARE @MAX_FISCAL_PERIOD INT;
EXEC Plex.sp_max_fiscal_period @pcn = ?,@year = ?,@max_fiscal_period=@MAX_FISCAL_PERIOD OUT
SELECT @MAX_FISCAL_PERIOD
"""

  # cursor.execute(sql, (x, y, z))
  # row = cursor.fetchone()
  # print(row[0])

  cursor2.execute(sql_max, (pcn, year))
  row = cursor2.fetchone()
  max_fiscal_period = row[0]

  # print(max_fiscal_period)


  # https://docs.python-zeep.org/en/master/transport.html?highlight=authentication#http-authentication
  session = Session()
  session.auth = HTTPBasicAuth(username4,password4)
  # session.auth = HTTPBasicAuth('MGEdonReportsws@plex.com','9f45e3d-67ed-')

  client = Client(wsdl='/home/brent/src/Reporting2/prod/volume/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # prod
#%DEV%client = Client(wsdl='/home/brent/src/Reporting2/prod/volume/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # stand-alone .
  
  # https://docs.python-zeep.org/en/master/datastructures.html
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

      # e=e_type(DataSourceKey=8619,InputParameters=[{'Value':'4/26/2022','Name':'@Report_Date','Required':False,'Output':False}],DataSourceName='Detailed_Production_Get_New')
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
        str(round(float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value),5)),
        # i.Columns.Column[5].Value-i.Columns.Column[6].Value,
        i.Columns.Column[7].Value)) # ending balance
        # debug section
        # print(rec[row])
        # row=row+1

    
      # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
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

except Error as e:
    ret = 1
    print("Error while connecting to MySQL", e)

except BaseException as error:
    ret = 1
    print('An exception occurred: {}'.format(error))

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