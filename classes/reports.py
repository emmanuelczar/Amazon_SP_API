import openpyxl
import requests
from datetime import datetime
import json
import gzip
import urllib.request
import logging


from data.marketplace_dict import marketplace_dictionary
from data.report_dict import report_dictionary
from data.default_dates import date_dictionary
from classes.authenticator import Authenticator


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
mainFilePath = reference["paths"]["B4"].value
reference.close()
reportsEndpoint = "reports/2021-06-30"
amzDate = datetime.now().strftime("%Y%m%dT%H%M%SZ")

today = datetime.now()

class Report:
    def __init__(self, mp):
        self.authenticator = Authenticator(mp)
        self.path_json_base = pathJson
        self.path_gzip_base = pathGz
        self.endpoint = reportsEndpoint
        self.report_id = ""
        self.doc_id = ""
        self.report_status = ""
        self.report_url = ""
        self.comp_algo = ""
        self.mp = mp
        self.mp_host = marketplace_dictionary[mp]["Host"]
        self.mp_id = marketplace_dictionary[mp]["MarketplaceId"]
        self.header = {"host": self.mp_host,
                        "x-amz-access-token": self.authenticator.accessToken,
                        "x-amz-date": amzDate,
                        "user-agent": "AlpineData v.0"}


class newReport(Report):
    def __init__(self, report_key, mp):
        super().__init__(mp)
        self.report_type_options = report_dictionary[report_key]
        self.report_key = report_key
        self.report_name = self.report_type_options["report_name"]
        self.report_body = self.report_type_options["report_body"]
        self.jsonkey = self.report_type_options["json_key"]
        self.processors = self.report_type_options["processor"]
        self.json = ""
        self.update_report_body()
        self.requested_report_end_date = ""
        self.requested_report_start_date = ""
        self.filename_string = ""
        self.gz_file = ""

    def update_report_body(self, custom_start=None, custom_end=None):
        """Updates request report body by referring into default_dates.py
        accepts custom_start and custom_end dates following this format YYYY-MM-DD"""
        if self.report_key.upper() != "FORECAST" and self.report_key.upper() != "CATALOG":
            if (custom_start and custom_end) is None:
                self.default_start = date_dictionary[self.report_key]["defaultStart"]
                self.default_end = date_dictionary[self.report_key]["defaultEnd"]
                self.report_body["marketplaceIds"] = [self.mp_id]
                self.report_body.update({'dataStartTime': self.default_start, 'dataEndTime': self.default_end,
                                         'marketplaceIds':[self.mp_id]})
            else:
                self.report_body.update({'dataStartTime': custom_start, 'dataEndTime': custom_end,
                                         'marketplaceIds': [self.mp_id]})
        else:
            self.report_body.update({'marketplaceIds': [self.mp_id]})

    def request_report(self):
        """requests for a report, retrieves report_id"""
        try:
            params = {"marketplaceIds": [self.mp_id]}
            response = requests.post(url=f"https://{self.mp_host}/{self.endpoint}/reports",
                                     data=json.dumps(self.report_body), headers=self.header, params=params)
            if response.status_code == 202:
                response_data = response.json()
                self.report_id = response_data['reportId']
                print(response_data)
                return response.status_code
            else:
                error_message = f"Report request failed with status code: {response.status_code}"
                logging.error(error_message)
                print(error_message)
                raise Exception(error_message)

        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred during the report request: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

        except (ValueError, KeyError) as e:
            error_message = f"Invalid response data: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e
        except Exception as e:
            error_message = f"An unknown error occurred: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

    def get_report(self, report_id):
        """Gets the report document ID to be used in downloading the report"""
        try:
            response = requests.get(url=f"https://{self.mp_host}/{self.endpoint}/reports/{report_id}",
                                    headers=self.header)
            if response.status_code == 200:
                response_data = response.json()
                self.report_status = response_data["processingStatus"]

                if self.report_status == 'DONE':
                    self.doc_id = response_data["reportDocumentId"]
                    self.requested_report_end_date = response_data["dataEndTime"][:10]
                    self.requested_report_start_date = response_data["dataStartTime"][:10]
                    print(response_data)
                    return response.status_code
                else:
                    print(response_data)
                    return self.report_status
            else:
                error_message = f"Request failed with status code: {response.status_code}"
                logging.error(error_message)
                print(error_message)
                raise Exception(error_message)

        except (ValueError, KeyError) as e:
            error_message = f"Invalid response data: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred during the request: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

        except Exception as e:
            error_message = f"An unknown error occurred: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

    def get_report_link(self, doc_id):
        """
        Returns the information required for retrieving a report document's contents
        using doc_id retrieved from get_report method.
        report_url = url for downloading the compressed json
        comp_algo = compression algorithm used in the report
        """
        try:
            response = requests.get(url=f"https://{self.mp_host}/{self.endpoint}/documents/{doc_id}",
                                    headers=self.header)
            response.raise_for_status()
            response_data = response.json()
            if "compressionAlgorithm" not in response_data or "url" not in response_data:
                raise ValueError("Invalid response data format")
            self.comp_algo = response_data['compressionAlgorithm']
            self.report_url = response_data["url"]
            print(response_data)
            return response.status_code

        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred during the request: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

        except (ValueError, KeyError) as e:
            error_message = f"Invalid response data: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e
        except Exception as e:
            error_message = f"An unknown error occurred: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

    def download_report(self):
        try:
            if self.report_name.upper() == 'FORECAST':
                start = date_dictionary[self.report_key]["defaultStart"]
                end = date_dictionary[self.report_key]["defaultEnd"]
                self.filename_string = f"{self.mp}_{self.report_name}_{start}_{end}"
                self.gz_file = self.path_gzip_base + self.filename_string + ".json.gz"
                # self.json_file = self.path_json_base + self.filename_string + ".json"
            else:
                self.filename_string = f"{self.mp}_{self.report_name}_{self.requested_report_start_date}_{self.requested_report_end_date}"
                self.gz_file = self.path_gzip_base + self.filename_string + ".json.gz"
                # self.json_file = self.path_json_base + self.filename_string + ".json"
            # Download the compressed JSON file
            urllib.request.urlretrieve(self.report_url, self.gz_file)

            # Extract the JSON data from the compressed file
            # with gzip.open(self.gz_file, 'rb') as file:
            #     self.json = json.loads(file.read().decode('utf-8'))
            # Save the extracted JSON data to a file
            # with open(self.json_file, 'w') as outfile:
            #     json.dump(self.json, outfile)

        except FileNotFoundError as e:
            error_message = f"File not found: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

        except IOError as e:
            error_message = f"IO error occurred: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

        except Exception as e:
            error_message = f"An error occurred while requesting a report: {str(e)}"
            logging.exception(error_message)
            print(error_message)
            raise e

    def parse_and_update_report(self):
        from classes.report_parser import Parser
        from classes.report_updater import Updater
        for processor in self.processors: #list
            self.parser = processor['parser']
            self.updater = processor['updater']
            self.main_file = f"{mainFilePath}\{self.mp}_{processor['name_suffix']}.csv"
            self.secondary_file = f"{mainFilePath}\{self.mp}_{processor['secondary_table_name_suffix']}.csv"
            report_parser_obj = Parser(self)
            parser_method = getattr(report_parser_obj, self.parser)
            parser_method()
            report_parser_obj = Updater(self)
            update_method = getattr(report_parser_obj, self.updater)
            update_method()
