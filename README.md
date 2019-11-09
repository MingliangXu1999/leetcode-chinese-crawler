# leetcode-chinese-crawler
#### 此代码用于USTC 2019秋季学期web课程扩展实验

## 概述
爬取 LeetCode中文试题。

## 运行环境

Windows 10  python 3; 
库：
* requests
* requests_toolbelt
* codecs
* json
* time
* random
* json
* re

## 使用说明
使用前需改写python文件中的username以及password，该账户密码用于登录leetcode中文账户
后期版本可能会实现命令行输入操作


## 输出
将爬取到的内容按照
```
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
				"solution": 
				{
					'username':'力扣 (LeetCode)',
					'createdtime':'2018-05-27T16:26:11.200614+00:00',
					'viewCount':162904,
					'commentCount': 250,
					"content": "方法一：暴力法暴力法很简单，遍历每个元素 x..."   // 解答内容
				}
			},
			...
]
```
  输出至'./problems.txt'下，后期可能实现一题一目录形式以便用户做题
  


