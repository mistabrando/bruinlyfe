import re
import urllib2

def scrape1919(url):
	response = urllib2.urlopen(url)
	page_source = response.read()

	#Get a list of all grid cells, every third one belongs to each b/l/d
	menuPageP = re.compile("(<img src=\"images/cafe1919/title_bibite.png.*?<div id=\"combo\">)|(<img src=\"images/cafe1919/title((?!Hours)(?!What's New).)*?</tbody>)", re.S)
	menuPageTuple = menuPageP.findall(page_source)

	menuPageList = list(menuPageTuple)

	rawMenuP = re.compile("onmouseover=.*?>.*?</a>|alt=\".*?/><br />|\"beverageheader\">.*?</span>", re.S)

	menuList = []	#raw list of each item on the menu with titles
	#there are six pages
	for i in range(0, 6):	
		menuList.append(list(rawMenuP.findall("".join(menuPageList[i]))))

	#create unified list of items
	menuAsList = []
	for menu in menuList:
		for item in menu:
			menuAsList.append(item)

#parse the meals into readable data
def parseMenu(menuData):
	finalList = []
	for item in menuData:
		rawItemP = re.compile("t=\"(.*?)\" />|beverageheader\">(.*?)</span>|\">(.*?)</a>", re.S)
		rawItemListOfMatches = rawItemP.findall(item)
		#add "title" tag and clean things up a bit
		for match in rawItemListOfMatches:
			#match[0] == main titles
			#match[1] == sub titles
			#match[2] == items
			if(match[0] != ""):
				editableMatchItem = list(match[0])
				editableMatchItem.insert(0, "{\"title\":\"")
				editableMatchItem.append("\"}")
				finalList.append("".join(editableMatchItem))
			elif(match[1] != ""):
				editableMatchItem = list(match[1])
				editableMatchItem.insert(0, "{\"title\":\"")
				editableMatchItem.append("\"}")
				finalList.append("".join(editableMatchItem))
			else:
				matchItem = match[2]
				matchItem = re.sub("<.*?>", "", matchItem)
				matchItem = re.sub("&nbsp;", "", matchItem)
				finalList.append(matchItem)
	
	for item in finalList:
		item = re.sub('\xe9', '\xc3\xa9', item)
		item = re.sub('\xae', '\xc2\xae', item)
		item = unicode(item, "utf-8")

	return finalList		
			
	menuAsList = parseMenu(menuAsList)
	return menuAsList
