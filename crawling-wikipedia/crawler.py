import requests
import sys
from xml.dom.minidom import parseString

def requestWiki(arr_page_titles,str_offset,int_limit,str_direction):
	data_to_request = {"pages":"|".join(arr_page_titles),#os titulos são separados por "|"
			"offset":str_offset, #O offset é a data primeira revisão a ser coletada. Formato:
			"dir":str_direction,#direction='asc': a partir de offset até os mais recentes.
					#direction='desc': a partir de offset para os mais antigos
			"limit":int_limit, #Quantidade máxima de paginas/revisões
			"action":"submit",
			"title":"Special:Export"}

	url_to_request = "https://en.wikipedia.org/w/index.php"
	response = requests.post(url_to_request, data=data_to_request)
	return parseString(response.text)
def getTagData(dom,strTag):
	tag = dom.getElementsByTagName(strTag)
	if(len(tag)>0 and len(tag[0].childNodes)>0):
		return tag[0].childNodes[0].data.strip()
	return ""

def writeRevision(dom_rev,str_title):
	str_timestamp = getTagData(dom_rev, "timestamp")
	str_text = getTagData(dom_rev, "text")
	with open("output/"+str_title+"_"+str_timestamp+".txt","w") as out:
		out.write(str_text)
	return str_timestamp

def crawlArticle(str_title,str_last_timestamp):
	has_revision = True
	str_timestamp = str_last_timestamp
	while has_revision:
		#requisita as revisoes a partir da mais antiga até um
		#determinado limite
		print("Request: "+str_title+" from: '"+str_timestamp+"'")
		dom = requestWiki([str_title],str_offset=str_timestamp,int_limit=1000,str_direction="desc")
		#não achou revisão
		if not dom:
			return

		#obtem cada revisão
		revisions = dom.getElementsByTagName("revision")
		str_last_crawled_timestamp = ""
		for dom_rev in revisions:
			str_last_crawled_timestamp = writeRevision(dom_rev,str_title)
		if str_last_crawled_timestamp=="":
			has_revision = False
		else:
			#A ultima revisão coletada (i.e. a mais antiga)
			#será a próxima a ser requisitada
			str_timestamp = str_last_crawled_timestamp

if __name__ == "__main__":
	#será coletado os artigos até esta data
	str_last_timestamp = "2008-01-01T00:00:00Z"
	#abre um arquivo com o titulo que deseja requisitar
	with open(sys.argv[1]) as txt_file:
		#para cada titulo
		for str_title in txt_file:
			crawlArticle(str_title.replace("\n",""),str_last_timestamp)
