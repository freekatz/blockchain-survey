from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests
import json
import time
import copy
import re

from configs import *
from settings import *


class Crawler:
    def __init__(self):
        pass
    
    def open(self, url, payload=None, headers=None, method="GET"):
        """
        open the url and set the params
        :param headers: request headers
        :param url: site search url
        :param payload: url payload, get or post
        :param method: http method, get or post
        :return: text of response html
        """
        if payload is None:
            payload = {}
        if method == "GET":
            resp = requests.get(url, params=payload, headers=headers, proxies=proxies)
            return BeautifulSoup(resp.text, "lxml")
        elif method == "POST":
            resp = requests.post(url, data=payload, headers=headers, proxies=proxies)
            return resp.text
        else:
            raise Exception("Un-support protocol type")
        print(resp.url)
    
    def save(self, output, target):
        """
        with the target path, saving the list of dict: output
        :param output: dict list
        :param target: file path
        :return: NULL
        """
        df = pd.DataFrame(output)
        df = df[out_data.keys()]
        ext = re.split(r"\.", target)[-1]
        if ext == "xlsx" or ext == "xls":
            df.to_excel(target, encoding='utf-8', index=False)
        elif ext == "csv":
            df.to_csv(target, encoding="utf-8", index=False)
        elif ext == "json":
            df.to_json(target, encoding="utf-8")
        else:
            raise Exception("Un-support file type")
    
    def run(self):
        pass


class ArxivCrawler(Crawler):
    
    def __init__(self):
        super().__init__()
    
    def detail(self, out):
        soup = self.open(out["url"])
        out["title"] = soup.select_one("h1.title").text.replace("Title:", "")
        out["topics"] = ""
        out["publisher"] = "arxiv"
        out["cite"] = ""
        out["factor"] = ""
        author_item = soup.select_one("div.authors")
        a_items = author_item.select("a")
        authors = ""
        for a in a_items:
            authors += a.text + ","
        out["authors"] = authors[:-1]
        dy = re.split(r"\.", re.split(r"/", out["url"])[-1])[0]
        # out["date"] = "20" + str(dy[0:2]) + "-" + str(dy[2:])
        out["date"] = "20" + str(dy[0:2])
        out["abstract"] = soup.select_one("blockquote.abstract").text
        print(out)
    
    def run(self):
        """

        :return: NULL
        """
        soup = super().open(arxiv_base_url_adv, arxiv_payload_adv)
        print(soup)
        url_items = soup.select("p.list-title")
        output = []
        i = 1
        for url_item in url_items:
            out = copy.deepcopy(out_data)
            out["url"] = url_item.a["href"]
            out["origin"] = "arxiv"
            self.detail(out)
            output.append(out)
            super().save(output, arxiv_target_path)
            i += 1
            print(i)


class SpringerCrawler(Crawler):
    def __init__(self):
        super(SpringerCrawler, self).__init__()
    
    def detail(self, out):
        print(out["url"])
        soup = self.open(out["url"])
        if "article" in out["url"]:
            header_soup = soup.select_one("div.c-article-header")
            topics = ""
            topic_items = soup.select("li.c-article-subject-list__subject")
            for topic_item in topic_items:
                topics += topic_item.text + ","
            out["topics"] = topics[:-1]
            out["publisher"] = header_soup.select_one("p.c-article-info-details").text
            try:
                out["cite"] = header_soup.select("li.c-article-metrics-bar__item")[1].select_one(
                    "p.c-article-metrics-bar__count").text.replace("Citations", "").strip()
            except:
                pass
            out["factor"] = ""
            author_item = soup.select_one("ul.c-author-list")
            li_items = author_item.select("li")
            authors = ""
            for li in li_items:
                authors += li.text
            out["authors"] = authors
            out["date"] = header_soup.select_one("time")["datetime"]
            out["abstract"] = soup.select_one("div.c-article-section__content").text
        elif "chapter" in out["url"]:
            topics = ""
            topic_items = soup.select("span.Keyword")
            for topic_item in topic_items:
                topics += topic_item.text + ","
            out["topics"] = topics[:-1]
            out["publisher"] = soup.select_one("span.bibliographic-information__value").text
            out["cite"] = ""
            out["factor"] = ""
            out["authors"] = soup.select_one("div.authors__list").text
            try:
                out["date"] = soup.select_one("span.article-dates__first-online").text
            except:
                out["date"] = ""
            out["abstract"] = soup.select_one("p.Para").text
        else:
            pass
        
        # print(out)
    
    def run(self):
        """

        :return: output list of dict
        """
        output = []
        for i in range(springer_index_range_begin, springer_index_range_end + 1):
            soup = super().open(springer_base_url % i, springer_payload)
            url_items = soup.select("a.title")
            for url_item in url_items:
                out = copy.deepcopy(out_data)
                out["url"] = springer_detail_base_url + url_item["href"]
                out["origin"] = "springer"
                out["title"] = url_item.text
                self.detail(out)
                output.append(out)
            super().save(output, springer_target_path)
            print(i + 1)


