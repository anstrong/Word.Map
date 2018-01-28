from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer

####################################### FUNCTIONS ###############################################

def read_html(address):
	# Open the page
	url = Request(address)#, headers={'User-Agent': 'Mozilla/5.0'})
	# Parse the HTML
	html = urlopen(url).read()

	return html

def get_synonyms(word):
	url = 'http://www.thesaurus.com/browse/' + word

	# Open and parse page
	html = read_html(url)

	# Turn raw html into scrapable 'soup'
	soup = BeautifulSoup(html, "html.parser")

	div = soup.find("div", {"class": "relevancy-list"})
	span = div.find_all("span", {"class": "text"})

	synonyms = []

	for i in range(len(span)):
		tag = span[i - 1]
		synonym = tag.string
		synonyms.append(synonym)

	return synonyms

########################################## LOGIC ###############################################
#word = input("What word do you want to map? ")
word = 'athletic'

print(get_synonyms(word))
