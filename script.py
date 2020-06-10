from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import csv
#import requests


# CSV Read
# save all in dict
# query through dict
# Write dict out

# State
# City
# Population
# First Name
# Last Name
# Email
# Web Form
# Phone
# Fax
# Address 1
# Zip Code 
# Term End

# Read CSV with Pandas - INCOMPLETE
# df = pd.read_csv('mayors.csv', index_col=1)
# ##df = pd.read_csv('mayorstrans.csv')

# print(df)
# df.set_index('City', inplace = True)
# # print(df.dtypes)

# # city_row = df[df['City'] == "Tacoma"]
# # print(city_row)

# print(df.loc['Tacoma'])

# # df.at[2,'Zip Code'] = 55555

# # print(city_row)

def search_mayors_selenium (file_city, file_state):
	#takes city, state parameters
	# returns pagesource
	driver = webdriver.Chrome()
	driver.implicitly_wait(10)
	driver.get('https://www.usmayors.org/mayors/')

	search_input = '//*[@id="searchform"]/input[1]'
	search_submit = '//*[@id="searchform"]/input[2]'

	driver.find_element_by_xpath(search_input).send_keys(file_city)
	driver.find_element_by_xpath(search_submit).click()

	try:
	    pagesource = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="post-330"]/div/ul')))
	    print ("Page is ready!")
	    return driver.page_source
	except TimeoutException:
	    print ("Loading took too much time!")
	finally:
		driver.close()

#def search_mayors_post (file_city, file_state): #unable to get working due to incomplete response - likely due to invalid/incomplete headers?
	url = 'https://www.usmayors.org/mayors/'
	session = requests.session()
	payload = 	{'searchTerm': file_city,
					'submit': 'search'}	
	headers = {
				# 'authority': 'www.usmayors.org',
				# 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				# 'origin':'https://www.usmayors.org',
				# 'referer':'https://www.usmayors.org/mayors/meet-the-mayors',
				# 'upgrade-insecure-requests': '1',
				# 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
			  }

	response = requests.post(url, data=payload, headers = headers)
	# print (response.text)
	return response.text




# MAIN
# Read CSV with csv library
donerows = []

with open('mayors.csv') as csvfile:
	
	# readCSV = csv.reader(csvfile, delimiter=',')
	# next(readCSV) #skip header
	
	# city = ""
	# state = ""

	# for row in readCSV:
	# 	filledrow = []
	# 	city = row[1]
	# 	state = row[0]
	# 	# print(city + ', ' + state)
	# 	# filledrow.append()
	# 	donerows.append([city, state])
	# 	# print(filledrow)
	# 	# print (len(donerows))



	# print(donerows[2])
	# print(donerows[2][0] +" ,"+ donerows[2][1])

	#rawhtml = search_mayors_db(donerows[2][0], donerows[2][1])
	#rawhtml = search_mayors_selenium("New York", "NY") #test row

	rawhtml = search_mayors_selenium("New York", "NY") #test row


	doc = BeautifulSoup(rawhtml, "html.parser")
	# print(doc)

	#strip away anything besides results
	searchresults = doc.find('div', class_='post-content').find_all('ul', limit=3) #FOR SELENIUM TODO REMOVE LIMIT
	#searchresults = doc.find('div', class_='post-content').find_all('ul', limit=3) #FOR REQUESTS #NOT ABLE TO CAPTURE RESULTS IN RESPONSE

	# print(searchresults)
	
	mayordetails = []

	for searchresult in searchresults:
		# print('searchresult:')
		# print(searchresult)
		# mayorhtml = searchresult.find('ul')
		# print('mayorhtml:')
		# print(mayorhtml)
		# print('end mayorhtml')
		# print (searchresult.text)
		img = searchresult.find('img')
		print(img['src'])

		result = list(searchresult)
		print("results lis")
		print(result)
		print (result[3]) #name
		
		#STARTHERE
		name = result[3]
		namearray = name.split()
		fname = namearray[0]
		lname = namerray[-1]
		print(fname)
		print(lname)

		print (result[5]) #city, state
		print (result[7]) #population
		print (result[11]) #next election date
		print (result[13]) #bio
		print (result[16]) #phone
		print (result[19]) #email

		contactlinks = searchresult.find_all('a')

		for contactlink in contactlinks:
			if(contactlink.string != "Bio"):
				print(contactlink.string)
			else:
				print(contactlink['href'])

		#make mayor object with attributes
		mayordetails.append([result])

		
	
	# print(mayordetails)



