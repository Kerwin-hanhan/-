# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class BookSpider(RedisCrawlSpider):
    name = 'book'
    allowed_domains = ['amazon.cn']
    # start_urls = ['http://amazon.cn/']
    redis_key = 'amazon'

    rules = (
        # 匹配一级分类url地址
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='a-unordered-list a-nostyle a-vertical s-ref-indent-one']//li",)), follow=True),  # 无需定位到href属性，只需定位到对应元素即可
        # 二级、三级分类url地址
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='a-unordered-list a-nostyle a-vertical s-ref-indent-two']//li",)), follow=True),
        # 匹配列表页翻页
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']")), follow=True),
        # 匹配图书的url地址
        Rule(LinkExtractor(restrict_xpaths=("//ul[contains(@class, 's-result-list-hgrid s-height')]/li//h2/..")), follow=False, callback='parse_book_detail'),
    )

    cookies = "session-id=459-1482163-4192941; i18n-prefs=CNY; ubid-acbcn=462-9595365-7798366; x-wl-uid=1eNE6OS/EkJNJawnNGC1FVzqCcQKdA0iauCanmhUKrXvw4QelLFSP7nq4RgWBMKRIbbcHfkw8I90=; lc-acbcn=zh_CN; session-token=j4sRUuTc5kfFxvqFuiadyV0vEvoz5x00uHNhUFx5EskKfFv/U2TfAFfjFS5ew9apS2qC2TfPgnika8BzUpqrnNDNj2eX58FZTMBOrquTpHbZuUX7OEsCKx0Ez4HiIiBvweSN5hTnNWx3PdXlwrTzij9YmXc66wxiRhZVOHNMDA8tStkULmo1lBDF0vCSEYkH; session-id-time=2082729601l; csm-hit=tb:3AF2S2JEBRJMQG3CDHM3+s-5RV98XCCZDEDESTVDGNS|1584245141855&t:1584245141855&adb:adblk_yes"
    cookies = {i.split('=')[0]:i.split('=')[1] for i in cookies.split(';')}

    def parse_book_detail(self, response):
        print(response.body.decode())
        item = {}
        item['title'] = response.xpath("//h1[@id='title']/span[1]/text()").extract_first()
        item['authors'] = response.xpath("//span[@class='author notFaded']//a/text()").extract()
        item['book_img'] = response.xpath("//div[@id='ebooks-img-canvas']//img/@src").extract_first()
        item['press'] = response.xpath("//div[@class='content']/ul/li/b[contains(text(), '出版社')]/../text()").extract_first()
        item['brief'] = response.xpath("//div[@id='postBodyPS']/div/text()").extract()
        item['price'] = response.xpath("//span[@class='a-color-base']/span/text()").extract_first()
        item['bigcate'] = response.xpath("//ul[@class='a-unordered-list a-horizontal a-size-small']/li[@class='' and position()=3]").extract_first()
        item['smallcate'] = response.xpath("//ul[@class='a-unordered-list a-horizontal a-size-small']/li[@class='' and position()=5]").extract_first()
        print(item)
        return item
