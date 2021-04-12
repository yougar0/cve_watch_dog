import datetime
import sys
import time
from urllib.parse import urljoin

import urllib3
from requests_html import HTMLSession
import ding_message
import config


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if sys.version_info[0] == 2:
    sys.version_info.major
    sys.setdefaultencoding("utf-8")

# now_time = datetime.datetime.today().strftime('Y%.m%.%d')

class AliYunDetector:
    report_url: str = "https://m.aliyun.com/doc/notice_list/9213612.html"

    def __init__(self):
        self.html_session = HTMLSession()
        self.html_session.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Mobile Safari/537.36"
        }
        self.html_session.verify = False
        self.vul_url = ''

    def get_data(self):
        resp = self.html_session.get(self.report_url)
        tags = resp.html.find("div.xs-content > a")
        url_new = urljoin(resp.url, tags[0].attrs["href"])
        if self.vul_url == '':
            tag_a = tags[0]
            url = urljoin(resp.url, tag_a.attrs["href"])
            tag_date, tag_title = tag_a.find("div")
            self.notice(
                {
                    "date": tag_date.text,
                    "title": tag_title.text,
                    "url": url,
                    "content": self.get_content(url)
                })
        else:
            for tag_a in tags:
                url = urljoin(resp.url, tag_a.attrs["href"])
                if self.vul_url != url:
                    tag_date, tag_title = tag_a.find("div")
                    self.notice(
                        {
                            "date": tag_date.text,
                            "title": tag_title.text,
                            "url": url,
                            "content": self.get_content(url)
                        }
                    )
        self.vul_url = url_new

    def get_content(self, url):
        resp = self.html_session.get(url)
        datas = {}
        last_key = None
        for tag_p in resp.html.pq("div#se-knowledge > p").items():
            key = tag_p("strong").text()
            text = tag_p.text().strip()
            if key:
                last_key = key
            elif text and last_key:
                if last_key not in datas:
                    datas[last_key] = ""
                datas[last_key] += f"{text}\n"
            elif not text:
                last_key = None
        return datas

    def notice(self, data):
        title, body = self.format_msg(data)
        ding_message.send_ding(title, body)
        # mail_to(body, title)

    def format_msg(self, data):
        title = f"阿里云安全漏洞预警--{data['title']}\n"

        body = f"漏洞等级: {data['content'].get('漏洞评级','未知').strip().split()[-1]}\n参考链接:{data['url']}\n漏洞日期：{data['date']}"

        return title, body

if __name__ == '__main__':
    d = AliYunDetector()
    d.get_data()