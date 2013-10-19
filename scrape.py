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
	
	mealdata['lunch'] = lunch
	mealdata['dinner'] = dinner
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
	return mealdata
