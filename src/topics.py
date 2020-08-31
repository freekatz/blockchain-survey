#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   topics.py    
@Desc    :   
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/08/28 16:25       1uvu           1.0         
"""

import texthero as hero
import pandas as pd

if __name__ == '__main__':
    text = "Since the release of Bitcoins as crypto currency, Bitcoin has played a prominent part in the media. However, not Bitcoin but the underlying technology blockchain offers the possibility to innovatively change industries. The decentralized structure of the blockchain is particularly suitable for implementing control and business processes in microgrids, using smart contracts and decentralized applications. This paper provides a state of the art survey overview of current blockchain technology based projects with the potential to revolutionize microgrids and provides a first attempt to technically characterize different start-up approaches. The most promising use case from the microgrid perspective is peer-to-peer trading, where energy is exchanged and traded locally between consumers and prosumers. An application concept for distributed PV generation is provided in this promising area."
    s = pd.Series(text)
    s = hero.clean(s)
    print(s[0])
