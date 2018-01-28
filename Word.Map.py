from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer

import pydot
import graphviz

####################################### FUNCTIONS ###############################################

def read_html(address):
	# Open the page
	url = Request(address, headers={'User-Agent': 'Mozilla/5.0'})
	# Parse the HTML
	html = urlopen(url).read()

	return html

def get_synonyms(word):

	split_word = word.split(' ')

	word = '%20'.join(split_word)

	url = 'http://www.thesaurus.com/browse/' + word + '?s=t'

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

def make_node(parent, name):
	global graph

	new_node = pydot.Node(name)
	graph.add_node(new_node)
	graph.add_edge(pydot.Edge(parent, new_node))

def map_synonym(word):
	global graph
	global recursion

	synonyms = get_synonyms(word)

	for i in range(len(synonyms)):
		recursion += 1
		synonym = synonyms[i - 1]
		make_node(word, synonym)

		if recursion <= 2:
			map_synonym(synonym)

def map_word(word):
	global graph
	global tree_top
	global recursion

	if tree_top == True:
		graph.add_node(pydot.Node(word))

	synonyms = get_synonyms(word)

	for i in range(len(synonyms)):
		recursion = 1
		synonym = synonyms[i - 1]
		make_node(word, synonym)

		map_synonym(synonym)


########################################## LOGIC ###############################################
tree_top = True
recursion = 0

word = input("What word do you want to map? ")

graph = pydot.Dot(graph_type='graph')

map_word(word)

graph.write_png(word + '.png')

print('Mapping complete. ')
