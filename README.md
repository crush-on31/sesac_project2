<div align="center">
<img src="https://github.com/user-attachments/assets/567809d6-ce04-4149-8fb1-c07c988b880e"  width="700" height="250">
</div>

# [2025] Streamlit NEWS BRIEFING DashBoard

:mag_right: 네이버 뉴스를 토대로 특정 카테고리의 토픽을 분석하고,
이를 워드클라우드 형태로 시각화합니다. <br>

  동시에 국내 주식을 시각화하여 직관적이고 효율적인 데이터분석 경험을 사용자에게 제공합니다.
  ㅎ


- 팀원 소개
> ![team member image](https://github.com/user-attachments/assets/da2b3706-3410-4a8b-8478-d6e07e929563)

* * *
## 목차
  - [프로젝트 구조](#프로젝트-구조)
  - [파일별 기능](#파일별-기능)
  - [참고 문서](#참고-문서)

## 프로젝트 구조
```
DASHBOARD_PROJECT/
├── 📁data/
│    ├── articles_IT.csv
│    ├── articles_economy.csv
│    ├── articles_life.csv
│    ├── articles_politics.csv
│    ├── articles_word.csv
│    └── articles_society.csv
└── 📁naver_news_crawling/
    ├── __pycache__
    ├──📁view/
    │   ├── __pycache__
    │   ├── __init__.py
    │   ├── home.py
    │   ├── main.py
    │   ├── news_view.py
    │   ├── page_2.py
    │   └── style.py
    ├────── __init__.py
    ├────── crawl_marketindex.py
    ├────── naver_news_crawling.py
    ├────── README.md
    └────── topic_modeling.py
```


# 파일별 기능
### 1. 📁data
- 최신 뉴스를 크롤링하여 데이터 전처리한 csv파일 모음.

### 2. 📁view
2.1 home.py
- 홈 화면 페이지.
- 앱의 기본 정보와 환율 정보를 표시.

2-2. main.py
- Streamlit 앱의 메인 파일.
- 기본 홈 화면 역할을 하며, 사이드바를 통해 다른 페이지로 이동할 수 있도록 구성.

2.3 news_view.py
- 첫 번째 추가 페이지.
- 최신 뉴스 크롤링과 최신 뉴스 키워드 워드클라우드 생성 기능을 포함

2.4 page_2.py
- 두 번째 추가 페이지.
- Naver 금융 데이터를 크롤링하여 주식 시장 데이터를 시각화하고 분석
- 주식 차트 시각화 그래프(추세 그래프, 막대 그래프, 파이 그래프)

2.5 style.py
- streamlit 기본 테마 스타일 설정

### 3. 📁naver_news_crawling
3.1 crawl_marketindex.py
- 실시간 환율을 제공하는 파일.

3.2 naver_news_crawling.py
- 최신 뉴스를 크롤링하는 함수들을 모아놓은 파일.

3.3 topic_modeling.py
- 최신 뉴스를 기반으로 토픽 모델링을 수행하는 파일.


# 참고 문서
- 불용어 사전 google docs <br>
  https://docs.google.com/document/d/e/2PACX-1vRn9KiLOzqSgx8hCzhJnctvy6n0lxSWTXUEN04WjHcauHhKpOIWXPFQdh32RWPjGtU2IJlr2GzhnWSZ/pub
