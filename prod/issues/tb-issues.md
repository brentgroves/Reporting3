# run tb

## Issue

If period range script is not ran before balance update script and the period range has changed in plex. Then the balance script will be retrieving records from periods that have not been deleted in the dw. The problem will not be because of the start period because that is calculated based upon the current date.  The problem will be with the end_date because that will be greater than the value in the dw that has not been updated. When the balance script tries to add records in the new end period it will fail because these records have not been deleted.

script accounting_balance_append_period_range_dw_import retrieves period balance records based upon the plex table. The Plex.accounting_balance_delete_period_range @pcn = ?; SPROC delete dw balance record based upon the start and end period stored in the dw period table. So the sproc will not delete the actual end period records which were retrieved by the Plex accounting_balance_append_period_range_dw_import script.

Fix: Since the balance script calls the accounting_balance_append_period_range_dw_import plex sproc the Plex.accounting_balance_delete_period_range script should take the start and end period as parameters instead assuming the period update script has ran and has updated these values in the dw period table.

Util the fix is made always run the AccountingPeriodRanges script prior to running the balance or activity summary scripts.

## Corner Case

On 2/4/25 3 accounts were added and "AccountingYearCategoryType" added the records for 2025 and 2026 but did not add them for 2024. Will this be ok? Yes. The code to handle adding the records to the previous and end periods year using the end_open_period year's "AccountingYearCategoryType" new records was added some time ago for AccountPeriodBalanceRecreatePeriodRange. Added code to handle adding the previous periods year using the end_open_periods year's "AccountingYearCategoryType" new records.
