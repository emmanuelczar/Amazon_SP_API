from datetime import datetime, timedelta
import openpyxl
file_path = "./app reference/reports.xlsx"
# Open the file containing the list of filepaths
reference = openpyxl.load_workbook(file_path)
dailyLag = int(reference["defaultDates"]["A1"].value)

today = datetime.now()

date_dictionary = {"SALES_D_S":
                        {"defaultStart": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d"),
                        "defaultEnd": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d")},
                    "SALES_D_M":
                        {"defaultStart": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d"),
                         "defaultEnd": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d")},
                    "SALES_W_S":
                        {"defaultStart": (today - timedelta(days=today.weekday() + 8)).strftime("%Y-%m-%d"),
                         "defaultEnd": (today - timedelta(days=today.weekday() + 2)).strftime("%Y-%m-%d")},
                    "SALES_W_M":
                        {"defaultStart": (today - timedelta(days=today.weekday() + 8)).strftime("%Y-%m-%d"),
                        "defaultEnd": (today - timedelta(days=today.weekday() + 2)).strftime("%Y-%m-%d")},
                   "INVENTORY_W_S":
                        {"defaultStart": (today - timedelta(days=today.weekday() + 8)).strftime("%Y-%m-%d"),
                        "defaultEnd": (today - timedelta(days=today.weekday() + 2)).strftime("%Y-%m-%d")},
                   "INVENTORY_W_M":
                        {"defaultStart": (today - timedelta(days=today.weekday() + 8)).strftime("%Y-%m-%d"),
                        "defaultEnd": (today - timedelta(days=today.weekday() + 2)).strftime("%Y-%m-%d")},
                   "NETPPM_D":
                        {"defaultStart": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d"),
                        "defaultEnd": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d")},
                   "TRAFFIC_D":
                        {"defaultStart": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d"),
                        "defaultEnd": (today - timedelta(days=dailyLag)).strftime("%Y-%m-%d")},
                   "FORECAST":
                        {"defaultStart": (today - timedelta(days=today.weekday()+1)).strftime("%Y-%m-%d"),
                        "defaultEnd": (today - timedelta(days=today.weekday()-5)).strftime("%Y-%m-%d")}
                   }

print(today.weekday())