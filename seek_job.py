import urllib3
import re
import requests
import certifi
import time
from html.parser import HTMLParser
from pyquery import PyQuery as pyquery
import json
import sqlite3


# regular exp.
def findResultNum(html):
	# jobList = re.findall('<span class="_2XFDIKN" data-automation="totalJobsCount" data-reactid="\d*">(.*?)</span>',html)
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
	# print(jobNum)
	totalPage = int((int(jobNum)-1)/20)+1
		# print(totalPage)
	return totalPage

#find all the links of jobs in some page
def getJobLinks(website):
	originContent = getWebsiteContent(website)
	listJobIds = re.findall('"jobIds":\[(.*?)\],',originContent)
	# print(len(listJobIds))
	jobIds = listJobIds[0]
	# print(jobIds)
	jobSet = jobIds.split(',')
	return jobSet
	# print(re.findall(r'"(\/job\/.*?)"',originContent))
	# jobLinks = re.findall(r'"(\/job\/.*?)"',originContent)
	# jobLinks = re.findall(r'"https://www.seek.co.nz/job/(.*?)"', originContent)
	# jobSet = set(jobLinks)

html_parser = HTMLParser()

def getWebsiteContent(website):
	html = requests.get(website)
	time.sleep(2)
	contents = ' '.join(html.content.decode('utf8').split())
	originContent = html_parser.unescape(contents)
	# py = pyquery(website)
	# t = py.text()
	# print(t)	
	return originContent


def getTitle(html):
	# title = re.findall('<h1 class="jobtitle">(.*?)</h1>',html)
	py = pyquery(html)
	title = py('.jobtitle').text()
	# print(title)
	return title

def getJobContent(html):
	# content2 = str("")
	# content = re.findall('<div class="templatetext">(.*?)</div><div class="details">[.*]</div>)',html)
	# content = re.findall('(<div class="templatetext">.*?) <div class="details">',html)
	# if len(content)==0:
	# 	return content2
	# print(content)
	py = pyquery(html)
	content1 = py('.templatetext').text().encode('ascii', 'ignore').decode('ascii')
	content2 = str(content1)	
	# print(content2)	
	# content = re.findall('<div class="templatetext">(.*?)<div class="details">[.*?]</div></div>',html)
	return content2


# website address of online jobs
basicWebsite = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand"
# website of different page
websitePrifix = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand?page="
# prifix + jobID to locate the content of each job
basicPrifix = "https://www.seek.co.nz/job/"

if __name__ == '__main__':
	#get the total num of search results
	# jobLink = "33805061"
	# jobAddress = basicPrifix+jobLink
	# pageContent = getWebsiteContent(jobAddress)
	# strTitle = str(getTitle(pageContent))
	# fileName = jobLink + '.txt'
	# file = open(fileName,'w')
	# if len(strTitle)==0:
	# 	print("no title found! job id is: " + jobLink)

	# title = strTitle.strip()+"("+str(jobLink)+")"
	# file.write(title)

	# jobContent = getJobContent(pageContent)
	# if len(jobContent)==0:
	# 	print("no job content found! job id is: " + jobLink)
	# # print(jobContent)
	# # jobContent = format(jobContent.encode('iso-8859-1', 'ignore'))
	# jobContent = format(jobContent)
	# file.write(jobContent)

	# file.flush()
	# file.close()

	pageNum = getTotalPage(basicWebsite)
	pageNum =1
	page = 1
	# html = requests.get("https://www.seek.co.nz/job/33846987")
	# file = open('out.txt','w')
	# file.write(str(html.content))
	# file.close()
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
			# print(jobContent)
			# write them into file
			if len(jobContent) == 0:
				print("no job content found! job id is: " + jobLink+ "search again!")
				jobContent = getJobContent(pageContent)

				# string = jobContent.replace('\u2013','')
				# jobContent = str(jobContent.encode('iso-8859-1', 'ignore'))
			# jobContent = format(content.encode('iso-8859-1', 'ignore'))

			cur.execute('''INSERT OR IGNORE INTO OriginJobContent(uid,url,title,content) 
				VALUES ( ?, ?, ?, ? )''', (jobLink, jobAddress, title, jobContent, ) )
			cur.execute('SELECT uid FROM OriginJobContent WHERE (url==(?))',(jobAddress,))
			job_id = cur.fetchone()[0]
			# print(job_id)

			# jobC = str(content)
			# file.write(jobC)
			# file.write("\n\n")
			# file.flush()
			# file.close()

	conn.commit()
	cur.close()
	print("Process finished")
