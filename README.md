Property Data Scraping and Financial Impact Analysis
This repository contains code written in Python using the Selenium library to scrape property data from cookcountypropertyinfo.com. The purpose of this data scraping is to conduct a Financial Impact Analysis, aiming to quantify the financial implications of tax delinquency and tax buyer transactions, with a focus on assessing the costs and benefits to local governments and communities.

Analysis Objectives
The primary objectives of this analysis are as follows:

Calculate the lost revenue resulting from tax delinquency.
Determine the revenue generated from tax buyer sales.
Assess any subsequent costs associated with the management and redevelopment of properties involved in tax buyer transactions.

Repository Contents
scrapeSeleniumCookCntyPortal.py: Python script for scraping property data from cookcountypropertyinfo.com. The scraped data includes property addresses, mailing addresses (used to identify property owners), property characteristics, property values, related tax information, tax amounts owed/paid, tax sale occurrences, and documents related to property ownership issues. Note that the PIN_numbers file contains only a small sample of data for code testing purposes.

image scraper [in progress]: Python script for scraping property images. This step may be necessary for further analysis, especially for properties that have been demolished or significantly altered.

financial_analysis [in progress]: Python script for conducting the financial impact analysis. This script performs calculations to determine the overall debt resulting from tax delinquency and tax buyer transactions.

Getting Started
To use this code and perform the Financial Impact Analysis, follow these steps:

Clone this repository to your local machine.

Run scrapeSeleniumCookCntyPortal.py to scrape the property data from cookcountypropertyinfo.com. The scraped data will be saved in a suitable format for further analysis.

Please note that this code is provided as-is, and any use or modification should comply with the terms and conditions of the cookcountypropertyinfo.com website. 