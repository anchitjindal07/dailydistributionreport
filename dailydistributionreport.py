import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def get_data():
	district = "Sri Muktsar Sahib";
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(firefox_options=options,executable_path="./geckodriver")

	driver.get("https://epos.punjab.gov.in/Month_Abst_Int.jsp")
	time.sleep(10)
	res = driver.find_elements_by_xpath("//*[@id='tabcolor']/tbody/tr[contains(.,'"+district+"')]/td")
	
	items = []
	for result in res:
		items.append(result.text)
	items.append(str(datetime.now()))

	driver.quit()	
	return(items)


def save_data(data):
	SCOPES = ['https://www.googleapis.com/auth/drive']
	creds =  ServiceAccountCredentials.from_json_keyfile_name("creds_service_account.json",SCOPES)
	client = gspread.authorize(creds)

	sheet = client.open("DailyDistributionReport").get_worksheet(0)
	
	current_row = len(sheet.get_all_values())+1

	for column,item in enumerate(data):
		sheet.update_cell(current_row,column+1,item)
		
data = get_data()
save_data(data)
