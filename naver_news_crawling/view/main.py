import streamlit as st
from datetime import datetime
from importlib import import_module
from style import apply_custom_styles
import sys
import os
# 프로젝트 최상위 디렉토리를 PYTHONPATH에 추가 - , '..', '..' 상위폴더 2개
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# 상위 폴더에 있는거 import
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# NaverMarketIndexScraper 경로 수정
from crawl_marketindex import NaverMarketIndexScraper

def main():
    scraper = NaverMarketIndexScraper()
    print("NaverMarketIndexScraper 초기화 완료")

if __name__ == "__main__":
    main()

# 페이지 설정
st.set_page_config(page_title="Today's news briefing", page_icon=":newspaper:", layout="wide")
st.image(r"C:\Users\msdus\project2\dashboard_project3\naver_news_crawling\view\002.png", width=500)

# CSS 스타일 정의
button_style = """
    <style>
    .stButton button {
        background-color: #3b404e;  /* 버튼 배경 색상 변경 */
        color: white;  /* 텍스트 색상 */
        font-size: 16px;  /* 텍스트 크기 */
        border-radius: 25px;  /* 버튼 모서리 둥글게 */
        cursor: pointer; /* 커서 모양 변경 */
        width: 100%; /* 버튼 너비를 사이드바 너비에 맞춤 */
        padding: 8px 10px;  /* 버튼 안의 여백 */
        border: 1px solid white;  /* 버튼 테두리 색상 (원하는 색상으로 변경) */
    }
    .stButton button:hover {
        background-color: #0064FF;  /* 버튼에 마우스를 올렸을 때 배경 색상 */
        color: white;  /* 텍스트 색상 */
        cursor: pointer; /* 커서 모양 변경 */
        width: 100%; /* 버튼 너비를 사이드바 너비에 맞춤 */
        border: 1px solid white;  /* 버튼 테두리 색상 (원하는 색상으로 변경) */

    }
    .stButton button:active {
        background-color: #0033CC;  /* 버튼 클릭 시 배경 색상 */
        font color: white;  /* 클릭 시 텍스트 색상 (화이트) */
        border: 1px solid white;  /* 클릭 시 테두리 색상 (화이트) */
    }
    [data-testid="baseButton-secondary"]:active {
        background-color: #0033CC;  /* 버튼 클릭 시 배경 색상 */
        color: white;  /* 클릭 시 텍스트 색상 (화이트) */
        border: 1px solid white;  /* 클릭 시 테두리 색상 (화이트) */
    }
    </style>
    """
st.markdown(button_style, unsafe_allow_html=True)

# 상태 초기화
st.session_state.clicked = False


# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "Home"

def render_exchange_rate():
    """환율 정보를 렌더링하는 함수"""
    st.subheader("실시간 환율 정보")
    scraper = NaverMarketIndexScraper()
    scraper.fetch_data()
    data = scraper.parse_data()

    option = st.selectbox(
        '**환율 정보 선택**',
        ['미국', '일본', '유럽연합', '중국', '영국', '국제 금', '국내 금'],
        key='home_currency_selectbox',
    )

    if option:
        selected_data = {
            '미국': data[0],
            '일본': data[1],
            '유럽연합': data[2],
            '중국': data[3],
            '영국': data[6],
            '국제 금': data[10],
            '국내 금': data[11],
        }.get(option, None)

        if selected_data:
            title, sale, change = selected_data
            st.metric(label=f"**{title}**", value=sale, delta=change)
        else:
            st.write("잘못된 옵션이 선택되었습니다.")

def render_common_elements():
    """모든 페이지에 공통적으로 표시할 요소"""
    # 현재 날짜 표시
    current_date = datetime.now().strftime("%Y년 %m월 %d일")
    st.title(f":earth_asia: {current_date}의 뉴스, 증시")


def change_page(page_name):
    """세션 상태의 페이지를 변경합니다."""
    st.session_state.page = page_name

# 페이지 네비게이터
pages = {
    "목차": [
        {"module": "home", "title": "Home", "icon": ":material/sentiment_satisfied_alt:"},
        {"module": "news_view", "title": "세션별 뉴스 기사 보기", "icon": ":material/wysiwyg:"},
        {"module": "page_2", "title": "국내 증시 보기", "icon": ":material/insert_chart_outlined:"},
    ]
}

# 사이드바에 네비게이터 UI 생성 
st.sidebar.title("목차")
for page in pages["목차"]:
    if st.sidebar.button(f"{page['icon']} {page['title']}", key=page['title']):
        change_page(page["title"])

# 현재 선택된 페이지 확인하세요
current_page = None
for page in pages["목차"]:
    if page["title"] == st.session_state.page:
        current_page = page
        break

if not current_page:
    current_page = pages["목차"][0]

# 공통 요소 렌더링
render_common_elements()

# Home 페이지일 때만 환율 정보 표시
if current_page["title"] == "Home":
    render_exchange_rate()

# 동적으로 모듈 가져오기
module_name = current_page["module"]
try:
    module = import_module(module_name)
    module.render_page(change_page)
except ModuleNotFoundError as e:
    st.error(f"모듈 {module_name}을 찾을 수 없습니다.")
    print(f"ModuleNotFoundError: {e}")
except AttributeError:
    st.error(f"{module_name} 모듈에서 render_page 함수를 찾을 수 없습니다.")