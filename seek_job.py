import urllib3
import re
import requests
import certifi
import time
from html.parser import HTMLParser

# regular exp.
def findResultNum(html):
	jobList = re.findall('<span class="_2XFDIKN" data-automation="totalJobsCount" data-reactid="\d*">(.*?)</span>',html)
	return jobList

# find the result of job numbers
def getTotalPage(website):
	totalPage = 0
	html = requests.get(website)
	contents = html.content.decode('utf-8')
	result = findResultNum(contents)
	if len(result)>0:
		jobNum = result[0]
		# print(jobNum)
		totalPage = int((int(jobNum)-1)/20)+1
		print(totalPage)
	return totalPage

#find all the links of jobs in some page
def getJobLinks(website):
	html = requests.get(website)
	contents = ' '.join(html.content.decode('utf-8').split())
	html_parser = HTMLParser()
	originContent = html_parser.unescape(contents)
	file = open ('page.txt','w')
	file.write(str(html.content))
	file.flush()
	file.close()
	# print(re.findall(r'"(\/job\/.*?)"',originContent))
	jobLinks = re.findall(r'"(\/job\/.*?)"',originContent)
	print(len(jobLinks))
	file = open ('joblinks.txt','w')
	for jobLink in jobLinks:
		file.write(jobLink + "\n")

	file.flush()
	file.close()

# website address of online jobs
basicWebsite = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand"
websitePrifix = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand?page="
basicPrifix = "https://www.seek.co.nz"

if __name__ == '__main__':
	pageNum = getTotalPage(basicWebsite)
	page = 1
	while(page<=1):
		site = websitePrifix + str(page)
		# print(site)
		getJobLinks(site)
		page += 1



