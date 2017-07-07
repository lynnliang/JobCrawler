import urllib3
import re
import requests
import certifi
import time
from html.parser import HTMLParser
from pyquery import PyQuery as pyquery
import json

# #定义HTMLParser的子类,用以复写HTMLParser中的方法
# class MyHTMLParser(HTMLParser):
 
#     #构造方法,定义data数组用来存储html中的数据
#     def __init__(self):
#         HTMLParser.__init__(self)
#         self.data = []
 
#     #覆盖starttag方法,可以进行一些打印操作
#     def handle_starttag(self, tag, attrs):
#         pass
#         #print("Start Tag: ",tag)
#         #for attr in attrs:
#         #   print(attr)
     
#     #覆盖endtag方法
#     def handle_endtag(self, tag):
#         pass
 
#     #覆盖handle_data方法,用来处理获取的html数据,这里保存在data数组
#     def handle_data(self, data):
#         if data.count('\n') == 0:
#             self.data.append(data)

# parser = MyHTMLParser() 



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
	contents = ' '.join(html.content.decode('utf8').split())
	originContent = html_parser.unescape(contents)
	# py = pyquery(website)
	# t = py.text()
	# print(t)	
	return originContent


def getTitle(html):
	title = re.findall('<h1 class="jobtitle">(.*?)</h1>',html)

	return title

def getJobContent(html):
	content2 = str("")
	# content = re.findall('<div class="templatetext">(.*?)</div><div class="details">[.*]</div>)',html)
	content = re.findall('(<div class="templatetext">.*?)<div class="details">',html)
	if len(content)==0:
		return content2

	py = pyquery(content[0])
	content1 = py('div').text()
	content2 = str(content1)		
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
	pageNum = getTotalPage(basicWebsite)
	pageNum = 1
	page = 1
	# html = requests.get("https://www.seek.co.nz/job/33846987")
	# file = open('out.txt','w')
	# file.write(str(html.content))
	# file.close()

	file = open ('jobContent.txt','w')
	while(page<=pageNum):
		page += 1
		site = websitePrifix + str(page)
		# get the job id in every page
		jobSet=getJobLinks(site)
		for jobLink in jobSet:
			jobAddress = basicPrifix + jobLink
			pageContent = getWebsiteContent(jobAddress)
			strTitle = getTitle(pageContent)
			if len(strTitle) > 0:
				title = str(strTitle[0]) + "(" + str(jobLink) + ")"
				
			jobContent = getJobContent(pageContent)
			# print(jobContent)
			# write them into file
			if len(jobContent) > 0:
				# string = jobContent.replace('\u2013','')
				jobContent = str(jobContent.encode('iso-8859-1', 'ignore'))
				file.write(jobContent)
				file.write("\n\n")
				# if isinstance(jobContent,basestring):
				# 	string = jobContent.encode('utf-8')
				# else:
				# 	string = unicode(jobContent).encode('utf-8')
				# file.write(string)


	file.flush()
	file.close()
