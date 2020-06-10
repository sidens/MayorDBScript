from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
#import pandas as pd
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

def search_selenium (file_city, file_state):
	#takes city, state parameters
	#returns pagesource
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


def parse_mayors_data ():



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

	#MASTER VARIABLES
	searchcity = "New York"
	searchstate = "NY"

	#Call selenium based lookup function and capture the HTML
	rawhtml = search_selenium(searchcity, searchstate)
	doc = BeautifulSoup(rawhtml, "html.parser")

	#strip away anything besides results
	searchresults = doc.find('div', class_='post-content').find_all('ul') #FOR SELENIUM TODO REMOVE LIMIT
	#searchresults = doc.find('div', class_='post-content').find_all('ul') #FOR REQUESTS #NOT ABLE TO CAPTURE RESULTS IN RESPONSE - NEED BETTER HEADERS?
	
	mayorcontactlist = []

	for searchresult in searchresults:
		mayorentry = []

		#make navigable mayor details section
		result = list(searchresult)
		
		#Extract details of mayor
		citystate = result[5].split(', ')
		city = citystate[0]
		state = citystate[-1]

		
		
		#if the city result does not match with the search query, iterate to the next city
		if ( searchcity == city and searchstate == state):
			name = result[3].get_text()
			namearray = list(name.split())
			fname = namearray[0] #get firstname by position
			lname = namearray[-1] #get lastname by position
			phone = result[16].string #phone
			email = result[19].string #email

			#make mayor object with attributes
			mayordetails = [fname, lname, email, phone]
			#print(mayordetails)
			
			mayorcontactlist.append(mayordetails)

			# Other variables available
			# print (result[5]) #city, state
			# print (result[7]) #population
			# print (result[11]) #next election date
			# print (result[13]) #bio
		else:
			continue

	
	print(mayorcontactlist)

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()



