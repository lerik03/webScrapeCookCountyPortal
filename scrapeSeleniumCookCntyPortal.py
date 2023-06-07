import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import requests

import time
import csv


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(ChromeDriverManager().install())


# Load the PINs from the Excel file
pins_df = pd.read_excel('PIN_numbers.xls', dtype=str)


# Format the PINs
pins_df = pins_df.apply(lambda x: x.str.zfill(2) if x.name == "pin1" or x.name == "pin2" else x.str.zfill(3) if x.name in ["pin3", "pin4"] else x.str.zfill(4) if x.name == "pin5" else x)
pin_l = pins_df.values.tolist()


# Define the header for the CSV file
header = ['PIN', 'Name', 'MailingAddress1', 'MailingAddress2', 'PropertyAddress', 'City', 'Zip', 'Township', 'PropertyValue',
          'LotSize', 'BuildingSize', 'Property Class', 'TaxRate', 'TaxCode', 'taxamount22', 'taxamount21', 'taxamount20', 'taxamount19',
          'taxamount18', 'taxSale2022', 'taxSale2021', 'taxSale2020', 'taxSale2019', 'taxSale2018', 'Deeds']


# Write the data to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    

    # Loop over all the PINs
    for i in range(len(pin_l)):
        driver.get("http://www.cookcountypropertyinfo.com/default.aspx")
        # Enter the PIN number and click search
        driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox1').send_keys(pin_l[i][0])
        driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox2').send_keys(pin_l[i][1])
        driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox3').send_keys(pin_l[i][2])
        driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox4').send_keys(pin_l[i][3])
        driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$PINAddressSearch$pinBox5').send_keys(pin_l[i][4])
        driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$PINAddressSearch$btnSearch').click()


        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_TaxYearInfo_propertyClass')))


        # Scrape the data
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        
        pin = soup.find('span', id='ContentPlaceHolder1_lblResultTitle').text.strip()
        name = soup.find('span', id='ContentPlaceHolder1_PropertyInfo_propertyMailingName').text.strip()
        mailing_address = soup.find('span', id='ContentPlaceHolder1_PropertyInfo_propertyMailingAddress').text.strip()
        mailing_address2 = soup.find('span', id='ContentPlaceHolder1_PropertyInfo_propertyMailingCityStateZip').text.strip()
        property_address = soup.find('span', id='ContentPlaceHolder1_PropertyInfo_propertyAddress').text.strip()
        city = soup.find('span', id='ContentPlaceHolder1_PropertyInfo_propertyCity').text.strip()
        zipcode = soup.find('span', id='ContentPlaceHolder1_PropertyInfo_propertyZip').text.strip()
        township = soup.find('span', id='ContentPlaceHolder1_PropertyInfo_propertyTownship').text.strip()

        
        estPropertyValue = soup.find('span', id='ContentPlaceHolder1_TaxYearInfo_propertyEstimatedValue').text.strip()
        lotSize = soup.find('span', id='ContentPlaceHolder1_TaxYearInfo_propertyLotSize').text.strip()
        buildingSize = soup.find('span', id='ContentPlaceHolder1_TaxYearInfo_propertyBuildingSize').text.strip()
        propertyClass = [e.text.strip().replace("-", "--") for e in soup.find_all('span', id='ContentPlaceHolder1_TaxYearInfo_propertyClass')]
        taxRate = soup.find('span', id='ContentPlaceHolder1_TaxYearInfo_propertyTaxRate').text.strip()
        taxCode = soup.find('span', id='ContentPlaceHolder1_TaxYearInfo_propertyTaxCode').text.strip()

        
        taxamount22 = soup.find('span', id='ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_0').text.strip()
        taxamount21 = soup.find('span', id='ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_1').text.strip()
        taxamount20 = soup.find('span', id='ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_2').text.strip()
        taxamount19 = soup.find('span', id='ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_3').text.strip()
        taxamount18 = soup.find('span', id='ContentPlaceHolder1_TaxBillInfo_rptTaxBill_taxBillAmount_4').text.strip()
        taxSale = driver.find_elements_by_xpath(".//a[contains(@class, 'js-open-modal2')]")
        taxSale = [y.text.strip() for y in taxSale [19:]]
        deeds = soup.find_all('div', class_='toggle2Display recorddocspace')
        deeds = [d.text.strip() for d in deeds]


        # Write the data to the CSV file
        row = [pin, name, mailing_address, mailing_address2, property_address, city, zipcode, township, estPropertyValue, lotSize, buildingSize, propertyClass, taxRate, taxCode, taxamount22, taxamount21, taxamount20, taxamount19, taxamount18]+taxSale+deeds
        csvwriter.writerow(row)
   
