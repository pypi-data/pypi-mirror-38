import re
import sys
import time
import json
import os.path
import urllib.parse
from string import Template
from datetime import datetime

import twnews.common as common
from twnews.soup import NewsSoup

import requests
from bs4 import BeautifulSoup

class NewsSearchException(Exception):
    pass

class NewsSearch:

    def __init__(self, channel, limit=25, beg_date=None, end_date=None):
        """
        配置新聞搜尋器
        """
        # 防止用中時搜尋
        if channel == 'chinatimes':
            msg = '頻道 {} 不支援搜尋功能'.format(channel)
            raise NewsSearchException(msg)

        # 防止中央社、東森、三立、聯合使用日期範圍
        if channel in ['cna', 'ettoday', 'setn', 'udn']:
            if not (beg_date is None and end_date is None):
                msg = '頻道 {} 不支援日期範圍條件'.format(channel)
                raise NewsSearchException(msg)

        # 防止開始日期和結束日期只設定了一個
        if beg_date is None or end_date is None:
            if end_date is not None:
                msg = '遺漏了開始日期'
                raise NewsSearchException(msg)
            if beg_date is not None:
                msg = '遺漏了結束日期'
                raise NewsSearchException(msg)

        # 防止開始日期和結束日期格式錯誤
        self.beg_date = None
        self.end_date = None
        try:
            if beg_date is not None:
                self.beg_date = datetime.strptime(beg_date, '%Y-%m-%d')
            if end_date is not None:
                self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            msg = '日期必須是 ISO 格式 (yyyy-mm-dd)'
            raise NewsSearchException(msg)

        # 防止開始日期大於結束日期
        if self.beg_date is not None:
            delta = self.end_date - self.beg_date
            if delta.days < 0:
                msg = '開始日期必須小於或等於結束日期'
                raise NewsSearchException(msg)
            if delta.days > 90 and channel == 'ltn':
                msg = '頻道 {} 的日期條件必須在 90 天內'.format(channel)
                raise NewsSearchException(msg)

        self.conf = common.get_channel_conf(channel, 'search')
        self.limit = limit
        self.pages = 0
        self.elapsed = 0
        self.host = None
        self.url_base = None
        self.soup = None
        self.json = None

    def by_keyword(self, keyword, title_only=False):
        """
        關鍵字搜尋
        """
        logger = common.get_logger()
        page = 1
        results = []
        no_more = False
        begin_time = time.time()

        while not no_more and len(results) < self.limit:
            # 組查詢條件
            replacement = {
                'PAGE': page,
                'KEYWORD': urllib.parse.quote_plus(keyword)
            }
            url = Template(self.conf['url']).substitute(replacement)

            # 再加上日期範圍
            if self.beg_date is not None:
                url += self.beg_date.strftime(self.conf['begin_date_format'])
                url += self.end_date.strftime(self.conf['end_date_format'])

            # 查詢
            session = common.get_session()
            logger.debug('新聞搜尋 ' + url)
            resp = session.get(url, allow_redirects=False)
            if resp.status_code == 200:
                logger.debug('回應 200 OK')
                for (k, v) in resp.headers.items():
                    logger.debug('{}: {}'.format(k, v))
                ctype = resp.headers['Content-Type']
                if 'text/html' in ctype:
                    self.soup = BeautifulSoup(resp.text, 'lxml')
                if 'application/json' in ctype:
                    self.json = resp.json()
            elif resp.status_code == 404:
                logger.debug('回應 404 Not Found，視為沒有更多查詢結果')
                self.json = None
                no_more = True
            else:
                logger.warning('回應碼: {}'.format(resp.status_code))
                break

            # 拆查詢結果 Soup
            if self.soup is not None:
                result_nodes = self.soup.select(self.conf['result_node'])
                if len(result_nodes) > 0:
                    for n in result_nodes:
                        title = self.__parse_title_node(n)
                        if (not title_only) or (keyword in title):
                            link = self.__parse_link_node(n)
                            date_inst = self.__parse_date_node(n)
                            results.append({
                                "title": title,
                                "link": link,
                                'date': date_inst
                            })
                            if len(results) == self.limit: break
                else:
                    no_more = True

            # 拆查詢結果 JSON
            if self.json is not None:
                result_nodes = self.json
                for k in self.conf['result_node']:
                    result_nodes = result_nodes[k]
                for r in result_nodes:
                    title = self.__parse_title_field(r)
                    if (not title_only) or (keyword in title):
                        link = self.__parse_link_field(r)
                        date_inst = self.__parse_date_field(r)
                        results.append({
                            "title": title,
                            "link": link,
                            'date': date_inst
                        })
                        if len(results) == self.limit: break

            page += 1

        # 以連結網址為基準去重複化
        filtered = []
        for (i, r) in enumerate(results):
            duplicated = False
            for j in range(i):
                p = results[j]
                if r['link'] == p['link']:
                    duplicated = True

            if not duplicated:
                filtered.append(r)
            else:
                logger.warning('查詢結果的 {}, {} 筆重複，新聞網址 {}'.format(i, j, r['link']))

        self.result_list = filtered
        self.pages = page - 1
        self.elapsed = time.time() - begin_time

        return self

    def to_dict_list(self):
        """
        回傳新聞查詢結果
        """
        return self.result_list

    def to_soup_list(self):
        """
        回傳新聞查詢結果的分解器
        """
        soup_list = []
        for r in self.result_list:
            nsoup = NewsSoup(r['link'])
            soup_list.append(nsoup)
        return soup_list

    def __parse_title_node(self, result_node):
        """
        單筆查詢結果範圍內取標題文字 (soup)
        """
        title_node = result_node.select(self.conf['title_node'])[0]
        return title_node.text.strip()

    def __parse_link_node(self, result_node):
        """
        單筆查詢結果範圍內取新聞連結 (soup)
        """
        link_node = result_node.select(self.conf['link_node'])[0]
        href = link_node['href']

        # 完整網址
        if href.startswith('https://'):
            return href

        # 絕對路徑
        if href.startswith('/'):
            if not self.host:
                m = re.match(r'^https://([^/]+)/', self.conf['url'])
                self.host = m.group(1)
            return 'https://{}{}'.format(self.host, href)

        # 相對路徑
        # 自由的 <head> 有設定 base_url
        if not self.url_base:
            nodes = self.soup.select('head > base')
            if len(nodes) == 1:
                self.url_base = nodes[0]['href']
            else:
                base_end = self.conf['url'].rfind('/')
                self.url_base = self.conf['url'][0:base_end+1]

        # 消除三立的 ../
        full_url = self.url_base + href
        spos = full_url.find('/', 10)
        reduced_url = full_url[0:spos] + os.path.realpath(full_url[spos:])
        return reduced_url

    def __parse_date_node(self, result_node):
        """
        單筆查詢結果範圍內取報導日期 (soup)
        """
        date_node = result_node.select(self.conf['date_node'])[0]

        if 'date_pattern' in self.conf:
            # DOM node 除了日期還有其他文字
            m = re.search(self.conf['date_pattern'], date_node.text)
            date_text = m.group(0)
        else:
            # DOM 只有日期
            date_text = date_node.text.strip()
        date_inst = datetime.strptime(date_text, self.conf['date_format'])
        return date_inst

    def __parse_title_field(self, result):
        """
        單筆查詢結果範圍內取標題文字 (dict)
        """
        field = self.conf['title_node']
        return result[field]

    def __parse_link_field(self, result):
        """
        單筆查詢結果範圍內取新聞連結 (dict)
        """
        field = self.conf['link_node']
        href = result[field]

        # 完整網址
        if href.startswith('https://'):
            return href

        # 絕對路徑
        if not self.host:
            m = re.match(r'^https://([^/]+)/', self.conf['url'])
            self.host = m.group(1)
        return 'https://{}{}'.format(self.host, href)

    def __parse_date_field(self, result):
        """
        單筆查詢結果範圍內取報導日期 (dict)
        """
        field = self.conf['date_node']
        date_inst = datetime.strptime(result[field], self.conf['date_format'])
        return date_inst
