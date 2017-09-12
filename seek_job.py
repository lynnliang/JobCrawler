# Run in python 3.6

import urllib
import re
import requests
import certifi
import time
from html.parser import HTMLParser
from pyquery import PyQuery as pyquery
import json
import sqlite3
from difflib import SequenceMatcher

#check the similarity of two string (text)
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# regular exp.
def findResultNum(html):
	jobNum = re.findall('"totalCount":(.*?),',html)
	return jobNum

# find the result of job numbers
def getTotalPage(website):
	totalPage = 0
	originContent = getWebsiteContent(website)
	result = findResultNum(originContent)
	if len(result) == 0:
		return totalPage
	jobNum = result[0]
	totalPage = int((int(jobNum)-1)/20)+1
	return totalPage

#find all the links of jobs in some page
def getJobLinks(website):
	originContent = getWebsiteContent(website)
	listJobIds = re.findall('"jobIds":\[(.*?)\],',originContent)
	jobIds = listJobIds[0]
	jobSet = jobIds.split(',')
	return jobSet

html_parser = HTMLParser()

def getWebsiteContent(website):
	html = requests.get(website)
	time.sleep(2)
	contents = ' '.join(html.content.decode('utf8').split())
	originContent = html_parser.unescape(contents)
	return originContent


def getTitle(html):
	py = pyquery(html)
	title = py('.jobtitle').text()
	return title

def getJobContent(html):
	py = pyquery(html)
	content1 = py('.templatetext').text().encode('ascii', 'ignore').decode('ascii')
	content2 = str(content1)	
	return content2


# website address of online jobs
basicWebsite = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand"
# website of different page
websitePrifix = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand?page="
# prifix + jobID to locate the content of each job
basicPrifix = "https://www.seek.co.nz/job/"

if __name__ == '__main__':
	#get the total num of search results
	pageNum = getTotalPage(basicWebsite)
	pageNum =1
	page = 1

	conn = sqlite3.connect('onlineJobs.sqlite')
	cur = conn.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS OriginJobContent 
    	(uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, url TEXT UNIQUE, title TEXT, 
    	 content TEXT)''')
	print("DB connected!")

	# file = open ('jobContent.txt','w')
	while(page<=pageNum):
		page += 1
		site = websitePrifix + str(page)
		# get the job id in every page
		jobSet=getJobLinks(site)
		for jobLink in jobSet:
			jobAddress = basicPrifix + jobLink
			pageContent = getWebsiteContent(jobAddress)
			time.sleep(1)
			strTitle = getTitle(pageContent)
			# fileName = jobLink + '.txt'
			# file = open(fileName,'w')
			if len(strTitle) == 0:
				print("no title found! job id is: " + jobLink + "search again!")
				strTitle = getTitle(pageContent)

			title = strTitle.strip()
			# title = strTitle.strip() + "(" + str(jobLink) + ")" + "\n"
			# file.write(title)
			
			jobContent = getJobContent(pageContent)
			if len(jobContent) == 0:
				print("no job content found! job id is: " + jobLink+ "search again!")
				jobContent = getJobContent(pageContent)

			cur.execute('''INSERT OR IGNORE INTO OriginJobContent(uid,url,title,content) 
				VALUES ( ?, ?, ?, ? )''', (jobLink, jobAddress, title, jobContent, ) )
			cur.execute('SELECT uid FROM OriginJobContent WHERE (url==(?))',(jobAddress,))
			job_id = cur.fetchone()[0]

	conn.commit()
	cur.close()
	print("Process finished")
