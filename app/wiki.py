import wikipedia

from threading import Thread

GOOGLE_SEARCH_URL_PREFIX = "https://www.google.com/search?q="
DEFAULT_RESPONSE = "No Wikipedia entry available."

class WikipediaResponse:
	def __init__(self):
		self.wikipedia_link = None
		self.definition = None

def fetch_wikipedia_for_term(term, wikipedia_response):
	wikipedia_response.wikipedia_link = get_wikipedia_link(term)
	wikipedia_response.definition = get_definition(term)

def fetch_wikipedia_for_terms(terms):
	threads = []
	term_to_wikipedia_response = dict()
	for term in terms:
		wikipedia_response = WikipediaResponse()
		threads.append(Thread(target=fetch_wikipedia_for_term, args=(term, wikipedia_response)))
		term_to_wikipedia_response[term] = wikipedia_response

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	return term_to_wikipedia_response

def get_wikipedia_link(term, choice = 0):
	link = ""
	try:
		link = wikipedia.page(term).url
	except:
		return GOOGLE_SEARCH_URL_PREFIX + term
	return link

def get_definition(term):
	summary = ""
	try:
		summary = wikipedia.summary(term, sentences=1)
	except:
		return DEFAULT_RESPONSE
	return summary
