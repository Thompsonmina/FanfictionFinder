#gets fanfiction stories from the site based on number of reviews

import requests
from bs4 import BeautifulSoup
import re

def main():
	print("-------------------FanfictionFinder----------------------", "\n\n\n\n\n")
	categories = {1: "book", 2: "anime", 3: "cartoons", 4: "movies", 5: "tv", 6: "games", 7: "plays"}
	print(categories, "\n\n")
	# displays fanfiction categories to choose from
	while True:
		try:
			categoryNum = int(input("select a category by its number : "))
			if not categoryNum in range(1, 8):
				print("select a number provided")
			else:	break
		except:
			print("you can only provide a digit only")

	# get title of the fanfiction and ensure that the page is valid
	while True:
		nameOfFic = input("What's the title ? : ").replace(" ", "-")
		restOfLink = f"{categories[categoryNum]}/{nameOfFic}"
		if not titlePageExists(restOfLink):
			print("the title you inputed isn't quite correct") 
		else:
			break

	while True:
		try:
			reviews = int(input("enter the minumum number of reviews allowed : "))
			pages = int(input("how many pages should be searched through : "))
			break
		except ValueError:
			print("please enter numbers")

	compileFics(restOfLink, pages, reviews)
	print("succesful")


def titlePageExists(partOfLink):
	pageData = requests.get(f"https://www.fanfiction.net/{partOfLink}")
	pageHtml = BeautifulSoup(pageData.text, "html.parser")
	storyFooter = pageHtml.select(".z-padtop2")

	if storyFooter:
		return True
	return False

def extractStoryDetails(storyTitle, storyFooter):
	"""Gets all the stories and thier links from a page"""
	stories = []
	for i in range(len(storyTitle)):
		storyTitlesDetail = (storyTitle[i].get_text(), storyTitle[i].get("href"))
		stories.append({"title":storyTitlesDetail, "reviews":getReviewNumbers(storyFooter[i])})
	
	return stories

def getReviewNumbers(singleStoryFooter):
	"""Gets the number of reviews from the html using regex"""
	words = singleStoryFooter.get_text()
	review = re.compile(r"Reviews: \d+").search(words)
	if review:
		reviewNum = review.group()[9:]
		return int(reviewNum)
	else: return 0

def filterByReview(minReviewNum, stories):
	"""filters through all the stories and returns an abridged list based on the minimum reviews given"""
	sortedstories = filter(lambda s: s["reviews"] >= minReviewNum, stories)
	return [x for x in sortedstories]

def compileFics(title, numOfPages,minNumOfReviews):
	"""gets the html, processes it into a giant list  and writes that list to a txt file """
	megaList = []
	for i in range(1, numOfPages):
		pageData = requests.get(f"https://www.fanfiction.net/{title}/?&srt=1&r=10&p={i}")
		pageHtml = BeautifulSoup(pageData.text, "html.parser")
		storyFooter = pageHtml.select(".z-padtop2")
		storyTitles = pageHtml.select(".stitle")

		body = extractStoryDetails(storyTitles, storyFooter)
		books = filterByReview(minNumOfReviews, body)
		megaList.append(books)
		writeFics(megaList)

def writeFics(listOfFics):

	with open("fanfiction.txt", "w") as file:
		for line in listOfFics:
			for stories in line:
				file.write("title : " + stories["title"][0]  + "\n")
				file.write("link : fanfiction.net" + stories["title"][1] + "\n")
				file.write("reviews : " + str(stories["reviews"]) +"\n\n")
	return True



	
if __name__ == "__main__":
	main()
