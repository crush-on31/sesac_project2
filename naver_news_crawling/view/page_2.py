import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

plt.rcParams.update({'axes.titlesize': 14, 'font.size': 10})

font_path = r"C:\Users\msdus\Downloads\font\Pretendard-Regular.otf"
fontprop = fm.FontProperties(fname=font_path)

# Set font for Matplotlib
def set_korean_font():
    plt.rcParams['font.family'] = 'Pretendard-Regular'  # Replace with 'Malgun Gothic' if on Windows
    plt.rcParams['axes.unicode_minus'] = False  # Fix negative sign display issue

try:
    set_korean_font()
except Exception as e:
    st.error(f"Failed to set Korean font: {e}")

class FinanceCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }

    def fetch_data(self, endpoint):
        """지정된 엔드포인트에서 데이터를 크롤링."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            st.error(f"Failed to fetch data: HTTP {response.status_code}")
            return None

        return response.text

    def parse_stock_data(self, html):
        """HTML에서 주식 데이터를 파싱."""
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select('table.type_2 tr')

        data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                data.append([
                    col.get_text(strip=True) for col in cols
                ])

        # 열 이름 설정 및 DataFrame 생성
        header_row = soup.select_one('table.type_2 thead tr')
        if header_row:
            columns = [th.get_text(strip=True) for th in header_row.find_all('th')]
        else:
            columns = [f"Column {i+1}" for i in range(len(data[0]))]

        df = pd.DataFrame(data, columns=columns)
        df.index = range(1,len(df)+1)
        
        return df


def render_page(change_page):
    st.markdown(
    "<h1 style='font-size:30px; text-align:left;'>증시 데이터 시각화</h1>",
    unsafe_allow_html=True)
    base_url = 'https://finance.naver.com'
    endpoint = 'sise/sise_market_sum.nhn?sosok=0'

    crawler = FinanceCrawler(base_url)
    st.write("")
    html_content = crawler.fetch_data(endpoint)

    if not html_content:
        st.error("HTML 콘텐츠를 가져오지 못했습니다.")
        return

    try:
        stock_data = crawler.parse_stock_data(html_content)
        st.write("")
        
        # 첫 번째 열 삭제
        stock_data = stock_data.iloc[:, 1:-1]
        st.dataframe(stock_data.head())  # Display modified data

        # Process numeric data
        stock_data['현재가'] = pd.to_numeric(stock_data['현재가'].str.replace(',', ''), errors='coerce')
        stock_data['거래량'] = pd.to_numeric(stock_data['거래량'].str.replace(',', ''), errors='coerce')
        stock_data = stock_data.dropna()


        if stock_data.empty:
            st.error("처리할 유효한 주식 데이터가 없습니다.")
            return

        # Add spacing between graphs
        st.write("")  # Add blank line
        st.markdown("<br>", unsafe_allow_html=True)  # Add HTML-style line break

        # Visualizations
        st.markdown("### 시각화 자료")

        # Update global font size
        plt.rcParams.update({'axes.titlesize': 14, 'font.size': 10})

        # Graph: 시간에 따른 주가 변화
        # 상위 20개 종목만 선택
        limited_stock_data = stock_data.head(20)

        # 첫 번째 그래프를 위한 cubehelix 팔레트 생성
        colorp1 = sns.cubehelix_palette(n_colors=len(limited_stock_data), start=.5, rot=-.75)

        fig1, ax1 = plt.subplots(figsize=(9, 6))
        # 전체 데이터를 한 번에 플로팅
        ax1.plot(limited_stock_data['종목명'], limited_stock_data['현재가'], marker='o', linestyle='-', color=colorp1[10])

        # 각 데이터 포인트에 대해 색상만 변경
        for i, (name, price) in enumerate(zip(limited_stock_data['종목명'], limited_stock_data['현재가'])):
            ax1.plot(name, price, marker='o', color=colorp1[i])

        ax1.set_title("시간에 따른 주가 변화", fontsize=16, fontproperties=fontprop)  # Direct fontsize 설정
        ax1.set_xlabel("종목명", fontsize=14, fontproperties=fontprop)
        ax1.set_ylabel("현재가", fontsize=14, fontproperties=fontprop)
        ax1.set_xticks(range(len(limited_stock_data['종목명'])))
        ax1.set_xticklabels(limited_stock_data['종목명'], rotation=45, ha='right', fontsize=10, fontproperties=fontprop)
        ax1.grid(True)
        plt.tight_layout()
        st.pyplot(fig1)

        # Add spacing between graphs
        st.write("")  # Add blank line
        st.markdown("<br>", unsafe_allow_html=True)  # Add HTML-style line break

        # 두 번째 그래프를 위한 cubehelix 팔레트 생성
        colorp2 = sns.cubehelix_palette(n_colors=10, start=2, rot=.5)

        st.subheader("거래량 상위 10 종목(막대 그래프)")
        top_10 = stock_data.nlargest(10, '거래량')
        fig2, ax2 = plt.subplots(figsize=(9, 6))
        ax2.bar(top_10['종목명'], top_10['거래량'], color=colorp2)
        ax2.set_title("거래량 상위 10 종목", fontproperties=fontprop)  # 폰트 크기 개별 설정
        ax2.set_xlabel("종목명", fontsize=12, fontproperties=fontprop)
        ax2.set_ylabel("거래량", fontsize=12, fontproperties=fontprop)
        ax2.tick_params(axis='x', rotation=45, labelsize=10)
        ax2.set_xticklabels(ax2.get_xticklabels(), fontproperties=fontprop)
        st.pyplot(fig2)

        # Add spacing between graphs
        st.write("")  # Add blank line
        st.markdown("<br>", unsafe_allow_html=True)  # Add HTML-style line break

        st.subheader("거래량 상위 10 종목 비율(파이 차트)")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.pie(top_10['거래량'], labels=top_10['종목명'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors,
        pctdistance=0.85,  # 퍼센트 텍스트를 중심에서 바깥쪽으로 이동
        textprops={'fontproperties': fontprop, 'fontsize': 8})
        ax3.set_title("거래량 상위 10 종목 비율", fontproperties=fontprop, fontsize=16)  # 폰트 크기 개별 설정
        st.pyplot(fig3)

    except Exception as e:
        st.error(f"데이터 파싱 또는 처리 중 오류 발생: {e}")


# def render_page(change_page):
#     st.title("증시 :chart:")
#     st.write("최신 주식 시장 정보를 확인하세요.")

#     # 탭 생성
#     tab_titles = ["주식", "ETF"]
#     tabs = st.tabs(tab_titles)

#     # 각 탭 실행
#     with tabs[0]:
#         st.header('주식')
#         st.write('주식 관련 데이터를 확인하세요.')
#         # 주식 크롤링 코드 추가

#     with tabs[1]:
#         st.header('ETF')
#         st.write('ETF 관련 데이터를 확인하세요.')
#         # ETF 크롤링 코드 추가
