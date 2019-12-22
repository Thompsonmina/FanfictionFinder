#gets fanfiction stories from the site based on number of reviews

import requests
from bs4 import BeautifulSoup
import re


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
		pageData = requests.get(f"https://www.fanfiction.net/book/{title}/?&srt=1&r=10&p={i}")
		pageHtml = BeautifulSoup(pageData.text, "html.parser")
		storyFooter = pageHtml.select(".z-padtop2")
		storyTitles = pageHtml.select(".stitle")
		
		if not storyFooter:
			return False

		body = extractStoryDetails(storyTitles, storyFooter)
		books = sortByReview(minNumOfReviews, body)
		megaList.append(books)

	with open("fanfiction.txt", "w") as file:
		for line in megaList:
			file.write(str(line) + "\n")
	return True


def main():
	print("-------------------FanfictionFinder----------------------", "\n\n\n\n\n")
	nameOfFic = input("What's the title ? : ").replace(" ", "-")
	while True:
		try:
			reviews = int(input("enter the minumum number of reviews allowed : "))
			pages = int(input("how many pages should be searched through : "))
			break
		except ValueError:
			print("please enter numbers")

	if compileFics(nameOfFic, pages, reviews):
		print("succesful")
		return
	else:
		print("the title you inputed isn't quite correct")
	
if __name__ == "__main__":
	main()
