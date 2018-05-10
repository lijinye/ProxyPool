# -*- coding:utf-8 -*-
import json
from proxypool.utils import get_page
from pyquery import PyQuery as pq
import json


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if k.startswith('crawl_'):
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count:页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_ip181(self):
        """
        获取ip181
        :return: 代理
        """
        start_url = 'http://www.ip181.com/'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            res = json.loads(html)
            results = res.get('RESULT')
            if results:
                for result in results:
                    ip = result.get('ip')
                    port = result.get('port')
                    yield ':'.join([ip, port])
