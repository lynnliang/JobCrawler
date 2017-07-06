import urllib3
import re
import requests
import certifi
import time
from html.parser import HTMLParser

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
	# file = open ('page.txt','w')
	# file.write(str(html.content))
	# file.flush()
	# file.close()
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

def getWebsiteContent(website):
	html = requests.get(website)
	contents = ' '.join(html.content.decode('utf-8').split())
	html_parser = HTMLParser()
	originContent = html_parser.unescape(contents)
	return originContent


def getTitle(html):
	title = re.findall('<h1 class="jobtitle">(.*?)</h1>',html)
	return title

def getJobContent(html):
	content = re.findall('<div class="templatetext">(.*?)<div class="details">[.*?]</div></div>',html)
	return content

# website address of online jobs
basicWebsite = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand"
# website of different page
websitePrifix = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand?page="
# prifix + jobID to locate the content of each job
basicPrifix = "https://www.seek.co.nz/job/"

if __name__ == '__main__':
	#get the total num of search results
	pageNum = getTotalPage(basicWebsite)
	pageNum = 1
	page = 1
	file = open ('joblinks.txt','w')
	while(page<=pageNum):
		site = websitePrifix + str(page)
		# get the job id in every page
		jobSet=getJobLinks(site)
		for jobLink in jobSet:
			jobAddress = basicPrifix + jobLink
			pageContent = getWebsiteContent(jobAddress)
			strTitle = getTitle(pageContent)
			if len(strTitle) > 0:
				title = str(strTitle[0]) + "(" + str(jobLink) + ")"
				print(title)

			jobContent = getJobContent(pageContent)
			print(jobContent)
			# write them into file
			file.write(jobLink + "\n")

		page += 1

	file.flush()
	file.close()



