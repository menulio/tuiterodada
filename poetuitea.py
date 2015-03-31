import sys
import re
import random
import codecs
from urllib.request import Request, urlopen
from urllib.error import URLError
from os import listdir, path
from twitter import *

def get_next_block(page):
    start_block = page.find(b'<p>')
    if start_block == -1: 
        return None, 0
    beg = page.find(b'<p>', start_block)
    end = page.find(b'</p>', beg + 3)
    b = page[beg + 1:end]
    return b, end

def get_next_target(page):
    start_link = page.find(b'<a href="http://')
    if start_link == -1: 
        return None, 0
    start_quote = page.find(b'"', start_link)
    end_quote = page.find(b'"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
	
def get_all_blocks(page):
    blocks = []
    while True:
        b,endpos = get_next_block(page)
        if b:
            blocks.append(b)
            page = page[endpos:]
        else:
            break
    return blocks

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
		return page
	except:
		print('Error accediendo a url: ', url)

def read_file(filename):
	try:
		f = open(filename, 'rb')
		print('Leyendo fichero: ', filename)
		return f.read()
	except:
		print('Error leyendo fichero: ', filename)
		return
	f.close()

def get_encoding(file_content):
	try:
		decoded_file = file_content.decode("utf-8")
	except:
		try:
			decoded_file = file_content.decode("latin_1")
		except:
			try:
				decoded_file = file_content.decode("ascii")
			except:
				decoded_file = nil
				
	return decoded_file
	
def write_file(filename, contents):
	f = open(filename, 'wb')
	try:
		f.write(contents)
		print('Escribiendo fichero... ', filename)
	except:
		print('Error escribiendo fichero: ', filename)
	f.close()

def get_message(bolsa):
	message = "";
	not_number = re.compile('([^0-9_])+')
	# Agtola suavemente. 
	while True:
		# Ahora saco cada recorte uno tras otro. 
		worz = random.choice(bolsa)
		if not_number.match(worz) and worz.find('_') == -1 and worz.find('0') == -1 and worz.find('1') == -1 and worz.find('2') == -1 and worz.find('3') == -1 and worz.find('4') == -1 and worz.find('5') == -1 and worz.find('6') == -1 and worz.find('7') == -1 and worz.find('8') == -1 and worz.find('9') == -1:
			# Copio concienzudamente en el orden en que han salido de la bolsa. 
			message += worz
			pos = bolsa.index(worz)
			del bolsa[pos]

			if len(message) < 140:
				message += " "
			else:
				break;
		
	message = message[0: message.rindex(" ")]
	return message

DIR_AEDE = 'aede/'
	
# Palabras a excluir, Tzara las habra dejado, pero yo soy mainstream
HTML_TAGS = ["abbr", "acronym", "address", "applet", "area", "article", "aside", "audio", "base", "basefont", "bdi", "bdo",
"big", "blockquote", "body", "br", "button", "canvas", "caption", "center",  "cite", "code", "col", "colgroup",
"datalist", "dd", "del", "details",  "dfn", "dialog", "dir", "div", "dl", "dt", "em", "embed", "fieldset",
"figcaption", "figure", "font", "footer", "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head",
"header", "hr", "html", "iframe", "img", "input", "ins", "kbd", "keygen", "label", "legend", "li", "link", "main",
"map", "mark", "menu", "menuitem", "meta", "meter", "nav", "noframes", "noscript", "object", "ol", "optgroup", "option",
"output", "param", "pre", "progress", "rp", "rt", "ruby", "samp", "script", "section", "select", "small", "source", 
"span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th",
"thead", "time", "title", "tr", "track", "tt", "ul", "var", "video", "wbr", "com", "document", "nbsp", "aacute", 
"eacute", "iacute", "oacute", "uacute", "page", "www", "target", "true", "false", "zoneid", "b", "c", "d", "f", "g", 
"h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "class", "teaser", "headline", "href","crm", "alt", "thumb", 
"jpg", "cookies", "frameborder", "javascript", "php", "edition", "down", "widget", "ordf", "metha", "js", "aspx", "gif", "comment", 
"imgs", "amp", "rgb", "runner", "banners"]
# Palabras a excluir, Tzara las habra dejado, pero yo soy mainstream	
HTML_ATTRS = ["azimuth", "angle", "left-side" "far-left", "left", "center-left", "center", "center-right", "right", "far-right", "right-side", 
"behind", "leftwards", "rightwards", "inherit", "aural", "background-attachment", "scroll", "fixed", "background-color", "transparent",
"background-image", "background-position", "percentage", "length", "top", "bottom", "background-repeat", "repeat", "repeat-x", "repeat-y", "no-repeat",
"background", "background-color", "background-image", "background-repeat", "background-attachment", "background-position", "border-collapse", "collapse", 
"separate", "border-color", "border-spacing", "border-style", "border-top", "border-right", "border-bottom", "border-left", "border-width", "border-style", 
"border-top-color", "border-right-color", "border-bottom-color", "border-left-color", "border-top-style", "border-right-style", "border-bottom-style", 
"border-left-style", "border-style", "border-top-width", "border-right-width", "border-bottom-width", "border-left-width",  "border-width", "border", 
"bottom", "caption-side", "clear", "none", "clip", "color", "content", "string", "uri", "counter", "open-quote", "close-quote", "no-open-quote", 
"no-close-quote", "counter-increment", "counter-reset", "cue-after", "cue-before", "cue", "cue-before", "cue-after", "cursor", "crosshair", "default", 
"pointer", "move", "e-resize", "ne-resize", "nw-resize", "n-resize", "se-resize", "sw-resize", "s-resize", "w-resize", "text", "wait", "help", "progress",
"direction", "ltr", "rtl", "display", "inline", "block", "list-item", "inline-block", "table", "inline-table", "table-row-group", "table-header-group", 
"table-footer-group", "table-row", "table-column-group", "table-column", "table-cell", "table-caption",  "elevation", "below", "level", "above", "higher", "lower", 
"empty-cells", "show", "hide", "float", "font-family", "family-name", "generic-family", "font-size", "absolute-size", "relative-size", "font-style", "italic", 
"oblique", "font-variant", "small-caps", "font-weight", "bold", "bolder", "lighter", "font", "caption", "icon", "message-box", "small-caption", "status-bar", 
"height", "left", "letter-spacing", "line-height", "list-style-image", "list-style-position", "list-style-type", "disc", "circle", "square", "decimal", 
"decimal-leading-zero", "lower-roman", "upper-roman", "lower-greek", "lower-latin", "upper-latin", "armenian", "georgian", "lower-alpha", "upper-alpha", 
"list-style", "margin-right", "margin-left", "margin-top", "margin-bottom", "margin", "max-height", "max-width", "min-height", "min-width", "orphans", 
"outline-color", "outline-style", "outline-width", "outline", "outline-color", "outline-style", "outline-width", "overflow", "padding-top", "padding-right",
"padding-bottom", "padding-left", "padding", "padding-width", "page-break-after", "always", "avoid", "left", "right", "page-break-before", "always", "avoid", 
"left", "right", "page-break-inside", "pause-after", "pause-before", "pause", "pitch-range", "pitch", "frequency", "x-low", "low", "medium", "high", "x-high", 
"play-during", "uri", "mix", "repeat", "position", "static", "relative", "absolute", "fixed", "quotes", "richness", "speak-header", "once", "always",
"speak-numeral", "digits", "continuous","speak-punctuation", "speak", "speech-rate", "stress", "table-layout", "text-align", "text-decoration", "text-indent",
"text-transform","capitalize", "uppercase", "lowercase", "top", "unicode-bidi" "vertical-align", "baseline", "sub", "super", "top", "text-top", "middle", 
"bottom", "text-bottom", "visibility", "hidden", "collapse", "volume", "silent", "x-soft", "soft", "medium", "loud", "x-loud", "white-space", "pre", 
"nowrap", "pre-wrap", "http", "src", "img", "pre-line", "widows", "width", "word-spacing", "z-index"]

CONSUMER_KEY = 'sVPIUgtS4jorwCJbrHIlacLRO'
CONSUMER_SECRET = '9ihdMaFf22gpSdftSpCti8g1FhNAAEo4IuIQo9HVTAjS47tB1c'

try:
	# Voy al kiosko
	periodicos = [ f for f in listdir(DIR_AEDE) if path.isfile(path.join(DIR_AEDE,f)) ]
	# Entro en tuiter
	MY_TWITTER_CREDS = path.expanduser('~/.tuiterodada_credentials')
	
	if not path.exists(MY_TWITTER_CREDS):
		oauth_dance("poetuits_dada", CONSUMER_KEY, CONSUMER_SECRET,MY_TWITTER_CREDS)
		
	oauth_token, oauth_token_secret = read_token_file(MY_TWITTER_CREDS)
	twitter = Twitter(auth=OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET))
	# ...lleva un rato
	
	while True:
		filename = DIR_AEDE
		# Cojo un diario
		filename += random.choice(periodicos)
		file_content = read_file(filename)
		if file_content:
			decoded_file = get_encoding(file_content)
			# Cojo unas tijeras
			if len(decoded_file) > 0:
				# Escojo en el diario un artculo de la longitud que cuenta darle a mi poema. 
				articulos = re.findall(r'<p>.*</p>', decoded_file)
				bolsa = []
				for x in range(0, len(articulos)):
					# Recorto el artculo
					aux = re.findall(r'(\w+)', articulos[x])
					for y in range(0, len(aux)):
						if aux[y] not in HTML_TAGS and aux[y] not in HTML_ATTRS:
							# Recorto en seguida con cuidado cada una de las palabras que forman el artculo y mtolas en una bolsa
							bolsa.append(aux[y])
				if len(bolsa) > 0:
					# Agtola suavemente. Ahora saco cada recorte uno tras otro. Copio concienzudamente en el orden en que han salido de la bolsa. 
					twitter.statuses.update(status=get_message(bolsa))
					# print(get_message(bolsa))
					break
		
except:
	print('Error Fatal, siempre haciendo tontadas: ', sys.exc_info()[0])
	raise	
