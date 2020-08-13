from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import copy
import re

from configs import *
from settings import *


class Crawler:
    def __init__(self):
        pass
    
    def open(self, url, payload=None, method="GET"):
        """
        open the url and set the params
        :param url: site search url
        :param payload: url payload, get or post
        :param method: http method, get or post
        :return: text of response html
        """
        if payload is None:
            payload = {}
        if method == "GET":
            resp = requests.get(url, params=payload, proxies=proxies)
        elif method == "POST":
            resp = requests.post(url, data=payload, proxies=proxies)
        else:
            raise Exception("Un-support protocol type")
        # print(resp.url)
        return BeautifulSoup(resp.text, "lxml")
    
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
        out["title"] = soup.select_one("h1.title").text
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
        out["date"] = "20" + str(dy[0:2]) + "-" + str(dy[2:])
        out["abstract"] = soup.select_one("blockquote.abstract").text
        print(out)
    
    def run(self):
        """

        :return: NULL
        """
        soup = super().open(arxiv_base_url, arxiv_payload, "GET")
        url_items = soup.select("p.list-title")
        output = []
        for url_item in url_items:
            out = copy.deepcopy(out_data)
            out["url"] = url_item.a["href"]
            self.detail(out)
            output.append(out)
        super().save(output, "./out/arxiv.xlsx")


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
        for index in range(springer_index_range_begin, springer_index_range_end+1):
            soup = super().open(springer_base_url % index, springer_payload, "GET")
            url_items = soup.select("a.title")
            for url_item in url_items:
                out = copy.deepcopy(out_data)
                out["url"] = springer_detail_base_url + url_item["href"]
                out["title"] = url_item.text
                self.detail(out)
                output.append(out)
            super().save(output, "./out/springer.xlsx")
            print(index)
    
    def science_direct(self):
        """

        :return: output list of dict
        """
        pass
    
    def ieee(self):
        """

        :return: output list of dict
        """
        pass


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
        for url_item in url_items:
            out = copy.deepcopy(out_data)
            out["url"] = acm_detail_base_url + url_item.a["href"]
            self.detail(out)
            output.append(out)
        
        super().save(output, "./out/acm.xlsx")


if __name__ == '__main__':
    # arxiv = ArxivCrawler()
    # arxiv.run()
    
    springer = SpringerCrawler()
    springer.run()
    
    # acm = AcmCrawler()
    # acm.run()
