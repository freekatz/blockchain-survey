#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   mod.py
@Desc    :   添加新功能
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/29 17:22       1uvu           0.0.1
"""
import pandas as pd
import re

from settings import *
from utils import *

path = '/all-nf.xlsx'
df = pd.read_excel(output_root_dir + "/all-nf.xlsx")
df = df.dropna()
title_items = df['title']
topics_items = df['topics']

labels = {
    'security': 'security==cyber attack==cyber-attack==cyberattack==network attack==human and societal aspect of '
                'security and privacy==cyber security==cybersecurity==network security==system security==distribute '
                'system security==authentication==vulnerability==computer security==formal verification==cyber '
                'attack==computer crime==data security==attack==volatility==verification==intrusion '
                'detection==vulnerability==threat==risk==information security==model check==threat model==distribute '
                'system security==system security==communication security==human and societal aspect of security and '
                'privacy==risk management==ddos==denial-of-service attack==cybercrime==operational risk==credit '
                'risk==cyber spy==stateful firewall==secure network==do attack==eclipse attack==sybil==cloud compute '
                'security==provable security==ghost==unforgeable==threat factor==mine attack==security '
                'issue==security level analysis==threat model analysis==security threat==cyberattacks==secure '
                'multi-party computation==stalker attack==51% attack==security assurance==security '
                'vulnerability==security protocol==crytography==hardware security module==iot security==risk '
                'research==technical risk==risk-benefit==decentralize pki==mean-risk analysis==security '
                'challenge==tamper resistance==resistance==secure bill==social aspect of security==risk '
                'assessment==uc-security==cutlery fork==application security==denial',
    'privacy': 'privacy==data privacy==information privacy==human and societal aspect of security and '
               'privacy==privacy-preserving==privacy protection==preserve privacy==privacy-preserving '
               'technology==privacy-preserving smart contract==data integrity',
    'performance': 'performance==data storage==scalability==throughput==computer performance==performance '
                   'evaluation==performance evaluation criterion==network performance evaluation==performance '
                   'model==firm performance==performance analysis==network performance analysis==performance '
                   'optimization==performance evaluation criterion',
}

title_list = []
tag_list = []
for title, topics in zip(title_items, topics_items):
    topics_list = re.split(',', topics)
    _tag = []
    for key in labels:
        if isInter(topics_list, re.split('==', labels[key])):
            if title not in title_list:
                title_list.append(title)
            _tag.append(key)
            print(_tag, topics_list)
    tag_list.append(','.join(_tag))

tag_list = [l for l in tag_list if l != '']
title_list = list(set(title_list))
print(tag_list)
print(len(title_list))
print(len(tag_list))

ddf = df[df['title'].isin(title_list)]
ddf['tags'] = tag_list

dddf = pd.DataFrame(columns=['tags', 'title', 'topics', 'abstract'])
dddf['tags'] = tag_list
dddf['title'] = list(ddf['title'])
dddf['topics'] = list(ddf['topics'])
dddf['abstract'] = list(ddf['abstract'])

ddf.to_excel(analyzer_output_dir + '/spp.xlsx', index=False)
dddf.to_html(analyzer_output_dir + '/spp.htm', index=True)
