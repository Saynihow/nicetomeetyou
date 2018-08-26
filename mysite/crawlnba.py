import schedule
import time
import requests
import urllib.request, urllib.error
from requests_html import HTML
import urllib.parse as urlparse
import os
import psycopg2

def job():
    url_nba = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url_nba.path[1:]
    user = url_nba.username
    password = url_nba.password
    host = url_nba.hostname
    port = url_nba.port
    def fetch(url):
        '''
        尋找不止一頁最新的資料!!
        '''

        def parse_next_link(doc):
            html = HTML(html=doc)
            controls = html.find('.pagelink a')
            '''我們需要上一頁資料(較舊的)，去抓controls中第六個(index為5)的href，但是進去下一頁後排序並不線性 我用if找出data-id為'right'的href'''
            for con in controls:
                if con.attrs.get('data-id') == 'right':
                    link = con.attrs.get('href')
            return urllib.parse.urljoin('https://nba.udn.com/', link)

        response = requests.get(url)
        response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
        html = HTML(html=response.text)
        post_entries = html.find(
            'div#news_list_body dt')  # nba_news_list都放在　div 'id'="news_list_body"裡面 文章詳情連結在element='dt'
        Next_link = parse_next_link(response.text)
        return post_entries, Next_link

    def fetch_detail_data(url):
        response = requests.get(url)
        response = requests.get(url, cookies={'over18': '1'})
        html = HTML(html=response.text)
        body_list = html.find(
            'div#sb-site div#container div#wrapper div#story_body div#story_body_content p')  # 藉由print(response.text)可以發現圖片連結都在Element 'a'的樹裡，而且不屬於別的Element底下
        author_list = html.find(
            'div#sb-site div#container div#wrapper div#story_body div#story_body_content div.shareBar div.shareBar__info div.shareBar__info--author span')
        image_list = html.find('div#story_body_content img')
        for a in author_list:
            author = a.text

        body = ""
        for b in body_list[1:]:
            body += b.text

        for img in image_list:
            image = img.attrs['data-src']

        video_list = html.find(
            'div#sb-site div#container div#wrapper div#story_body div#story_body_content iframe.lazyload')
        if video_list == []:
            video = ""
        else:
            for vid in video_list:
                video = vid.attrs['src']
        return author, body, image, video

    def parse_meta(entry):
        link = entry.find('a', first=True).attrs['href']
        meta = {
            'link': urllib.parse.urljoin('https://nba.udn.com/', link),
            'small_image': entry.find('img', first=True).attrs['data-src'],
            'title': entry.find('h3', first=True).text,
        }

        return meta

        # print(title, push, date, author, reallink)

    start_url = 'https://nba.udn.com/nba/cate/6754/-1/newest/1'
    num_pages = 2  # num_pages為每次啟動爬蟲所爬頁數
    collected_meta = []
    for a in range(num_pages):
        meta_onepage, link = fetch(start_url)
        meta_data = [parse_meta(onepost) for onepost in meta_onepage]
        collected_meta += meta_data
        start_url = link

    # print(collected_meta) meta_data是每一篇的詳情連結小圖連結標題，每頁收集完成後把dict放入collected_data這個list裡
    # print(len(collected_meta))
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()

    for post in collected_meta:

        cur.execute('SELECT title FROM nbanews_news WHERE link = %s', (post['link'],))
        row = cur.fetchone()  # 去抓Links table有跟"page"一樣欄位的row

        if row is None:
            author, body, image, video_src = fetch_detail_data(post['link'])  # 由fetch_detail_data得到文章內容、圖片、作者
            cur.execute('''INSERT INTO nbanews_news (author, body, image_link, link, title, small_image, video)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (author, body, image, post['link'], post['title'], post['small_image'], video_src))

        else:
            continue

        conn.commit()  # save the changes

schedule.every(1).hour.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)