import requests
from bs4 import BeautifulSoup


def definicao(query):
	r = requests.get('https://www.dicionarioinformal.com.br/'+query)
	soup = BeautifulSoup(r.text, "html.parser")
	nome = query
	tit = soup.find('p','text-justify')
	desc = soup.find('blockquote','text-justify')
	try:
		desc = desc.get_text().replace('\n'[0],'').replace('                 ','').replace('''\n                ''','')
	except:
		desc = ''
	tit = tit.get_text()[17:].replace('''\n                ''','')
	if len(tit) < 245:
		tit = tit
	else:
		tit = tit[:245]+'…\n<a href="https://www.dicionarioinformal.com.br/{}/">leia mais sobre {}</a>'.format(link,nome)
	resp = {'tit':tit,'desc':desc.replace('\r', ' '),'link':r.url}

	return dict(results=resp)
