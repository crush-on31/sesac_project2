import streamlit as st
from datetime import datetime
from crawl_marketindex import NaverMarketIndexScraper  # naver_market_scraper.py에서 클래스를 import

def render_page(change_page):
    st.write(":three_button_mouse:페이지를 이동하려면 버튼을 **더블 클릭**하세요.")
    if st.button("**뉴스**로 이동"):
        change_page("세션별 뉴스 기사 보기")
    if st.button("**증시**로 이동"):
        change_page("국내 증시 보기")


# NaverMarketIndexScraper 객체 생성
scraper = NaverMarketIndexScraper()
# 데이터를 가져오는 메서드 호출
scraper.fetch_data()
# 환율 넣기