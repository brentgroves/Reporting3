# Linamar Migration

- Created backup of Linamar's Azure SQL MI and imported into an OnPrem SQL Server database. Then created a backup of the OnPrem database and imported into the Azure SQL database. Direct importing of backup is not supported from Azure SQL MI to Azure SQL database. Done.
- connect to Plex using OpenAccess datadirect ODBC driver from 2nd system running newer version of Ubuntu and OpenSSL which does not support the preferred TLS 1.2 cipher suite that the DataDirect driver uses by default. Done.
- create linamar Azure SQL database DSN. Done.
- run Southfield's Trial Balance ETL scripts pointing to Mobex Azure SQL MI as usual.
- run Southfield's Trial Balance ETL scripts pointing to Linamar Azure SQL database.
- compare rowcounts and a few values of all 5 work tables in Mobex Azure SQL MI to the same tables in Linamar's Azure SQL database.
- Import the Mobex Azure SQL MI Trial Balance result into Linamar's Azure SQL database and compare result set using SQL.
- Run Southfield's Trial Balance Power BI report pointing to Linamar's Azure SQL database result set, export Excel for last 13 periods, and send to Dan Martin for verification.

## update lastpass for mi

```bash
pushd .. 
cd ~/src/Reporting2/prod/k8s/secrets/lastpass
./print-etc-lastpass.sh
# on dev system update local passwords in /etc/lastpass
./sed-lastpass-sh.sh reports31 30031 reports32 30332 reports 1
ls /etc/lastpass
# ssh to dev system
./lastpass_mi.sh
./print-etc-lastpass.sh

```

## run tb

## update lastpass for repsys1

```bash
pushd .. 
cd ~/src/Reporting2/prod/k8s/secrets/lastpass
./print-etc-lastpass.sh
# on dev system update local passwords in /etc/lastpass
./sed-lastpass-sh.sh reports31 30031 reports32 30332 reports 1
ls /etc/lastpass
# ssh to dev system
./lastpass_repsys1.sh
./print-etc-lastpass.sh

```
