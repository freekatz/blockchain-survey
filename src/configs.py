""" arxiv config
"""
arxiv_base_url_nor = "https://arxiv.org/search"
arxiv_base_url_adv = "https://arxiv.org/search/advanced"
arxiv_xhr_url = "https://partner.semanticscholar.org/v1/paper/arXiv:%s?include_unknown_references=true"
arxiv_payload_nor = {
    "query": "blockchain review",
    "searchtype": "all",
    "abstracts": "show",
    "order": "",
    "size": "200",
    "start": "60"
}
arxiv_payload_adv = {
    "advanced": "1",
    "terms-0-operator": "AND",
    "terms-0-term": "survey",
    "terms-0-field": "title",
    "terms-1-operator": "AND",
    "terms-1-term": "smart contract",
    "terms-1-field": "abstract",
    "terms-2-operator": "OR",
    "terms-2-term": "review",
    "terms-2-field": "title",
    "terms-3-operator": "AND",
    "terms-3-term": "smart contract",
    "terms-3-field": "abstract",
    "terms-4-operator": "OR",
    "terms-4-term": "tutorial",
    "terms-4-field": "title",
    "terms-5-operator": "AND",
    "terms-5-term": "smart contract",
    "terms-5-field": "abstract",
    "terms-6-operator": "OR",
    "terms-6-term": "overview",
    "terms-6-field": "title",
    "terms-7-operator": "AND",
    "terms-7-term": "smart contract",
    "terms-7-field": "abstract",
    "classification-physics_archives": "all",
    "classification-include_cross_list": "include",
    "date-filter_by": "date_range",
    "date-year": "",
    "date-from_date": "2009",
    "date-to_date": "2020",
    "date-date_type": "announced_date_first",
    "abstracts": "show",
    "order": "",
    "size": "200",
    "start": "0",
}
arxiv_headers_xhr = {
    "x-api-key": "6VzaAKS9aL8Q7L4qwuZyc1vFy2KCsdMSmICmjgNb"
}
arxiv_target_path = "./out/arxiv.xlsx"

""" Springer config
"""
springer_base_url = "https://link.springer.com/search/page/%s"
springer_index_range_begin = 2
springer_index_range_end = 58
springer_detail_base_url = "https://link.springer.com"
springer_payload = {
    "date-facet-mode": "between",
    "dc.title": "smart contract",
    "facet-start-year": "2009",
    "facet-end-year": "2020",
    "showAll": "true",
    "query": "(survey OR review OR overview OR tutorial)"
}
springer_target_path = "./out/springer.xlsx"

""" acm config
"""
acm_base_url = "https://dl.acm.org/action/doSearch"
acm_detail_base_url = "https://dl.acm.org"
acm_payload = {
    "fillQuickSearch": "false",
    "expand": "all",
    "AfterYear": "2009",
    "BeforeYear": "2020",
    "AllField": "Abstract:(cryptocurrency OR consensus OR smart contract) AND Title:(survey OR review OR tutorial OR overview)",
    "pageSize": "50"
}

acm_target_path = "./out/acm.xlsx"

""" science direct config
"""
science_direct_base_url = "https://www.sciencedirect.com/search"
science_direct_detail_base_url = "https://www.sciencedirect.com/science/article/abs/pii"
science_direct_xhr_url = "https://www.sciencedirect.com/sdfe/arp/pii/%s/citingArticles?creditCardPurchaseAllowed=true&preventTransactionalAccess=false&preventDocumentDelivery=true"
science_direct_payload = {
    "date": "2009-2020",
    # "tak": "smart contract",
    "title": "blockchain AND consensus AND (survey OR review OR tutuorial OR overview)",
    "show": "100",
    "offset": "0"
}
science_direct_target_path = "./out/science_direct.xlsx"

science_direct_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
}

""" ieee config
"""
ieee_base_url = "https://ieeexplore.ieee.org/search/searchresult.jsp"
# ieee_base_url_post = "https://ieeexplore.ieee.org/rest/search"
ieee_detail_base_url = "https://ieeexplore.ieee.org"
ieee_payload = {
    "newsearch": "true",
    "queryText": "(\"Document Title\":cryptocurrency) AND ((\"Document Title\":survey) OR (\"Document Title\":review) OR (\"Document Title\":tutorial) OR (\"Document Title\":overview))",
    "highlight": "true",
    "returnFacets": ["ALL"],
    "returnType": "SEARCH",
    "matchPubs": "true",
    "refinements":["ContentType:Conferences","ContentType:Journals"],
    "rowsPerPage":"100",
    "pageNumber":"1"
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

ieee_target_path = "./out/ieee.xlsx"
ieee_target_u_path = "./out/ieee_u.xlsx"