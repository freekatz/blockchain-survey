from settings import *

""" arxiv config
"""
# arxiv_base_url_nor = "https://arxiv.org/search"
arxiv_base_url_adv = "https://arxiv.org/search/advanced"
arxiv_xhr_url = "https://partner.semanticscholar.org/v1/paper/arXiv:%s?include_unknown_references=true"
# arxiv_payload_nor = {
#     "query": "blockchain review",
#     "searchtype": "all",
#     "abstracts": "show",
#     "order": "",
#     "size": "200",
#     "start": "0"
# }
arxiv_payload_adv = {
    "advanced": "1",
    "terms-0-operator": "AND",
    "terms-0-term": "Bitcoin OR Ethereum OR Blockchain OR (Distributed AND Ledger)",
    "terms-0-field": "abstract",
    "terms-1-operator": "AND",
    "terms-1-term": "security OR risk OR threat OR challenges OR attack OR vulnerabilities OR vulnerability",
    "terms-1-field": "abstract",
    "terms-2-operator": "AND",
    "terms-2-term": "NOT Survey AND NOT Overview AND NOT Review AND NOT Tutorial",
    "terms-2-field": "title",
    "classification-physics_archives": "all",
    "classification-include_cross_list": "include",
    "date-filter_by": "date_range",
    "date-year": "",
    "date-from_date": "2014",
    "date-to_date": "2020",
    "date-date_type": "announced_date_first",
    "abstracts": "show",
    "order": "",
    "size": "200",
    "start": "1",  # this
}
"""
https://arxiv.org/search/advanced?advanced=&terms-0-field=&terms-1-operator=AND&terms-1-term=&terms-1-field=abstract&terms-2-operator=AND&terms-2-term=NOT+Survey&terms-2-field=title&terms-3-operator=AND&terms-3-term=NOT+Overview&terms-3-field=title&terms-4-operator=AND&terms-4-term=NOT+Review&terms-4-field=title&terms-5-operator=AND&terms-5-term=NOT+Tutorial&terms-5-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2014&date-to_date=2020&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first
"""

arxiv_headers_xhr = {
    "x-api-key": "6VzaAKS9aL8Q7L4qwuZyc1vFy2KCsdMSmICmjgNb"
}
arxiv_target_path = crawler_output_dir + "/arxiv.xlsx"

""" Springer config
"""
springer_base_url = "https://link.springer.com/search/page/%s"
springer_index_range_begin = 1  # begin is 1
springer_index_range_end = 10  # base the search result
springer_detail_base_url = "https://link.springer.com"
springer_payload = {
    "date-facet-mode": "between",
    # "dc.title": "",
    "facet-start-year": "2014",
    "facet-end-year": "2020",
    "facet-language": "En",
    # "facet-content-type": "ConferencePaper",  # ConferencePaper and Article
    # OR
    "facet-content-type": "Article",
    "showAll": "true",
    "query": "(Bitcoin OR Ethereum OR Blockchain OR (Distributed AND Ledger)) \
            AND (security OR risk OR threat OR challenges OR attack OR vulnerabilities OR vulnerability) \
            AND NOT (Survey OR Overview OR Review OR Tutorial)"
}
springer_target_path = crawler_output_dir + "/springer.xlsx"

""" acm config
"""
acm_base_url = "https://dl.acm.org/action/doSearch"
acm_detail_base_url = "https://dl.acm.org"
acm_payload = {
    "fillQuickSearch": "false",
    "expand": "all",
    "AfterYear": "2014",
    "BeforeYear": "2020",
    "ContentItemType": "research-article",
    "AllField": "Keyword:(security OR risk OR threat OR challenges OR attack OR vulnerabilities OR vulnerability) AND Title:(NOT (Survey OR Overview OR Review OR Tutorial)) AND Abstract:(Bitcoin OR Ethereum OR Blockchain OR (Distributed AND Ledger))",
    "pageSize": "168"  # use the search result, any number
}

"""
https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=all&AfterYear=2014&BeforeYear=2020&AllField=Keyword%3A%28security+OR+risk+OR+threat+OR+challenges+OR+attack+OR+vulnerabilities+OR+vulnerability%29+AND+Title%3A%28NOT+%28Survey+OR+Overview+OR+Review+OR+Tutorial%29%29+AND+Abstract%3A%28Bitcoin+OR+Ethereum+OR+Blockchain+OR+%28Distributed+AND+Ledger%29%29
"""

acm_target_path = crawler_output_dir + "/acm.xlsx"

""" science direct config
"""
science_direct_base_url = "https://www.sciencedirect.com/search"
science_direct_detail_base_url = "https://www.sciencedirect.com/science/article/abs/pii"
science_direct_xhr_url = "https://www.sciencedirect.com/sdfe/arp/pii/%s/citingArticles?creditCardPurchaseAllowed=true&preventTransactionalAccess=false&preventDocumentDelivery=true"
science_direct_payload = {
    "date": "2014-2020",
    "qs": "security risk threat challenges attack vulnerabilities vulnerability",
    "tak": "Bitcoin OR Ethereum OR Blockchain OR (Distributed AND Ledger)",
    "title": "NOT (Survey OR Overview OR Review OR Tutorial)",
    "articleTypes": "REV,FLA",
    "show": "100",  # 25, 50 or 100 per page, others don't to take effect
    "offset": "1"
}

"""
https://www.sciencedirect.com/search?
qs=security%20risk%20threat%20challenges%20attack%20vulnerabilities%20vulnerability
&date=2014-2020
&tak=Bitcoin%20OR%20Ethereum%20OR%20Blockchain%20OR%20%28Distributed%20AND%20Ledger%29
&title=NOT%20%28Survey%20OR%20Overview%20OR%20Review%20OR%20Tutorial%29
&articleTypes=REV%2CFLA
"""

science_direct_target_path = crawler_output_dir + "/science_direct.xlsx"

science_direct_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
}

""" ieee config
"""
ieee_base_url = "https://ieeexplore.ieee.org/search/searchresult.jsp"
# ieee_base_url_post = "https://ieeexplore.ieee.org/rest/search"
ieee_detail_base_url = "https://ieeexplore.ieee.org"
ieee_payload = {
    "action": "search",
    "matchBoolean": "true",
    "queryText": '(NOT ("Document Title":"Survey")) AND (NOT ("Document Title":"Overview")) AND (NOT ("Document Title":"Review")) AND (NOT ("Document Title":"Tutorial")) \
    AND (("All Metadata":"Bitcoin") OR ("All Metadata":"Bitcoin") OR ("All Metadata":"Ethereum") OR ("All Metadata":"Blockchain") OR ("All Metadata":"Distributed Ledger")) \
    AND (("Author Keywords":"security") OR ("Author Keywords":"risk") OR ("Author Keywords":"threat") OR ("Author Keywords":"challenges") OR ("Author Keywords":"attack") OR ("Author Keywords":"vulnerabilities") OR ("Author Keywords":"vulnerability"))',
    "highlight": "true",
    "returnFacets": ["ALL"],
    "returnType": "SEARCH",
    "matchPubs": "true",
    "ranges": "2014_2020_Year",
    "refinements": ["ContentType:Conferences", "ContentType:Journals"],
    "rowsPerPage": "100",
    "pageNumber": ""
}

ieee_headers = {
    "Host": "ieeexplore.ieee.org",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Referer": ""
}

ieee_target_path = crawler_output_dir + "/ieee.xlsx"
ieee_target_u_path = crawler_output_dir + "/ieee_u.xlsx"
