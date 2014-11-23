#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import re
import json

class AliCrawler:

    def __init__(self):
        self.alidomain = 'aliexpress.com'

    def getItemById(self, item_id, store_stats=False):
        url = 'http://www.%s/item/-/%d.html' % (self.alidomain, item_id)
        req = requests.get(url)
        html = req.text
        bs4 = BeautifulSoup(html)

        data = {}
        data['title'] = bs4.select('h1.product-name')[0].string
        data['original_price'] = float(bs4.select('#sku-price')[0].string.split(' ')[0])
        data['link'] = req.url

        #
        # images
        #
        data['image1'] = bs4.select('meta[property=og:image]')[0].attrs['content']
        data['image2'] = bs4.select('a.ui-image-viewer-thumb-frame img')[0].attrs['src']

        #
        # rating
        #
        try:
            data['rating'] = float(bs4.select('span[itemprop=ratingValue]')[0].string)
        except:
            data['rating'] = 0.0

        #
        # orders
        #
        try:
            data['orders'] = int(bs4.select('span.orders-count')[0].b.string)
        except:
            data['orders'] = 0

        #
        # discount_price
        #
        try:
            discount_price = bs4.select('#sku-discount-price')[0]
            if discount_price.span:
                data['discount_price'] = float(discount_price.span.string)
            else:
                data['discount_price'] = float(discount_price.string)
        except:
            data['discount_price'] = data['original_price']

        #
        # unit_price
        #
        try:
            data['piece_price'] = float(bs4.select('#sku-per-piece-price')[0].string)
        except:
            data['piece_price'] = data['discount_price']

        data['pieces'] = 1
        if(data['piece_price'] != data['discount_price'] and data['piece_price'] > 0):
            data['pieces'] = int(round(data['discount_price']/data['piece_price']))

        #
        # store
        #
        store = bs4.select('a.store-lnk')[0]
        data['store_name'] = store.string
        data['store_link'] = store.attrs['href']
        data['store_id'] = int(bs4.select('#hid_storeId')[0].attrs['value'])

        #
        # offline
        #
        data['offline'] = True
        try:
            offline = re.findall('window.runParams.offline=(\w+);', html)[0]
            if offline == "false":
                data['offline'] = False
        except:
            pass

        #
        # store stats
        #
        if store_stats and not data['offline']:
            try:
                admin_id = int(re.findall('window.runParams.adminSeq="(\w+)";', html)[0])
                stats = self.getSellerStatsByAdminId(admin_id)
                data['store_perc'] = float(stats[1])
                data['store_points'] = int(stats[3])
            except:
                data['store_perc'] = None
                data['store_points'] = None

        #
        # shipping
        #
        data['shipping'] = 0.0
        if not data['offline']:
            data['shipping'] = self.getItemShippingById(item_id)

        return data

    def getItemShippingById(self, item_id):
        url = ('http://freight.%s/ajaxFreightCalculateService.htm'
            '?callback=json&f=d&userType=cnfm&country=BR&count=1'
            '&currencyCode=USD&productid=%d' % (self.alidomain, item_id))

        try:
            req = requests.get(url)
            data = json.loads(req.text[5:-1])
            prices = []
            for shipment in data['freight']:
                prices.append(float(shipment['price']))
            shipping = min(prices)
        except:
            shipping = None

        return shipping

    def getSellerStatsByAdminId(self, admin_id):
        url = ('http://www.%s/cross-domain/feedback/index.html'
            '?memberType=seller&ownerMemberId=%d' % (self.alidomain, admin_id))

        try:
            req = requests.get(url)
            data = req.text.split('\n')[1].split(',')
        except:
            data = []

        return data

if __name__ == "__main__":
    ali = AliCrawler()
    ids = "1527079450,1600106660,1439525019,1439525019,1743878872,1435779436,1461847096"
    for id in ids.split(","):
        print "===== %d" % int(id)
        print ali.getItemById(int(id))
