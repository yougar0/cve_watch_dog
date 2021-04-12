import urllib
import requests,re,time
import datetime
import config
from ding_message import send_ding
from aliyun_cve_monitor import AliYunDetector


def getNews():
    try:
        year = datetime.datetime.now().year
        api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated".format(year)
        req = requests.get(api).text
        cve_total_count = re.findall('"total_count":*.{1,10}"incomplete_results"',req)[0][14:17]
        cve_descriptions = re.findall('"description":*.{1,200}"fork"',req)
        cve_urls = re.findall('"svn_url":*.{1,200}"homepage"',req)

        return cve_total_count, cve_descriptions, cve_urls

    except Exception as e:
        print (e, 'github链接不通')


def sendNews():
    text = '漏洞描述:{},漏洞URL:{}'
    title = 'Github有新的CVE送达'
    print('cve 监控中 ...')
    cve_total_count, cve_descriptions, cve_urls = getNews()
    total_count = int(cve_total_count) - 1
    detector =  AliYunDetector()
    try:
        while True:
            if total_count != int(cve_total_count):
                for i in range(int(cve_total_count) - total_count):
                    cve_description = cve_descriptions[i].replace("\",\"fork\"", '').replace("\"description\":\"", '')
                    cve_url = cve_urls[i].replace("\",\"homepage\"", '').replace("\"svn_url\":\"", '')
                    info = text.format(cve_description, cve_url)
                    print(info)
                    send_ding(title, info)
                total_count = int(cve_total_count)
            detector.get_data()
            time.sleep(config.timing)
            cve_total_count, cve_descriptions, cve_urls = getNews()

    except Exception as e:
        raise e


if __name__ == '__main__':
    sendNews()