import re
import urllib2

p = re.compile("<td class=\"menugridcell.*?</td>", re.S)

response = urllib2.urlopen("http://menu.ha.ucla.edu/foodpro/default.asp?location=07")
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
if len(menuGridCellList) == 27:
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
elif len(menuGridCellList) == 18:
	while len(menuGridCellList) > currentIndex:
		if currentType == 0:	#if brunch
			brunchGrids.append(menuGridCellList[currentIndex])
			currentType = 1
		else:	#if dinner
			dinnerGrids.append(menuGridCellList[currentIndex])
			currentType = 0
		currentIndex = currentIndex + 1
	
	
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
				s.insert(0, " { \"title\": ")
				s.append(" }")
				r = "".join(s)
				finalList.append(r)
			
	return finalList

if len(menuGridCellList) == 27:
	breakfastGrids = parseMeal(breakfastGrids)
	print("!!!!!!!!!!!!!!PRINTING FINAL BREAKFAST LIST!!!!!!!!!")
	for item in breakfastGrids:
		print item
		
	lunchGrids = parseMeal(lunchGrids)
	print("!!!!!!!!!!!!!!PRINTING FINAL LUNCH LIST!!!!!!!!!")
	for item in lunchGrids:
		print item
		
	dinnerGrids = parseMeal(dinnerGrids)
	print("!!!!!!!!!!!!!!PRINTING FINAL DINNER LIST!!!!!!!!!")
	for item in dinnerGrids:
		print item

elif len(menuGridCellList) == 18:
	brunchGrids = parseMeal(brunchGrids)
	print("!!!!!!!!!!!!!!PRINTING FINAL BRUNCH LIST!!!!!!!!!")
	for item in brunchGrids:
		print item
	
	dinnerGrids = parseMeal(dinnerGrids)
	print("!!!!!!!!!!!!!!PRINTING FINAL DINNER LIST!!!!!!!!!")
	for item in dinnerGrids:
		print item
