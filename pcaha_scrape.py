from bs4 import BeautifulSoup
import requests

source = requests.get('https://pcaha.ca/').text
	
soup = BeautifulSoup(source,'lxml')

#table = BeautifulSoup(source,'lxml')

#summary = table.find('div', class_='table').text
header = soup.find('header')

#print(soup.prettify())

print(header)