import urllib2
from bs4 import BeautifulSoup
# or if your're using BeautifulSoup4:
# from bs4 import BeautifulSoup
# http://stackoverflow.com/questions/2081586/web-scraping-with-python#comment15573854_2082025

soup = BeautifulSoup(
	urllib2.urlopen('http://www.timeanddate.com/worldclock/astronomy.html?n=64').read()
	)

# requests doesn't return the complete html, why?
# soup = BeautifulSoup(
# 	requests.get('http://www.timeanddate.com/worldclock/astronomy.html‌​?n=64').text
# 	) 

for row in soup('table', {'class' : 'spad'})[0].tbody('tr'):
	tds = row('td')
	print tds[0].string, tds[1].string
	# will print date and sunrise