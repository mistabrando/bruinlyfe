from bs4 import BeautifulSoup
import requests

def threemeals(url):
	mealdata = {}
	#create soup object
	response = requests.get(url)
	soup = BeautifulSoup(response.text)

	#dinner needs a seperate loop because fucking webdevs made it a seperate class
	breakfast = []
	lunch = []
	counter = True
	for group in soup.find_all("td", { "class" : "menugridcell" }):
	    if counter:
	    	for item in group.find_all("li", {"class" : "category2", "class" : "category4", "class" : "category5"}):
	    		breakfast.append({"title" : item.get_text()})
			for item in group.find_all("a", { "class" : "itemlinkt" }):
				breakfast.append(item.get_text())
			for item in group.find_all("a", { "class" : "itemlink" }):
			    breakfast.append(item.get_text())
	    else:
	    	for item in group.find_all("li", {"class" : "category2", "class" : "category4", "class" : "category5"}):
	    		lunch.append({"title" : item.get_text()})
	    	for item in group.find_all("a", { "class" : "itemlinkt" }):
				lunch.append(item.get_text())
	        for item in group.find_all("a", { "class" : "itemlink" }):
			    lunch.append(item.get_text())
	    if counter:
	    	counter = False
	    else:
	    	counter = True

	#dinner here
	dinner = []
	for group in soup.find_all("td", { "class" : "menugridcell_last" }):
		for item in group.find_all("li", {"class" : "category2", "class" : "category4", "class" : "category5"}):
			dinner.append({"title" : item.get_text()})
		for item in group.find_all("a", { "class" : "itemlinkt" }):
			dinner.append(item.get_text())
		for item in group.find_all("a", { "class" : "itemlink" }):
		    dinner.append(item.get_text())	

	mealdata['breakfast'] = breakfast
	mealdata['lunch'] = lunch
	mealdata['dinner'] = dinner
	return mealdata

def twomeals(url):
	mealdata = {}
	#create soup object
	response = requests.get(url)
	soup = BeautifulSoup(response.text)

	#dinner needs a seperate loop because fucking webdevs made it a seperate class
	lunch = []
	for group in soup.find_all("td", { "class" : "menugridcell" }):
	    for item in group.find_all("a", { "class" : "itemlinkt" }):
			lunch.append(item.get_text())
        for item in group.find_all("a", { "class" : "itemlink" }):
		    lunch.append(item.get_text())

	#dinner here
	dinner = []
	for group in soup.find_all("td", { "class" : "menugridcell_last" }):
		for item in group.find_all("a", { "class" : "itemlinkt" }):
			dinner.append(item.get_text())
		for item in group.find_all("a", { "class" : "itemlink" }):
		    dinner.append(item.get_text())	
	
	mealdata['breakfast'] = []
	mealdata['lunch'] = lunch
	mealdata['dinner'] = dinner
	mealdata['latenight'] = []
	return mealdata

