import openpyxl
import pandas as pd
import gzip
import json
from datetime import datetime, timedelta
from data.marketplace_dict import marketplace_dictionary
from dateutil import parser
import logging

logging.basicConfig(
    level=logging.WARNING,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
    filename='app reference/app.log',  # Specify the log file name
    filemode='a'  # Set the file mode (w: write, a: append)
)

# TODO 1: Set variables saved from credentials.csv
file_path = "./app reference/reference.xlsx"
# Open the file containing the list of filepaths
reference = openpyxl.load_workbook(file_path)
pathGz = reference["paths"]["B2"].value
pathJson = reference["paths"]["B3"].value
pathParsed = reference["paths"]["B5"].value
# pathASIN = reference["paths"]["B6"].value
pathInv = reference["paths"]["B6"].value
pathPrio = reference["paths"]["B7"].value
reference.close()


#TODO just inherit from Report, remove unnecessary attribute init? or will create cyclical reference
class Parser:
    def __init__(self, reportobj):
        self.path_gzip_base = reportobj.path_gzip_base
        self.path_parsed = pathParsed
        self.jsonkey = reportobj.jsonkey
        self.report_name = reportobj.report_name
        self.start_date = reportobj.requested_report_start_date
        self.end_date = reportobj.requested_report_end_date
        self.gz_file = reportobj.gz_file
        self.csv_file = pathParsed + reportobj.filename_string + ".csv"
        self.secondary_file = reportobj.secondary_file
        self.pathASIN = marketplace_dictionary[reportobj.mp]["ASIN_Path"]

    def parse_source_pos_item_details(self):
        ASIN_df = pd.read_excel(self.pathASIN, sheet_name="LIST")
        ASIN_df_key = 'ASIN'
        ASIN_df = ASIN_df.rename(columns={"Item Number": "Alpine Item#"})
        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))[self.jsonkey]
            arrange_cols = ['ASIN'
                            , 'Product Title'
                            , 'Shipped Revenue'
                            , "Shipped Revenue - Prior Period"
                            , "Shipped Revenue - Same Period Last Year"
                            , "Shipped COGS"
                            , "Shipped COGS - Prior Period"
                            , "Shipped COGS - Same Period Last Year"
                            , "Shipped Units"
                            , "Shipped Units - Prior Period"
                            , "Shipped Units - Same Period Last Year"
                            , "Customer Returns"
                            , "Customer Returns - Prior Period"
                            , "Customer Returns - Same Period Last Year"
                            , "Week Ending"
                            , "Distributor View"
                            , "Reporting Range"
                            , "Alpine Item#"
                            , "AVG Sales Price TY"
                            , "Key"
                            # , "To_Date"
                            ]
            try:
                df = pd.DataFrame(jsondata)
                pd.set_option('display.max_columns', None)
                df_key = "ASIN"

                df['Shipped COGS'] = df['shippedCogs'].apply(lambda x: x['amount'] if x is not None else 0)
                # df['Currency Code'] = df['shippedCogs'].apply(lambda x: x['currencyCode'] if x is not None else None)
                df['Shipped Revenue'] = df['shippedRevenue'].apply(lambda x: x['amount'] if x is not None else 0)
                df.drop('shippedCogs', axis=1, inplace=True)
                df.drop('shippedRevenue', axis=1, inplace=True)
                df = df.rename(
                    columns={"asin": "ASIN"
                             , "customerReturns": "Customer Returns"
                             , "shippedUnits": "Shipped Units"
                             })
                df['Product Title'] = None
                df['Shipped Revenue - Prior Period'] = None
                df['Shipped Revenue - Same Period Last Year'] = None
                df['Shipped COGS - Prior Period'] = None
                df['Shipped COGS - Same Period Last Year'] = None
                df['Shipped Units - Prior Period'] = None
                df['Shipped Units - Same Period Last Year'] = None
                df['Customer Returns - Prior Period'] = None
                df['Customer Returns - Same Period Last Year'] = None
                df['Week Ending'] = df['startDate']
                df['Distributor View'] = 'Sourcing'
                df['Reporting Range'] = 'Daily'
                df['AVG Sales Price TY'] = df['Shipped Revenue'] / df['Shipped Units']

                df['key_date'] = pd.to_datetime(df['startDate'], format='%Y-%m-%d')
                df['key_serial'] = df['key_date'].apply(lambda x:
                                                        str(int((x - datetime(1900, 1, 1)).total_seconds() // (
                                                                    24 * 60 * 60)) + 2))
                df['Key'] = df['ASIN'] + "Daily" + df['key_serial']
                df.drop(['startDate', 'key_date', 'key_serial'], axis=1, inplace=True)

                merged_df = pd.merge(df, ASIN_df, left_on=df_key, right_on=ASIN_df_key, how='left')
                merged_df = merged_df[arrange_cols]
                merged_df.to_csv(self.csv_file, index=False)
                print("success parsing file")
            except Exception as e:
                blank_data = {col: [] for col in arrange_cols}
                blank_df = pd.DataFrame(blank_data)
                blank_df.to_csv(self.csv_file, index=False)
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                logging.exception(error_message)

    def parse_manufacturing_pos_item_details(self):
        ASIN_df = pd.read_excel(self.pathASIN, sheet_name="LIST")
        ASIN_df_key = 'ASIN'
        ASIN_df = ASIN_df.rename(columns={"Item Number": "Alpine Item#"})
        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))[self.jsonkey]
            arrange_cols = ['ASIN'
                            , 'Product Title'
                            , "Ordered Revenue"
                            , "Ordered Revenue - Prior Period"
                            , "Ordered Revenue - Same Period Last Year"
                            , "Ordered Units"
                            , "Ordered Units - Prior Period"
                            , "Ordered Units - Same Period Last Year"
                            , "Shipped Revenue"
                            , "Shipped Revenue - Prior Period"
                            , "Shipped Revenue - Same Period Last Year"
                            , "Shipped COGS"
                            , "Shipped COGS - Prior Period"
                            , "Shipped COGS - Same Period Last Year"
                            , "Shipped Units"
                            , "Shipped Units - Prior Period"
                            , "Shipped Units - Same Period Last Year"
                            , "Customer Returns"
                            , "Customer Returns - Prior Period"
                            , "Customer Returns - Same Period Last Year"
                            , "Week Ending"
                            , "Distributor View"
                            , "Reporting Range"
                            , "Alpine Item#"
                            # , "To_Date"
                            ]
            try:
                df = pd.DataFrame(jsondata)
                pd.set_option('display.max_columns', None)
                df_key = "ASIN"

                df['Ordered Revenue'] = df['orderedRevenue'].apply(lambda x: x['amount'] if x is not None else 0)
                # df['Currency Code'] = df['orderedRevenue'].apply(lambda x: x['currencyCode'] if x is not None else None)
                df['Shipped COGS'] = df['shippedCogs'].apply(lambda x: x['amount'] if x is not None else 0)
                df['Shipped Revenue'] = df['shippedRevenue'].apply(lambda x: x['amount'] if x is not None else 0)
                df.drop('shippedCogs', axis=1, inplace=True)
                df.drop('shippedRevenue', axis=1, inplace=True)
                df = df.rename(
                    columns={"asin": "ASIN"
                            , "orderedUnits": "Ordered Units"
                            , "customerReturns": "Customer Returns"
                            , "shippedUnits": "Shipped Units"
                             })
                df['Product Title'] = None
                df['Ordered Revenue - Prior Period'] = None
                df['Ordered Revenue - Same Period Last Year'] = None
                df['Ordered Units - Prior Period'] = None
                df['Ordered Units - Same Period Last Year'] = None
                df['Shipped Revenue - Prior Period'] = None
                df['Shipped Revenue - Same Period Last Year'] = None
                df['Shipped COGS - Prior Period'] = None
                df['Shipped COGS - Same Period Last Year'] = None
                df['Shipped Units - Prior Period'] = None
                df['Shipped Units - Same Period Last Year'] = None
                df['Customer Returns - Prior Period'] = None
                df['Customer Returns - Same Period Last Year'] = None
                df['Week Ending'] = df['startDate']
                df['Distributor View'] = 'Manufacturing'
                df['Reporting Range'] = 'Daily'

                df.drop(['startDate'], axis=1, inplace=True)

                merged_df = pd.merge(df, ASIN_df, left_on=df_key, right_on=ASIN_df_key, how='left')

                merged_df = merged_df[arrange_cols]
                merged_df.to_csv(self.csv_file, index=False)
                print("success parsing file")
            except Exception as e:
                blank_data = {col: [] for col in arrange_cols}
                blank_df = pd.DataFrame(blank_data)
                blank_df.to_csv(self.csv_file, index=False)
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                logging.exception(error_message)

    def parse_source_inventory_health(self):
        ASIN_df = pd.read_excel(self.pathASIN, sheet_name="LIST")
        ASIN_df_key = 'ASIN'
        ASIN_df = ASIN_df.rename(columns={"Item Number": "SKU"})
        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))[self.jsonkey]
            arrange_cols = ['DATE'
                            , 'ASIN'
                            , 'SKU'
                            , 'Product title'
                            , 'Vendor Confirmation Rate'
                            , 'Vendor Confirmation Rate - Prior Period'
                            , 'Vendor Confirmation Rate - Same Period Last Year'
                            , 'Net Received'
                            , 'Net Received – Prior Period'
                            , 'Net Received – Same Period Last Year'
                            , 'Net Received Units'
                            , 'Net Received Units – Prior Period'
                            , 'Net Received Units – Same Period Last Year'
                            , 'Open Purchase Order Quantity'
                            , 'Open Purchase Order Quantity – Prior Period'
                            , 'Open Purchase Order Quantity – Same Period Last Year'
                            , 'Receive Fill Rate %'
                            , 'Receive Fill Rate % – Prior Period'
                            , 'Receive Fill Rate % – Same Period Last Year'
                            , 'Overall Vendor Lead Time (days)'
                            , 'Overall Vendor Lead Time (days) – Prior Period'
                            , 'Overall Vendor Lead Time (days) – Same Period Last Year'
                            , 'Aged 90+ Days Sellable Inventory'
                            , 'Aged 90+ Days Sellable Inventory – Prior Period'
                            , 'Aged 90+ Days Sellable Inventory – Same Period Last Year'
                            , 'Aged 90+ Days Sellable Units'
                            , 'Aged 90+ Days Sellable Units – Prior Period'
                            , 'Aged 90+ Days Sellable Units – Same Period Last Year'
                            , 'Sellable On Hand Inventory'
                            , 'Sellable On-Hand Inventory – Prior Period'
                            , 'Sellable On-Hand Inventory – Same Period Last Year'
                            , 'Sellable On Hand Units'
                            , 'Sellable On-Hand Units – Prior Period'
                            , 'Sellable On-Hand Units – Same Period Last Year'
                            , 'Unsellable On Hand Inventory'
                            , 'Unsellable On Hand Inventory – Prior Period'
                            , 'Unsellable On-Hand Inventory – Same Period Last Year'
                            , 'Unsellable On Hand Units'
                            , 'Unsellable On-Hand Units – Prior Period'
                            , 'Unsellable On-Hand Units – Same Period Last Year'
                            , 'Sell-Through Rate'
                            , 'Sell-Through Rate – Prior Period'
                            , 'Sell-Through Rate – Same Period Last Year'
                            , 'Unhealthy Inventory'
                            , 'Unhealthy Inventory – Prior Period'
                            , 'Unhealthy Inventory – Same Period Last Year'
                            , 'Unhealthy Units'
                            , 'Unhealthy Units – Prior Period'
                            , 'Unhealthy Units – Same Period Last Year'
                            , 'QOH'
                            , 'Selling Price'
                            , 'Total Sellable'
                            ]
            try:
                df = pd.DataFrame(jsondata)
                pd.set_option('display.max_columns', None)
                df_key = "ASIN"

                #split columns
                df['Net Received'] = df['netReceivedInventoryCost'].apply(lambda x: x['amount'] if x is not None else 0)
                # df['Currency Code'] = df['netReceivedInventoryCost'].apply(lambda x: x['currencyCode'] if x is not None else None)
                df['Sellable On Hand Inventory'] = df['sellableOnHandInventoryCost'].apply(lambda x: x['amount'] if x is not None else 0)
                df['Unsellable On Hand Inventory'] = df['unsellableOnHandInventoryCost'].apply(lambda x: x['amount'] if x is not None else 0)
                df['Aged 90+ Days Sellable Inventory'] = df['aged90PlusDaysSellableInventoryCost'].apply(lambda x: x['amount'] if x is not None else 0)
                df['Unhealthy Inventory'] = df['unhealthyInventoryCost'].apply(lambda x: x['amount'] if x is not None else 0)

                df.drop(['netReceivedInventoryCost','sellableOnHandInventoryCost','unsellableOnHandInventoryCost',
                         'aged90PlusDaysSellableInventoryCost','unhealthyInventoryCost'], axis=1, inplace=True)

                df = df.rename(columns={"asin": "ASIN"
                            , "startDate" : "DATE"
                            , "vendorConfirmationRate" : "Vendor Confirmation Rate"
                            , "netReceivedInventoryUnits" : "Net Received Units"
                            , "openPurchaseOrderUnits": "Open Purchase Order Quantity"
                            , "receiveFillRate": "Receive Fill Rate %"
                            , "averageVendorLeadTimeDays": "Overall Vendor Lead Time (days)"
                            , "aged90PlusDaysSellableInventoryUnits" : "Aged 90+ Days Sellable Units"
                            , "sellableOnHandInventoryUnits" : "Sellable On Hand Units"
                            , "unsellableOnHandInventoryUnits" : "Unsellable On Hand Units"
                            , "sellThroughRate" : "Sell-Through Rate"
                            , "unhealthyInventoryUnits" : "Unhealthy Units"
                             })
                #create null columns for prior period and same period last year

                df['Sellable On Hand Units'] = df['Sellable On Hand Units'].fillna(0)
                df['Product title'] = None
                df['Vendor Confirmation Rate - Prior Period'] = None
                df['Vendor Confirmation Rate - Same Period Last Year'] = None
                df['Net Received – Prior Period'] = None
                df['Net Received – Same Period Last Year'] = None
                df['Net Received Units – Prior Period'] = None
                df['Net Received Units – Same Period Last Year'] = None
                df['Open Purchase Order Quantity – Prior Period'] = None
                df['Open Purchase Order Quantity – Same Period Last Year'] = None
                df['Receive Fill Rate % – Prior Period'] = None
                df['Receive Fill Rate % – Same Period Last Year'] = None
                df['Overall Vendor Lead Time (days) – Prior Period'] = None
                df['Overall Vendor Lead Time (days) – Same Period Last Year'] = None
                df['Aged 90+ Days Sellable Inventory – Prior Period'] = None
                df['Aged 90+ Days Sellable Inventory – Same Period Last Year'] = None
                df['Aged 90+ Days Sellable Units – Prior Period'] = None
                df['Aged 90+ Days Sellable Units – Same Period Last Year'] = None
                df['Sellable On-Hand Inventory – Prior Period'] = None
                df['Sellable On-Hand Inventory – Same Period Last Year'] = None
                df['Sellable On-Hand Units – Prior Period'] = None
                df['Sellable On-Hand Units – Same Period Last Year'] = None
                df['Unsellable On Hand Inventory – Prior Period'] = None
                df['Unsellable On-Hand Inventory – Same Period Last Year'] = None
                df['Unsellable On-Hand Units – Prior Period'] = None
                df['Unsellable On-Hand Units – Same Period Last Year'] = None
                df['Sell-Through Rate – Prior Period'] = None
                df['Sell-Through Rate – Same Period Last Year'] = None
                df['Unhealthy Inventory – Prior Period'] = None
                df['Unhealthy Inventory – Same Period Last Year'] = None
                df['Unhealthy Units – Prior Period'] = None
                df['Unhealthy Units – Same Period Last Year'] = None
                df['QOH'] = df['Open Purchase Order Quantity'].fillna(0) + df['Sellable On Hand Units'].fillna(0)
                df['Selling Price'] = df.apply(lambda row: row['Sellable On Hand Inventory'] / row['Sellable On Hand Units'] if (hasattr(row, 'Sellable On Hand Units') and pd.notnull(row['Sellable On Hand Units']) and row['Sellable On Hand Units'] != 0) else 0, axis=1)
                df['Total Sellable'] = df['QOH'] * df['Selling Price']

                merged_df = pd.merge(df, ASIN_df, left_on=df_key, right_on=ASIN_df_key, how='left')
                merged_df = merged_df[arrange_cols]
                merged_df.to_csv(self.csv_file, encoding='utf-8', index=False)
                print("success parsing file")
            except Exception as e:
                blank_data = {col: [] for col in arrange_cols}
                blank_df = pd.DataFrame(blank_data)
                blank_df.to_csv(self.csv_file, index=False)
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                logging.exception(error_message)

    def parse_traffic(self):
        ASIN_df = pd.read_excel(self.pathASIN, sheet_name="LIST")
        ASIN_df_key = 'ASIN'
        ASIN_df = ASIN_df.rename(columns={"Item Number": "Alpine Item"})
        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))[self.jsonkey]
            arrange_cols = ['ASIN'
                            , 'Product Title'
                            , 'Glance Views'
                            , "Glance Views - Prior Period"
                            , "Glance Views - Same Period Last Year"
                            , "Week Ending"
                            , "Reporting Range"
                            , "Alpine Item"
                            ]
            try:
                df = pd.DataFrame(jsondata)
                pd.set_option('display.max_columns', None)
                df_key = "ASIN"

                df = df.rename(
                    columns={"asin": "ASIN"
                            , "glanceViews": "Glance Views"
                            , "startDate": "Week Ending"
                             })
                df['Product Title'] = None
                df['Glance Views - Prior Period'] = None
                df['Glance Views - Same Period Last Year'] = None
                df['Glance Views - Prior Period'] = None
                df['Reporting Range'] = 'Daily'

                merged_df = pd.merge(df, ASIN_df, left_on=df_key, right_on=ASIN_df_key, how='left')
                merged_df = merged_df[arrange_cols]
                merged_df.to_csv(self.csv_file, index=False)
                print("success parsing file")
            except Exception as e:
                blank_data = {col: [] for col in arrange_cols}
                blank_df = pd.DataFrame(blank_data)
                blank_df.to_csv(self.csv_file, index=False)
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                logging.exception(error_message)

    def parse_pos_data(self):
        ASIN_df = pd.read_excel(self.pathASIN, sheet_name="LIST")
        ASIN_df = ASIN_df.rename(columns={"Item Number": "SKU"})
        ASIN_df_key = 'ASIN'

        Inv_df = pd.read_excel(pathInv, sheet_name="inventory_file")
        columns_to_keep = ['ITEM', 'GROUP_CD']
        Inv_df = Inv_df.loc[:, columns_to_keep]
        Inv_df = Inv_df.rename(columns={"GROUP_CD": "SKU Category"})
        Inv_df_key = 'ITEM'

        prio_df = pd.read_excel(pathPrio, sheet_name="priority")
        prio_df = prio_df.rename(columns={"Type": "Priority Category"})
        prio_df = prio_df.drop('Rank', axis=1)
        prio_df_key = 'item'

        print('done reading 3 df')

        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))[self.jsonkey]
            arrange_cols = ["Priority Category"
                            , "SKU Category"
                            , "ASIN"
                            , "Item Name"
                            , "Amazon \nModel #"
                            , "Week"
                            , "Qty"
                            , "Week_Start"]
            try:
                df = pd.DataFrame(jsondata)
                pd.set_option('display.max_columns', None)
                df_key = "asin"

                df_columns_to_keep = ['asin', 'shippedUnits']
                df = df.loc[:, df_columns_to_keep]

                date_obj = datetime.strptime(self.start_date, '%Y-%m-%d')
                df['Week_Start'] = date_obj.strftime('%m/%d/%Y')
                df['Week'] = f'Week {date_obj.isocalendar()[1]}'
                df = df.rename(columns={'shippedUnits': 'Qty'})

                print(df.head())

                merged_df = pd.merge(df, ASIN_df, left_on=df_key, right_on=ASIN_df_key, how='left')
                merged_df_key = 'SKU'
                merged_df = merged_df.drop('asin', axis=1)
                merged_df = pd.merge(merged_df, Inv_df, left_on=merged_df_key, right_on=Inv_df_key, how='left')
                merged_df = merged_df.drop('ITEM', axis=1)
                merged_df = pd.merge(merged_df, prio_df, left_on=merged_df_key, right_on=prio_df_key, how='left')
                merged_df = merged_df.rename(columns={'SKU': 'Amazon \nModel #', 'item': 'Item Name'})
                merged_df['Item Name'] = None
                print(merged_df.head())

                merged_df = merged_df[arrange_cols]
                merged_df.to_csv(self.csv_file, encoding='utf-8', index=False)
                print(merged_df.head())
            except Exception as e:
                blank_data = {col: [] for col in arrange_cols}
                blank_df = pd.DataFrame(blank_data)
                blank_df.to_csv(self.csv_file, index=False)
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                logging.exception(error_message)

    def parse_forecast(self):
        ASIN_df = pd.read_excel(self.pathASIN, sheet_name="LIST")
        ASIN_df = ASIN_df.rename(columns={"Item Number": "SKU"})
        ASIN_df_key = 'ASIN'

        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))[self.jsonkey]
            arrange_cols = ['Key'
                            , 'Week Start'
                            , 'ASIN'
                            , "SKU"
                            , "Average 12 weeks"
                            , "Week"
                            , "Qty"
                            ]
            # print(jsondata)
            try:
                df = pd.DataFrame(jsondata)
                pd.set_option('display.max_columns', None)
                df_key = 'asin'
                df1 = df
                df1['startDate'] = pd.to_datetime(df1['startDate'])

                min_date = df1['startDate'].min()
                limit_date = (min_date + timedelta(days=56))#.strftime('%m/%d/%Y')

                df_filtered = df1[df1['startDate'] < limit_date]

                columns_to_keep = ['asin'
                    , 'startDate'
                    , 'endDate'
                    , "p70ForecastUnits"
                    ]
                df_avg = df_filtered[columns_to_keep]

                df_avg = df_avg.groupby('asin').agg({'p70ForecastUnits': 'mean'}).reset_index()
                df_avg.rename(columns={'p70ForecastUnits': 'Average 12 weeks'}, inplace=True)

                # df_avg.to_csv(self.csv_file, index=False)
                df_avg_key = 'asin'
                # print(ASIN_df)
                # print(df_avg)

                merged_df1 = pd.merge(df_avg, ASIN_df, left_on=df_avg_key, right_on=ASIN_df_key, how='left')
                columns_to_keep = ['asin'
                                , 'SKU'
                                , 'Average 12 weeks'
                                   ]
                merged_df1 = merged_df1[columns_to_keep]
                merged_df1_key = 'asin'

                df['key_date'] = pd.to_datetime(df['startDate'], format='%Y-%m-%d')

                df['Week_num'] = ((df['startDate'] - min_date) / timedelta(weeks=1)).astype(int)
                # df['Week'] = 'Week ' + (df['Week_num'] + 1).astype(str) + ' - P70 Forecast'
                df['Week'] = 'Week ' + df['Week_num'].apply(lambda x: f"{x:2d}") + ' - P70 Forecast' #inserting one space before single digit integers

                df['key_serial'] = df['key_date'].apply(lambda x:
                                                        str(int((x - datetime(1900, 1, 1)).total_seconds() // (
                                                                    24 * 60 * 60)) + 2))

                merged_df2 = pd.merge(df, merged_df1, left_on=merged_df1_key, right_on=df_key, how='left')
                merged_df2['Key'] = merged_df2['key_serial'] + merged_df2['SKU']
                merged_df2['Week Start'] = min_date.strftime('%m/%d/%Y')
                merged_df2 = merged_df2.rename(columns={"asin":"ASIN", "p70ForecastUnits":"Qty"})
                print(merged_df2)

                merged_df2 = merged_df2[arrange_cols]
                merged_df2.to_csv(self.csv_file, index=False)
                print("finished parsing")
            except Exception as e:
                blank_data = {col: [] for col in arrange_cols}
                blank_df = pd.DataFrame(blank_data)
                blank_df.to_csv(self.csv_file, index=False)
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                logging.exception(error_message)

    def parse_netppm(self):
        ASIN_df = pd.read_excel(self.pathASIN, sheet_name="LIST")
        ASIN_df_key = 'ASIN'
        ASIN_df = ASIN_df.rename(columns={"Item Number": "AlpineSKU"})

        sales_df = pd.read_csv(self.secondary_file)
        sales_df_key = ['ASIN', 'Week Ending']
        sales_columns = ['ASIN', 'Week Ending', 'Shipped COGS']
        sales_df = sales_df[sales_columns]
        print(sales_df.head())

        with gzip.open(self.gz_file, 'rb') as file:
            jsondata = json.loads(file.read().decode('utf-8'))[self.jsonkey]
            arrange_cols = ["ASIN"
                            , "Subcategory"
                            , "Product Title"
                            , "Net PPM"
                            , "Net PPM - Prior Period"
                            , "Net PPM - Last Year"
                            , "Benchmark PPM"
                            , "Shipped COGS Month"
                            , "Variance PPM"
                            , "Estimated $ owe to Amazon"
                            , "AlpineSKU"
                            , "Over/Under 38%"
                            , "DateType"
                            , "Date"
                            , "Key"
                            , "Shipped COGS"
                            , "Shipped COGS LY"
                            ]

            try:
                df = pd.DataFrame(jsondata)
                pd.set_option('display.max_columns', None)

                df = df.rename(columns={"asin": "ASIN", "netPureProductMargin": "Net PPM", "startDate": "Date"})
                df_key = "ASIN"

                df['Subcategory'] = None
                df['Product Title'] = None
                df['Net PPM - Prior Period'] = None
                df['Net PPM - Last Year'] = None
                df['Benchmark PPM'] = .38
                df['Shipped COGS Month'] = None
                df['Variance PPM'] = None #replaced in Sisense
                df['Estimated $ owe to Amazon'] = None
                df['DateType'] = 'Daily'
                df['Over/Under 38%'] = df['Net PPM'].apply(lambda x: 'Over38%' if x > 0.38 else 'Under38%')

                # df.to_csv(self.csv_file, index=False)
                print(df.head())

                merged_df1 = pd.merge(df, ASIN_df, left_on=df_key, right_on=ASIN_df_key, how='left')
                # merged_df1.to_csv(self.csv_file, index=False)
                merged_df1_key = ['ASIN', 'Date']
                merged_df2 = pd.merge(merged_df1, sales_df, left_on=merged_df1_key, right_on=sales_df_key, how='left')

                merged_df2['Shipped COGS LY'] = None
                merged_df2['Key'] = None

                merged_df2['key_date'] = pd.to_datetime(merged_df2['Date'], format='%Y-%m-%d')
                merged_df2['key_serial'] = merged_df2['key_date'].apply(lambda x:
                                                                        str(int(
                                                                            (x - datetime(1900, 1, 1)).total_seconds() // (
                                                                                    24 * 60 * 60)) + 2))
                merged_df2['Key'] = merged_df2['ASIN'] + "Daily" + merged_df2['key_serial']
                merged_df2.drop(['key_date', 'key_serial'], axis=1, inplace=True)

                merged_df2 = merged_df2[arrange_cols]
                merged_df2.to_csv(self.csv_file, index=False)
                print(merged_df2.head())
            except Exception as e:
                blank_data = {col: [] for col in arrange_cols}
                blank_df = pd.DataFrame(blank_data)
                blank_df.to_csv(self.csv_file, index=False)
                error_message = f"An error occurred: {str(e)}"
                print(error_message)
                logging.exception(error_message)













