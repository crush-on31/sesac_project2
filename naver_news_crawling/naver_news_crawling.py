import requests
from bs4 import BeautifulSoup
import time

import pandas as pd
import numpy as np
import csv
import re
from konlpy.tag import Okt
import os

class NewsCrawler:
    def __init__(self, ajax_url):
        self.ajax_url = ajax_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Accept-Language': 'ko-KR,ko;q=0.9',
        }
    # 뉴스 매인화면 크롤링(더보기 5번 누름)
    def fetch_articles(self, sid, start_page=1, max_pages=5):
        print("섹션 ID : ",sid)
        """sid 값을 기준으로 페이지를 순회하며 기사 제목과 링크 크롤링."""
        articles = []
        next_value = None  # 초기 next 값은 None으로 설정
        for page_no in range(start_page, start_page + max_pages):
            params = {
                'sid': sid,  # 섹션 ID
                'sid2': '',
                'cluid': '',
                'pageNo': page_no,
                'date': '',
                'next': next_value,
                '_': int(time.time() * 1000),  # 현재 타임스탬프
            }
            response = requests.get(self.ajax_url, params=params, headers=self.headers)

            if response.status_code != 200:
                print(f"Failed to fetch page {page_no} for sid {sid}: HTTP {response.status_code}")
                break

            try:
                data = response.json()
                html_content = data.get("renderedComponent", {}).get("SECTION_ARTICLE_LIST", "")
                soup = BeautifulSoup(html_content, 'html.parser')

                # 기사 추출
                for item in soup.select('.sa_list li.sa_item'):
                    title_tag = item.select_one('.sa_text a')
                    title = title_tag.get_text(strip=True) if title_tag else "No title"
                    link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else "No link"
                    articles.append({'title': title, 'link': link})

                # 다음 페이지의 next 값 추출
                next_cursor_tag = soup.select_one('div[data-cursor]')
                next_value = next_cursor_tag.get('data-cursor') if next_cursor_tag else None

                if not next_value:
                    print(f"No more pages to fetch for sid {sid}.")
                    break
            except Exception as e:
                print(f"Error parsing response for page {page_no} and sid {sid}: {e}")
                break

        return articles

    # 각각 기사 url 접속해서 크롤링
    def fetch_article_content(self, url):
        """개별 기사 페이지에서 제목과 본문 크롤링."""
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            #print(f"Failed to fetch article: HTTP {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            title = soup.select_one('.media_end_head_headline').get_text(strip=True)
            body = soup.select_one('#dic_area').get_text(strip=True)
            return {'title':title, 'body': body}
        except Exception as e:
            print(f"Error parsing article content: {e}")
            return None

    #명사를 추출하는 함수
    def extract_nouns(self, text):
        okt = Okt()
        # 명사만 추출하여 리스트로 반환
        nouns = okt.nouns(text)
        # 한 글자 짜리 명사 제외
        filtered_nouns = [noun for noun in nouns if len(noun) > 1]
        return ' '.join(filtered_nouns)  # 리스트를 공백으로 연결하여 문자열로 변환
