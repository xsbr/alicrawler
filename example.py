#!/usr/bin/env python

from alicrawler.alicrawler import AliCrawler

ali = AliCrawler()
print ali.getItemById(1461847096, store_stats=True)