class AcmCrawler(Crawler):
    def __init__(self):
        super(AcmCrawler, self).__init__()
    
    def detail(self, out):
        if "book" in out["url"]: return
        print(out["url"])
        soup = super().open(out["url"])
        out["title"] = soup.select_one("h1.citation__title").text
        topics = ""
        topic = ""
        try:
            topic_items = soup.select_one("div.article__index-terms").select("ol.rlist")[1].text
        except:
            topic_items = ""
            topics = ","
        for ch in topic_items:
            if 'A' <= ch <= 'Z':
                topics += topic + ","
                topic = ""
            topic += ch
        topics += topic
        out["topics"] = topics[1:]
        out["publisher"] = soup.select_one("span.epub-section__title").text
        out["cite"] = soup.select_one("span.citation").text.replace("citation", "")
        out["factor"] = ""
        author_items = soup.select("span.loa__author-name")
        authors = ""
        for author_item in author_items:
            authors += author_item.text + ","
        out["authors"] = authors[:-1].replace("about this author", "")
        out["date"] = soup.select_one("span.epub-section__date").text
        out["abstract"] = soup.select_one("div.abstractSection").text
        print(out)
    
    def run(self):
        """

        :return: output list of dict
        """
        soup = super().open(acm_base_url, acm_payload)
        url_items = soup.select("span.hlFld-Title")
        output = []
        i = 1
        for url_item in url_items:
            out = copy.deepcopy(out_data)
            out["url"] = acm_detail_base_url + url_item.a["href"]
            out["origin"] = "acm"
            self.detail(out)
            output.append(out)
            super().save(output, acm_target_path)
            i += 1
            print(i)


class ScienceDirectCrawler(Crawler):
    def __init__(self):
        super(ScienceDirectCrawler, self).__init__()
    
    def detail(self, out):
        print(out["url"])
        soup = super().open(out["url"], headers=science_direct_headers)
        out["title"] = soup.select_one("span.title-text").text
        topics = ""
        try:
            topic_item = soup.select_one("div.Keywords").text.strip().replace("Keywords", "")
            topic = ""
        except:
            topic_item = ""
            topic = ","
        for ch in topic_item:
            if 'A' <= ch <= 'Z':
                topics += topic + ","
                topic = ""
            topic += ch
        topics += topic
        out["topics"] = topics[1:]
        try:
            out["publisher"] = soup.select_one("a.publication-title-link").text
        except:
            out["publisher"] = ""
        out["cite"] = ""
        out["factor"] = ""
        authors = ""
        author_items = soup.select("a.author")
        for author_item in author_items:
            authors += author_item.text + ","
        out["authors"] = authors[:-1]
        date = re.split(", ", soup.select_one("div.text-xs").text.strip())
        try:
            out["date"] = date[1]
        except:
            out["date"] = date[0].replace("Available online ", "")
        
        try:
            out["abstract"] = soup.select_one("div.Abstracts").text
        except:
            out["abstract"] = ""
        # print(out)
    
    def run(self):
        """

        :return: output list of dict
        """
        soup = super().open(science_direct_base_url, science_direct_payload, science_direct_headers)
        url_items = soup.select("div.result-item-content")
        output = []
        i = 1
        for url_item in url_items:
            out = copy.deepcopy(out_data)
            out["url"] = science_direct_detail_base_url + \
                         re.split(r"pii", science_direct_base_url + url_item.h2.span.a["href"])[1]
            out["origin"] = "science_direct"
            self.detail(out)
            output.append(out)
            
            super().save(output, science_direct_target_path)
            i += 1
            print(i)


