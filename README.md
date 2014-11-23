AliCrawler
==========

AliCrawler is a python Class to retrieve data from AliExpress products using HTML output.

Unfortunately access to AliExpress API is very restricted and documentation is only in Chinese (http://gw.api.alibaba.com/dev/doc/sys_auth.htm?ns=aliexpress.open)

### Example

    #!/usr/bin/env python
    import alicrawler

    ali = AliCrawler()
    print ali.getItemById(1461847096, store_stats=True)

Results:

    {'rating': 4.7, 'piece_price': 6.48, 'store_id': 337581, 'original_price': 35.99,
    'offline': False, 'title': u'H4555# Nova navy girl dress kids 18m/6y newest..',
    'discount_price': 32.39, 'shipping': 0.0, 'pieces': 5, 'store_perc': 98.5,
    'store_name': u'Nova Factory Retail Shop', 'store_points': 8908, 'link':
    u'http://www.aliexpress.com/item/H4555-Nova-....html',
    'image2': u'http://i00.i.aliimg.com/wsphoto/v2/..._350x350.jpg',
    'image1': u'http://i00.i.aliimg.com/wsphoto/v2/....jpg',
    'store_link': u'http://www.aliexpress.com/store/337581', 'orders': 12}
