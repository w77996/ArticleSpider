# -*- coding: utf-8 -*-
import datetime
import re
from urllib import parse

import scrapy
from scrapy import Request

from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self,response):
            # 通过xpath进行解析
            # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
            # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()
            # praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
            # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
            # match_re = re.match(".*?(\d+).*", fav_nums)
            # if match_re:
            #     fav_nums = match_re.group(1)
            #
            # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
            # match_re = re.match(".*?(\d+).*", comment_nums)
            # if match_re:
            #     comment_nums = match_re.group(1)
            #
            # content = response.xpath("//div[@class='entry']").extract()[0]
            #
            # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
            # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
            # tags = ",".join(tag_list)


            # 通过css选择器提取字段

            # 文章封面图
            front_image_url = response.meta.get("front_image_url", "")
            article_item = JobBoleArticleItem()
            title = response.css(".entry-header h1::text").extract()[0]
            create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
            praise_nums = response.css(".vote-post-up h10::text").extract()[0]
            fav_nums = response.css(".bookmark-btn::text").extract()[0]
            match_re = re.match(".*?(\d+).*", fav_nums)
            if match_re:
                fav_nums = int(match_re.group(1))
            else:
                fav_nums = 0

            comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
            match_re = re.match(".*?(\d+).*", comment_nums)
            if match_re:
                comment_nums = int(match_re.group(1))
            else:
                comment_nums = 0

            content = response.css("div.entry").extract()[0]

            tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
            tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
            tags = ",".join(tag_list)

            article_item["url_object_id"] = get_md5(response.url)
            article_item["title"] = title
            article_item["url"] = response.url
            try:
                create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
            except Exception as e:
                create_date = datetime.datetime.now().date()
            article_item["create_date"] = create_date
            article_item["front_image_url"] = [front_image_url]
            article_item["praise_nums"] = praise_nums
            article_item["comment_nums"] = comment_nums
            article_item["fav_nums"] = fav_nums
            article_item["tags"] = tags
            article_item["content"] = content
            # print(title)
            yield article_item