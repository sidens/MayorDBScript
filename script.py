from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


def search_selenium (searchcity, searchstate):
	#takes city, state parameters
	#returns pagesource
	driver = webdriver.Chrome()
	driver.implicitly_wait(10)
	driver.get('https://www.usmayors.org/mayors/')

	search_input = '//*[@id="searchform"]/input[1]'
	search_submit = '//*[@id="searchform"]/input[2]'

	driver.find_element_by_xpath(search_input).send_keys(searchcity)
	driver.find_element_by_xpath(search_submit).click()

	try:
	    pagesource = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="post-330"]/div/ul')))
	    print ("Page is ready!")
	    return driver.page_source
	except TimeoutException:
	    print ("Loading took too much time!")
	finally:
		driver.close()

#def search_mayors_post (searchcity, searchstate): #unable to get working due to incomplete response - likely due to invalid/incomplete headers?
	# url = 'https://www.usmayors.org/mayors/'
	# session = requests.session()
	# payload = 	{'searchTerm': searchcity,
	# 				'submit': 'search'}	
	# headers = {
	# 			# 'authority': 'www.usmayors.org',
	# 			# 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	# 			# 'origin':'https://www.usmayors.org',
	# 			# 'referer':'https://www.usmayors.org/mayors/meet-the-mayors',
	# 			# 'upgrade-insecure-requests': '1',
	# 			# 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
	# 		  }

	# response = requests.post(url, data=payload, headers = headers)
	# # print (response.text)
	# return response.text


def parse_mayors_data (searchcity, searchstate):

	#Call selenium based lookup function and capture the HTML
	rawhtml = search_selenium(searchcity, searchstate)
	doc = BeautifulSoup(rawhtml, "html.parser")

	#strip away anything besides results
	searchresults = doc.find('div', class_='post-content').find_all('ul') #FOR SELENIUM TODO REMOVE LIMIT
	#searchresults = doc.find('div', class_='post-content').find_all('ul') #FOR DIRECT POST REQUESTS #NOT ABLE TO CAPTURE RESULTS IN RESPONSE - NEED BETTER HEADERS?
	
	mayorcontactlist = []

	for searchresult in searchresults:
		mayorentry = []

		#make navigable mayor details section
		result = list(searchresult)

		#Extract details of mayor
		citystate = result[5].split(', ')
		city = citystate[0]
		state = citystate[-1]

		
		#if the city/state result is an exact match with the search query, capture details and return them
		if ( searchcity == city and searchstate == state):
			name = result[3].get_text()
			namearray = list(name.split())
			fname = namearray[0] #get firstname by position
			lname = namearray[-1] #get lastname by position
			phone = result[16].string #phone
			email = result[19].string #email

			#make mayor object with attributes
			mayordetails = [city, state, fname, lname, email, phone]
			#print(mayordetails)
			
			# Other variables available
			# print (result[5]) #city, state
			# print (result[7]) #population
			# print (result[11]) #next election date
			# print (result[13]) #bio
		else:
			continue

	return mayordetails

	

def main():
    #MASTER VARIABLES
	searchcity = "Seattle"
	searchstate = "WA"

	mayor = parse_mayors_data(searchcity,searchstate)
	print(mayor)

if __name__ == "__main__":
    main()



