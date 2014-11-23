AliCrawler
==========

AliCrawler is a python Class to retrieve data from AliExpress products using HTML output.

Unfortunately access to AliExpress API is very restricted and documentation is only in Chinese (http://gw.api.alibaba.com/dev/doc/sys_auth.htm?ns=aliexpress.open)

### Example

    #!/usr/bin/env python
    import alicrawler

    ali = AliCrawler()
    print ali.getItemById(1461847096, store_stats=True)
