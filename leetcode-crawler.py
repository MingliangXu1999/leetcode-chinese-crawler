#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import requests
import requests_toolbelt
import codecs
import json
import time
import random
import json
import re

username=''
password=''


textpath='./problems.txt'
originurl='https://leetcode-cn.com'
problemsurl='https://leetcode-cn.com/api/problems/all'
problemurl="https://leetcode-cn.com/problems/"
loginurl='https://leetcode-cn.com/accounts/login'
qlurl = 'https://leetcode-cn.com/graphql'
user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'

#cookie样例
#set-cookie:LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiOTgwMTEzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXV0aGVudGljYXRpb24uYXV0aF9iYWNrZW5kcy5QaG9uZUF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjNiMDE2OTc4MGFiZTAxMmU4MGQ4Njg0NjhlMmI0NDc4ZDBiZTAzNTAiLCJpZCI6OTgwMTEzLCJlbWFpbCI6IiIsInVzZXJuYW1lIjoibWluZ2xpYW5neHUiLCJ1c2VyX3NsdWciOiJtaW5nbGlhbmd4dSIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLWNuLmNvbS9hbGl5dW4tbGMtdXBsb2FkL2RlZmF1bHRfYXZhdGFyLnBuZyIsInBob25lX3ZlcmlmaWVkIjp0cnVlLCJ0aW1lc3RhbXAiOiIyMDE5LTExLTA1IDE1OjAwOjI5LjA5MjM0NyswMDowMCIsIlJFTU9URV9BRERSIjoiMTcyLjIxLjYuMTYyIiwiSURFTlRJVFkiOiJhMDRkMjM3NzgxMTJhYzhkMGY1YWMxN2Y4Mjk4MjM3NyIsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.dgS-XkU6NSiv6mytcJMOWmj4ozI3CvkduEQ63YF-dLw; Domain=.leetcode-cn.com; expires=Tue, 19 Nov 2019 15:00:29 GMT; HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax; Secure
#set-cookie: csrftoken=T1Jff14KdAbLyVDplS2Qvp4rTZ3n46lYT0WmTr0BTVcEsbCGhFljnGXFic2tOb4T; Domain=.leetcode-cn.com; expires=Tue, 03 Nov 2020 15:00:29 GMT; Max-Age=31449600; Path=/; SameSite=Lax; Secure

#将字符串保存在文件中
def save2file(file_name, contents):
	fh =codecs.open(file_name, 'w','utf-8')
	fh.write(contents)
	fh.close()

