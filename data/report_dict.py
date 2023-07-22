import openpyxl

file_path = "app reference/reports.xlsx"
sheet_name = "all_reports"

workbook = openpyxl.load_workbook(file_path)
sheet = workbook[sheet_name]

main_report_filename_dict = {}
for row in sheet.iter_rows(min_row=2, values_only=True):
    cell_value = row[0]
    if cell_value is not None:
        key = cell_value
        value = row[1] if row[1] is not None else ""
        main_report_filename_dict[key] = value
workbook.close()


report_dictionary = {"SALES_D_S":
                        {"report_name": "Sales_Daily_Sc",
                        "json_key": "salesByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "DAY", "distributorView": "SOURCING", "sellingProgram": "RETAIL"},
                            "reportType": "GET_VENDOR_SALES_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': 'parse_source_pos_item_details',
                                      'updater': 'update_source_pos_item_details',
                                      'name_suffix': main_report_filename_dict["SALES_D_S"],
                                      'secondary_table_name_suffix':''}]
                        },
                    "SALES_D_M":
                        {"report_name": "Sales_Daily_Mf",
                        "json_key": "salesByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "DAY", "distributorView": "MANUFACTURING","sellingProgram": "RETAIL"},
                            "reportType": "GET_VENDOR_SALES_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': 'parse_manufacturing_pos_item_details',
                                      'updater': 'update_manufacturing_pos_item_details',
                                      'name_suffix': main_report_filename_dict["SALES_D_M"],
                                      'secondary_table_name_suffix':''}]
                        },
                     "SALES_W_S":
                        {"report_name": "Sales_Weekly_Sc",
                        "json_key": "salesByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "WEEK", "distributorView": "SOURCING", "sellingProgram": "RETAIL"},
                            "reportType": "GET_VENDOR_SALES_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': 'parse_pos_data',
                                      'updater': 'update_pos_data',
                                      'name_suffix': main_report_filename_dict["SALES_W_S"],
                                      'secondary_table_name_suffix':''}]
                        },
                     "SALES_W_M":
                        {"report_name": "Sales_Weekly_Mf",
                         "json_key": "salesByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "WEEK", "distributorView": "MANUFACTURING", "sellingProgram": "RETAIL"},
                            "reportType": "GET_VENDOR_SALES_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': '',
                                      'updater': '',
                                      'name_suffix': main_report_filename_dict["SALES_W_M"],
                                      'secondary_table_name_suffix':''}]
                        },
                     "FORECAST":
                        {"report_name": "Forecast",
                        "json_key": "forecastByAsin",
                        "report_body": {
                            "reportOptions": {"sellingProgram": "RETAIL"},
                            "reportType": "GET_VENDOR_FORECASTING_REPORT",
                            "marketplaceIds": []},
                        "processor": [{'parser': 'parse_forecast',
                                      'updater': 'update_forecast',
                                      'name_suffix': main_report_filename_dict["FORECAST"],
                                      'secondary_table_name_suffix':''}]
                        },
                     "INVENTORY_W_S":
                        {"report_name": "Inventory_Weekly_Sc",
                        "json_key": "inventoryByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "WEEK", "distributorView": "SOURCING", "sellingProgram": "RETAIL"},
                            "reportType": "GET_VENDOR_INVENTORY_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': 'parse_source_inventory_health',
                                      'updater': 'update_source_inventory_health',
                                      'name_suffix': main_report_filename_dict["INVENTORY_W_S"],
                                      'secondary_table_name_suffix':''}]
                        },
                     "INVENTORY_W_M":
                        {"report_name": "Inventory_Weekly_Mf",
                        "json_key": "inventoryByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "WEEK", "distributorView": "MANUFACTURING", "sellingProgram": "RETAIL"},
                            "reportType": "GET_VENDOR_INVENTORY_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': '',
                                      'updater': '',
                                      'name_suffix': main_report_filename_dict["INVENTORY_W_M"],
                                      'secondary_table_name_suffix':''}]
                        },
                     "NETPPM_D":
                        {"report_name": "NetPPM",
                        "json_key": "netPureProductMarginByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "DAY"},
                            "reportType": "GET_VENDOR_NET_PURE_PRODUCT_MARGIN_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': 'parse_netppm',
                                      'updater': 'update_netppm',
                                      'name_suffix': main_report_filename_dict["NETPPM_D"],
                                      'secondary_table_name_suffix': main_report_filename_dict["SALES_D_S"]}]
                        },
                        "TRAFFIC_D":
                        {"report_name": "Traffic",
                        "json_key": "trafficByAsin",
                        "report_body": {
                            "reportOptions": {"reportPeriod": "DAY"},
                            "reportType": "GET_VENDOR_TRAFFIC_REPORT",
                            "dataStartTime": "",
                            "dataEndTime": "",
                            "marketplaceIds": []},
                        "processor": [{'parser': 'parse_traffic',
                                      'updater': 'update_traffic',
                                      'name_suffix': main_report_filename_dict["TRAFFIC_D"],
                                      'secondary_table_name_suffix':''}]
                        },
                        "CATALOG":
                        {"report_name": "Catalog",
                        "json_key": "",
                        "report_body": {
                            "marketplaceIds": []},
                        "processor": [{'parser': '',
                                      'updater': '',
                                      'name_suffix': main_report_filename_dict["CATALOG"],
                                      'secondary_table_name_suffix':''}]
                        },

                     }
