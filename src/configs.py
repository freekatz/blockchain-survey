""" arxiv config
"""

arxiv_base_url = "https://arxiv.org/search/advanced"
arxiv_payload = {
    "advanced": "1",
    "terms-0-operator": "AND",
    "terms-0-term": "blockchain",
    "terms-0-field": "abstract",
    "terms-1-operator": "AND",
    "terms-1-term": "survey",
    "terms-1-field": "title",
    "terms-2-operator": "OR",
    "terms-2-term": "blockchain",
    "terms-2-field": "abstract",
    "terms-3-operator": "AND",
    "terms-3-term": "review",
    "terms-3-field": "title",
    "terms-4-operator": "OR",
    "terms-4-term": "blockchain",
    "terms-4-field": "abstract",
    "terms-5-operator": "AND",
    "terms-5-term": "tutorial",
    "terms-5-field": "title",
    "terms-6-operator": "OR",
    "terms-6-term": "blockchain",
    "terms-6-field": "abstract",
    "terms-7-operator": "AND",
    "terms-7-term": "overview",
    "terms-7-field": "title",
    "classification-physics_archives": "all",
    "classification-include_cross_list": "include",
    "date-filter_by": "date_range",
    "date-year": "",
    "date-from_date": "2009",
    "date-to_date": "2020",
    "date-date_type": "announced_date_first",
    "abstracts": "show",
    "size": "200",
    "order": ""
}

""" Springer config
"""
springer_base_url = "https://link.springer.com/search/page/%s"
springer_index_range_begin = 37
springer_index_range_end = 58
springer_detail_base_url = "https://link.springer.com"
springer_payload = {
    "date-facet-mode": "between",
    "dc.title": "blockchain",
    "facet-start-year": "2009",
    "facet-end-year": "2020",
    "showAll": "true",
    "query": "(survey OR review OR overview OR tutorial)"
}

""" acm config
"""
acm_base_url = "https://dl.acm.org/action/doSearch"
acm_detail_base_url = "https://dl.acm.org"
acm_payload = {
    "fillQuickSearch": "false",
    "expand": "all",
    "AfterYear": "2009",
    "BeforeYear": "2020",
    "AllField": "Abstract:(blockchain) AND Title:(survey OR review OR tutorial OR overview)",
    "pageSize": "50"
}

