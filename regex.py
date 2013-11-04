import re
import urllib2
import sys

def bcafeGetData(url):
	response = urllib2.urlopen(url)
	page_source = response.read()
	regex = re.compile("<td class=\"layouttablecell\">(.*?)</td>", re.S) #regex1 is used to isolate items from the source, including gibberish that surrounds it
	regexdata = regex.findall(page_source) #first we do meal items, we need a different regex for drinks
	regex = re.compile("<td class=\"layouttablecell_full\">(.*?)</table>", re.S) #for drinks here
	regexdata = regexdata + regex.findall(page_source)
	return regexdata


def bcafeGetItems(regexdata):
	regex = re.compile(";\">(.*?)<", re.S) #for items
	regex2 = re.compile("<h1>(.*?)</h1>", re.S) #for titles
	regex2data = []
	for section in regexdata:
		skip = False
		titles = regex2.findall(section)
		for title in titles:
			if title == "The B-Caf\xe9 Combo" or title == "Combo Meal": #we don't want these combos
				skip = True
				break
			if title == "&nbsp;": #chips has no title so we need a seperate handler for this :(
				regex2data.append({'title' : 'Chips'}) 
				break
			regex2data.append({'title' : title})
		if not skip:
			items = regex.findall(section)
			for item in items:
				regex2data.append(item)
	return regex2data

#print bcafeGetItems(bcafeGetData("http://menu.ha.ucla.edu/foodpro/bruincafe.asp"))

def seperateMeals(url):
	response = urllib2.urlopen(url)
	page_source = response.read()

	#Get a list of all grid cells, every third one belongs to each b/l/d
	menuGridCellItemP = re.compile("<td class=\"menugridcell.*?</td>", re.S)
	menuGridCellList = menuGridCellItemP.findall(page_source)
	breakfastGrids = []
	lunchGrids = []
	dinnerGrids = []
	brunchGrids = []	#for weekends

	#for each cell
	currentIndex = 0
	currentType = 0

	allmeals = {}
	if len(menuGridCellList) %  2 == 0:
		while len(menuGridCellList) > currentIndex:
			if currentType == 0:	#if brunch
				brunchGrids.append(menuGridCellList[currentIndex])
				currentType = 1
			else:	#if dinner
				dinnerGrids.append(menuGridCellList[currentIndex])
				currentType = 0
			currentIndex = currentIndex + 1
		allmeals['breakfast'] = brunchGrids
		allmeals['lunch'] = brunchGrids
		allmeals['dinner'] = dinnerGrids
	else:
		while len(menuGridCellList) > currentIndex:
			if currentType == 0:	#if breakfast
				breakfastGrids.append(menuGridCellList[currentIndex])
				currentType = 1
			elif currentType == 1:	#if lunch
				lunchGrids.append(menuGridCellList[currentIndex])
				currentType = 2
			else:	#if dinner
				dinnerGrids.append(menuGridCellList[currentIndex])
				currentType = 0
			currentIndex = currentIndex + 1
		allmeals['breakfast'] = breakfastGrids
		allmeals['lunch'] = lunchGrids
		allmeals['dinner'] = dinnerGrids

	return allmeals
	
	
#for index in range(0, len(breakfastGrids)):
#	print breakfastGrids[index]
#	print lunchGrids[index]
#	print dinnerGrids[index] 
#	print("----------")

def parseMeal(mealData):	#parse the meal grids into readable data
	#itemMatchList contains meal data and HTML junk
	#Returns the meal items AND the locations
	rawItemP = re.compile("onmouseover=.*?>.*?</a>|<li class=\"category\d\">.*?</li>", re.S)
	itemMatchList = rawItemP.findall("".join(mealData))

	#for item in itemMatchList:
	#	print item
		
	#print("-----------")

	#Clean up the HTML shit for each menu item
	refinedItemP = re.compile(">.*?</a>|\"category\d\">.*?</li>", re.S)
	refinedItemMatchList = refinedItemP.findall("".join(itemMatchList))

	#for item in refinedItemMatchList:
	#	print item
		
	#print("-----------")

	finalList = []
	#Remove the final HTML crap, then print
	for r in refinedItemMatchList:
		#check if meal item or kitchen title
		if "</a>" in r:
			#if meal item
			s = list(r)
			s.remove(">")
			s.pop()
			s.pop()
			s.pop()
			s.pop()
			r = "".join(s)
			finalList.append(r)
		else:
			finalItemP = re.compile("\d\">.*?</li>", re.S)
			finalItemMatchList = finalItemP.findall(r)
			for i in finalItemMatchList:
				s = list(i)
				s.remove('"')
				s.remove(">")
				s.pop(0)
				s.pop()
				s.pop()
				s.pop()
				s.pop()
				s.pop()
				s.insert(0, "{\"title\":\"")
				s.append("\"}")
				r = "".join(s)
				finalList.append(r)
			
	return finalList

def returnMealData(url):
	mealDataWTags = seperateMeals(url)
	mealData = {}
	mealData['breakfast'] = parseMeal(mealDataWTags['breakfast'])
	mealData['lunch'] = parseMeal(mealDataWTags['lunch'])
	mealData['dinner'] = parseMeal(mealDataWTags['dinner'])
	return mealData

