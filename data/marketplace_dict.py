import openpyxl


# TODO 1: Set variables saved from credentials.csv
file_path = "./app reference/reference.xlsx"
# Open the file containing the list of filepaths
reference = openpyxl.load_workbook(file_path)
marketplaceID_US = reference["marketplace"]["B2"].value
marketplaceID_CA = reference["marketplace"]["B3"].value
marketplaceID_UK = reference["marketplace"]["B4"].value
marketplaceID_MX = reference["marketplace"]["B5"].value
pathASIN_US = reference["paths"]["B8"].value
pathASIN_CA = reference["paths"]["B9"].value
pathASIN_MX = reference["paths"]["B10"].value
pathASIN_UK = reference["paths"]["B11"].value



reference.close()

NA_Host = "sellingpartnerapi-na.amazon.com"
EU_Host = "sellingpartnerapi-eu.amazon.com"


marketplace_dictionary = {
    "US": {"Host": NA_Host, "MarketplaceId": marketplaceID_US, "seller_central_url": "https://sellercentral.amazon.com","ASIN_Path": pathASIN_US},
    "CA": {"Host": NA_Host, "MarketplaceId": marketplaceID_CA,"seller_central_url": "https://sellercentral.amazon.ca","ASIN_Path": pathASIN_CA},
    "MX": {"Host": NA_Host, "MarketplaceId": marketplaceID_MX, "seller_central_url": "https://sellercentral.amazon.com.mx","ASIN_Path": pathASIN_MX},
    "UK": {"Host": EU_Host, "MarketplaceId": marketplaceID_UK, "seller_central_url": "https://sellercentral-europe.amazon.com","ASIN_Path": pathASIN_UK}
    }


#US & CA share the same sheet
credentials_mapping = {"US": "US_credentials",
                       "CA": "US_credentials",
                       "MX": "MX_credentials",
                       "UK": "UK_credentials"}