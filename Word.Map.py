from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer

####################################### FUNCTIONS ###############################################

def read_html(address):
	# Open the page
	url = Request(address)#, headers={'User-Agent': 'Mozilla/5.0'})
	# Parse the HTML
	html = urlopen(url).read()

	return html

########################################## LOGIC ###############################################
address = 'http://www.thesaurus.com/browse/human'

# Open and parse page
html = read_html(address)

# Turn raw html into scrapable 'soup'
soup = BeautifulSoup(html, "html.parser")

div = soup.find("div", {"class": "relevancy-list"})
span = div.find_all("span", {"class": "text"})

for i in range(len(span)):
    tag = span[i - 1]
    print(tag.string)
