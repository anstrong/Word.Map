import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
import subprocess
import pydot
import sys

# Upon my honor, I have neither given nor recieved unauthorized aid.

#Sources:
#BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#urllib documentation: https://docs.python.org/3/library/urllib.request.html#module-urllib.request
#pydot tutorial: https://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot/

####################################### FUNCTIONS ###############################################

def read_html(address):

	try:
		# Open the page
		url = Request(address, headers={'User-Agent': 'Mozilla/5.0'})
		# Parse the HTML
		html = urlopen(url).read()

		return html

	except urllib.error.HTTPError:
		print('Word not found on Thesaurus.com. Check your spelling or try another word!')
		sys.exit()

def get_synonyms(word):
	global level

	level += 1

	# Replace spaces, if any exist, for url compatibility
	split_word = word.split(' ')
	word = '%20'.join(split_word)

	# Piece together url
	url = 'http://www.thesaurus.com/browse/' + word + '?s=t'

	# Open and parse page
	html = read_html(url)

	# Turn raw html into scrapable 'soup'
	soup = BeautifulSoup(html, "html.parser")

	# Isolate synonym-containing div
	div = soup.find("div", {"class": "relevancy-list"})

	# List spans within div that contain actual synonym text
	span = div.find_all("span", {"class": "text"})

	# Create list for scraped synonyms
	synonyms = []

	# Cycle through synonym-containing tags, isolate string within tag, and save
	for i in range(len(span)):
		tag = span[i - 1]
		synonym = tag.get_text()
		synonyms.append(synonym)

	return synonyms

def make_node(parent, name):
	global graph
	global level
	global word

	# Create new node for word
	new_node = pydot.Node(name)

	# Add node to graph
	graph.add_node(new_node)

	# Connect to parent word
	graph.add_edge(pydot.Edge(parent, new_node))

def map_synonym(word):
	global graph
	global level

	max_level = 4

	# Scrape synonyms from word's thesaurus page
	synonyms = get_synonyms(word)

	# For debigging and process monitoring
	print(synonyms)

	for i in range(len(synonyms)):
		# Create node for word
		synonym = synonyms[i - 1]
		make_node(word, synonym)

		# Fetch next level of synonyms
		if level < max_level:
			map_synonym(synonym)

def map_word(word):
	global graph
	global level

	max_level = 3

	# Generate node for original parent word
	if level == 0:
		graph.add_node(pydot.Node(word))

	# Scrape synonyms from word's thesaurus page
	synonyms = get_synonyms(word)
	print(synonyms)

	for i in range(len(synonyms)):
		level = 2
		# Create node for word
		synonym = synonyms[i - 1]
		make_node(word, synonym)

		map_synonym(synonym)

########################################## LOGIC ###############################################
# Set default tree-level value
level = 0

# Ask for word to map
word = input("What word do you want to map? ")

# Create graph
graph = pydot.Dot(graph_type='graph')

# Run mapping for given word
map_word(word)

# Create map image
filename = word + '.png'
graph.write_png(filename)

# Print confirmation
print('Mapping complete. ')

# Open file location
subprocess.call(["open", "-R", filename])
