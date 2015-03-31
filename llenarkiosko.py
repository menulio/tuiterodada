import sys
from urllib.request import Request, urlopen
from urllib.error import URLError

def get_next_target(page):
    start_link = page.find(b'<a href="http://')
    if start_link == -1: 
        return None, 0
    start_quote = page.find(b'"', start_link)
    end_quote = page.find(b'"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
			
def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links
	
def get_file_name(url, dir):
	return dir + '/' + url[url.find('.') + 1:len(url)][0:url[url.find('.') + 1:len(url)].find('.')]

def get_page(url):
	try:
		req = Request(url)
		response = urlopen(req)
		page = response.read()
		print(response.info().get_content_type())
		return page
	except:
		print('Error accediendo a url: ', url)
	
def write_file(filename, contents):
	f = open(filename, 'wb')
	try:
		f.write(contents)
		print('Escribiendo fichero... ', filename)
	except:
		print('Error escribiendo fichero: ', filename)
	f.close()

DIR_AEDE = 'aede'
	
try:
	page = get_page('http://www.aede.es/publica/Periodicos_Asociados.asp')
	# Recopilar portadas de diarios
	links = get_all_links(page)
	
	# Guarda cada una en un fichero
	for x in range(0, len(links)):
		url = links[x].decode();
		# Evitamos guardar enlaces a la propia pgina
		if url.find(DIR_AEDE) < 0:
			filename = get_file_name(url, DIR_AEDE)
			write_file(filename, get_page(url))
except:
	print('Error Fatal, siempre haciendo tontadas: ', sys.exc_info()[0])
	raise	
