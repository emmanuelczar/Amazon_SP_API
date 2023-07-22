import openpyxl
import pandas as pd
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
pathParsed = reference["paths"]["B5"].value
pathMainFile = reference["paths"]["B4"].value

reference.close()

# did not inherit from Report due to a chance of cyclical dependency


class Updater:
    def __init__(self, reportobj):
        self.report_name = reportobj.report_name
        self.start_date = reportobj.requested_report_start_date
        self.end_date = reportobj.requested_report_end_date
        self.path_parsed = pathParsed
        self.csv_file = pathParsed + reportobj.filename_string + ".csv"
        self.main_file = reportobj.main_file

    def update_source_pos_item_details(self):
        try:
            main_df = pd.read_csv(self.main_file, encoding='UTF-8')
            new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
            new_dates = new_df['Week Ending'].unique()

            main_df_filtered = main_df[~main_df['Week Ending'].isin(new_dates)].dropna(how='all')
            main_df_filtered = main_df_filtered.drop('To_Date', axis=1)
            updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)

            all_dates = updated_df['Week Ending'].unique()
            to_date = max([parser.parse(date)for date in all_dates]).strftime('%m/%d/%Y')
            updated_df['To_Date'] = to_date

            print("success updating main file")
            updated_df.to_csv(self.main_file, encoding='utf-8', index=False)
        except Exception as e:
            error_message = f"An error occurred in function update_source_pos_item_details while updating the main file: {str(e)}"
            logging.exception(error_message)

    def update_manufacturing_pos_item_details(self):
        try:
            main_df = pd.read_csv(self.main_file, encoding='UTF-8')
            new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
            new_dates = new_df['Week Ending'].unique()

            main_df_filtered = main_df[~main_df['Week Ending'].isin(new_dates)].dropna(how='all')
            main_df_filtered = main_df_filtered.drop('To_Date', axis=1)
            updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)

            all_dates = updated_df['Week Ending'].unique()
            to_date = max([parser.parse(date)for date in all_dates]).strftime('%m/%d/%Y')
            updated_df['To_Date'] = to_date

            print("success updating main file")
            updated_df.to_csv(self.main_file, encoding='utf-8', index=False)
        except Exception as e:
            error_message = f"An error occurred in function update_manufacturing_pos_item_details while updating the main file: {str(e)}"
            logging.exception(error_message)

    def update_traffic(self):
        try:
            main_df = pd.read_csv(self.main_file, encoding='UTF-8')
            new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
            new_dates = new_df['Week Ending'].unique()
    
            main_df_filtered = main_df[~main_df['Week Ending'].isin(new_dates)].dropna(how='all')
            main_df_filtered = main_df_filtered.drop('To_Date', axis=1)
            updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)
    
            all_dates = updated_df['Week Ending'].unique()
            to_date = max([parser.parse(date)for date in all_dates]).strftime('%m/%d/%Y')
            updated_df['To_Date'] = to_date
    
            print("success updating main file")
            updated_df.to_csv(self.main_file, encoding='utf-8', index=False)
        except Exception as e:
            error_message = f"An error occurred in function update_traffic while updating the main file: {str(e)}"
            logging.exception(error_message)

    def update_pos_data(self):
        try:
            main_df = pd.read_csv(self.main_file, encoding='UTF-8')
            new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
            new_dates = new_df['Week_Start'].unique()

            main_df_filtered = main_df[~main_df['Week_Start'].isin(new_dates)].dropna(how='all')
            updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)

            print("success updating main file")
            updated_df.to_csv(self.main_file, encoding='utf-8', index=False)
        except Exception as e:
            error_message = f"An error occurred in function update_pos_data while updating the main file: {str(e)}"
            logging.exception(error_message)

    def update_source_inventory_health(self):
        try:
            main_df = pd.read_csv(self.main_file, encoding='UTF-8')
            new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
            new_dates = new_df['DATE'].unique()

            main_df_filtered = main_df[~main_df['DATE'].isin(new_dates)].dropna(how='all')
            updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)

            print("success updating main file")
            updated_df.to_csv(self.main_file, encoding='utf-8', index=False)
        except Exception as e:
            error_message = f"An error occurred in function update_source_inventory_health while updating the main file: {str(e)}"
            logging.exception(error_message)

    def update_forecast(self):
        try:
            main_df = pd.read_csv(self.main_file, encoding='UTF-8')
            new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
            new_dates = new_df['Week Start'].unique()

            main_df_filtered = main_df[~main_df['Week Start'].isin(new_dates)].dropna(how='all')
            updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)

            print("success updating main file")
            updated_df.to_csv(self.main_file, encoding='utf-8', index=False)
        except Exception as e:
            error_message = f"An error occurred in function update_forecast while updating the main file: {str(e)}"
            logging.exception(error_message)

    def update_netppm(self):
        try:
            main_df = pd.read_csv(self.main_file, encoding='UTF-8')
            new_df = pd.read_csv(self.csv_file, encoding='UTF-8')
            new_dates = new_df['Date'].unique()

            main_df_filtered = main_df[~main_df['Date'].isin(new_dates)].dropna(how='all')
            main_df_filtered = main_df_filtered.drop('To date', axis=1)
            updated_df = pd.concat([main_df_filtered, new_df], ignore_index=True)

            all_dates = updated_df['Date'].unique()
            to_date = max([parser.parse(date) for date in all_dates]).strftime('%m/%d/%Y')
            updated_df['To date'] = to_date

            print("success updating main file")
            updated_df.to_csv(self.main_file, encoding='utf-8', index=False)

            to_date = max([parser.parse(date)for date in new_dates]).strftime('%m/%d/%Y')
            updated_df['To_Date'] = to_date
        except Exception as e:
            error_message = f"An error occurred in function update_netppm while updating the main file: {str(e)}"
            logging.exception(error_message)





