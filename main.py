import time
from classes.reports import newReport
from data.report_dict import report_dictionary
from data.marketplace_dict import marketplace_dictionary
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
    filename='app reference/app.log',  # Specify the log file name
    filemode='a'  # Set the file mode (w: write, a: append)
)
reports = ['INVENTORY_W_S']
markets = ['US']

# reports = ['SALES_D_S']
# markets = ['US']

def run_manual(report_type, mp, x, y):
    report = newReport(report_type, mp)
    report.update_report_body(custom_start=x, custom_end=y)
    report.request_report()
    while report.report_status != "DONE":
        report.get_report(report.report_id)
        if report.doc_id != "":
            report.get_report_link(report.doc_id)
            report.download_report()
            # report.parse_and_update_report()
        else:
            time.sleep(20)


def run_auto(reports, markets):
    # Create a list to store the objects
    report_objects = []
    excluded_report_objects = []

    for market in markets:
        for report in reports:
            new_report = newReport(f"{report}", f"{market}")
            if new_report.request_report() == 202:
                report_objects.append(new_report)
            else:
                excluded_report_objects.append(new_report)
            time.sleep(2)

    done_processing_report_objects = []
    no_of_reports = len(report_objects)

    print(report_objects)
    print(excluded_report_objects)

    while no_of_reports != len(done_processing_report_objects):
        for report in report_objects:
            report.get_report(report.report_id)

            if report.report_status == 'FATAL':
                report_objects.remove(report)
                no_of_reports -= 1

                error_message = f"Removed {report} from downloads, report Status: {report.report_status}"
                logging.error(error_message)
                print(error_message)
                raise Exception(error_message)

            elif report.report_status == 'DONE':
                done_processing_report_objects.append(report)
                report_objects.remove(report)
                if report.doc_id != "":
                    report.get_report_link(report.doc_id)
                    report.download_report()
                    report.parse_and_update_report()
                else:
                    print("DONE but no doc_id???")
            else:
                pass
            time.sleep(20)

    print(report_objects)
    print(excluded_report_objects)
    print(done_processing_report_objects)


report_type = input("Type M for manual or A for auto: ")

if report_type.upper() == 'M':
    reports_list = [key for key in report_dictionary]
    markets_list = [key for key in marketplace_dictionary]
    print(reports_list)
    print(markets_list)
    Report_Value = input("Type in desired Report: ")
    Market = input("Type in desired Market: ")
    Start_Date = input("Type in desired Start Date: ")
    End_Date = input("Type in desired End Date: ")

    run_manual(Report_Value, Market, Start_Date, End_Date)

elif report_type.upper() == 'A':
    print(f"Report will run for the following reports: {reports} and marketplace {markets}")
    run_auto(reports, markets)
else:
    print("You didn't choose a valid option")

# report = newReport('NETPPM_D', 'US')
# report.gz_file = 'C:/Users/emman/PycharmProjects/Amazon_SP-API/raw_data/US_NetPPM_2023-07-13_2023-07-13.json.gz'
# report.filename_string = 'US_NetPPM_2023-07-13_2023-07-13'
# # report.csv_file = 'C:/Users/emman/PycharmProjects/Amazon_SP-API/parsed_csv_temp/US_NetPPM_2023-07-13_2023-07-13.csv'
# report.parse_and_update_report()

# report = newReport('INVENTORY_W_S', 'US')
# report.gz_file = 'C:/Users/emman/PycharmProjects/Amazon_SP-API/raw_data/US_Inventory_Weekly_Sc_2023-07-02_2023-07-08.json.gz'
# report.filename_string = 'US_Inventory_Weekly_Sc_2023-07-02_2023-07-08'
# # report.csv_file = 'C:/Users/emman/PycharmProjects/Amazon_SP-API/parsed_csv_temp/US_Inventory_Weekly_Sc_2023-07-02_2023-07-08.csv'
# report.parse_and_update_report()



