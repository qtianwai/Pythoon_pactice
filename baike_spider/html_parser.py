import re
import urllib.parse
from bs4 import BeautifulSoup


class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
     #<a class="title" href="https://m.douban.com/time/column/85?dt_time_source=douban-web_anonymous" target="_blank">黑镜人生——网络生活的传播学肖像</a>
      #  class ="video-title" href="https://www.douban.com/doubanapp/dispatch?uri=/tv/30155361/trailer%3Ftrailer_id%3D231053%26trailer_type%3DL&amp;dt_dapp=1" > 如此接地气的佟丽娅，迷住你了吗？ | 《瓣嘴4》第6期 < / a >
        links = soup.find_all('a', href=re.compile(r"https://m.douban.com/time/column"))
        # 网址有变，表达式做了调整
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            # Py3中用到的模块名称变为urllib.parse
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}

        # url
        res_data['url'] = page_url

        # <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()

        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_='lemma-summary')
        if summary_node is None:
            return
        res_data['summary'] = summary_node.get_text()

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
