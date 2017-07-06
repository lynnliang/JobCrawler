import urllib3
import re
import requests
import certifi
import time

def findResultNum(html):
	jobList = re.findall('<span class="_2XFDIKN" data-automation="totalJobsCount" data-reactid="\d*">(.*?)</span>',html)
	return jobList

def getTotalPage(basicWebsite):
	totalPage = 0
	html = requests.get(basicWebsite)
	contents = html.content.decode('utf-8')
	file = open ('page.txt','w')
	file.write(str(html.content))
	file.flush()
	file.close()
	result = findResultNum(contents)
	if len(result)>0:
		jobNum = result[0]
		print(jobNum)
		totalPage = (float(jobNum)-1)/20+1
		print(totalPage)
	return totalPage


basicWebsite = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand"
websitePrifix = "https://www.seek.co.nz/jobs-in-information-communication-technology/testing-quality-assurance/in-All-New-Zealand?page="

if __name__ == '__main__':
	getTotalPage(basicWebsite)