class Leetcode_Session():
	#__init__
	def __init__(self):
		self.session=requests.Session()
		self.csrftoken=''
		self.problems={}#存储字典类型的问题摘要
		self.data=[]#存储最终的数据

	
	#爬虫模拟浏览器，模拟登录leetcode中文账号，
	def login(self):

		#获取cookies
		cookies=self.session.get(originurl).cookies
		for cookie in cookies:
				if cookie.name == 'csrftoken':
					self.csrftoken = cookie.value
					break
		#提交的data
		params_data = {'csrfmiddlewaretoken':self.csrftoken,'login': username,'password': password,'next': 'problems'}

		#模拟浏览器
		headers={'User-Agent':user_agent,'Connection':'keep-alive','Referer':loginurl,'origin':originurl}
	
		#数据处理
		m = requests_toolbelt.MultipartEncoder(params_data)
		headers['Content-Type'] = m.content_type

		#post请求
		self.session.post(loginurl,headers=headers,data=m,timeout = 10, allow_redirects = False)

		#print(self.session.cookies.get('LEETCODE_SESSION') is None)
		#返回登录成功标识
		print('登录是否成功:'+self.session.cookies.get('LEETCODE_SESSION') is not None)
		return self.session.cookies.get('LEETCODE_SESSION') is not None

	#获取问题目录并将有用的信息如问题网址加入self.problems
	def get_problems_contents(self):

		r=self.session.get(problemsurl)
		s=json.loads(r.text)
		self.problems=s['stat_status_pairs']
		#print(self.problems)

	
	#将self.problems内的必要内容输出到最终的data文件中，并进一步访问每一个问题
	'''
				[
			{
				"questionId": "135",					  // id
				"titleSlug": "candy",					 // 题目url
				"title": "Candy",						 // 题目标题
				"content": "<p>There are <em>N</em> ...", // 题目描述
				"difficulty": "Hard",					 // 难度
				"likes": 623,							 // 赞数
				"dislikes": 131,						  // 踩数
				"topicTags": [							// 类比标签
				"Greedy",
				...
				],
				"codeSnippets": [						 // 所有语言的代码模板
				{
					"lang": "Python",					 // 语言
					"code": "class Solution(object):...", // 代码模板
				},
				...
				],
				"totalAccepted": 112669,				  // 通过数量
				"totalSubmission": 381432,				// 提交数量
				"solution": {
				"id": "90",							 // 解答id
				"content": "[TOC]\n\n## Solution ..."   // 解答内容
				"averageRating": 4.931,				 // 平均评分
				"votes": 29							 // 票数
				}
			},
			...
			]

	'''
	def init_data(self):
		for dictt in self.problems[::-1]:

			dicto={}
			dicto['questionId']=dictt['stat']['question_id']
			dicto['titleSlug']=dictt['stat']['question__title_slug']
			dicto['title']=''
			dicto['content']=''
			if dictt['difficulty']['level']==1:
				dicto['difficulty']="简单"
			elif dictt['difficulty']['level']==2:
				dicto['difficulty']="中等"
			elif dictt['difficulty']['level']==3:
				dicto['difficulty']="困难"
			dicto['likes']=0
			dicto['dislikes']=0
			dicto['topicTags']=[]
			dicto['codeSnippets']=[]
			dicto['totalAccepted']=dictt['stat']['total_acs']
			dicto['totalSubmission']=dictt['stat']['total_submitted']
			dicto['solution']={}
			self.data.append(dicto)



	#针对每一个问题补充data
	def complete_data(self):
		
		for dictt in self.problems[::-1]:
			print('正在插入题目：'+str(dictt['stat']['question_id'])+':', end='')
			problemlink=problemurl+dictt['stat']['question__title_slug']

			headers={'User-Agent':user_agent,'Connection':'keep-alive','Content-Type': 'application/json','Referer':problemlink}
			params={"operationName":"questionData","variables":{"titleSlug":dictt['stat']['question__title_slug']},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    book {\n      id\n      bookName\n      pressName\n      description\n      bookImgUrl\n      pressImgUrl\n      productUrl\n      __typename\n    }\n    isSubscribed\n    __typename\n  }\n}\n"}

			json_data=json.dumps(params).encode('utf8')
			resp = self.session.post(qlurl, data=json_data, headers=headers, timeout=10)
			problemdict={}
			problemdict=json.loads(resp.text)
			print(problemdict['data']['question']['translatedTitle'])
			for dicto in self.data:
				if dicto['questionId']==dictt['stat']['question_id']:
					dicto['title']=problemdict['data']['question']['translatedTitle']
					dicto['content']=problemdict['data']['question']['translatedContent']
					dicto['likes']=problemdict['data']['question']['likes']
					dicto['dislikes']=problemdict['data']['question']['dislikes']
					for dicttt in list(problemdict['data']['question']['topicTags']):
						dicto['topicTags'].append(dicttt['translatedName'])
					try:
						for dictor in problemdict['data']['question']['codeSnippets']:
							dicto['codeSnippets'].append({'lang': dictor['lang'],'code':dictor['code']})
					except TypeError:
						print('---------------------------账号权限不足，无法获取该题具体信息')
					'''try:
						dicto['solution'].update({'id':problemdict['data']['question']['solution']['id']})
					except TypeError:
						print('---------------------------In this problem, there is no solution can apply for you.'
					'''
					#接下来访问该解答的具体信息
					#由于中英文网站的对应情况不是一致的,solution模块将改写为：(这里的解答均为leetcode官方解答)
					'''
							"solution": {
								'username':'力扣 (LeetCode)',
								'createdtime':'2018-05-27T16:26:11.200614+00:00',
								'viewCount':162904,
								'commentCount': 250,
								"content": "方法一：暴力法暴力法很简单，遍历每个元素 x..."   // 解答内容
								}
					'''
					#需要重新获取solution网站内容
						#获取官方用户名（每一题的官方解答用户不一致）
					headers={'User-Agent':user_agent,'Connection':'keep-alive','Content-Type': 'application/json','Referer':problemlink+'/solution/'}
					params={"operationName":"questionSolutionArticles","variables":{"questionSlug":"two-sum","first":10,"skip":0,"orderBy":"DEFAULT"},"query":"query questionSolutionArticles($questionSlug: String!, $skip: Int, $first: Int, $orderBy: SolutionArticleOrderBy, $userInput: String) {\n  questionSolutionArticles(questionSlug: $questionSlug, skip: $skip, first: $first, orderBy: $orderBy, userInput: $userInput) {\n    totalNum\n    edges {\n      node {\n        ...article\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment article on SolutionArticleNode {\n  title\n  slug\n  reactedType\n  status\n  identifier\n  canEdit\n  reactions {\n    count\n    reactionType\n    __typename\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    __typename\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    profile {\n      userAvatar\n      userSlug\n      realName\n      __typename\n    }\n    __typename\n  }\n  summary\n  topic {\n    id\n    commentCount\n    viewCount\n    __typename\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  isEditorsPick\n  upvoteCount\n  upvoted\n  hitCount\n  __typename\n}\n"}
					json_data=json.dumps(params).encode('utf8')
					respsolutions = self.session.post(qlurl, data=json_data, headers=headers, timeout=10)
					solutionsdict=json.loads(respsolutions.text)
						#获取官方用户名解决的此问题
					headers={'User-Agent':user_agent,'Connection':'keep-alive','Content-Type': 'application/json','Referer':problemlink+'/solution/'+str(solutionsdict['data']['questionSolutionArticles']['edges'][0]['node']['slug'])}
					params={"operationName":"solutionDetailArticle","variables":{"slug":solutionsdict['data']['questionSolutionArticles']['edges'][0]['node']['slug']},"query":"query solutionDetailArticle($slug: String!) {\n  solutionArticle(slug: $slug) {\n    ...article\n    content\n    __typename\n  }\n}\n\nfragment article on SolutionArticleNode {\n  title\n  slug\n  reactedType\n  status\n  identifier\n  canEdit\n  reactions {\n    count\n    reactionType\n    __typename\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    __typename\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    profile {\n      userAvatar\n      userSlug\n      realName\n      __typename\n    }\n    __typename\n  }\n  summary\n  topic {\n    id\n    commentCount\n    viewCount\n    __typename\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  isEditorsPick\n  upvoteCount\n  upvoted\n  hitCount\n  __typename\n}\n"}
					json_data=json.dumps(params).encode('utf8')
					respsolution = self.session.post(qlurl, data=json_data, headers=headers, timeout=10)
					solutiondict=json.loads(respsolution.text)
					dicto['solution'].update({'username':solutiondict['data']['solutionArticle']['author']['profile']['realName']})
					dicto['solution'].update({'createdtime':solutiondict['data']['solutionArticle']['createdAt']})
					dicto['solution'].update({'viewCount':solutiondict['data']['solutionArticle']['topic']['viewCount']})
					dicto['solution'].update({'commentCount':solutiondict['data']['solutionArticle']['topic']['commentCount']})
					dicto['solution'].update({'content':solutiondict['data']['solutionArticle']['content']})

			save2file(textpath,str(self.data))




			
if __name__=='__main__':
	test = Leetcode_Session()
	test.login()
	test.get_problems_contents()
	test.init_data()
	test.complete_data()