import requests
from bs4 import BeautifulSoup


def definicao(query):
	r = requests.get('https://www.dicionarioinformal.com.br/'+query)
	soup = BeautifulSoup(r.text, "html.parser")
	nome = query
	tit = soup.find_all('h3','di-blue')
	if tit == None:
		tit = soup.find_all('h3','di-blue-link')
	title = []
	for i in tit:
		a = i.find('a')
		if a != None:
			title.append(a.get('title'))
	if a == None:
		tit = soup.find_all('h3','di-blue-link')
	for i in tit:
		a = i.find('a')
		if a != None:
			title.append('você quiz dizer: {}'.format(a.get('title')))
	ti = soup.find_all('p','text-justify')
	tit = []
	for i in ti:
		ti = i.get_text()[17:].replace('''\n                ''','')
		tit.append(ti)
	des = soup.find_all('blockquote','text-justify')
	des.append(' ')
	desc = []
	for i in des:
		try:
			des = i.get_text().replace('\n'[0],'').replace('                 ','').replace('''\n                ''','')
		except:
			pass
		desc.append(des)
	result = []
	max = 0
	for i in title:
		try:
			b = {'title':i,'tit':tit[max],'desc':desc[max]}
			max += 1
			result.append(b)
		except Exception as e:
			print(e)
			
	return dict(results=result)