class IeeeCrawler(Crawler):
    def __init__(self):
        super(IeeeCrawler, self).__init__()
    
    def detail(self, out):
        print(out["url"])
        html = super().open(out["url"]).text
        try:
            js_str = "{" + re.search(r"global.document.metadata={(.*)};", html).groups()[0] + "}"
        except:
            return
        js = json.loads(js_str)
        print(js)
        out["title"] = js["title"]
        topics = ""
        try:
            for topic_item in js["topics"]:
                topics += topic_item + ","
        except:
            for topic_item in js["pubTopics"]:
                topics += topic_item["name"] + ","
        out["topics"] = topics[:-1]
        out["publisher"] = js["displayPublicationTitle"]
        out["cite"] = js["metrics"]["citationCountPaper"]
        out["factor"] = ""
        try:
            authors = ""
            for author_item in js["authors"]:
                authors += author_item["name"] + ","
            out["authors"] = authors[:-1]
        except:
            pass
        out["date"] = js["publicationDate"]
        out["abstract"] = js["abstract"]
        
        print(out)
    
    def run(self):
        """

        :return: output list of dict
        """
        # self.url_get()
        df = pd.read_excel(ieee_target_u_path)
        url_items = list(df["url"])
        output = []
        for i in range(0, len(url_items)):
            url_item = url_items[i]
            out = copy.deepcopy(out_data)
            out["url"] = url_item
            out["origin"] = "ieee"
            self.detail(out)
            output.append(out)
            super().save(output, ieee_target_path)
            print(i + 1)

    def url_get(self):
        driver = webdriver.Firefox()
        output = []
        for i in range(1, 10):
            ieee_payload["pageNumber"] = str(i)
            t_resp = requests.get(ieee_base_url, ieee_payload)
            ieee_headers["Referer"] = t_resp.url
            # self.send_request(driver, ieee_base_url_post, ieee_payload)
            driver.get(t_resp.url)
            time.sleep(10)
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            url_items = soup.select("div.List-results-items")
            for url_item in url_items:
                out = copy.deepcopy(out_data)
                out["url"] = ieee_detail_base_url + url_item.select_one("a")["href"]
                out["origin"] = "ieee"
                # self.detail(out)
                output.append(out)
                super().save(output, ieee_target_u_path)
            print(i)
    
    # def send_request(self, driver, url, params, method='POST'):
    #     if method == 'GET':
    #         parm_str = ''
    #         for key, value in params.items():
    #             parm_str = parm_str + key + '=' + str(value) + '&'
    #         if parm_str.endswith('&'):
    #             parm_str = '?' + parm_str[:-1]
    #         driver.get(url + parm_str)
    #     else:
    #         jquery = open("./res/js/jquery.min.js", "r").read()
    #         driver.execute_script(jquery)
    #         ajax_query = '''
    #                         $.ajax({
    #                             url: "%s",
    #                             data: "%s",
    #                             type: "%s",
    #                             dataType: "json",
    #                             contentType: "application/json;charset=utf-8",
    #                             success: function(returnData){
    #                                 console.log(returnData);
    #                             },
    #                             error: function(xhr, ajaxOptions, thrownError){
    #                                 console.log(xhr.status);
    #                                 console.log(thrownError);
    #                             }
    #                         });
    #                     ''' % (url, params.__str__(), method)
    #         print(ajax_query)
    #         ajax_query = ajax_query.replace(" ", "").replace("\n", "")
    #         resp = driver.execute_script("return " + ajax_query)
    #         print(resp)


if __name__ == '__main__':
    # arxiv = ArxivCrawler()
    # arxiv.run()

    # springer = SpringerCrawler()
    # springer.run()
    
    # acm = AcmCrawler()
    # acm.run()
    
    # science_direct = ScienceDirectCrawler()
    # science_direct.run()
    
    ieee = IeeeCrawler()
    ieee.run()