def bcafe(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	mealdata = []
	for group in soup.find_all("td", { "class" : "layouttablecell"}):
		for item in group.find_all("h1"):
			mealdata.append({"title" : item.get_text()})
		for item in group.find_all("a", { "class" : "itemlink" }):
			mealdata.append(item.get_text())
	data = sortbcafe(mealdata)
	return data

def sortbcafe(data):
	mealdata = {}
	onBreakfast = True;
	onLunch = False;
	onDinner = False;
	spaghetti = False #omigod this is terrible, but we need to know after Lunch on the Go stops
	breakfast = []
	lunch = []
	dinner = []
	for item in data:
		try:
			item['title']
		except TypeError:
			pass
		else:
			if(onLunch and spaghetti):
				onBreakfast = False
				onLunch = True
				onDinner = True
			if(item['title'] == "Lunch on the Go"):
				onBreakfast = False
				onLunch = True
				onDinner = False
				spaghetti = True
		if(onBreakfast):
			breakfast.append(item)
		if(onLunch):
			lunch.append(item)
		if(onDinner and spaghetti):
			dinner.append(item)
	#special little bit of code here to move the soup, patch fix until we regex to work...
	kosher = lunch.pop(56)
	lunch.insert(66, kosher)
	kosher = dinner.pop(32)
	dinner.insert(42, kosher)
	mealdata['breakfast'] = breakfast
	mealdata['lunch'] = lunch
	mealdata['dinner'] = dinner
	mealdata['latenight'] = dinner
	return mealdata

def late(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	mealdata = []
	for sectionnum in range(0,3):
		switchdict = ["Entrees", "Sides", "Pizza and Wings"]
		mealdata.append({"title" : switchdict[sectionnum]})
		sectionid = "s" + str(sectionnum)
		section = soup.find("div", { "id" : sectionid })
		for item in section.find_all("a", { "class" : "itemlink" }):
			mealdata.append(item.get_text())
	return mealdata

def nineteen(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	mealdata = []
	for sectionnum in range(0,7):
		switchdict = ["Pizzette", "Panini", "Insalate", "Lasagna", "Sides", "Bibite", "Dolci"]
		mealdata.append({ "title" : switchdict[sectionnum]})
		sectionid = "s" + str(sectionnum)
		section = soup.find("div", { "id" : sectionid })
		for item in section.find_all("a", { "class" : "itemlink" }):
			mealdata.append(item.get_text())
	data = sortnineteen(mealdata)
	return data

def sortnineteen(data):
	mealdata = {}
	onBreakfast = False;
	onLunch = True;
	onDinner = True;
	breakfast = []
	lunch = []
	dinner = []
	for item in data:
		try:
			item['title']
		except TypeError:
			pass
		else:
			if(item['title'] == "Lasagna"):
				onBreakfast = False
				onLunch = False
				onDinner = True
			if(item['title'] == "Sides"):
				onBreakfast = False
				onLunch = True
				onDinner = True

		if(onBreakfast):
			breakfast.append(item)
		if(onLunch):
			lunch.append(item)
		if(onDinner):
			dinner.append(item)
	mealdata['breakfast'] = []
	mealdata['lunch'] = lunch
	mealdata['dinner'] = dinner
	mealdata['latenight'] = dinner
	return mealdata

def rende(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	mealdata = []
	for sectionnum in range(0,3):
		switchdict = ["Breakfast", "Mexican", "Asian"]
		mealdata.append({ "title" : switchdict[sectionnum]})
		sectionid = "s" + str(sectionnum)
		section = soup.find("div", { "id" : sectionid})
		for item in section.find_all("a", { "class" : "itemlink" }):
			if sectionnum is 0 and item.get_text() == "Apple Juice":
				mealdata.append({ "title" : "Beverages"})
			if sectionnum is 0 and item.get_text() == "Oatmeal":
				mealdata.append({ "title" : "Express Breakfast"})
			if sectionnum > 0 and item.get_text() == "Fountain Beverage":
				mealdata.append({ "title" : "Beverages"})
			if item.get_text():
				mealdata.append(item.get_text())
	truemealdata = sortrende(mealdata) #look we be sorting it
	return truemealdata

def sortrende(rendedata):
	mealdata = {}
	onBreakfast = True;
	onLunch = False;
	onDinner = False;
	breakfast = []
	lunch = []
	dinner = []
	for item in rendedata:
		try:
			item['title']
		except TypeError:
			pass
		else:
			if(item['title'] == "Mexican"):
				onBreakfast = False
				onLunch = True
				onDinner = True

		if(onBreakfast):
			breakfast.append(item)
		if(onLunch):
			lunch.append(item)
		if(onDinner):
			dinner.append(item)
	mealdata['breakfast'] = breakfast
	mealdata['lunch'] = lunch
	mealdata['dinner'] = dinner
	mealdata['latenight'] = dinner
	return mealdata

#----LOLLLLL------
def hedrick():
	mealData = {}
	mealData['breakfast'] = ["We wish we knew, but there's no data online so :("]
	mealData['lunch'] = ["We wish we knew, but there's no data online so :("]
	mealData['dinner'] = ["We wish we knew, but there's no data online so :("]
	mealData['latenight'] = ["We wish we knew, but there's no data online so :("]
	return mealData
