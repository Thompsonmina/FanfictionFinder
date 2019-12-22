#gets fanfiction stories from the site based on number of reviews

import requests
from bs4 import BeautifulSoup
import pprint, re, time


def extractStoryDetails(storyTitle, storyFooter):
	stories = []
	for i in range(len(storyTitle)):
		storyTitlesDetail = (storyTitle[i].get_text(), storyTitle[i].get("href"))
		stories.append({"title":storyTitlesDetail, "reviews":getReviewNumbers(storyFooter[i])})
	
	return stories

def getReviewNumbers(singleStoryFooter):
	words = singleStoryFooter.get_text()
	review = re.compile(r"Reviews: \d+").search(words)
	if review:
		reviewNum = review.group()[9:]
		return int(reviewNum)
	else: return 0

def sortByReview(num, stories):
	sortedstories = filter(lambda s: s["reviews"] >= num, stories)
	return [x for x in sortedstories]

def main(num):
	megaList2 = []
	for i in range(1, num):
		pageData = requests.get(f"https://www.fanfiction.net/book/Harry-Potter/?&srt=1&r=103&p={i}")
		pageHtml = BeautifulSoup(pageData.text, "html.parser")
		storyFooter = pageHtml.select(".z-padtop2")
		storyTitles = pageHtml.select(".stitle")

		body = extractStoryDetails2(storyTitles, storyFooter)
		books2 = sortByReview(1000, body)
		megaList2.append(books2)

	with open("harrypotter.txt", "w") as file:
		for line in megaList2:
			file.write(str(line) + "\n")
	return ''


