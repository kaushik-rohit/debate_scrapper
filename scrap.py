from dateutil import rrule
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib.request as request
from urllib.parse import urljoin
import json



HOME_PAGE = 'https://www.parliament.uk/business/publications/hansard/commons/by-date/#session=27&year={}&month={}&day={}'
DEBATE_LINK = 'https://publications.parliament.uk/pa/cm{}/cmhansrd/cm{}/debindx/{}-x.htm'


def format_link(year, month, day):
	'''return the link to webpage that has debate info for a paricular date.'''
	next_year = year % 100
	year_string = '{}{}'.format(year - 1, next_year)
	date_descriptor = '{}{:02d}{:02d}'.format(next_year, month, day)
	return DEBATE_LINK.format(year_string, date_descriptor, date_descriptor)


def get_utterance_text(link):
	link_param = link.split('#')
	url = link_param[0]
	anchor_name = link_param[1]

	speech_html = request.urlopen(url)
	soup = BeautifulSoup(speech_html)
	anchor = soup.find('a', {'class': 'anchor', 'name':anchor_name})
	para = anchor.parent
	
	return para.get_text().replace('\n', ' ')
	
		
def parse_debate_for_date(date):
	'''parse debate info'''
	
	data = []
	debate_page = format_link(date.year, date.month, date.day)
	print(debate_page)
	
	try:
		debate_page_html = request.urlopen(debate_page)
		soup = BeautifulSoup(debate_page_html)
	except urllib.error.HTTPError:
	    print 'We failed with error code - %s.' % e.code

    	if e.code == 404:
        	# do stuff..  
    	else:
        	# other stuff...
	
	for para in soup.findAll('p'):
		link = para.find('a', {'shape': 'rect'}, href=True)
		
		if link is None:
			continue
		
		utterance = {'speaker': '', 'speech':''}
		
		speaker = link.find('b').get_text()
		speaker = speaker.replace('\n', ' ')
		href = urljoin(debate_page, link['href'])
		speech = get_utterance_text(href)
		
		utterance['speaker'] = speaker
		utterance['speech'] = speech
		data.append(utterance)
		
	filename = date.strftime('%Y-%m-%d')
	filepath = './data/{}.json'.format(filename)
	
	with open(filepath, 'w') as f:
		json.dump(data, f)


def get_debate_for_period(start_date, end_date):
	'''iterate over days to get debate for a period'''
	delta = timedelta(days=1)
	date_iter = start_date
	while date_iter <= end_date:
		parse_debate_for_date(date_iter)
		date_iter += delta
	
	
if __name__ == '__main__':
	start_date = datetime(2016, 1, 1) #1st Jan 2016
	end_date = datetime(2016, 1, 31) #31st Jan 2016
	get_debate_for_period(start_date, end_date)
