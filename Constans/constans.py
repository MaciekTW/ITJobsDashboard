import os

if os.getenv('IS_PROD_ENV'):
    DATA_DIRECTORY = "/server/scrapping/data/"
else:
    DATA_DIRECTORY = "E:\\Scrapinng\\JobsDashboard\\Data"
