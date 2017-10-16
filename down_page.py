#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.robotparser

def download(url, user_agent='fred_spider', proxy=None, retry=3):
    print('下载如下链接：', url)
    headers = {'User-agent': user_agent}
    try:
        request = urllib.request.Request(url, headers=headers)

        opener = urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))

        html = opener.open(request).read()
    except urllib.request.URLError as e:
        print('下载遇到错误：', e.reason)
        html = None
        if retry > 0:
            if hasattr(e, 'code') and 400 <= e.code <= 600:
                return download(url, user_agent, proxy, retry - 1)
    return html

#从页面爬取帖子url
def find_article_url_in_page(page_url):
    crawl_pages = [page_url]
    seen = {page_url: 0}  # 防止重复
    article_url_num = 0  # 爬到的帖子数

    rp = get_robots(page_url)
    print(123,rp)
    exit(0)
    # throttle = Throttle(delay)
    # headers = headers or {}
    # if user_agent:
    #     headers['User-agent'] = user_agent
    #
    # while crawl_queue:
    #     url = crawl_queue.pop()
    #     depth = seen[url]
    #     # check url passes robots.txt restrictions
    #     if rp.can_fetch(user_agent, url):
    #         throttle.wait(url)
    #         html = download(url, headers, proxy=proxy, num_retries=num_retries)
    #         links = []
    #         if scrape_callback:
    #             links.extend(scrape_callback(url, html) or [])
    #
    #         if depth != max_depth:
    #             # can still crawl further
    #             if link_regex:
    #                 # filter for links matching our regular expression
    #                 links.extend(link for link in get_links(html) if re.match(link_regex, link))
    #
    #             for link in links:
    #                 link = normalize(seed_url, link)
    #                 # check whether already crawled this link
    #                 if link not in seen:
    #                     seen[link] = depth + 1
    #                     # check link is within same domain
    #                     if same_domain(seed_url, link):
    #                         # success! add this new link to queue
    #                         crawl_queue.append(link)
    #
    #         # check whether have reached downloaded maximum
    #         num_urls += 1
    #         if num_urls == max_urls:
    #             break
    #     else:
    #         print
    #         'Blocked by robots.txt:', url


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp

find_article_url_in_page('https://www.baidu.com')