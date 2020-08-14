#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test.py
@Desc    :
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, ZJH567.CN
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/08/13 22:34       1uvu           1.0
"""

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ${NAME}.py
@Desc    :
@Project :   ${PROJECT_NAME}
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
${YEAR}/${MONTH}/${DAY} ${TIME}       1uvu           1.0
"""

import requests
from lxml import etree
import json

# 输入
conferenceNum = 8961330  # 会议编号


# 输出
# 此会议所有文章

# 获取issueNumber
def get_issueNumber(conferenceNum):
    conferenceNum = str(conferenceNum)
    gheaders = {
        'Referer': 'https://ieeexplore.ieee.org/xpl/conhome/' + conferenceNum + '/proceeding',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    md_url = 'https://ieeexplore.ieee.org/rest/publication/home/metadata?pubid=' + conferenceNum
    md_res = requests.get(md_url, headers=gheaders)
    md_dic = json.loads(md_res.text)
    issueNumber = str(md_dic['currentIssue']['issueNumber'])
    return issueNumber


# 爬取论文及其下载链接
def get_article_info(conferenceNum, issueNumber):
    conferenceNum = str(conferenceNum)
    issueNumber = str(issueNumber)
    # 将论文名和下载链接存到txt中去
    alf = open(r'%s_%s_downloadLinks.txt' % (conferenceNum, issueNumber), 'w')
    
    # 从第一页开始下载
    pageNumber = 1
    while (True):
        toc_url = 'https://ieeexplore.ieee.org/rest/search/pub/' + conferenceNum + '/issue/' + issueNumber + '/toc'
        payload = '{"pageNumber":' + str(
            pageNumber) + ',"punumber":"' + conferenceNum + '","isnumber":' + issueNumber + '}'
        headers = {
            'Host': 'ieeexplore.ieee.org',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Referer': 'https://ieeexplore.ieee.org/xpl/conhome/' + conferenceNum + '/proceeding?pageNumber=' + str(
                pageNumber),
        }
        toc_res = requests.post(toc_url, headers=headers, data=payload)
        toc_dic = json.loads(toc_res.text)
        try:
            articles = toc_dic['records']
        except KeyError:
            break
        else:
            for article in articles:
                title = article['highlightedTitle']
                link = 'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=' + article[
                    'articleNumber'] + '&ref='
                alf.write(title.replace('\n', '') + '>_<' + link + '\n')
            pageNumber = pageNumber + 1
            # 停一下防禁ip
            import time
            time.sleep(1)
    
    alf.close()
    return


# start
issueNumber = get_issueNumber(conferenceNum)
get_article_info(conferenceNum, issueNumber)