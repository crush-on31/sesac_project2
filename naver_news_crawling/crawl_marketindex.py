import requests
from bs4 import BeautifulSoup
import time
import os

class NaverMarketIndexScraper:
    def __init__(self, url="https://finance.naver.com/marketindex/"):
        """
        Naver 시장 지수 스크래퍼 초기화
        :param url: 스크래핑 대상 URL (기본값: Naver Finance 시장 지수)
        """
        self.url = url
        self.soup = None

    def fetch_data(self):
        """
        대상 URL에서 데이터를 가져와 BeautifulSoup 객체 생성
        """
        response = requests.get(self.url)
        response.encoding = 'euc-kr'  # Naver Finance 인코딩 설정
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Failed to fetch data, status code: {response.status_code}")

    def parse_data(self):
        """
        BeautifulSoup 객체에서 'tit'과 'sale' 데이터를 추출
        :return: 제목과 값의 리스트
        """
        if not self.soup:
            raise Exception("No data to parse. Call fetch_data() first.")
        
        titles = [title.text.strip() for title in self.soup.select('div.data ul li a h3 span')]
        sales = [sale.text.strip() for sale in self.soup.select('div.data ul li a span.value')]
        change = [sale.text.strip() for sale in self.soup.select('div.data ul li a span.change')]
        return list(zip(titles, sales, change))

    def display_data(self):
        """
        추출한 데이터를 출력
        """
        data = self.parse_data()
        for title, sale in data:
            print(f"{title}: {sale}")

# 사용 예시
if __name__ == "__main__":
    scraper = NaverMarketIndexScraper()
    scraper.fetch_data()
    scraper.display_data()
